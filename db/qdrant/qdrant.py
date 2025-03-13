from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


def initialize_qdrant(
    host: str,
    port: int,
    collection_name: str,
    vector_size: int,
    distance: Distance = Distance.COSINE,
) -> QdrantClient:
    """
    Initializes Qdrant client and creates collection if it doesn't exist.
    """
    client = QdrantClient(host=host, port=port)
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
        )
    return client


def add_points_to_collection(
    client: QdrantClient,
    collection_name: str,
    points: list[PointStruct]
):
    """
    Adds vector points to the specified collection.
    """
    client.upsert(collection_name=collection_name, points=points)


def search_collection(
    client: QdrantClient,
    collection_name: str,
    query_vector: list[float],
    top_k: int
):
    """
    Performs a similarity search in the specified collection.
    """
    return client.query_points(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )
