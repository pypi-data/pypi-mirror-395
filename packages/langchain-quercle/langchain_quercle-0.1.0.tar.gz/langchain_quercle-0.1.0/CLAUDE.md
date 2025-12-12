# CLAUDE.md - Quercle LangChain Integration

## Project Overview

Python package integrating Quercle web tools with LangChain agents. Provides `QuercleSearchTool` and `QuercleFetchTool` for AI-powered web search and URL fetching.

## Development Guidelines

**IMPORTANT:**
- Always use the **latest stable versions** of all dependencies
- Use **`uv`** for Python package management (NOT pip)
- Use modern Python patterns and type hints
- Check PyPI for current versions before specifying dependencies

## Quercle API

### Authentication
- Header: `X-API-Key: qk_...`
- Env var: `QUERCLE_API_KEY`

### Endpoints

**POST https://quercle.dev/api/v1/fetch**
```json
// Request
{"url": "https://...", "prompt": "Summarize this page"}
// Response
{"result": "AI-processed content..."}
```

**POST https://quercle.dev/api/v1/search**
```json
// Request
{"query": "...", "allowed_domains": ["*.edu"], "blocked_domains": ["spam.com"]}
// Response
{"result": "Synthesized answer with [1] citations...\n\nSources:\n[1] Title - URL"}
```

## Package Structure

```
quercle_langchain/
├── __init__.py          # Exports QuercleSearchTool, QuercleFetchTool
├── tools.py             # LangChain Tool implementations (uses quercle SDK)
└── py.typed             # PEP 561 marker
tests/
└── test_tools.py
pyproject.toml
README.md
LICENSE                  # MIT
```

## Tools

### QuercleSearchTool
- Extends `langchain_core.tools.BaseTool`
- Name: `search`
- Description: Imported from `quercle.SEARCH_TOOL_DESCRIPTION`
- Args: `query: str`, `allowed_domains: Optional[List[str]]`, `blocked_domains: Optional[List[str]]`

### QuercleFetchTool
- Extends `langchain_core.tools.BaseTool`
- Name: `fetch`
- Description: Imported from `quercle.FETCH_TOOL_DESCRIPTION`
- Args: `url: str`, `prompt: str`

## Commands

```bash
uv sync                    # Install deps
uv run pytest             # Run tests
uv run ruff check .       # Lint
uv build                  # Build package
uv publish                # Publish to PyPI
```

## Dependencies

- Python 3.10+
- quercle >= 0.1.0 (Quercle Python SDK)
- langchain-core >= 0.2.0
- pydantic >= 2.0

## Usage Example

```python
from quercle_langchain import QuercleSearchTool, QuercleFetchTool

# Initialize with API key (or use QUERCLE_API_KEY env var)
search = QuercleSearchTool()
fetch = QuercleFetchTool(api_key="qk_...")

# Use with agent
from langchain.agents import initialize_agent
agent = initialize_agent(tools=[search, fetch], llm=llm)

# Direct usage
result = search.invoke({"query": "What is TypeScript?"})
result = fetch.invoke({"url": "https://example.com", "prompt": "Summarize"})
```

## Publishing

- Package name on PyPI: `langchain-quercle`
- Use trusted publishing with GitHub Actions OIDC
