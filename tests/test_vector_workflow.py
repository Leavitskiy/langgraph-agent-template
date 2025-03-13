from services.embeddings import get_embedding


def test_embedding_generation():
    embedding = get_embedding("Test message for embedding.")
    assert isinstance(embedding, list)
    assert len(embedding) > 100  # Usually 1536 for ada-002
