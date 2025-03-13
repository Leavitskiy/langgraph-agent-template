from core.graph_logic import summarization_node
from core.state import ExtendedMessagesState
from langchain_core.messages import HumanMessage


def test_summarization_node_runs():
    state = ExtendedMessagesState(
        messages=[
            HumanMessage(content="I feel tired all day."),
            HumanMessage(content="Maybe it's work stress."),
        ],
        summary=""
    )
    new_state = summarization_node(state)
    assert isinstance(new_state["summary"], str)
    assert len(new_state["summary"].strip()) > 0
