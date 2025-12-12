# quercle-langchain

LangChain tools for [Quercle](https://quercle.dev) web search and URL fetching.

## Installation

```bash
uv add langchain-quercle
```

Or with pip:

```bash
pip install langchain-quercle
```

## Quick Start

```python
from quercle_langchain import QuercleSearchTool, QuercleFetchTool

# Initialize tools (uses QUERCLE_API_KEY env var by default)
search = QuercleSearchTool()
fetch = QuercleFetchTool()

# Or with explicit API key
search = QuercleSearchTool(api_key="qk_...")
fetch = QuercleFetchTool(api_key="qk_...")
```

## Usage with LangChain Agents

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from quercle_langchain import QuercleSearchTool, QuercleFetchTool

# Initialize tools
tools = [QuercleSearchTool(), QuercleFetchTool()]

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Run the agent
result = agent.run("Search for the latest Python release and summarize it")
```

## Direct Tool Usage

### Search

```python
from quercle_langchain import QuercleSearchTool

search = QuercleSearchTool()

# Basic search
result = search.invoke({"query": "What is TypeScript?"})
print(result)

# With domain filtering
result = search.invoke({
    "query": "machine learning tutorials",
    "allowed_domains": ["*.edu", "*.org"],
    "blocked_domains": ["ads.com"],
})
```

### Fetch

```python
from quercle_langchain import QuercleFetchTool

fetch = QuercleFetchTool()

result = fetch.invoke({
    "url": "https://docs.python.org/3/whatsnew/3.12.html",
    "prompt": "Summarize the key new features in bullet points",
})
print(result)
```

## Async Usage

Both tools support async operations:

```python
import asyncio
from quercle_langchain import QuercleSearchTool, QuercleFetchTool

async def main():
    search = QuercleSearchTool()
    fetch = QuercleFetchTool()

    # Async search
    result = await search.ainvoke({"query": "async Python programming"})
    print(result)

    # Async fetch
    result = await fetch.ainvoke({
        "url": "https://example.com",
        "prompt": "Extract main topics",
    })
    print(result)

asyncio.run(main())
```

## Configuration

### Environment Variable

Set your API key as an environment variable:

```bash
export QUERCLE_API_KEY=qk_your_api_key_here
```

### Tool Parameters

Both tools accept these optional parameters:

- `api_key`: Your Quercle API key (falls back to `QUERCLE_API_KEY` env var)
- `timeout`: Request timeout in seconds

```python
tool = QuercleSearchTool(
    api_key="qk_...",
    timeout=60.0,
)
```

## Tool Descriptions

### QuercleSearchTool

- **Name**: `search`
- **Description**: Search the web and get AI-synthesized answers with citations
- **Arguments**:
  - `query` (required): The search query
  - `allowed_domains` (optional): List of domains to include (e.g., `["*.edu"]`)
  - `blocked_domains` (optional): List of domains to exclude

### QuercleFetchTool

- **Name**: `fetch`
- **Description**: Fetch a URL and analyze its content with AI
- **Arguments**:
  - `url` (required): The URL to fetch
  - `prompt` (required): Instructions for content analysis

## License

MIT
