"""
Módulo CLI para el sistema OCR.
"""
from .interactive_menu import InteractiveMenu
from .menu_utils import MenuOption, create_file_menu_options, check_system_requirements

__all__ = [
    'InteractiveMenu', 
    'MenuOption', 
    'create_file_menu_options',
    'check_system_requirements'
]