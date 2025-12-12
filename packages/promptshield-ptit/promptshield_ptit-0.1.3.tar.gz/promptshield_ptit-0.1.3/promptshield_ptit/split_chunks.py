from typing import List

from .input_processor import split_into_sentences


def chunk_by_words(text: str, chunk_size: int, overlap: int) -> List[str]:
    assert overlap < chunk_size, "overlap phải nhỏ hơn chunk_size"

    words = text.split()
    if len(words) <= chunk_size:
        return [" ".join(words)] if words else []

    chunks: List[str] = []
    start = 0
    last_start = -1

    while start < len(words):
        if start == last_start:
            break  # tránh loop vô hạn
        last_start = start

        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start = end - overlap
        if start <= last_start or len(words) - start <= overlap:
            break

    return chunks


def chunk(input_text: str, chunk_size: int = 50, overlap: int = 10) -> List[str]:
    sentences = split_into_sentences(input_text)
    return chunk_by_words(" ".join(sentences), chunk_size, overlap)
