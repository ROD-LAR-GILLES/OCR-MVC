"""
Modelos para el sistema OCR.
"""

from .document import Document
from .validator import DocumentValidator
from .result_manager import ResultManager
from .pdf_processor import pdf_processor, AdvancedPDFProcessor

__all__ = ['Document', 'DocumentValidator', 'ResultManager', 'pdf_processor', 'AdvancedPDFProcessor']
