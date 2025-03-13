from langgraph.graph import MessagesState


class ExtendedMessagesState(MessagesState):
    """
    Extended state used within the LangGraph workflow.
    You can add custom fields here for additional tracking or analysis.
    """
    summary: str
