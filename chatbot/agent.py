"""
LangChain agent for the veterinary clinic AI assistant.
Uses OpenRouter with the glm-4.5-air:free model.
"""

import os
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from .prompts import SYSTEM_PROMPT, SEARCH_RESTRICTION_PROMPT
from .tools import get_clinic_info, get_services_list, get_veterinarians, search_veterinary_info


def get_llm():
    """Initialize the LLM with OpenRouter configuration."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    
    return ChatOpenAI(
        model="z-ai/glm-4.5-air:free",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=1024,
    )


def get_tools():
    """Get the list of tools available to the agent."""
    return [
        get_clinic_info,
        get_services_list,
        get_veterinarians,
        search_veterinary_info,
    ]


def create_agent():
    """Create and return the LangChain agent with tools."""
    llm = get_llm()
    tools = get_tools()
    
    # Create the agent using langgraph's create_react_agent
    system_message = SYSTEM_PROMPT + "\n\n" + SEARCH_RESTRICTION_PROMPT
    
    agent = create_react_agent(
        llm,
        tools,
        prompt=system_message,
    )
    
    return agent


def convert_chat_history(history: List[Dict[str, str]]) -> List:
    """Convert chat history from dict format to LangChain message format."""
    messages = []
    for msg in history:
        if msg.get("role") == "user":
            messages.append(HumanMessage(content=msg.get("content", "")))
        elif msg.get("role") == "assistant":
            messages.append(AIMessage(content=msg.get("content", "")))
    return messages


def chat(user_message: str, chat_history: List[Dict[str, str]] = None) -> str:
    """
    Process a user message and return the assistant's response.
    
    Args:
        user_message: The user's input message
        chat_history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
    
    Returns:
        The assistant's response string
    """
    if chat_history is None:
        chat_history = []
    
    try:
        agent = create_agent()
        
        # Convert history to LangChain format and add current message
        messages = convert_chat_history(chat_history)
        messages.append(HumanMessage(content=user_message))
        
        # Run the agent
        result = agent.invoke({"messages": messages})
        
        # Extract the response from the result
        if result and "messages" in result:
            # Get the last AI message
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage) and msg.content:
                    return msg.content
        
        return "Извините, произошла ошибка при обработке запроса."
        
    except ValueError as e:
        if "OPENROUTER_API_KEY" in str(e):
            return "Ассистент временно недоступен. Пожалуйста, свяжитесь с нами по телефону."
        raise
    except Exception as e:
        # Log the error in production
        print(f"Chat agent error: {e}")
        return f"Извините, произошла ошибка. Пожалуйста, попробуйте позже или свяжитесь с нами по телефону."
