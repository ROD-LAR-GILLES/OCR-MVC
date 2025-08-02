"""
Utilidades del sistema OCR.
"""
from .config.tesseract_config import tesseract_config
from .dynamic_dictionary import dynamic_dictionary

__all__ = ['tesseract_config', 'dynamic_dictionary']