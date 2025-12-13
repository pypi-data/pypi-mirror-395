"""
Document loaders for various file formats.
All loaders are fully offline.
"""

from .pdf_loader import load_pdf
from .text_loader import load_text
from .docx_loader import load_docx
from .base import load_document

__all__ = [
    "load_pdf",
    "load_text",
    "load_docx",
    "load_document",
]
