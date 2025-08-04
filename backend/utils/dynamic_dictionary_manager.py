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
            
            elif source_path.suffix.lower() == '.txt':
                # Texto de ejemplo para aprender vocabulario válido
                with open(source_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                stats = self.dictionary.learn_from_text(text, f"seed_{source_path.name}")
                logger.info(f"Diccionario inicializado aprendiendo de texto: {stats}")
                return stats['new_valid_words']
            
        except Exception as e:
            logger.error(f"Error inicializando diccionario: {e}")
    def export_learned_corrections(self, export_path: Path) -> bool:
        """Exporta correcciones aprendidas a archivo JSON.
        
        Args:
            export_path: Ruta donde guardar las correcciones exportadas
            
        Returns:
            True si la exportación fue exitosa, False en caso contrario
        """
        try:
            export_data = {
                'corrections': self.dictionary.corrections,
                'valid_words': list(self.dictionary.valid_words),
                'error_patterns': self.dictionary.error_patterns,
                'statistics': self.dictionary.get_statistics(),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Correcciones exportadas a: {export_path}")
            return True
        except Exception as e:
            logger.error(f"Error exportando: {e}")
            return False
    
    def get_learning_report(self) -> Dict[str, any]:
        """Genera reporte de aprendizaje dinámico.
        
        Returns:
            Diccionario con estadísticas completas del aprendizaje
        """
        stats = self.dictionary.get_statistics()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'learning_mode': 'dynamic',
            'hardcoded_words': 0,  # ¡CERO palabras hardcodeadas!
            'learned_corrections': stats['total_corrections'],
            'learned_vocabulary': stats['valid_words'],
            'learning_sessions': stats['learning_sessions'],
            'auto_detected_patterns': stats['error_patterns'],
            'last_learning_session': stats['last_session'],
            'dictionary_health': 'dynamic_learning' if stats['total_corrections'] > 0 else 'learning_ready'
        }

# Instancia global
dynamic_dictionary_manager = DynamicDictionaryManager()