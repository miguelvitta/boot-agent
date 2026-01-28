# AI Code Assistant Agent

A **CLI-based AI agent** that can inspect, execute, and debug a Python project using **Google Gemini**.
This repository demonstrates how to build a minimal but practical *agentic loop* around a large language model (LLM) with tool/function calling.

The project is intentionally small, explicit, and educational, while remaining useful as a base for further experimentation or extension.

---

## Table of Contents

* [Overview](#overview)
* [Core Concepts](#core-concepts)
* [Features](#features)
* [Project Structure](#project-structure)
* [Requirements](#requirements)
* [Setup](#setup)
* [Usage](#usage)
* [Agent Execution Flow](#agent-execution-flow)
* [Implementation Overview](#implementation-overview)
* [Testing](#testing)
* [Limitations](#limitations)
* [Extending the Project](#extending-the-project)
* [License](#license)

---

## Overview

This agent can answer questions such as:

> “How does the calculator render results to the console?”

by dynamically:

* Inspecting source files
* Executing Python code
* Iterating over tool calls until a final answer is produced

The target project (`calculator/`) is deliberately simple, allowing the focus to remain on **agent mechanics**, not application complexity.

---

## Core Concepts

This project demonstrates:

* LLM invocation via API
* Tool / function calling
* Controlled file inspection and execution
* Stateful conversation management
* Iterative reasoning with a bounded loop

It can be viewed as a minimal reference implementation of an **LLM-powered code inspection agent**.

---

## Features

### Command-Line Interface

* Interact with the agent using natural-language prompts from the terminal.

### LLM Integration

* Uses **Google Gemini** (`gemini-2.5-flash` by default).

### Tool Calling

The model may request execution of the following tools:

* `get_files_info` — list available project files
* `get_file_content` — read file contents
* `run_python_file` — execute Python files and capture output
* `write_file` — modify files (e.g., apply fixes)

### Agent Loop

* Maintains a structured `messages` conversation history.
* Appends:

  * Model responses
  * Tool execution results
* Iterates until:

  * A final natural-language response is produced, or
  * A maximum iteration limit is reached

---

## Project Structure

```text
.
├── main.py
├── config.py
├── prompts.py
├── call_function.py
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/
│   └── (example calculator project)
├── test_*.py
├── pyproject.toml
└── .python-version
```

### Key Files

* **`main.py`**
  CLI entry point. Initializes the Gemini client and runs the agent loop.

* **`config.py`**
  Centralized configuration (e.g., `MAX_ITERS`).

* **`prompts.py`**
  Defines the system prompt that constrains and guides model behavior.

* **`call_function.py`**
  Dispatch layer for executing model-requested tools.

* **`functions/`**
  Individual tool implementations.

* **`calculator/`**
  Example target project used for inspection and execution.

---

## Requirements

* Python version specified in `.python-version` / `pyproject.toml`
* A virtual environment manager (recommended: [uv](https://github.com/astral-sh/uv))
* A Google AI Studio API key for Gemini

All Python dependencies are declared in `pyproject.toml`.

---

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-dir>
```

### 2. Install Dependencies

Using `uv`:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Or export it directly:

```bash
export GEMINI_API_KEY=your_api_key_here
```

The project uses `python-dotenv` to load environment variables.

---

## Usage

Run the agent from the project root:

```bash
uv run main.py "how does the calculator render results to the console?"
```

### Optional Flags

* **`--verbose`**
  Prints additional details such as token usage and tool call results.

```bash
uv run main.py "list the files in the calculator project" --verbose
```

---

## Agent Execution Flow

1. The user prompt and system prompt are sent to Gemini.
2. The model may request tool calls.
3. Requested tools are executed locally.
4. Tool outputs are appended to the conversation history.
5. The loop continues until:

   * The model returns a final response, or
   * `MAX_ITERS` is exceeded

If the iteration limit is reached without completion, the program:

* Prints an error message
* Exits with status code `1`

---

## Implementation Overview

### `main()`

* Parses CLI arguments
* Loads environment variables
* Initializes the message history
* Runs the agent loop (bounded by `MAX_ITERS`)

### `generate_content()`

* Calls `client.models.generate_content()` with:

  * Current conversation history
  * Tool definitions
  * System prompt
* Appends model responses to `messages`
* If tool calls are present:

  * Executes them via `call_function()`
  * Appends tool results as a new user message
  * Returns control to the loop
* If no tool calls remain:

  * Returns the final response

This structure forms a minimal, explicit **agentic reasoning loop**.

---

## Testing

Run the test suite using:

```bash
uv run python -m pytest
```

or, if tests are simple scripts:

```bash
uv run python calculator/tests.py
```

(Adjust based on your test layout.)

---

## Limitations

* Tools are explicitly whitelisted and limited to those in `functions/`
* The agent uses a fixed iteration cap to prevent infinite loops
* Error handling is intentionally minimal
* The project is not sandboxed; tools execute local code

---

## Extending the Project

Possible extensions include:

* Adding new tools (e.g., file search, static analysis, test runners)
* Persisting conversation history to disk
* Supporting multiple models or providers
* Exposing the agent via an HTTP API
* Adding structured logging and tracing
* Hardening execution with sandboxing or permissions

---

## License
