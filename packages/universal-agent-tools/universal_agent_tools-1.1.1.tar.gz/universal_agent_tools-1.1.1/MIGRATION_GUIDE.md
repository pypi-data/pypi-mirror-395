# Migration Guide

This guide helps you migrate from the old code locations to the new `universal_agent_tools` package.

## Installation

```bash
pip install -e .  # For development
# or
pip install universal-agent-tools  # When published
```

## Import Changes

### Ollama + Tools

**Old:**
```python
from universal_agent_nexus_examples.08_local_agent_runtime.runtime.agent_runtime import (
    MCPToolLoader,
    MCPTool,
    create_llm_with_tools,
    parse_tool_calls_from_content
)
```

**New:**
```python
from universal_agent_tools.ollama_tools import (
    MCPToolLoader,
    MCPTool,
    create_llm_with_tools,
    parse_tool_calls_from_content
)
```

### Code Chunking

**Old:**
```python
from universal_agent_nexus_examples.09_autonomous_flow.tools.chunk_manager import (
    chunk_content,
    chunk_python_content,
    get_file_type
)
```

**New:**
```python
from universal_agent_tools.code_chunking import (
    chunk_content,
    FileTypeDetector,
    PythonChunker
)
```

### Tool Registry

**Old:**
```python
from universal_agent_nexus_examples.tools.registry.tool_registry import (
    ToolRegistry,
    ToolDefinition,
    get_registry
)
```

**New:**
```python
from universal_agent_tools.tool_registry import (
    ToolRegistry,
    ToolDefinition,
    get_registry
)
```

## API Changes

### Chunking System

The chunking system now uses a Strategy Pattern. The API is mostly compatible, but you can now:

1. **Use custom chunkers:**
```python
from universal_agent_tools.code_chunking import Chunker, ChunkingStrategy

class MyCustomChunker(ChunkingStrategy):
    def chunk(self, content: str, file_path: str) -> List[Dict]:
        # Custom logic
        return chunks

chunker = Chunker()
chunker.register_strategy("custom_type", MyCustomChunker())
```

2. **Extend file type detection:**
```python
from universal_agent_tools.code_chunking import FileTypeDetector

FileTypeDetector.register_extension(".ts", "typescript")
```

### MCP Tools

The MCPTool class now properly handles optional parameters in schemas. No breaking changes.

### Tool Registry

No breaking changes. The API is identical.

## Remaining Components

The following components are still being extracted:
- Codebase Analyzer (Priority 2)
- GitHub Integration (Priority 2)
- Document Generator (Priority 3)
- Sync State Management (Priority 3)

These will be available in future releases. For now, continue using them from the original locations.

## Testing

Run tests to verify migration:

```bash
pytest universal_agent_tools/tests/
```

## Support

If you encounter issues during migration, check:
1. All dependencies are installed (`pip install -r requirements.txt`)
2. Import paths are updated
3. Tests pass

For questions, see the main README.md or open an issue.

