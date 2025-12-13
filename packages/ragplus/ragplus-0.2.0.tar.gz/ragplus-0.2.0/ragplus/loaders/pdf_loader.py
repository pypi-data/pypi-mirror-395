"""
PDF document loader using pdfplumber (fully offline).
"""

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def load_pdf(file_path: str) -> str:
    """
    Load text from a PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text content
        
    Raises:
        ImportError: If pdfplumber is not installed
        FileNotFoundError: If file doesn't exist
    """
    if pdfplumber is None:
        raise ImportError("Install pdfplumber: pip install pdfplumber")
    
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()
