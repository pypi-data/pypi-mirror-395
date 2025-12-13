# Realm Python SDK

Observability and time-travel debugging for AI agents. Track every decision, tool call, and state change in your agent workflows.

## Features

- 🔍 **Automatic Tracking**: Capture agent reasoning, tool calls, and state changes
- 🌳 **Git-like Branching**: Fork agent sessions at any point
- ⏪ **Time Travel**: Replay and debug past agent executions
- 🔗 **Framework Agnostic**: Works with LangChain, custom agents, and more
- 📊 **Visual UI**: Beautiful web interface to explore agent behavior

## Installation

### From PyPI

```bash
# Standard installation
pip install realm-sdk

# With LangChain integration
pip install realm-sdk[langchain]

# All integrations
pip install realm-sdk[all]
```

### From GitHub

```bash
pip install git+https://github.com/neelshar/Realm.git#subdirectory=packages/python-sdk
```

### Local Development

```bash
cd packages/python-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
from realm import RealmClient

# Initialize client
client = RealmClient(
    api_url="https://realm-api.vercel.app",  # Or your self-hosted URL
    project_id="your-project-id"
)

# Create a session
session_id = client.create_session(name="Customer Support Agent")

# Track tool calls
client.track_tool_call(
    session_id=session_id,
    tool_name="search_knowledge_base",
    tool_input={"query": "password reset"},
    tool_output={"articles": ["KB-001", "KB-002"]},
    reasoning="Searching for relevant articles"
)

# Track LLM decisions
client.track_decision(
    session_id=session_id,
    reasoning="User already tried KB solutions. Escalating to human support.",
    alternatives=["Try another KB article", "Ask for more info"],
    confidence=0.85
)

# Close session
client.close_session(session_id)
```

### LangChain Integration

```python
from realm import RealmClient, RealmCallbackHandler
from langchain.agents import AgentExecutor, create_react_agent

# Initialize Realm
client = RealmClient(api_url="...", project_id="...")
session_id = client.create_session(name="LangChain Agent")

# Create callback handler
handler = RealmCallbackHandler(client, session_id, verbose=True)

# Use with LangChain - automatic tracking!
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[handler],  # ← That's it!
    verbose=True
)

result = agent_executor.invoke({"input": "Help user with login issue"})
```

The callback handler automatically tracks:
- ✅ Agent reasoning (Chain of Thought)
- ✅ Tool calls (inputs & outputs)
- ✅ Tool errors
- ✅ Agent completion

## Examples

- [`examples/simple_agent.py`](../../examples/simple_agent.py) - Basic agent tracking
- [`examples/langchain_agent.py`](../../examples/langchain_agent.py) - Full LangChain integration

## Documentation

- [Getting Started](https://docs.realm.space/getting-started)
- [API Reference](https://docs.realm.space/api-reference)
- [LangChain Integration](https://docs.realm.space/integrations/langchain)

## Support

- 📧 Email: support@realm.space
- 💬 Discord: [Join our community](https://discord.gg/realm)
- 🐛 Issues: [GitHub Issues](https://github.com/neelshar/Realm/issues)

## License

MIT License - see [LICENSE](LICENSE) for details.

