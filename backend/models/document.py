"""
Modelo de documento - VERSIÓN CENTRALIZADA sin duplicaciones.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Resultado de procesamiento de página."""
    content: str
    tables: List[Dict]
    confidence: float
    method: str
    processing_time: float
    success: bool = True

class Document:
    """Representa un documento procesado por OCR - FUNCIONALIDAD CENTRALIZADA."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.content = ""
        self.pages = 0
        self.processing_time = 0.0
        self.file_size_mb = 0.0
        self.file_size_bytes = 0
        self.created_at = datetime.now()
        self.success = False
        self.method = "integrated"
        self.tables = []
        self.word_count = 0
        self.character_count = 0
        self.error = None
    
    def set_file_info(self, file_path: Path):
        """Establece información completa del archivo - EXPANDIDO."""
        try:
            if file_path.exists():
                stat_info = file_path.stat()
                self.file_size_bytes = stat_info.st_size
                self.file_size_mb = stat_info.st_size / (1024 * 1024)
                logger.debug(f"Archivo {file_path.name}: {self.file_size_mb:.2f} MB")
            else:
                logger.warning(f"Archivo no existe: {file_path}")
        except Exception as e:
            logger.error(f"Error obteniendo info de archivo {file_path}: {e}")
    
    def add_content(self, text: str, page_count: int, tables: List[Dict] = None):
        """Añade contenido con estadísticas completas - MEJORADO."""
        self.content = text.strip()
        self.pages = page_count
        self.tables = tables or []
        
        # Calcular estadísticas automáticamente
        self._calculate_content_stats()
    
    def _calculate_content_stats(self):
        """Calcula estadísticas del contenido - NUEVO."""
        if self.content:
            self.word_count = len(self.content.split())
            self.character_count = len(self.content)
        else:
            self.word_count = 0
            self.character_count = 0
    
    def mark_as_processed(self, processing_time: float, method: str = "integrated"):
        """Marca como procesado exitosamente."""
        self.processing_time = processing_time
        self.method = method
        self.success = True
        self.error = None
        logger.info(f"Documento {self.filename} procesado en {processing_time:.2f}s")
    
    def mark_as_failed(self, error: str):
        """Marca como fallido."""
        self.success = False
        self.error = error
        logger.error(f"Documento {self.filename} falló: {error}")
    
    def get_tables_count(self) -> int:
        """Obtiene número de tablas detectadas - MÉTODO PRINCIPAL."""
        return len(self.tables)
    
    def _safe_timestamp(self, timestamp: Optional[datetime] = None) -> str:
        """Conversión segura de timestamps - CENTRALIZADO."""
        try:
            ts = timestamp or self.created_at
            if hasattr(ts, 'isoformat'):
                return ts.isoformat()
            elif ts:
                return str(ts)
            else:
                return datetime.now().isoformat()
        except Exception:
            return datetime.now().isoformat()
    
    def to_dict(self, include_content: bool = True) -> Dict[str, Any]:
        """Convierte a diccionario - MÉTODO PRINCIPAL centralizado."""
        base_dict = {
            "filename": self.filename,
            "pages": self.pages,
            "processing_time": self.processing_time,
            "file_size_mb": self.file_size_mb,
            "file_size_bytes": self.file_size_bytes,
            "method": self.method,
            "created_at": self._safe_timestamp(),
            "success": self.success,
            "tables_count": self.get_tables_count(),
            "word_count": self.word_count,
            "character_count": self.character_count
        }
        
        if include_content:
            base_dict.update({
                "content": self.content,
                "tables": self.tables
            })
        
        if self.error:
            base_dict["error"] = self.error
            
        return base_dict
    
    def get_metadata_only(self) -> Dict[str, Any]:
        """Obtiene solo metadatos sin contenido - NUEVO."""
        return self.to_dict(include_content=False)
    
    def get_file_info(self) -> Dict[str, Any]:
        """Información del archivo - CENTRALIZADO."""
        return {
            "filename": self.filename,
            "size_bytes": self.file_size_bytes,
            "size_mb": self.file_size_mb,
            "size_kb": self.file_size_bytes / 1024 if self.file_size_bytes > 0 else 0,
            "exists": self.file_size_bytes > 0,
            "created_at": self._safe_timestamp()
        }
    
    def get_summary(self) -> str:
        """Obtiene resumen del documento."""
        if not self.success:
            error_msg = f" ({self.error})" if self.error else ""
            return f"❌ Error procesando {self.filename}{error_msg}"
        
        tables_info = f", {self.get_tables_count()} tablas" if self.tables else ""
        word_info = f", {self.word_count:,} palabras" if self.word_count > 0 else ""
        
        return f"✅ {self.filename}: {self.pages} páginas{tables_info}{word_info}, {self.processing_time:.2f}s"
    
    def get_detailed_summary(self) -> Dict[str, Any]:
        """Resumen detallado - NUEVO."""
        return {
            "basic_info": {
                "filename": self.filename,
                "success": self.success,
                "processing_time": self.processing_time,
                "method": self.method
            },
            "content_stats": {
                "pages": self.pages,
                "tables": self.get_tables_count(),
                "words": self.word_count,
                "characters": self.character_count
            },
            "file_info": self.get_file_info(),
            "summary_text": self.get_summary()
        }
    
    @staticmethod
    def create_error_result(filename: str, error: str, context: str = "general") -> 'Document':
        """Crear Document de error - REEMPLAZA ErrorHandlers.create_error_result."""
        logger.error(f"Error {context}: {error}")
        
        # Crear Document con error
        doc = Document(
            filename=filename,
            content="",
            success=False,
            error=error
        )
        doc.processing_method = "error"
        doc.page_count = 0
        doc.tables = []
        
        return doc

# Factory function para compatibilidad
def create_document(filename: str, file_path: Optional[Path] = None) -> Document:
    """Crea documento con información opcional de archivo."""
    doc = Document(filename)
    if file_path:
        doc.set_file_info(file_path)
    return doc
# Auto-generated comment - 20:13:37
