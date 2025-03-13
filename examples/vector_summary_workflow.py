"""
Example: Simulate a user conversation, store it in Qdrant via embeddings,
and perform summarization based on retrieved similar messages.
"""

from config.settings import settings
from core.state import ExtendedMessagesState
from langchain_core.messages import HumanMessage

from db.qdrant.qdrant import initialize_qdrant
from services.cleaning import clean_text
from services.embeddings import get_embedding
from services.vector_service import upsert_documents, search_similar_documents
from core.graph_logic import summarization_node

COLLECTION_NAME = "conversation_snippets"
VECTOR_SIZE = 1536  # Expected size for text-embedding-ada-002


def simulate_conversation() -> list[str]:
    """
    Simulated user conversation messages.
    """
    return [
        "Hi, I'm having trouble focusing at work lately.",
        "I think it might be due to stress from recent deadlines.",
        "Sometimes I also feel unmotivated and tired all day.",
        "What are some ways to stay productive and energized?",
    ]


def main():
    # Step 1: Simulate conversation
    messages = simulate_conversation()

    # Step 2: Clean and embed messages
    cleaned_messages = [clean_text(msg) for msg in messages]
    embeddings = [get_embedding(msg) for msg in cleaned_messages]

    # Step 3: Filter out failed embeddings
    cleaned_messages = [
        msg for msg, emb in zip(cleaned_messages, embeddings) if emb and len(emb) == VECTOR_SIZE
    ]
    embeddings = [emb for emb in embeddings if emb and len(emb) == VECTOR_SIZE]

    # Step 4: Initialize Qdrant and store documents
    client = initialize_qdrant(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        collection_name=COLLECTION_NAME,
        vector_size=VECTOR_SIZE,
    )
    upsert_documents(client, COLLECTION_NAME, cleaned_messages, embeddings)

    # Step 5: Simulate new query
    new_message = "I often feel very tired during the day. Could this be stress-related?"
    query_vector = get_embedding(clean_text(new_message))

    if not query_vector or len(query_vector) != VECTOR_SIZE:
        print("Failed to generate embedding for query message.")
        return

    # Step 6: Retrieve similar documents
    retrieved_messages = search_similar_documents(
        client, COLLECTION_NAME, query_vector=query_vector, top_k=3
    )

    print("\n--- Retrieved Messages ---")
    for msg in retrieved_messages:
        print(f"- {msg}")

    # Step 7: Summarize retrieved messages
    messages_for_summary = [HumanMessage(content=text) for text in retrieved_messages]
    state = ExtendedMessagesState(messages=messages_for_summary, summary="")
    final_state = summarization_node(state)

    print("\n--- Summary ---")
    print(final_state["summary"])


if __name__ == "__main__":
    main()
