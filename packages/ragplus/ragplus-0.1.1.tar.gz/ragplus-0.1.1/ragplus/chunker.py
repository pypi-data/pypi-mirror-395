from typing import List

def chunk_text(text, size=500, overlap=50):
    """
    Split text into overlapping chunks.
    
    Args:
        text: Input text to chunk
        size: Maximum chunk size in characters
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    text = text.strip()
    if not text:
        return []

    if size <= 0:
        raise ValueError("chunk size must be > 0")

    if overlap >= size:
        raise ValueError("overlap must be < chunk size")

    chunks = []
    n = len(text)

    start = 0
    while start < n:
        end = min(start + size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move forward, not backward
        next_start = start + size - overlap
        if next_start <= start:  # safety check
            break
        start = next_start

    return chunks
