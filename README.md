# Agent Framework

A lightweight, modular agent framework for building AI assistants with tool integration.

## Features

- **Modular Architecture**: Easy to add and manage tools
- **Mistral AI Integration**: Uses Mistral's API for powerful AI responses
- **Tool Calling**: Supports function calling for external data fetching
- **Rich Output Formatting**: Beautiful console output with Rich library
- **Debug Mode**: Optional debug information for development

## Installation

```bash
uv sync
```

This will automatically create a virtual environment and install all dependencies from `pyproject.toml`.

## Setup

1. Create a `.env` file with your API key:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

2. The agent is configured to use Mistral AI by default. To switch to Gemini API, modify the `base_url` in `main.py`.

## Usage

Run the agent:

```bash
uv run main.py
```

Then enter your query when prompted. The agent will:
1. Process your query
2. Call any necessary tools
3. Generate a response

### Using an Alias (Optional)

For convenience, add this to your shell config:

```bash
alias agent="uv run main.py"
```

Then you can simply run:

```bash
agent
```

## Tools

### Available Tools

- **fetch_security_data**: Get stock market data (price, change, P/E ratio, industry) for Indian securities using NSE data

### Adding New Tools

To add a new tool:

1. Define the tool function in `core/tools.py`
2. Create a Pydantic model for the arguments
3. Add the tool to the `TOOLS` list in `main.py`

Example:

```python
# In core/tools.py
def my_new_tool(param1: str, param2: int):
    # Implementation
    return result

class MyNewToolArgs(BaseModel):
    param1: str = Field(..., description="Description of param1")
    param2: int = Field(..., description="Description of param2")
```

```python
# In main.py
TOOLS.append({
    "schema": {
        "type": "function",
        "function": {
            "name": "my_new_tool",
            "description": "Description of what the tool does",
            "parameters": MyNewToolArgs.model_json_schema(),
        },
    },
    "function": my_new_tool,
})
```

## Configuration

### Debug Mode

Enable debug mode in `main.py`:

```python
agent = Agent(client, system, tools, debug=True)
```

This will show detailed tool execution information.

### Custom System Prompt

Modify the system prompt in `main.py`:

```python
system = "You are a helpful AI assistant specialized in X, Y, Z."
```

## Project Structure

```
agents/
├── main.py                  # Entry point and configuration
├── core/
│   ├── agent.py             # Core agent logic
│   └── tools.py             # Tool definitions
├── app/
│   └── execution_builder.py # Application logic
├── presentation/
│   ├── cli_renderer.py      # CLI output rendering
│   └── formatting.py        # Formatting utilities
├── domain/
│   └── models.py            # Data models
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── .env                     # Environment variables (not committed)
```

## Examples

### Query Stock Information

```
Query: What is the current price of Infosys?

Tool Called: fetch_security_data
Arguments: {"symbol": "INFY"}

Assistant Response:
Price: ₹1,234.56, Change: +1.23%, P/E: 24.56, Industry: Information Technology
```

## Dependencies

All dependencies are listed in `pyproject.toml` and will be installed automatically with `uv sync`.

## License

MIT License
