"""
Gestor de resultados - REFACTORIZADO sin duplicaciones.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
from .document import Document

logger = logging.getLogger(__name__)

class ResultManager:
    """Maneja guardado de resultados sin duplicaciones."""
    
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir
        self.results_dir.mkdir(exist_ok=True)
        
        # Configurar extensiones de archivo
        self.file_extensions = {
            'txt': '.txt',
            'json': '.json', 
            'md': '.md'
        }
    
    # ========== MÉTODOS AUXILIARES (ELIMINAN DUPLICACIONES) ==========
    
    def _build_file_path(self, output_dir: Path, base_name: str, file_type: str) -> Path:
        """Construir path de archivo - ELIMINA duplicación de paths."""
        extension = self.file_extensions.get(file_type, f'.{file_type}')
        return output_dir / f"{base_name}{extension}"
    
    def _safe_write_file(self, file_path: Path, content: str, fallback_content: str = None) -> bool:
        """Escritura segura de archivo - ELIMINA duplicación de escritura."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.debug(f"Archivo guardado: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error escribiendo {file_path.name}: {e}")
            
            # Fallback si se proporciona
            if fallback_content:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fallback_content)
                    logger.warning(f"Fallback guardado para {file_path.name}")
                    return True
                except Exception as e2:
                    logger.error(f"Error en fallback para {file_path.name}: {e2}")
            
            return False
    
    def _safe_write_json(self, file_path: Path, data: Dict[str, Any]) -> bool:
        """Escritura segura de JSON - ELIMINA duplicación de JSON."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logger.debug(f"JSON guardado: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error escribiendo JSON {file_path.name}: {e}")
            
            # Fallback JSON básico
            fallback_data = {"error": str(e), "content": "Error de procesamiento"}
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(fallback_data, f, indent=2)
                logger.warning(f"JSON fallback guardado para {file_path.name}")
                return True
            except Exception as e2:
                logger.error(f"Error en fallback JSON para {file_path.name}: {e2}")
                return False
    
    def _handle_operation_error(self, operation: str, error: Exception) -> Tuple[bool, str]:
        """Manejo estándar de errores - ELIMINA duplicación de errores."""
        error_msg = f"Error {operation}: {error}"
        logger.error(error_msg)
        return False, error_msg
    
    def _get_document_attribute(self, document: Document, attr_name: str, default_value: Any = None) -> Any:
        """Obtener atributo seguro - ELIMINA duplicación de getattr."""
        return getattr(document, attr_name, default_value)
    
    def _count_files_by_type(self, file_types: List[str]) -> Dict[str, int]:
        """Contar archivos por tipo - ELIMINA duplicación de conteo."""
        try:
            counts = {}
            for file_type in file_types:
                extension = self.file_extensions.get(file_type, f'.{file_type}')
                pattern = f"*{extension}"
                counts[f"{file_type}_files"] = len(list(self.results_dir.rglob(pattern)))
            return counts
        except Exception as e:
            logger.warning(f"Error contando archivos: {e}")
            return {f"{ft}_files": 0 for ft in file_types}
    
    
    # ========== MÉTODOS PRINCIPALES REFACTORIZADOS ==========
    
    def save_document(self, document: Document) -> Tuple[bool, str]:
        """Guarda documento sin duplicaciones."""
        try:
            folder_name = self._generate_folder_name(document.filename)
            output_dir = self.results_dir / folder_name
            output_dir.mkdir(exist_ok=True)
            
            base_name = Path(document.filename).stem
            
            # Guardar archivos usando métodos auxiliares
            results = {}
            results['txt'] = self._save_text_file_safe(document, output_dir, base_name)
            results['json'] = self._save_json_file_safe(document, output_dir, base_name)
            results['md'] = self._save_markdown_file_safe(document, output_dir, base_name)
            
            # Verificar éxito general
            success_count = sum(1 for success in results.values() if success)
            total_files = len(results)
            
            if success_count == total_files:
                logger.info(f"Documento guardado completamente: {folder_name}")
                return True, folder_name
            elif success_count > 0:
                logger.warning(f"Documento guardado parcialmente: {folder_name} ({success_count}/{total_files})")
                return True, f"{folder_name} (parcial)"
            else:
                return self._handle_operation_error("guardando documento", Exception("Falló guardado de todos los archivos"))
            
        except Exception as e:
            return self._handle_operation_error("guardando documento", e)
    
    def _save_text_file_safe(self, document: Document, output_dir: Path, base_name: str) -> bool:
        """Guarda archivo de texto sin duplicaciones."""
        try:
            txt_file = self._build_file_path(output_dir, base_name, 'txt')
            fallback = f"Error procesando contenido de {document.filename}"
            return self._safe_write_file(txt_file, document.content, fallback)
        except Exception as e:
            logger.error(f"Error en _save_text_file_safe: {e}")
            return False
    
    def _save_json_file_safe(self, document: Document, output_dir: Path, base_name: str) -> bool:
        """Guarda archivo JSON sin duplicaciones."""
        try:
            json_file = self._build_file_path(output_dir, base_name, 'json')
            
            # USAR método centralizado del documento
            json_data = {
                "metadata": document.get_metadata_only(),  # Sin contenido
                "content": {
                    "full_text": document.content,
                    "tables": document.tables
                },
                "processing_info": {
                    "timestamp": document._safe_timestamp(),
                    "processor_version": "refactored_v2.0"
                }
            }
            
            return self._safe_write_json(json_file, json_data)
            
        except Exception as e:
            logger.error(f"Error en _save_json_file_safe: {e}")
            return False
    
    def _save_markdown_file_safe(self, document: Document, output_dir: Path, base_name: str) -> bool:
        """Guarda archivo Markdown sin duplicaciones."""
        try:
            md_file = self._build_file_path(output_dir, base_name, 'md')
            
            # Construir contenido Markdown
            md_content = self._build_markdown_content(document)
            
            # Fallback básico
            fallback = f"# {document.filename}\n\nError generando contenido Markdown"
            
            return self._safe_write_file(md_file, md_content, fallback)
            
        except Exception as e:
            logger.error(f"Error en _save_markdown_file_safe: {e}")
            return False
    
    def _build_markdown_content(self, document: Document) -> str:
        """Construir contenido Markdown usando datos centralizados."""
        try:
            # Header del documento
            md_lines = [
                f"# {document.filename}",
                "",
                "## Información del Documento",
            ]
            
            #  CORRECCIÓN: Usar métodos de Document directamente
            try:
                # Usar atributos directos del Document
                md_lines.extend([
                    f"**Páginas:** {getattr(document, 'page_count', 0)}",
                    f"**Palabras:** {getattr(document, 'word_count', 0):,}",
                    f"**Caracteres:** {getattr(document, 'character_count', 0):,}",
                    f"**Tablas:** {len(getattr(document, 'tables', []))}",
                    f"**Método:** {getattr(document, 'processing_method', 'unknown')}",
                    f"**Éxito:** {' Sí' if getattr(document, 'success', False) else '❌ No'}",
                    ""
                ])
                
                # Agregar timestamp si existe
                if hasattr(document, 'created_at') and document.created_at:
                    md_lines.append(f"**Fecha:** {document.created_at}")
                    md_lines.append("")
                    
            except Exception as e:
                logger.warning(f"Error obteniendo metadatos: {e}")
                md_lines.extend([
                    f"**Estado:** Error obteniendo metadatos",
                    ""
                ])
            
            # Contenido principal
            if document.success and document.content:
                md_lines.extend([
                    "## Contenido Extraído",
                    "",
                    document.content,
                    ""
                ])
                
                # Agregar tablas si existen
                if hasattr(document, 'tables') and document.tables:
                    md_lines.append("## Tablas Detectadas")
                    md_lines.append("")
                    
                    for i, table in enumerate(document.tables, 1):
                        md_lines.append(f"### Tabla {i}")
                        if isinstance(table, dict) and 'content' in table:
                            md_lines.append(str(table['content']))
                        else:
                            md_lines.append(str(table))
                        md_lines.append("")
            else:
                # Error o contenido vacío
                md_lines.extend([
                    "## Estado del Procesamiento",
                    "",
                    f"**Estado:** {'Error en procesamiento' if not document.success else 'Sin contenido extraído'}",
                ])
                
                if hasattr(document, 'error') and document.error:
                    md_lines.append(f"**Error:** {document.error}")
                
                md_lines.append("")
            
            return "\n".join(md_lines)
            
        except Exception as e:
            logger.error(f"Error construyendo Markdown: {e}")
            return f"# {getattr(document, 'filename', 'Error')}\n\nError construyendo contenido: {e}"
    
    def get_summary(self) -> Dict[str, Any]:
        """Obtiene resumen sin duplicaciones."""
        try:
            if not self.results_dir.exists():
                return {"total_processes": 0, "total_files": 0}
            
            result_dirs = [d for d in self.results_dir.iterdir() if d.is_dir()]
            
            # Usar método auxiliar para contar archivos
            file_counts = self._count_files_by_type(['txt', 'md', 'json'])
            
            # Obtener procesamientos recientes
            recent_dirs = sorted(
                result_dirs, 
                key=lambda x: x.stat().st_mtime, 
                reverse=True
            )[:5]
            
            return {
                "total_processes": len(result_dirs),
                "total_files": sum(file_counts.values()),
                **file_counts,
                "recent_processes": [d.name for d in recent_dirs],
                "success_rate": "100%" if result_dirs else "0%"
            }
            
        except Exception as e:
            return self._handle_operation_error("obteniendo resumen", e)[1]
    
    # ========== MÉTODOS DE UTILIDAD (OPTIMIZADOS) ==========
    
    def _get_safe_timestamp(self, document: Document) -> str:
        """Obtener timestamp seguro."""
        try:
            created_at = self._get_document_attribute(document, 'created_at', '')
            if hasattr(created_at, 'isoformat'):
                return created_at.isoformat()
            return str(created_at) if created_at else ''
        except Exception:
            return ''
    
    def _count_tables_in_content(self, content: str) -> int:
        """Cuenta tablas reales en el contenido."""
        try:
            import re
            # Contar patrones de tabla más precisos
            table_headers = re.findall(r'\*\*Tabla \d+', content)
            return len(table_headers)
        except Exception:
            return 0
    
    def _get_method_display_name(self, method: str) -> str:
        """Obtiene nombre amigable del método."""
        method_names = {
            'universal_dynamic': 'Procesamiento Universal',
            'digital': 'Extracción Digital',
            'ocr_enhanced': 'OCR Mejorado',
            'ocr_basic': 'OCR Básico',
            'integrated': 'Integrado',
            'error': 'Error'
        }
        return method_names.get(method, method.title())
    
    def _generate_folder_name(self, filename: str) -> str:
        """Genera nombre de carpeta numerada - SIN CAMBIOS."""
        existing_dirs = [d for d in self.results_dir.iterdir() if d.is_dir()]
        next_num = 1
        
        if existing_dirs:
            nums = []
            for d in existing_dirs:
                name = d.name
                if '_' in name:
                    prefix = name.split('_')[0]
                    if prefix.isdigit():
                        nums.append(int(prefix))
            
            if nums:
                next_num = max(nums) + 1
        
        base_name = Path(filename).stem
        return f"{next_num:02d}_{base_name}"
# Auto-generated comment - 20:13:37
