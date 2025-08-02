"""
Diccionario dinámico simplificado.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Set
from collections import Counter
from datetime import datetime

logger = logging.getLogger(__name__)

class DynamicDictionary:
    """Diccionario dinámico básico."""
    
    def __init__(self):
        self.dictionary_path = Path("/app/data/dynamic_dictionary.json")
        self.dictionary_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.corrections = {}
        self.valid_words = set()
        self.word_frequency = Counter()
        
        self._load_dictionary()
        logger.info(f"DynamicDictionary inicializado: {len(self.corrections)} correcciones")
    
    def _load_dictionary(self):
        """Carga diccionario desde archivo."""
        try:
            if self.dictionary_path.exists():
                with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.corrections = data.get('corrections', {})
                self.valid_words = set(data.get('valid_words', []))
                self.word_frequency = Counter(data.get('word_frequency', {}))
        except Exception as e:
            logger.warning(f"Error cargando diccionario: {e}")
    
    def save_dictionary(self):
        """Guarda diccionario."""
        try:
            data = {
                'corrections': self.corrections,
                'valid_words': list(self.valid_words),
                'word_frequency': dict(self.word_frequency),
                'updated': datetime.now().isoformat()
            }
            with open(self.dictionary_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error guardando diccionario: {e}")
    
    def correct_text(self, text: str, document_name: str = "unknown") -> str:
        """Corrige texto usando diccionario."""
        # Por ahora solo retorna el texto original
        # El aprendizaje se implementará gradualmente
        return text
    
    def learn_from_text(self, text: str, document_name: str = "unknown") -> Dict[str, int]:
        """Aprende de texto."""
        return {'new_words': 0, 'new_corrections': 0}
    
    def get_statistics(self) -> Dict[str, any]:
        """Estadísticas básicas."""
        return {
            'total_corrections': len(self.corrections),
            'valid_words': len(self.valid_words),
            'vocabulary_size': len(self.word_frequency)
        }

# Instancia global
dynamic_dictionary = DynamicDictionary()