def chunk_text(text: str, chunk_size: int, overlap: int = 10) -> list[str]:
    """
    Split text into chunks of specified size with optional overlap.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Percentage of chunks, you want to preserve as overlap, commonly 10-20%.
    
    Returns:
        List of text chunks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if 100<= overlap < 0:
        raise ValueError("overlap must be >= 0 and < 100 (percentage)")  
    # Convert overlap from percentage to characters
    overlap = int((overlap * chunk_size) / 100)
    
    chunks: list[str] = []
    pointer = 0
    step = chunk_size - overlap
    
    while pointer < len(text):
        chunk = text[pointer:pointer + chunk_size].strip()
        chunks.append(chunk)
        pointer += step
    
    return chunks