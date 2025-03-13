"""
Embedding generator using OpenAI API.
"""

import openai
from config.settings import settings


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Returns an embedding vector for the given text using OpenAI embeddings API.
    """
    try:
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"[Embedding Error] Failed to generate embedding: {e}")
        return []
