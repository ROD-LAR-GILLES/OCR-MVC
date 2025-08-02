"""
Controlador principal - CORRIGIENDO importaciones.
"""
import logging
import time
from pathlib import Path
from typing import Dict, Any, List

from models.validator import DocumentValidator
from models.pdf_processor import AdvancedPDFProcessor
from utils.config.tesseract_config import TesseractConfig
from models.document import Document
# CORREGIR: Usar la instancia global, no la clase
from models.pdf_processor import pdf_processor  # ← Cambiar esto
from models.result_manager import ResultManager

logger = logging.getLogger(__name__)

class OCRController:
    """Controlador principal SIN duplicaciones."""
    
    def __init__(self):
        """Inicializar controlador usando DocumentValidator."""
        paths = DocumentValidator.get_system_paths()
        self.pdfs_dir = paths["pdfs"]
        self.results_dir = paths["results"]
        
        # Crear directorios
        self.pdfs_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        
        # Inicializar gestor de resultados
        self.result_manager = ResultManager(self.results_dir)
        
        logger.info("OCRController inicializado usando DocumentValidator")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Verificar estado usando DocumentValidator."""
        try:
            dependencies = DocumentValidator.check_dependencies([
                'pytesseract', 'cv2', 'PIL', 'pdfplumber', 'fitz', 'pandas', 'numpy'
            ])
            
            tesseract_available = self._check_tesseract_with_utils()
            
            return {
                "tesseract_available": tesseract_available["available"],
                "tesseract_version": tesseract_available.get("version", ""),
                "languages_available": tesseract_available.get("languages", []),
                "dependencies": dependencies,
                "system_ready": tesseract_available["available"] and all(dependencies.values()),
                "errors": tesseract_available.get("errors", [])
            }
            
        except Exception as e:
            logger.error(f"Error verificando sistema: {e}")
            return {"error": str(e)}
    
    def get_available_pdfs(self) -> List[Path]:
        """Lista PDFs usando DocumentValidator."""
        try:
            if not self.pdfs_dir.exists():
                return []
            
            pdf_files = []
            for pdf_path in self.pdfs_dir.glob("*.pdf"):
                is_valid, _ = DocumentValidator.validate_pdf_basic(pdf_path)
                if is_valid:
                    pdf_files.append(pdf_path)
            
            return sorted(pdf_files, key=lambda x: x.name.lower())
            
        except Exception as e:
            logger.error(f"Error listando PDFs: {e}")
            return []
    
    def process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """Procesar PDF usando pdf_processor global."""
        try:
            # Validar archivo
            is_valid, errors = DocumentValidator.validate_pdf_basic(pdf_path)
            if not is_valid:
                return {"success": False, "error": f"Archivo inválido: {', '.join(errors)}"}
            
            # Crear documento
            document = Document(pdf_path.name)
            document.set_file_info(pdf_path)
            
            start_time = time.time()
            
            # USAR pdf_processor global en lugar de crear instancia
            result = pdf_processor.process_pdf(pdf_path)
            
            processing_time = time.time() - start_time
            
            if result.get("success"):
                document.add_content(
                    result["texto_procesado"], 
                    result["paginas"],
                    result.get("tablas", [])
                )
                
                document.mark_as_processed(processing_time, result.get("method", "integrated"))
                
                # Guardar resultados
                saved, folder_name = self.result_manager.save_document(document)
                
                return {
                    "success": True,
                    "paginas": document.pages,
                    "tablas": document.tables,
                    "processing_time": processing_time,
                    "results_saved": saved,
                    "output_folder": folder_name,
                    "method": result.get("method", "integrated")
                }
            else:
                document.mark_as_failed(result.get("error", "Error desconocido"))
                return {"success": False, "error": result.get("error")}
                
        except Exception as e:
            logger.error(f"Error procesando PDF: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    def _check_tesseract_with_utils(self) -> Dict[str, Any]:
        """Verificar Tesseract."""
        try:
            import subprocess
            result = subprocess.run(['tesseract', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                version = version_line.split()[-1] if version_line else "unknown"
                
                lang_result = subprocess.run(['tesseract', '--list-langs'], 
                                           capture_output=True, text=True, timeout=10)
                
                languages = []
                if lang_result.returncode == 0:
                    languages = lang_result.stdout.strip().split('\n')[1:]
                
                return {
                    "available": True,
                    "version": version,
                    "languages": languages
                }
            else:
                return {"available": False, "errors": ["Tesseract no ejecutable"]}
                
        except Exception as e:
            logger.error(f"Error verificando Tesseract: {e}")
            return {"available": False, "errors": [str(e)]}
    
    # Getters simples
    def get_results_summary(self) -> Dict[str, Any]:
        return self.result_manager.get_summary()
    
    def get_pdfs_dir(self) -> Path:
        return self.pdfs_dir
    
    def get_results_dir(self) -> Path:
        return self.results_dir
# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37
