# langchain-pubnub

[![PyPI version](https://badge.fury.io/py/langchain-pubnub.svg)](https://badge.fury.io/py/langchain-pubnub)
[![Python Version](https://img.shields.io/pypi/pyversions/langchain-pubnub.svg)](https://pypi.org/project/langchain-pubnub/)

LangChain integration for [PubNub](https://www.pubnub.com/) real-time messaging platform. This package provides tools that allow LangChain agents to publish messages, fetch message history, and subscribe to real-time updates.

## Installation

```bash
pip install langchain-pubnub langchain-core langchain langgraph-prebuilt langgraph langchain-openai
```

## Quick Start

### Using the Toolkit

```python
from langchain_pubnub import PubNubToolkit

# Initialize the toolkit
toolkit = PubNubToolkit(
    publish_key="your-publish-key",  # or "demo" for testing
    subscribe_key="your-subscribe-key",  # or "demo" for testing
    user_id="my-langchain-agent"
)

# Get all tools
tools = toolkit.get_tools()

# Or access individual tools
publish_tool = toolkit.publish_tool
history_tool = toolkit.history_tool
subscribe_tool = toolkit.subscribe_tool
```

### Using the Factory Function

```python
from langchain_pubnub import create_pubnub_tools

tools = create_pubnub_tools(
    publish_key="demo",
    subscribe_key="demo",
    user_id="my-agent"
)
```

### With a LangChain Agent

```python
from langchain_pubnub import create_pubnub_tools
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Create tools
tools = create_pubnub_tools(
    publish_key="your-publish-key",
    subscribe_key="your-subscribe-key",
    user_id="my-agent"
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-5")

# Create agent
prompt = PromptTemplate.from_template("""...""")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use the agent
agent_executor.invoke({
    "input": "Send a greeting to the 'announcements' channel"
})
```

## Available Tools

### PubNubPublishTool

Publish messages to a PubNub channel.

```python
result = publish_tool.invoke({
    "channel": "my-channel",
    "message": {"text": "Hello, World!"},
    "meta": {"priority": "high"}  # optional
})
```

**Parameters:**
- `channel` (str, required): The channel to publish to
- `message` (str | dict, required): The message payload (must be JSON-serializable)
- `meta` (dict, optional): Metadata for message filtering

### PubNubHistoryTool

Fetch historical messages from PubNub channels.

```python
result = history_tool.invoke({
    "channels": ["channel-1", "channel-2"],
    "count": 25,
    "include_meta": True
})
```

**Parameters:**
- `channels` (list[str], required): Channels to fetch history from
- `count` (int, optional): Number of messages per channel (default: 25, max: 100)
- `include_meta` (bool, optional): Include message metadata (default: False)
- `start` (int, optional): Start timetoken for pagination
- `end` (int, optional): End timetoken for pagination

### PubNubSubscribeTool

Subscribe to a channel and collect real-time messages.

```python
result = subscribe_tool.invoke({
    "channel": "my-channel",
    "timeout": 300,
    "max_messages": 10
})
```

**Parameters:**
- `channel` (str, required): The channel to subscribe to
- `timeout` (int, optional): Max seconds to wait (default: 300)
- `max_messages` (int, optional): Max messages to collect (default: 10)

## Configuration Options

The `PubNubToolkit` accepts additional configuration options:

```python
toolkit = PubNubToolkit(
    publish_key="your-publish-key",
    subscribe_key="your-subscribe-key",
    user_id="my-agent",
    ssl=True,  # Enable SSL (default: True)
    # Additional PNConfiguration options...
)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/pubnub/langchain-pubnub.git
cd langchain-pubnub

# Install dependencies
pip install -e ".[dev]"

# Install test dependencies
pip install -e ".[test]"
```

### Running Tests

```bash
# Run unit tests
pytest tests/unit_tests/ -v

# Run integration tests (requires network)
pytest tests/integration_tests/ -v

# Run all tests with coverage
pytest --cov=langchain_pubnub --cov-report=term-missing
```

### Linting

```bash
# Run ruff linter
ruff check .

# Run ruff formatter
ruff format .
```

### Type Checking

```bash
mypy langchain_pubnub
```

## Requirements

- Python >= 3.9
- langchain-core >= 0.2.0
- pubnub >= 10.0.0
- pydantic >= 2.0.0

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## Links

- [PubNub Documentation](https://www.pubnub.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [GitHub Repository](https://github.com/pubnub/langchain-pubnub)
