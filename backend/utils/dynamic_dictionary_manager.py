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
        """Inicializar diccionario desde fuente externa (solo la primera vez).
        
        Args:
            source_path: Ruta al archivo de fuente externa (.json o .txt)
            
        Returns:
            Número de elementos cargados exitosamente
        """
        try:
            if source_path.suffix.lower() == '.json':
                with open(source_path, 'r', encoding='utf-8') as f:
                    external_data = json.load(f)
                
                if isinstance(external_data, dict):
                    # Añadir como correcciones iniciales
                    for error, correction in external_data.items():
                        self.dictionary.add_manual_correction(error, correction, confidence=0.8)
                    
                    logger.info(f"Diccionario inicializado con {len(external_data)} correcciones")
                    return len(external_data)
            
        except Exception as e:
            logger.error(f"Error inicializando diccionario: {e}")
            return 0
    
    def get_learning_report(self) -> Dict[str, any]:
        """Genera reporte de aprendizaje dinámico."""
        stats = self.dictionary.get_statistics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'learning_mode': 'dynamic',
            'hardcoded_words': 0,
            'learned_corrections': stats['total_corrections'],
            'learned_vocabulary': stats['valid_words'],
            'dictionary_health': 'dynamic_learning' if stats['total_corrections'] > 0 else 'learning_ready'
        }

# Instancia global
dynamic_dictionary_manager = DynamicDictionaryManager()