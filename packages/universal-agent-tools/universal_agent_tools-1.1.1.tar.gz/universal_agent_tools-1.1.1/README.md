# Universal Agent Tools

Reusable tools and utilities extracted from the Universal Agent Nexus examples.

## Overview

This package contains production-ready, reusable components for:
- **Ollama + Tools Integration** - Working pattern for Ollama LLMs with MCP tools
- **Code Chunking** - Multi-format intelligent chunking (Python, YAML, Markdown, JSON)
- **MCP Server Framework** - Base classes for creating MCP-compliant servers
- **Tool Registry** - Centralized tool discovery and management
- **Codebase Analyzer** - AST parsing, dependency graphs, PageRank scoring
- **GitHub Integration** - CLI-based GitHub operations
- **Document Generator** - Structured document generation
- **Sync State Management** - Generic sync state tracking

## Installation

```bash
pip install universal-agent-tools
```

Or install with optional dependencies:

```bash
# With Qdrant support
pip install universal-agent-tools[qdrant]

# With GitHub API support
pip install universal-agent-tools[github]

# Development dependencies
pip install universal-agent-tools[dev]
```

## Quick Start

### Ollama + Tools

```python
from universal_agent_tools.ollama_tools import (
    MCPToolLoader,
    create_llm_with_tools
)

# Load tools from MCP server
tools = MCPToolLoader.load_from_server("http://localhost:8000/mcp")

# Create LLM with tools
llm, tools = create_llm_with_tools(tools, model="qwen2.5-coder:14b")
```

### Code Chunking

```python
from universal_agent_tools.code_chunking import chunk_content

# Chunk any file type
chunks = chunk_content(content, "example.py")

# Each chunk has: type, name, content, line_start, line_end, docstring
for chunk in chunks:
    print(f"{chunk['type']}: {chunk['name']} (lines {chunk['line_start']}-{chunk['line_end']})")
```

### Tool Registry

```python
from universal_agent_tools.tool_registry import get_registry

registry = get_registry()
registry.register_server("filesystem", "http://localhost:8000/mcp")
tools = registry.discover_tools()

for tool in registry.list_tools():
    print(f"{tool.name}: {tool.description}")
```

## Architecture

This package follows **SOLID design principles**:

- **Single Responsibility** - Each module has one clear purpose
- **Open/Closed** - Extensible without modification (e.g., custom chunkers)
- **Liskov Substitution** - Protocols/interfaces ensure substitutability
- **Interface Segregation** - Focused, minimal interfaces
- **Dependency Inversion** - Depend on abstractions, not concretions

## Components

### Priority 1 (Production-Ready)

1. **ollama_tools/** - Ollama + LangChain + MCP integration
2. **code_chunking/** - Multi-format chunking system
3. **mcp_framework/** - MCP server framework

### Priority 2 (Well-Tested)

4. **tool_registry/** - Tool discovery system
5. **codebase_analyzer/** - AST analysis and dependency graphs
6. **github_tools/** - GitHub CLI integration

### Priority 3 (Useful Patterns)

7. **document_generator/** - Structured document generation
8. **sync_state/** - Generic sync state tracking

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=universal_agent_tools

# Specific component
pytest tests/test_chunking.py
```

## License

MIT License

## Contributing

This package is extracted from `universal_agent_nexus_examples`. 
See `REFACTORING_ANALYSIS.md` in the examples repo for extraction details.

