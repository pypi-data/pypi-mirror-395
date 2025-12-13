"""
Ollama LLM Integration

Responsibility: Create Ollama LLM instances with tool binding support.
Uses ChatOpenAI with Ollama's OpenAI-compatible API for proper tool calling.
"""

from typing import Tuple, Optional, List
from langchain_core.tools import BaseTool


def create_llm_with_tools(
    tools: List[BaseTool],
    model: str = "qwen2.5-coder:14b",
    base_url: str = "http://localhost:11434/v1",
    temperature: float = 0.0
) -> Tuple[Optional[object], List[BaseTool]]:
    """
    Create Ollama LLM with function calling support.
    
    CRITICAL FIX: Use ChatOpenAI with Ollama's OpenAI-compatible API
    LangChain's ChatOllama doesn't properly parse tool calls from Ollama's native API.
    Using ChatOpenAI with Ollama's /v1 endpoint fixes this parsing issue.
    
    Args:
        tools: List of LangChain tools to bind
        model: Ollama model name (e.g., "qwen2.5-coder:14b")
        base_url: Ollama API base URL (default: http://localhost:11434/v1)
        temperature: LLM temperature (default: 0.0)
        
    Returns:
        Tuple of (LLM instance with tools bound, tools list)
        If binding fails, returns (LLM without tools, tools list)
        If import fails, returns (None, tools list)
    """
    try:
        # Use ChatOpenAI with Ollama's OpenAI-compatible API
        # This properly parses tool calls that ChatOllama misses
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model=model,
            base_url=base_url,
            api_key="ollama",  # Dummy key (Ollama doesn't require auth)
            temperature=temperature,
        )
        
        # Try to bind tools
        if tools:
            try:
                llm_with_tools = llm.bind_tools(tools)
                print(f"[OK] Tools bound successfully to {model} via OpenAI-compatible API")
                return llm_with_tools, tools
            except Exception as e:
                print(f"[WARN] Warning: bind_tools failed: {e}")
                print("   Using LLM without tool binding (manual tool calling)")
                return llm, tools
        else:
            return llm, []
            
    except ImportError:
        print("[ERROR] langchain-openai not installed")
        print("   Install with: pip install langchain-openai")
        # Fallback to ChatOllama if ChatOpenAI not available
        return _fallback_to_chatollama(tools, model, temperature)


def _fallback_to_chatollama(
    tools: List[BaseTool],
    model: str,
    temperature: float
) -> Tuple[Optional[object], List[BaseTool]]:
    """
    Fallback to ChatOllama if ChatOpenAI is not available.
    
    This follows Dependency Inversion Principle - abstract fallback strategy.
    """
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model=model, temperature=temperature)
        if tools:
            llm_with_tools = llm.bind_tools(tools)
            return llm_with_tools, tools
        return llm, []
    except ImportError:
        print("[ERROR] langchain-ollama not installed")
        print("   Install with: pip install langchain-ollama")
        return None, tools
    except Exception as e:
        print(f"[ERROR] Failed to create ChatOllama: {e}")
        return None, tools

