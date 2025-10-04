# AI-Agent

An LLM-powered command-line AI coding agent capable of autonomously reading, updating, and running Python code using the Gemini API with function calling.

## Features

- **File System Operations**: List directories, read file contents, and write/update files
- **Python Execution**: Run Python scripts with arguments within a secure working directory
- **Function Calling**: Utilizes Gemini's function calling API for structured interactions
- **Multi-turn Conversations**: Supports iterative agent conversations for complex tasks
- **Security**: Path validation to prevent directory traversal attacks

## Available Functions

The AI agent can perform the following operations:

- `get_files_info` - List files and directories in a specified path
- `get_file_content` - Read the contents of a file (with truncation for large files)
- `run_python` - Execute Python files with optional arguments
- `write_file` - Write or overwrite file contents

All file paths are relative to the working directory and automatically validated for security.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/leonardHD0433/AI-Agent.git
cd AI-Agent
```

2. Install dependencies using `uv`:
```bash
uv sync
```

Or using pip:
```bash
pip install google-genai python-dotenv
```

3. Set up your environment variables:
```bash
# Create a .env file in the root directory
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

Run the AI agent with a natural language prompt:

```bash
uv run main.py "your prompt here"
```

### Examples

```bash
# List files in the calculator directory
uv run main.py "show me what files are in the calculator directory"

# Read a specific file
uv run main.py "read the calculator/main.py file"

# Run a Python script
uv run main.py "run the calculator tests"

# Modify code (If there are any)
uv run main.py "fix the bug in calculator/pkg/calculator.py: 3 + 7 * 2 shouldn't be 20"
```

### Verbose Mode

Enable verbose output to see detailed function calling information:

```bash
uv run main.py "your prompt" --verbose
```

## Project Structure

```
AI-Agent/
├── main.py                    # Main entry point for the AI agent
├── call_function.py          # Function calling handler
├── functions/                # Function implementations
│   ├── get_files_info.py    # Directory listing
│   ├── get_file_content.py  # File reading
│   ├── run_python.py        # Python execution
│   ├── write_file.py        # File writing
│   └── utils.py             # Shared utilities
├── calculator/               # Example Python project
│   ├── main.py
│   ├── tests.py
│   └── pkg/
├── pyproject.toml           # Project dependencies
└── .env                     # API keys (not committed)
```

## How It Works

1. The user provides a natural language prompt via command line
2. The prompt is sent to Gemini 2.0 Flash with available function declarations
3. Gemini decides which functions to call based on the request
4. The agent executes the functions and returns results
5. Gemini processes the results and may call additional functions
6. The conversation continues until the task is complete (max 20 iterations)

## Security Features

- Path validation prevents directory traversal attacks
- All file operations are constrained to the working directory
- Python execution has a 30-second timeout limit
- File content is truncated for large files (>10k characters)

## Development

Run tests:
```bash
uv run tests.py
```

## Requirements

- Python ≥ 3.12
- google-genai ≥ 1.12.1
- python-dotenv ≥ 1.1.0

## Credits

Guided by [boot.dev](https://boot.dev)

## License

MIT