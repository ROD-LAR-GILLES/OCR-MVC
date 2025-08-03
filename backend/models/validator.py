"""
Validador de documentos unificado - SIN duplicaciones.
"""
import logging
from pathlib import Path
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)

class DocumentValidator:
    """Validador unificado de documentos - ABSORBE common_validators."""
    
    # Configuración centralizada
    MAX_FILE_SIZE_MB = 50
    MIN_FILE_SIZE_KB = 1
    ALLOWED_EXTENSIONS = {'.pdf'}
    
    @staticmethod
    def validate_pdf(file_path: Path, strict: bool = True) -> Tuple[bool, List[str]]:
        """
        Validación completa de PDF.
        
        Args:
            file_path: Ruta al archivo PDF
            strict: Si True, aplica validaciones de tamaño
            
        Returns:
            Tupla (es_válido, lista_de_errores)
        """
        errors = []
        
        # Validación básica: existencia
        if not file_path.exists():
            errors.append("El archivo no existe")
            return False, errors
        
        # Validación básica: extensión
        if file_path.suffix.lower() not in DocumentValidator.ALLOWED_EXTENSIONS:
            errors.append(f"Extensión no permitida. Permitidas: {DocumentValidator.ALLOWED_EXTENSIONS}")
        
        # Validación básica: header PDF
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                if not header.startswith(b'%PDF-'):
                    errors.append("No es un archivo PDF válido")
        except Exception as e:
            errors.append(f"Error leyendo archivo: {e}")
        
        # Validaciones de tamaño (solo si strict=True)
        if strict:
            try:
                size_bytes = file_path.stat().st_size
                size_mb = size_bytes / (1024 * 1024)
                size_kb = size_bytes / 1024
                
                if size_kb < DocumentValidator.MIN_FILE_SIZE_KB:
                    errors.append(f"Archivo muy pequeño ({size_kb:.1f} KB)")
                
                if size_mb > DocumentValidator.MAX_FILE_SIZE_MB:
                    errors.append(f"Archivo muy grande ({size_mb:.1f} MB)")
                    
            except Exception as e:
                errors.append(f"Error verificando tamaño: {e}")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.debug(f"PDF válido: {file_path.name}")
        else:
            logger.warning(f"PDF inválido {file_path.name}: {errors}")
        
        return is_valid, errors
    
    @staticmethod
    def validate_pdf_basic(file_path: Path) -> Tuple[bool, List[str]]:
        """Validación básica - MIGRADO desde common_validators."""
        return DocumentValidator.validate_pdf(file_path, strict=False)
    
    @staticmethod
    def check_dependencies(modules: List[str]) -> Dict[str, bool]:
        """Verificar dependencias - MIGRADO desde common_validators."""
        dependencies = {}
        for module in modules:
            try:
                __import__(module)
                dependencies[module] = True
                logger.debug(f"Módulo {module}: ✓")
            except ImportError:
                dependencies[module] = False
                logger.warning(f"Módulo {module}: ✗")
        return dependencies
    
    @staticmethod
    def get_system_paths() -> Dict[str, Path]:
        """Paths del sistema - MIGRADO desde common_validators."""
        base_path = Path("/app" if Path("/app").exists() else ".")
        return {
            "base": base_path,
            "pdfs": base_path / "pdfs",
            "results": base_path / "resultado",
            "config": base_path / "backend" / "utils" / "config"
        }
    
    @staticmethod
    def validate_multiple_pdfs(file_paths: List[Path], strict: bool = True) -> Dict[Path, Tuple[bool, List[str]]]:
        """Valida múltiples PDFs."""
        results = {}
        for file_path in file_paths:
            try:
                results[file_path] = DocumentValidator.validate_pdf(file_path, strict)
            except Exception as e:
                logger.error(f"Error validando {file_path}: {e}")
                results[file_path] = (False, [f"Error de validación: {e}"])
        return results

# Alias para compatibilidad
CommonValidators = DocumentValidator
# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:38
