#!/usr/bin/env python
"""
Punto de entrada principal para el sistema OCR CLI.
"""
import sys
from simple_menu import SimpleOCRMenu

def main():
    """Iniciar el menú OCR."""
    menu = SimpleOCRMenu()
    menu.run()

if __name__ == "__main__":
    main()