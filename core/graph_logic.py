from typing import Union
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langsmith import traceable

from core.state import ExtendedMessagesState
from config.settings import settings
from prompts import summarization_prompt

# Define message types for typing
MessageType = Union[AIMessage, HumanMessage, SystemMessage]

# Initialize LLM (you can switch model or source later)
llm = ChatOpenAI(model="gpt-4o", openai_api_key=settings.OPENAI_API_KEY)


@traceable()
def start_node(state: ExtendedMessagesState) -> ExtendedMessagesState:
    """
    Entry point node of the workflow.
    This is a simple example that sets a summary placeholder.
    """
    state["summary"] = "Summary will be generated during the workflow."
    return state


@traceable()
def summarization_node(state: ExtendedMessagesState) -> ExtendedMessagesState:
    """
    Summarization node using a predefined system prompt.
    """
    system_message = SystemMessage(content=summarization_prompt)
    messages = state["messages"] + [system_message]
    response = llm.invoke(messages)

    if isinstance(response, AIMessage):
        state["summary"] = response.content
    elif hasattr(response, "content"):
        state["summary"] = response.content
    else:
        state["summary"] = str(response)

    return state
