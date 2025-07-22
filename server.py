import os
import re
from pathlib import Path

from fastmcp import FastMCP
from ollama import AsyncClient
from typing_extensions import Annotated


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

ollama_client = AsyncClient()
model = os.getenv("MCP_CAFE_MODEL", "gemma3")


async def call_ollama(system: str, question: str) -> str:
    response = await ollama_client.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
    )
    return response["message"]["content"]


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


if __name__ == "__main__":
    mcp.run()
