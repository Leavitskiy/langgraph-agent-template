"""
Utilities for text chunking and token counting.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """
    Splits text into overlapping chunks for better embedding performance.
    """
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


def count_tokens(text: str, model: str = "text-embedding-ada-002") -> int:
    """
    Counts tokens in a given text for a specific model.
    """
    from tiktoken import encoding_for_model
    encoding = encoding_for_model(model)
    return len(encoding.encode(text))
