"""
Punto de entrada principal para la interfaz CLI.
"""
import sys
from pathlib import Path

def main():
    """Función principal del CLI."""
    # Agregar el directorio raíz al path para importaciones
    root_dir = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(root_dir))
    
    print("Iniciando Sistema OCR - Docker Version")
    print("=" * 40)
    
    try:
        # Usar menú simplificado para empezar
        from views.cli.simple_menu import main as simple_main
        simple_main()
        
    except ImportError as e:
        print(f"ERROR: No se pudieron importar los módulos necesarios:")
        print(f"  {e}")
        print("\nIntentando con menú básico...")
        
        # Fallback básico
        print("Sistema OCR básico iniciado")
        print("Verifique que Docker tenga todas las dependencias instaladas")
        
    except KeyboardInterrupt:
        print("\n\nSaliendo del sistema...")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR FATAL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
