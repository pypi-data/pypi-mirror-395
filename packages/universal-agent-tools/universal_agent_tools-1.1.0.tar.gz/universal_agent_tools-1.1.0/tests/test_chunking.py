"""
Tests for code chunking system.
"""

import pytest
from universal_agent_tools.code_chunking import (
    chunk_content,
    FileTypeDetector,
    PythonChunker,
    YamlChunker,
    MarkdownChunker,
    JsonChunker,
    GenericChunker
)


class TestFileTypeDetector:
    """Tests for file type detection."""
    
    def test_detect_python(self):
        assert FileTypeDetector.detect("test.py") == "python"
        assert FileTypeDetector.detect("module/__init__.py") == "python"
    
    def test_detect_yaml(self):
        assert FileTypeDetector.detect("config.yaml") == "yaml"
        assert FileTypeDetector.detect("config.yml") == "yaml"
    
    def test_detect_markdown(self):
        assert FileTypeDetector.detect("README.md") == "markdown"
    
    def test_detect_json(self):
        assert FileTypeDetector.detect("data.json") == "json"
    
    def test_detect_dockerfile(self):
        assert FileTypeDetector.detect("Dockerfile") == "dockerfile"
        assert FileTypeDetector.detect("test.dockerfile") == "dockerfile"
    
    def test_detect_unknown(self):
        assert FileTypeDetector.detect("unknown.txt") == "text"


class TestPythonChunker:
    """Tests for Python chunking."""
    
    def test_chunk_simple_function(self):
        code = """
def hello():
    return "world"
"""
        chunks = PythonChunker().chunk(code, "test.py")
        assert len(chunks) == 1
        assert chunks[0]["type"] == "function"
        assert chunks[0]["name"] == "hello"
    
    def test_chunk_class(self):
        code = """
class MyClass:
    def method(self):
        pass
"""
        chunks = PythonChunker().chunk(code, "test.py")
        assert len(chunks) == 1
        assert chunks[0]["type"] == "class"
        assert chunks[0]["name"] == "MyClass"
    
    def test_chunk_with_imports(self):
        code = """
import os
from pathlib import Path

def test():
    pass
"""
        chunks = PythonChunker().chunk(code, "test.py")
        assert len(chunks) == 1
        assert "import os" in chunks[0]["content"]


class TestYamlChunker:
    """Tests for YAML chunking."""
    
    def test_chunk_yaml_sections(self):
        yaml_content = """
key1: value1
key2: value2
"""
        chunks = YamlChunker().chunk(yaml_content, "test.yaml")
        assert len(chunks) >= 1
        assert any(chunk["type"] == "yaml_section" for chunk in chunks)


class TestMarkdownChunker:
    """Tests for Markdown chunking."""
    
    def test_chunk_by_headers(self):
        md_content = """
# Header 1
Content here

## Header 2
More content
"""
        chunks = MarkdownChunker().chunk(md_content, "test.md")
        assert len(chunks) >= 1


class TestJsonChunker:
    """Tests for JSON chunking."""
    
    def test_chunk_json(self):
        json_content = '{"key": "value"}'
        chunks = JsonChunker().chunk(json_content, "test.json")
        assert len(chunks) == 1
        assert chunks[0]["type"] == "json_document"


class TestGenericChunker:
    """Tests for generic chunking."""
    
    def test_chunk_small_file(self):
        content = "\n".join([f"line {i}" for i in range(50)])
        chunks = GenericChunker().chunk(content, "test.txt")
        assert len(chunks) == 1
    
    def test_chunk_large_file(self):
        content = "\n".join([f"line {i}" for i in range(200)])
        chunks = GenericChunker(chunk_size=50, overlap=5).chunk(content, "test.txt")
        assert len(chunks) > 1


class TestChunkContent:
    """Tests for main chunk_content function."""
    
    def test_chunk_python(self):
        code = "def test(): pass"
        chunks = chunk_content(code, "test.py")
        assert len(chunks) > 0
    
    def test_chunk_yaml(self):
        yaml = "key: value"
        chunks = chunk_content(yaml, "test.yaml")
        assert len(chunks) > 0

