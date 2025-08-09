"""
Gestor para el diccionario dinámico.
Maneja la inicialización, exportación y reportes del diccionario.
"""
import logging
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from utils.dynamic_dictionary import dynamic_dictionary

logger = logging.getLogger(__name__)

class DynamicDictionaryManager:
    """Gestiona el diccionario dinámico."""
    
    def __init__(self):
        """Inicializa el gestor del diccionario dinámico.
        
        Establece la conexión con el diccionario dinámico principal
        para gestionar correcciones y aprendizaje automático.
        """
        self.dictionary = dynamic_dictionary
    
    def seed_from_external_source(self, source_path: Path) -> int:
        """
        Inicializar diccionario desde fuente externa (solo la primera vez).
        Args:
            source_path (Path): Ruta al archivo de fuente externa (.json o .txt)
        Returns:
            int: Número de elementos cargados exitosamente. 0 si hubo error.
        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no tiene el formato esperado.
        """
        if not source_path.exists():
            logger.error(f"El archivo {source_path} no existe.")
            raise FileNotFoundError(f"El archivo {source_path} no existe.")
        try:
            if source_path.suffix.lower() == '.json':
                with source_path.open('r', encoding='utf-8') as f:
                    external_data = json.load(f)
                if not isinstance(external_data, dict):
                    logger.error("El archivo JSON no contiene un diccionario.")
                    raise ValueError("El archivo JSON no contiene un diccionario.")
                for error, correction in external_data.items():
                    self.dictionary.add_manual_correction(error, correction, confidence=0.8)
                logger.info(f"Diccionario inicializado con {len(external_data)} correcciones")
                return len(external_data)
            elif source_path.suffix.lower() == '.txt':
                text = source_path.read_text(encoding='utf-8')
                if not text.strip():
                    logger.warning(f"El archivo {source_path} está vacío.")
                    return 0
                stats = self.dictionary.learn_from_text(text, f"seed_{source_path.name}")
                logger.info(f"Diccionario inicializado aprendiendo de texto: {stats}")
                return stats.get('new_valid_words', 0)
            else:
                logger.error("Formato de archivo no soportado. Solo .json o .txt")
                raise ValueError("Formato de archivo no soportado. Solo .json o .txt")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Error leyendo el archivo: {e}")
            raise ValueError(f"Error leyendo el archivo: {e}")
        except Exception as e:
            logger.error(f"Error inicializando diccionario: {e}")
            return 0
    def export_learned_corrections(self, export_path: Path) -> bool:
        """
        Exporta correcciones aprendidas a archivo JSON.
        Args:
            export_path (Path): Ruta donde guardar las correcciones exportadas
        Returns:
            bool: True si la exportación fue exitosa, False en caso contrario
        """
        try:
            export_data = {
                'corrections': self.dictionary.corrections,
                'valid_words': list(self.dictionary.valid_words),
                'error_patterns': self.dictionary.error_patterns,
                'statistics': self.dictionary.get_statistics(),
                'exported_at': datetime.now().isoformat()
            }
            export_path.write_text(json.dumps(export_data, ensure_ascii=False, indent=2), encoding='utf-8')
            logger.info(f"Correcciones exportadas a: {export_path}")
            return True
        except Exception as e:
            logger.error(f"Error exportando: {e}")
            return False
    
    def get_learning_report(self) -> Dict[str, object]:
        """
        Genera reporte de aprendizaje dinámico.
        Returns:
            Dict[str, object]: Diccionario con estadísticas completas del aprendizaje
        """
        stats = self.dictionary.get_statistics()
        return {
            'timestamp': datetime.now().isoformat(),
            'learning_mode': 'dynamic',
            'hardcoded_words': 0,  # ¡CERO palabras hardcodeadas!
            'learned_corrections': stats.get('total_corrections', 0),
            'learned_vocabulary': stats.get('valid_words', []),
            'learning_sessions': stats.get('learning_sessions', 0),
            'auto_detected_patterns': stats.get('error_patterns', []),
            'last_learning_session': stats.get('last_session', None),
            'dictionary_health': 'dynamic_learning' if stats.get('total_corrections', 0) > 0 else 'learning_ready'
        }

# Instancia global
dynamic_dictionary_manager = DynamicDictionaryManager()