def build_context(chunks, max_chars=4000, sep="\n---\n"):
    """
    Build context string from chunks, respecting character limit.
    
    Args:
        chunks: List of text chunks
        max_chars: Maximum total characters
        sep: Separator between chunks
        
    Returns:
        Combined context string
    """
    ctx = []
    total = 0
    for ch in chunks:
        part = (sep if ctx else "") + ch
        if total + len(part) > max_chars:
            break
        ctx.append(part)
        total += len(part)
    return "".join(ctx)
