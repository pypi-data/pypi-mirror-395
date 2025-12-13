"""
Text file loader with encoding detection.
"""

import chardet


def load_text(file_path: str, encoding: str = None) -> str:
    """
    Load text from a text file with automatic encoding detection.
    
    Args:
        file_path: Path to text file
        encoding: Optional encoding (auto-detected if None)
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if encoding is None:
        # Detect encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
    
    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
        return f.read().strip()
