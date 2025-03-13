"""
Qdrant service functions for upserting and searching vector data.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from uuid import uuid4


def upsert_documents(
    client: QdrantClient,
    collection_name: str,
    texts: list[str],
    embeddings: list[list[float]]
) -> None:
    """
    Inserts or updates documents in the Qdrant collection with their embeddings.

    :param client: Initialized Qdrant client
    :param collection_name: Name of the Qdrant collection
    :param texts: List of texts to be stored
    :param embeddings: Corresponding list of embeddings
    """
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={"text": text}
        )
        for text, embedding in zip(texts, embeddings)
    ]

    client.upsert(collection_name=collection_name, points=points)


def search_similar_documents(
    client: QdrantClient,
    collection_name: str,
    query_vector: list[float],
    top_k: int = 5
) -> list[str]:
    """
    Searches for similar documents based on vector similarity in the specified collection.

    :param client: Initialized Qdrant client
    :param collection_name: Name of the Qdrant collection
    :param query_vector: Embedding vector to search with
    :param top_k: Number of top results to retrieve
    :return: List of text payloads from the most similar documents
    """
    search_results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    return [
        point.payload["text"] for point in search_results.points
        if point.payload and "text" in point.payload
    ]
