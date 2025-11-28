[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/fungiboletus-mcp-cafe-badge.png)](https://mseep.ai/app/fungiboletus-mcp-cafe)

# MCP Café

Sometimes, when one is stuck on an engineering problem, it helps to take a coffee break and talk to friends and co-workers about it. This is what MCP Café is all about.

MCP Café is an [MCP](https://en.wikipedia.org/wiki/Model_Context_Protocol) server that simulates technical discussions. Different agents can be configured to simulate different personalities and profiles.

## Profiles

<!-- profiles start -->

- **Senior Principal Engineer**: A senior engineer with a lot of experience, who can provide insights and advice on complex problems.
- **Enthusiast and Creative Intern**: A young and eager intern who is enthusiastic about learning and exploring new ideas. He can think outside the box and come up with creative solutions.
- **Senior Researcher**: A senior researcher with a deep understanding of the latest technologies and trends. He can provide insights into the latest research and development in the field.
- **Bean Counter Project Manager**: A project manager who is focused on the accounting and financial aspects of the project. He can remind you of the budget and deadlines, and help you stay on track.
- **Senior Software Architect**: A senior software architect who can provide insights into the design and architecture of the system. He can help you understand the big picture and how different components fit together.
- **Workaholic Junior Programmer**: A child-free junior programmer who spends all his time coding. He is very focused on the technical aspects of a project and can help you with coding-related questions.
- **PhD Student**: A PhD student who is the expert on a tiny part of a related field. He can provide creative and innovative solutions to problems, or suggest new directions for research.
- **Somewhat Burned Out Sysadmin**: A quite negative and pessimistic sysadmin who is always worried about the worst-case scenario. He can help you think about potential problems and how to avoid them.
- **Talented but Uncontrollable Rock star Engineer**: A talented and creative engineer who is not afraid to challenge the status quo. He can provide innovative solutions and push the boundaries of what is possible.
- **The White Hat Hacker**: A security expert who can help you think about security and privacy issues. He can provide insights into the latest security trends and best practices.
- **The UX Designer**: A user experience designer who can help you think about the user interface and user experience of the system. He can provide insights into the latest design trends and best practices.
- **The Boss**: The boss is a person down to earth, who wants on time, on spec, and on budget delivery. He is fair, but expects results. He can help you stay focused on the project goals and ensure that you are meeting the requirements.

<!-- profiles end -->

You are free to create other profiles that match more closely your needs.

## Available Tools

| Tool | Description |
|------|-------------|
| `have_a_coffee` | Have a coffee at the office to relax and think about the problem. Simulates conversations with various office profiles. |
| `go_for_a_walk` | Go for a walk to clear your mind. Provides internal reflection and introspection to help think through problems. |
| `take_a_shower` | Take a shower to refresh your mind and be in the best bug-fixing environment. Similar to walking but focused on finding solutions. |

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mcp-cafe.git
   cd mcp-cafe
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Make sure you have [Ollama](https://ollama.com/) installed and running with the `gemma3` model (or set `MCP_CAFE_MODEL` to your preferred model).

4. Run the server:

   ```bash
   ./start.sh
   ```

## Usage example in `mcp.json`

```json5
{
   "servers": {
      // ...
      "mcp-cafe": {
         "type": "stdio",
         "command": "/absolute-path-to-mcp-cafe/start.sh",
         "args": [],
         "env": {
            "MCP_CAFE_OLLAMA_ENDPOINT": "http://localhost:11434",
            "MCP_CAFE_MODEL": "gemma3",
            // "MCP_CAFE_OLLAMA_TOKEN": "token-if-needed"
         }
      },
      // ...
   },
}
```

## Configuration

MCP Café is designed to be generic, and can work with any Chat LLM. It can work with ChatGPT, Claude, Gemini, Mistral, Gwen, and many others. However, currently only [Ollama](https://ollama.com/) is supported out of the box.

The default model is `gemma3`, but you can change it to any model you want by setting the `MCP_CAFE_MODEL` environment variable.

You can configure the Ollama endpoint by setting the `MCP_CAFE_OLLAMA_ENDPOINT` environment variable. The default is `http://localhost:11434`.

Moreover, if your Ollama server requires an API token, you can set the `MCP_CAFE_OLLAMA_TOKEN` environment variable. It will be then used for bearer token authentication.

## Licence

Café is licensed under the [WTFPL](https://www.wtfpl.net/) licence.
