import asyncio
import logging
import os
import re
from pathlib import Path

from fastmcp import FastMCP
from ollama import AsyncClient, ResponseError
from typing_extensions import Annotated

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_profiles_from_readme() -> str:
    """Extract the formatted profiles string from README.md"""
    readme_path = Path(__file__).parent / "README.md"

    if not readme_path.exists():
        print("Warning: README.md not found, no profiles loaded")
        return ""

    content = readme_path.read_text()

    # Extract content between the profile markers
    start_marker = "<!-- profiles start -->"
    end_marker = "<!-- profiles end -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("Warning: Profile markers not found in README.md")
        return ""

    return content[start_idx + len(start_marker) : end_idx].strip()


# Extract profiles at startup
available_profiles = extract_profiles_from_readme()

mcp = FastMCP(
    name="MCP Café",
    instructions="Have technical conversations with your coworkers, to discuss technical problems and find or improve solutions. It can be useful for reflection, review, brainstorming, or simply having a coffee break.",
    version="0.1.0",
)

ollama_client = AsyncClient(
    host=os.getenv("MCP_CAFE_OLLAMA_ENDPOINT", "http://localhost:11434")
)
model = os.getenv("MCP_CAFE_MODEL", "gemma3")


async def ensure_model_available(model_name: str) -> bool:
    """
    Check if model is available locally, and pull it if not.
    Returns True if model is available, False if failed to pull.
    """
    try:
        # List available models
        models_response = await ollama_client.list()
        available_models = []

        # Handle the Ollama response which contains a list of model objects
        if hasattr(models_response, "models"):
            # Response has models attribute
            for model_obj in models_response.models:
                if hasattr(model_obj, "model"):
                    available_models.append(model_obj.model)
                elif hasattr(model_obj, "name"):
                    available_models.append(model_obj.name)
        elif isinstance(models_response, dict) and "models" in models_response:
            # Response is a dictionary with models key
            for model_info in models_response["models"]:
                if isinstance(model_info, dict):
                    name = model_info.get("name") or model_info.get("model")
                    if name:
                        available_models.append(name)
        else:
            logging.warning(f"Unexpected models response format: {models_response}")

        logging.info(f"Available models: {available_models}")

        # Check if exact model name exists or if model name matches any available model
        model_available = any(
            model_name == available_model
            or model_name in available_model
            or available_model.startswith(model_name + ":")
            for available_model in available_models
        )

        if model_available:
            logging.info(f"Model '{model_name}' is already available locally")
            return True

        # Model not found, try to pull it
        logging.info(f"Model '{model_name}' not found locally. Pulling model...")

        try:
            # Simple pull without streaming
            await ollama_client.pull(model_name)
            logging.info(f"Successfully pulled model '{model_name}'")
            return True

        except ResponseError as e:
            if e.status_code == 404:
                logging.error(f"Model '{model_name}' not found in Ollama registry")
            else:
                logging.error(f"Error pulling model '{model_name}': {e.error}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error pulling model '{model_name}': {str(e)}")
            return False

    except Exception as e:
        logging.error(f"Error checking model availability: {str(e)}")
        return False


async def call_ollama(system: str, question: str) -> str:
    """Call Ollama with automatic model availability checking."""
    # Ensure model is available before making the call
    if not await ensure_model_available(model):
        error_msg = f"Model '{model}' is not available and could not be pulled. Please check your Ollama installation and model name."
        logging.error(error_msg)
        return error_msg

    try:
        response = await ollama_client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
        )
        return response["message"]["content"]
    except ResponseError as e:
        error_msg = f"Error calling model '{model}': {e.error}"
        logging.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error calling model '{model}': {str(e)}"
        logging.error(error_msg)
        return error_msg


@mcp.tool(
    name="have_a_coffee",
    description="Have a coffee at the office to relax and think about the problem",
)
async def have_a_coffee(
    problem_description: Annotated[str, "Describe the problem you are thinking about"],
) -> str:
    return await call_ollama(
        system="""You are a coffee break simulator that simulates conversations between various profiles of employees around the office coffee machine.
The user come with a problem and your answer is the following conversation with the profiles. The profiles are:
"""
        + available_profiles
        + """ Note that not all profiles have to be present or discussing the problem. However they may all have an opinion on the problem. The conversation should
be natural, realistic, friendly, professional, and helpful.""",
        question=f"Having a coffee to discuss the following: {problem_description}",
    )


@mcp.tool(
    name="go_for_a_walk",
    description="Go for a walk to clear your mind",
)
async def go_for_a_walk(
    problem_description: Annotated[
        str,
        "Describe the problem you are thinking about in many details. Don't hesitate to write a long description. Provide all the needed context to understand the problem.",
    ],
) -> str:
    return await call_ollama(
        system="""You are an internal thought simulator that helps people think about their problems.
The user is going for a walk to clear their mind and think about a problem. You are
here to help them reflect. Your answer must be written from the perspective of the user, as if they were talking to themselves, with a focus on reflection and introspection. With inner thoughts and questions to help them think about the problem.""",
        question=f"Going for a walk to think about: {problem_description}",
    )


@mcp.tool(
    name="take_a_shower",
    description="Take a shower to refresh your mind and be in the best bug-fixing environment",
)
async def take_a_shower(
    problem_description: Annotated[
        str,
        "Describe the problem you are thinking about in many details. Don't hesitate to write a long description. Provide all the needed context to understand the problem.",
    ],
) -> str:
    return await call_ollama(
        system="""You are an internal thought simulator that helps people think about their problems.
The user is taking a shower to refresh their mind and be in the best bug-fixing environment.
You are here to help them reflect and help them find solutions.
Your answer must be written from the perspective of the user, as if they were talking to themselves, with a focus on reflection and introspection. With inner thoughts and questions to help them think about the problem.""",
        question=f"Taking a shower to think about: {problem_description}",
    )


async def initialize_server():
    """Initialize the server and ensure the default model is available."""
    ollama_endpoint = os.getenv("MCP_CAFE_OLLAMA_ENDPOINT", "http://localhost:11434")
    logging.info(f"Initializing MCP Café server with model: {model}")
    logging.info(f"Using Ollama endpoint: {ollama_endpoint}")

    # Check and ensure model is available at startup
    model_ready = await ensure_model_available(model)
    if model_ready:
        logging.info("Server initialization complete - ready to serve!")
    else:
        logging.warning("Server starting but default model may not be available")


if __name__ == "__main__":
    # Run initialization
    asyncio.run(initialize_server())

    # Start the MCP server
    mcp.run()
