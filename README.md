# AI Code Assistant Agent

This project is a small CLI-based AI “agent” that can inspect and debug a Python
calculator program using the Gemini API. It demonstrates:

- Calling a large language model (LLM)
- Tool/function calling (file inspection and execution)
- Maintaining a conversation history (`messages`)
- Running in a loop so the model can iteratively refine its work

The agent can, for example, answer questions like:

> “How does the calculator render results to the console?”

by reading files in the `calculator/` directory via tools you provide.

---

## Features

- **Command-line interface**: Pass a natural-language prompt from your terminal.
- **LLM integration**: Uses Google’s `gemini-2.5-flash` model.
- **Tool calling**: The model can call functions such as:
  - `get_files_info` – list available project files
  - `get_file_content` – read a file’s contents
  - `run_python_file` – execute Python files and capture output
  - `write_file` – modify files (e.g., to fix a bug)
- **Agent loop**:
  - Maintains a `messages` conversation history.
  - Adds both the model’s replies (`response.candidates`) and tool results into
  that history.
  - Iterates up to `MAX_ITERS` times until the model provides a final,
  non-tool response.

---

## Project Structure

Key files:

- `main.py`  
  Entry point. Sets up the CLI, the Gemini client, and the agent loop.
- `config.py`  
  Contains configuration like `MAX_ITERS`.
- `prompts.py`  
  Contains the system prompt used to steer the model’s behavior.
- `call_function.py`  
  Dispatches tool/function calls requested by the model.
- `functions/`  
  Individual tool implementations:
  - `get_files_info.py`
  - `get_file_content.py`
  - `run_python_file.py`
  - `write_file.py`
- `calculator/`  
  A small target project (a calculator app) the agent can inspect and run.

There are also a few test files (`test_*.py`) to validate tool behavior.

---

## Requirements

- Python (matching the version in `.python-version` / `pyproject.toml`)
- [uv](https://github.com/astral-sh/uv) or another way to run the project’s
virtual environment
- A Google AI Studio API key for Gemini

Python dependencies are managed via `pyproject.toml`.

---

## Setup

1. **Clone the repository** and enter the directory:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-dir>

Install dependencies (with uv):

uv sync

Set your API key:

Create a .env file in the project root:

echo "GEMINI_API_KEY=your_api_key_here" > .env

Or export it in your shell:

export GEMINI_API_KEY=your_api_key_here

The code uses python-dotenv (load_dotenv()) to read .env.

Usage
From the project root, run:

uv run main.py "how does the calculator render results to the console?"

Optional flags:

--verbose – prints token usage and function call results:

uv run main.py "explain what files are in the calculator project" --verbose

The agent will:

Send your prompt to Gemini along with the system prompt.
Allow the model to request tool calls (e.g., list files, read calculator/main.py).
Add both model messages and tool results to the conversation history.
Keep iterating until:
The model stops requesting tools and returns a final natural-language answer, or
The maximum number of iterations (MAX_ITERS in config.py) is reached.
If the max iterations are reached without a final answer, the program prints an
error message and exits with code 1.

How It Works (High-Level)
main():

Parses CLI args.
Loads GEMINI_API_KEY from environment.
Sets up the initial messages list with the user’s prompt.
Runs a loop up to MAX_ITERS, calling generate_content() each time.
Stops when generate_content() signals a final answer or when the iteration limit
is hit.
generate_content():

Calls client.models.generate_content() with:
The current messages history.
A tool config (tools=[available_functions]).
The system_prompt.
Appends each candidate.content from the response to messages.
If there are no function_calls, returns the final text (or signals completion,
depending on implementation).
If there are function_calls:
Uses call_function() to execute each tool.
Gathers tool output parts into a list.
Appends a new Content(role="user", parts=function_results) to messages.
Returns control to the loop for another iteration.
This pattern is a minimal example of an “agentic” loop around an LLM.

Testing
If you’re using the Boot.dev CLI, you can run the lesson’s checks locally
(replace <uuid> with the lesson’s ID):

bootdev run <uuid>

To run the test suite directly with Python/pytest (if configured), use something
like:

uv run python -m pytest

or:

uv run python calculator/tests.py

(Adjust based on the test layout you’re using.)

Notes & Limitations
The tools are limited to the specific functions implemented in functions/.
The agent uses a simple loop with a hard maximum iteration count to avoid
infinite tool‑calling.
Error handling is minimal; unexpected tool or API failures may terminate the run.
Extending the Project
Ideas for experiments:

Add more tools (e.g., search in files, run specific test suites).
Store conversation history to disk for later replay.
Swap models or tweak the system_prompt in prompts.py to change the agent’s “personality.”
Turn this into a small HTTP API instead of a CLI.
