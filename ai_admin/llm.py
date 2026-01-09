import os
from langchain_openai import ChatOpenAI

def get_llm(temperature=0.0, model="qwen/qwen3-coder:free"):
    """
    Initialize the LLM with OpenRouter configuration for AI Admin agents.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    
    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=temperature,
        max_tokens=2048,
    )
