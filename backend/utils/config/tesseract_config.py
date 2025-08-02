"""
Configuración de Tesseract optimizada para documentos escaneados.
"""
import os
import logging

logger = logging.getLogger(__name__)

class TesseractConfig:
    """Configuración optimizada de Tesseract para documentos escaneados."""
    
    def __init__(self):
        self.tesseract_cmd = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
        self.DEFAULT_DPI = 300
        # CAMBIO CRÍTICO: Agregar español como idioma principal
        self.default_language = "spa+eng"  # Español + Inglés
        
        logger.info(f"Tesseract configurado: {self.tesseract_cmd}, idioma: {self.default_language}")
    
    def get_tesseract_cmd(self) -> str:
        """Obtener comando de Tesseract."""
        return self.tesseract_cmd
    
    def get_ocr_language(self) -> str:
        """Obtener idioma OCR."""
        return self.default_language
    
    def get_ocr_config(self, config_type: str = 'default') -> str:
        """Obtener configuración OCR optimizada."""
        configs = {
            'default': '--oem 3 --psm 6',
            # CAMBIO: Remover whitelist restrictiva temporalmente
            'document': '--oem 3 --psm 6',
            'table': '--oem 3 --psm 6 -c preserve_interword_spaces=1',
            # NUEVAS configuraciones para documentos problemáticos
            'high_quality': '--oem 3 --psm 4',  # Una columna uniforme
            'aggressive': '--oem 3 --psm 3',    # Automático completo
            'single_block': '--oem 3 --psm 6',  # Bloque uniforme
            # Para debugging - sin restricciones
            'debug': '--oem 3 --psm 6 -c tessedit_char_blacklist=""',
            # Configuraciones adicionales para casos específicos
            'single_line': '--oem 3 --psm 7',   # Línea de texto única
            'single_word': '--oem 3 --psm 8',   # Palabra única
            'sparse_text': '--oem 3 --psm 11',  # Texto disperso
            'vertical_text': '--oem 3 --psm 5', # Bloque vertical
            # Configuraciones con parámetros adicionales
            'no_dict': '--oem 3 --psm 6 -c load_system_dawg=0 -c load_freq_dawg=0',
            'preserve_spaces': '--oem 3 --psm 6 -c preserve_interword_spaces=1',
            'numeric_only': '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.,',
            'alpha_only': '--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéíóúñÁÉÍÓÚÑ '
        }
        
        config = configs.get(config_type, configs['default'])
        logger.debug(f"Configuración OCR '{config_type}': {config}")
        return config
    
    def get_image_dpi(self) -> int:
        """Obtener DPI para conversión de imágenes."""
        return self.DEFAULT_DPI
    
    def get_enhanced_config(self) -> str:
        """Configuración especial para documentos escaneados mejorados."""
        return '--oem 3 --psm 4 -c tessedit_char_blacklist=""'
    
    def get_best_quality_config(self) -> str:
        """Configuración para máxima calidad (más lenta)."""
        return '--oem 1 --psm 4 -c tessedit_char_blacklist=""'
    
    def get_fast_config(self) -> str:
        """Configuración rápida para pruebas."""
        return '--oem 3 --psm 6'
    
    def get_custom_config(self, psm: int = 6, oem: int = 3, whitelist: str = None, 
                         blacklist: str = None, preserve_spaces: bool = False) -> str:
        """Crear configuración personalizada."""
        config = f"--oem {oem} --psm {psm}"
        
        if whitelist:
            config += f" -c tessedit_char_whitelist={whitelist}"
        
        if blacklist:
            config += f" -c tessedit_char_blacklist={blacklist}"
        
        if preserve_spaces:
            config += " -c preserve_interword_spaces=1"
        
        logger.debug(f"Configuración personalizada: {config}")
        return config
    
    def validate_installation(self) -> bool:
        """Validar que Tesseract esté instalado correctamente."""
        try:
            import subprocess
            result = subprocess.run([self.tesseract_cmd, '--version'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                logger.info(f"Tesseract validado: {version}")
                
                # Verificar idiomas disponibles
                lang_result = subprocess.run([self.tesseract_cmd, '--list-langs'], 
                                           capture_output=True, text=True, timeout=10)
                
                if lang_result.returncode == 0:
                    available_langs = lang_result.stdout.strip().split('\n')[1:]  # Skip header
                    logger.info(f"Idiomas disponibles: {available_langs}")
                    
                    # Verificar que español esté disponible
                    if 'spa' not in available_langs:
                        logger.warning("⚠️ Idioma español (spa) no disponible en Tesseract")
                        return False
                    
                    if 'eng' not in available_langs:
                        logger.warning("⚠️ Idioma inglés (eng) no disponible en Tesseract")
                        return False
                    
                    return True
                else:
                    logger.error("No se pudo obtener lista de idiomas de Tesseract")
                    return False
            else:
                logger.error(f"Error ejecutando Tesseract: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout ejecutando Tesseract")
            return False
        except FileNotFoundError:
            logger.error(f"Tesseract no encontrado en: {self.tesseract_cmd}")
            return False
        except Exception as e:
            logger.error(f"Error validando Tesseract: {e}")
            return False
    
    def get_all_configs(self) -> dict:
        """Obtener todas las configuraciones disponibles."""
        return {
            'default': self.get_ocr_config('default'),
            'document': self.get_ocr_config('document'),
            'table': self.get_ocr_config('table'),
            'high_quality': self.get_ocr_config('high_quality'),
            'aggressive': self.get_ocr_config('aggressive'),
            'single_block': self.get_ocr_config('single_block'),
            'debug': self.get_ocr_config('debug'),
            'single_line': self.get_ocr_config('single_line'),
            'single_word': self.get_ocr_config('single_word'),
            'sparse_text': self.get_ocr_config('sparse_text'),
            'vertical_text': self.get_ocr_config('vertical_text'),
            'no_dict': self.get_ocr_config('no_dict'),
            'preserve_spaces': self.get_ocr_config('preserve_spaces'),
            'numeric_only': self.get_ocr_config('numeric_only'),
            'alpha_only': self.get_ocr_config('alpha_only'),
            'enhanced': self.get_enhanced_config(),
            'best_quality': self.get_best_quality_config(),
            'fast': self.get_fast_config()
        }

# Instancia global para uso directo
tesseract_config = TesseractConfig()
# Auto-generated comment - 20:13:37
