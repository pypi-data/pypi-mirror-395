from typing import List
import re

try:
    import nltk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


def chunk_text(text, size=500, overlap=50, strategy="fixed"):
    """
    Split text into chunks using various strategies.
    
    Args:
        text: Input text to chunk
        size: Maximum chunk size in characters (for fixed strategy)
        overlap: Number of characters to overlap between chunks (for fixed strategy)
        strategy: Chunking strategy - "fixed", "sentence", "markdown", or "heading"
        
    Returns:
        List of text chunks
    """
    text = text.strip()
    if not text:
        return []

    if strategy == "fixed":
        return _chunk_fixed(text, size, overlap)
    elif strategy == "sentence":
        return _chunk_sentence(text, size)
    elif strategy == "markdown":
        return _chunk_markdown(text)
    elif strategy == "heading":
        return _chunk_heading(text)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def _chunk_fixed(text, size=500, overlap=50):
    """Fixed-size chunking with overlap."""
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


def _chunk_sentence(text, max_sentences=5):
    """Sentence-based chunking using nltk."""
    if not NLTK_AVAILABLE:
        # Fallback to simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
    else:
        try:
            sentences = nltk.sent_tokenize(text)
        except LookupError:
            # Download punkt tokenizer if not available
            try:
                nltk.download('punkt', quiet=True)
                sentences = nltk.sent_tokenize(text)
            except:
                # Fallback
                sentences = re.split(r'[.!?]+', text)
    
    # Group sentences into chunks
    chunks = []
    current_chunk = []
    
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        current_chunk.append(sent)
        
        if len(current_chunk) >= max_sentences:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    
    # Add remaining sentences
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def _chunk_markdown(text):
    """Markdown-aware chunking based on headers and sections."""
    # Split by markdown headers
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    
    for line in lines:
        # Check if line is a header
        if re.match(r'^#{1,6}\s', line):
            # Save previous chunk
            if current_chunk:
                chunks.append('\n'.join(current_chunk).strip())
            # Start new chunk with header
            current_chunk = [line]
        else:
            current_chunk.append(line)
    
    # Add final chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if chunk_text:
            chunks.append(chunk_text)
    
    return chunks if chunks else [text]


def _chunk_heading(text):
    """Heading-based chunking for structured documents."""
    # Split by common heading patterns
    heading_pattern = r'\n(?=[A-Z][A-Za-z\s]+:|\d+\.|Chapter|Section|Part)'
    
    chunks = re.split(heading_pattern, text)
    
    # Clean and filter chunks
    cleaned_chunks = []
    for chunk in chunks:
        chunk = chunk.strip()
        if chunk and len(chunk) > 10:  # Minimum chunk size
            cleaned_chunks.append(chunk)
    
    return cleaned_chunks if cleaned_chunks else [text]
