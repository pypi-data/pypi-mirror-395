"""
Unified document loader with auto-detection.
"""

import os
from .pdf_loader import load_pdf
from .text_loader import load_text
from .docx_loader import load_docx


def load_document(file_path: str) -> str:
    """
    Load document with automatic format detection.
    
    Supports: PDF, DOCX, TXT, MD, and other text formats.
    
    Args:
        file_path: Path to document file
        
    Returns:
        Extracted text content
        
    Raises:
        ValueError: If file format is not supported
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    # Route to appropriate loader
    if ext == '.pdf':
        return load_pdf(file_path)
    elif ext in ['.docx', '.doc']:
        return load_docx(file_path)
    elif ext in ['.txt', '.md', '.markdown', '.rst', '.log']:
        return load_text(file_path)
    else:
        # Try as text file
        try:
            return load_text(file_path)
        except Exception as e:
            raise ValueError(f"Unsupported file format: {ext}") from e
