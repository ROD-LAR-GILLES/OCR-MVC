"""
Interfaz CLI usando el controller simplificado.
"""
import os
import sys
from pathlib import Path

# Configurar path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from controllers.ocr_controller import OCRController


class OCRMenu:
    """Interfaz CLI simplificada."""
    
    def __init__(self):
        self.controller = OCRController()
        self.running = True
    
    def run(self):
        """Ejecutar menú principal."""
        while self.running:
            try:
                self._show_main_screen()
                choice = input("Seleccione una opción (1-3): ").strip()  # ← Cambiar a 1-3
                
                # ELIMINAR la opción "1" de verificar sistema
                if choice == "1":
                    self._handle_process_pdf()  # ← Mover a opción 1
                elif choice == "2":
                    self._handle_view_results()  # ← Mover a opción 2
                elif choice == "3":
                    self._handle_exit()  # ← Mover a opción 3
                else:
                    print("\nOpción inválida")
                
                if choice != "3":  # ← Cambiar a 3
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\nSaliendo...")
                self.running = False
            except Exception as e:
                print(f"\nError: {e}")
                input("\nPresione Enter para continuar...")
    
    def _show_main_screen(self):
        self._clear_screen()
        print("=" * 60)
        print("SISTEMA OCR - PROCESAMIENTO DE PDFs")
        print("=" * 60)
        print(f"PDFs: {self.controller.get_pdfs_dir()}")
        print(f"Resultados: {self.controller.get_results_dir()}")
        print()
        # ELIMINAR: print("1. Verificar sistema")
        print("1. Procesar PDF")      # ← Renumerar
        print("2. Ver resultados")    # ← Renumerar
        print("3. Salir")            # ← Renumerar
        print()
    
    # ELIMINAR COMPLETAMENTE este método:
    # def _handle_system_status(self):
    #     print("\nESTADO DEL SISTEMA")
    #     print("-" * 30)
    #     ...todo el método...
    
    def _handle_process_pdf(self):
        print("\nPROCESAR PDF")
        print("-" * 20)
        
        pdfs = self.controller.get_available_pdfs()
        if not pdfs:
            print("No hay PDFs disponibles")
            return
        
        for i, pdf in enumerate(pdfs, 1):
            size_mb = pdf.stat().st_size / (1024 * 1024)
            print(f"{i:2d}. {pdf.name} ({size_mb:.1f} MB)")
        
        try:
            choice = int(input(f"\nSeleccione PDF (1-{len(pdfs)}): "))
            if 1 <= choice <= len(pdfs):
                selected_pdf = pdfs[choice - 1]
                print(f"\nProcesando: {selected_pdf.name}")
                
                result = self.controller.process_pdf(selected_pdf)
                
                if result.get("success"):
                    method = result.get("method", "unknown")
                    print("✓ Procesamiento exitoso")
                    print(f"  Método: {method}")  # ← Mostrar método usado
                    print(f"  Páginas: {result.get('paginas', 0)}")
                    print(f"  Tablas detectadas: {len(result.get('tablas', []))}")
                    if result.get("results_saved"):
                        print("✓ Resultados guardados (TXT, JSON, MD)")
                else:
                    print(f"✗ Error: {result.get('error', 'Unknown')}")
        except ValueError:
            print("Número inválido")
    
    def _handle_view_results(self):
        print("\nRESULTADOS")
        print("-" * 20)
        
        summary = self.controller.get_results_summary()
        
        print(f"Procesamientos: {summary.get('total_processes', 0)}")
        print(f"Archivos: {summary.get('total_files', 0)}")
        print(f"  TXT: {summary.get('txt_files', 0)}")
        print(f"  MD: {summary.get('md_files', 0)}")
        print(f"  JSON: {summary.get('json_files', 0)}")
        # NO mostrar CSV porque no se generan
        
        recent = summary.get("recent_processes", [])
        if recent:
            print(f"\nÚltimos procesamientos:")
            for i, proc in enumerate(recent[:5], 1):
                print(f"  {i}. {proc}")
    
    def _handle_exit(self):
        print("\n¡Adiós!")
        self.running = False
    
    def _clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')


def main():
    menu = OCRMenu()
    menu.run()


if __name__ == "__main__":
    main()
# Auto-generated comment - 20:13:37
