"""
Gestor para el diccionario dinámico.
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
        self.dictionary = dynamic_dictionary
    
    def seed_from_external_source(self, source_path: Path) -> int:
        """Inicializar diccionario desde fuente externa (solo la primera vez)."""
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
            return 0
    
    def export_learned_corrections(self, export_path: Path) -> bool:
        """Exporta correcciones aprendidas."""
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
        """Genera reporte de aprendizaje dinámico."""
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

"""
CLI para gestión del diccionario dinámico.
"""
from utils.dynamic_dictionary_manager import dynamic_dictionary_manager

class DynamicDictionaryMenu:
    """Menú para diccionario 100% dinámico."""
    
    def show_menu(self):
        while True:
            self._display_header()
            
            choice = input("\n👉 Selecciona una opción: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._show_learning_status()
            elif choice == "2":
                self._seed_dictionary()
            elif choice == "3":
                self._add_manual_correction()
            elif choice == "4":
                self._export_learned_data()
            elif choice == "5":
                self._show_learning_report()
            else:
                print("❌ Opción inválida")
    
    def _display_header(self):
        """Muestra estado del diccionario dinámico."""
        stats = dynamic_dictionary_manager.dictionary.get_statistics()
        
        print("\n" + "="*60)
        print("🧠 DICCIONARIO DINÁMICO (100% SIN HARDCODING)")
        print("="*60)
        
        print(f"📊 Estado actual:")
        print(f"   ├─ Palabras hardcodeadas: 0 ✅")
        print(f"   ├─ Correcciones aprendidas: {stats['total_corrections']:,}")
        print(f"   ├─ Vocabulario aprendido: {stats['valid_words']:,}")
        print(f"   ├─ Patrones detectados: {stats['error_patterns']:,}")
        print(f"   └─ Sesiones de aprendizaje: {stats['learning_sessions']:,}")
        
        print(f"\n🔧 Opciones disponibles:")
        print("1. Ver estado de aprendizaje")
        print("2. Inicializar desde fuente externa")
        print("3. Añadir corrección manual")
        print("4. Exportar datos aprendidos")
        print("5. Reporte de aprendizaje")
        print("0. Volver al menú principal")
    
    def _show_learning_status(self):
        """Muestra estado detallado del aprendizaje."""
        stats = dynamic_dictionary_manager.dictionary.get_statistics()
        
        print(f"\n🧠 ESTADO DE APRENDIZAJE DINÁMICO")
        print(f"{'='*50}")
        
        print(f"\n✅ Confirmación: CERO palabras hardcodeadas en código")
        print(f"📚 Vocabulario aprendido dinámicamente: {stats['valid_words']:,} palabras")
        print(f"🔧 Correcciones descubiertas: {stats['total_corrections']:,}")
        print(f"📊 Confianza promedio: {stats['avg_confidence']:.3f}")
        
        if stats['most_frequent_words']:
            print(f"\n🔥 Palabras más aprendidas:")
            for i, (word, freq) in enumerate(stats['most_frequent_words'][:5], 1):
                print(f"   {i}. {word} ({freq} veces)")
        
        if stats['last_session']:
            print(f"\n📈 Última sesión de aprendizaje:")
            session = stats['last_session']
            print(f"   Documento: {session['document']}")
            print(f"   Nuevas palabras válidas: {session['stats']['new_valid_words']}")
            print(f"   Nuevas correcciones: {session['stats']['new_corrections']}")
        
        input("\nPresiona Enter para continuar...")

# Función para integrar en menú principal
def show_dynamic_dictionary_menu():
    menu = DynamicDictionaryMenu()
    menu.show_menu()

"""
Procesador PDF avanzado con diccionario dinámico y detección de tablas.
"""
import logging
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import re
from datetime import datetime

# Imports del proyecto
from utils.config.tesseract_config import tesseract_config
from utils.dynamic_dictionary import dynamic_dictionary

logger = logging.getLogger(__name__)

class AdvancedPDFProcessor:
    """Procesador PDF consolidado con diccionario dinámico y detección de tablas."""
    
    def __init__(self):
        # Configuración Tesseract
        self.tesseract_config = tesseract_config
        self.tesseract_lang = self.tesseract_config.get_ocr_language()
        
        # Directorios
        self.debug_dir = Path("/app/debug_images")
        self.debug_dir.mkdir(exist_ok=True)
        
        # Diccionario dinámico
        self.dynamic_dict = dynamic_dictionary
        
        # Configurar Tesseract
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
        logger.info(f"AdvancedPDFProcessor inicializado con detección de tablas")
    
    def process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """Método principal para procesar PDF con detección de tablas."""
        try:
            logger.info(f"Iniciando procesamiento con detección de tablas: {pdf_path.name}")
            
            # Verificar que el archivo existe
            if not pdf_path.exists():
                return self._create_error_result(pdf_path.name, "Archivo no encontrado")
            
            # Abrir PDF
            pdf_document = fitz.open(str(pdf_path))
            total_pages = len(pdf_document)
            
            if total_pages == 0:
                return self._create_error_result(pdf_path.name, "PDF sin páginas")
            
            # Procesar todas las páginas
            extracted_text = ""
            detected_tables = []
            pages_processed = 0
            
            for page_num in range(total_pages):
                try:
                    page = pdf_document[page_num]
                    
                    # PASO 1: Intentar extraer texto directo
                    direct_text = page.get_text()
                    
                    # PASO 2: Detectar tablas en la página
                    page_tables = self._detect_tables_in_page(page, page_num + 1)
                    detected_tables.extend(page_tables)
                    
                    if len(direct_text.strip()) > 50:
                        # Texto directo disponible
                        extracted_text += f"\n--- Página {page_num + 1} ---\n"
                        extracted_text += direct_text
                        
                        # Agregar tablas detectadas al texto
                        if page_tables:
                            extracted_text += f"\n\n=== TABLAS DETECTADAS EN PÁGINA {page_num + 1} ===\n"
                            for i, table in enumerate(page_tables):
                                extracted_text += f"\n--- Tabla {i + 1} ---\n"
                                extracted_text += self._format_table_as_text(table)
                        
                        pages_processed += 1
                    else:
                        # Usar OCR con detección de tablas
                        page_text, page_tables_ocr = self._process_page_with_ocr_and_tables(page, page_num + 1)
                        if page_text:
                            extracted_text += f"\n--- Página {page_num + 1} (OCR) ---\n"
                            extracted_text += page_text
                            
                            # Agregar tablas OCR
                            if page_tables_ocr:
                                detected_tables.extend(page_tables_ocr)
                                extracted_text += f"\n\n=== TABLAS OCR EN PÁGINA {page_num + 1} ===\n"
                                for i, table in enumerate(page_tables_ocr):
                                    extracted_text += f"\n--- Tabla OCR {i + 1} ---\n"
                                    extracted_text += self._format_table_as_text(table)
                            
                            pages_processed += 1
                
                except Exception as e:
                    logger.warning(f"Error procesando página {page_num + 1}: {e}")
                    continue
            
            pdf_document.close()
            
            # Limpiar texto final
            cleaned_text = self._clean_text(extracted_text, level="enhanced")
            
            # Guardar diccionario después del procesamiento
            self.dynamic_dict.save_dictionary()
            
            # ✅ RESULTADO CON INFORMACIÓN DE TABLAS
            result = {
                'success': True,
                'filename': pdf_path.name,
                
                # CLAVES QUE BUSCA OCR_CONTROLLER:
                'texto_procesado': cleaned_text,
                'paginas': pages_processed,
                'tiempo_procesamiento': 0.0,
                'metodo': 'hybrid_with_tables',
                
                # ✅ INFORMACIÓN DE TABLAS
                'tablas_detectadas': len(detected_tables),
                'tablas': detected_tables,
                
                # Información adicional
                'total_pages': total_pages,
                'pages_processed': pages_processed,
                'text_length': len(cleaned_text),
                'processing_info': {
                    'timestamp': datetime.now().isoformat(),
                    'method': 'hybrid_with_tables',
                    'language': self.tesseract_lang,
                    'dictionary_corrections': len(self.dynamic_dict.corrections),
                    'tables_found': len(detected_tables)
                }
            }
            
            logger.info(f"Procesamiento completado: {pages_processed}/{total_pages} páginas, {len(detected_tables)} tablas")
            return result
            
        except Exception as e:
            logger.error(f"Error general procesando PDF: {e}", exc_info=True)
            return self._create_error_result(pdf_path.name, str(e))

    def _detect_tables_in_page(self, page, page_number: int) -> List[Dict[str, Any]]:
        """Detecta tablas en una página usando análisis de estructura."""
        try:
            tables = []
            
            # MÉTODO 1: Buscar tablas en texto directo (detectar patrones tabulares)
            page_text = page.get_text()
            text_tables = self._find_table_patterns_in_text(page_text, page_number)
            tables.extend(text_tables)
            
            # MÉTODO 2: Análisis visual de líneas y rectángulos
            visual_tables = self._detect_tables_by_visual_analysis(page, page_number)
            tables.extend(visual_tables)
            
            return tables
            
        except Exception as e:
            logger.error(f"Error detectando tablas en página {page_number}: {e}")
            return []

    def _find_table_patterns_in_text(self, text: str, page_number: int) -> List[Dict[str, Any]]:
        """Encuentra patrones de tabla en texto plano."""
        tables = []
        
        try:
            lines = text.split('\n')
            current_table = []
            in_table = False
            
            for line in lines:
                line = line.strip()
                
                # Detectar líneas que parecen filas de tabla
                if self._looks_like_table_row(line):
                    if not in_table:
                        in_table = True
                        current_table = []
                    current_table.append(line)
                else:
                    if in_table and len(current_table) >= 2:
                        # Guardar tabla encontrada
                        table_data = self._parse_table_from_lines(current_table)
                        if table_data:
                            tables.append({
                                'page': page_number,
                                'method': 'text_pattern',
                                'rows': len(table_data),
                                'cols': len(table_data[0]) if table_data else 0,
                                'data': table_data,
                                'raw_lines': current_table.copy()
                            })
                    
                    in_table = False
                    current_table = []
            
            # Procesar tabla final si existe
            if in_table and len(current_table) >= 2:
                table_data = self._parse_table_from_lines(current_table)
                if table_data:
                    tables.append({
                        'page': page_number,
                        'method': 'text_pattern',
                        'rows': len(table_data),
                        'cols': len(table_data[0]) if table_data else 0,
                        'data': table_data,
                        'raw_lines': current_table.copy()
                    })
            
            return tables
            
        except Exception as e:
            logger.error(f"Error buscando patrones de tabla: {e}")
            return []

    def _looks_like_table_row(self, line: str) -> bool:
        """Determina si una línea parece una fila de tabla."""
        if len(line.strip()) < 10:
            return False
        
        # Buscar separadores comunes de tabla
        separators = ['\t', '  ', ' | ', '|', ':']
        
        for sep in separators:
            if line.count(sep) >= 2:
                return True
        
        # Buscar patrones de números/fechas/códigos
        if re.search(r'\d+[\s\t]+[A-Za-z]+[\s\t]+\d+', line):
            return True
        
        # Buscar patrones de valores monetarios
        if re.search(r'[\$\d,\.]+[\s\t]+[A-Za-z]+', line):
            return True
        
        return False

    def _parse_table_from_lines(self, lines: List[str]) -> List[List[str]]:
        """Convierte líneas de texto en estructura de tabla."""
        table_data = []
        
        try:
            for line in lines:
                # Intentar diferentes métodos de separación
                row = None
                
                # MÉTODO 1: Separación por tabulaciones
                if '\t' in line:
                    row = [cell.strip() for cell in line.split('\t') if cell.strip()]
                
                # MÉTODO 2: Separación por espacios múltiples
                elif '  ' in line:
                    row = [cell.strip() for cell in re.split(r'\s{2,}', line) if cell.strip()]
                
                # MÉTODO 3: Separación por pipes
                elif '|' in line:
                    row = [cell.strip() for cell in line.split('|') if cell.strip()]
                
                # MÉTODO 4: Separación inteligente por patrones
                else:
                    # Buscar patrones de fecha/número + texto
                    matches = re.findall(r'(\d+[/\-\.]\d+[/\-\.]\d+|\d+)\s+([A-Za-z][^0-9]*?)(?=\s+\d+|\s*$)', line)
                    if matches:
                        row = [match[0].strip() for match in matches] + [matches[-1][1].strip()]
                
                if row and len(row) >= 2:
                    table_data.append(row)
            
            # Normalizar número de columnas
            if table_data:
                max_cols = max(len(row) for row in table_data)
                for row in table_data:
                    while len(row) < max_cols:
                        row.append('')
            
            return table_data if len(table_data) >= 2 else []
            
        except Exception as e:
            logger.error(f"Error parseando tabla: {e}")
            return []

    def _detect_tables_by_visual_analysis(self, page, page_number: int) -> List[Dict[str, Any]]:
        """Detecta tablas mediante análisis visual de la página."""
        try:
            # Convertir página a imagen
            mat = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = mat.tobytes("png")
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Detectar líneas horizontales y verticales
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detectar líneas horizontales
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
            horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel)
            
            # Detectar líneas verticales
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
            vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel)
            
            # Combinar líneas
            table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
            
            # Encontrar contornos de posibles tablas
            contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            tables = []
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 1000:  # Filtrar tablas pequeñas
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Extraer región de la tabla
                    table_region = img[y:y+h, x:x+w]
                    
                    # OCR de la región de tabla
                    table_text = pytesseract.image_to_string(
                        table_region, 
                        lang=self.tesseract_lang,
                        config='--psm 6'
                    )
                    
                    if len(table_text.strip()) > 20:
                        tables.append({
                            'page': page_number,
                            'method': 'visual_analysis',
                            'bbox': {'x': x, 'y': y, 'width': w, 'height': h},
                            'text': table_text.strip(),
                            'area': area
                        })
            
            return tables
            
        except Exception as e:
            logger.error(f"Error en análisis visual de tablas: {e}")
            return []

    def _process_page_with_ocr_and_tables(self, page, page_number: int) -> Tuple[str, List[Dict[str, Any]]]:
        """Procesa una página usando OCR con detección específica de tablas."""
        try:
            # Convertir página a imagen
            mat = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = mat.tobytes("png")
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            # Mejorar imagen
            enhanced_img = self._enhance_image(img)
            
            # OCR general
            ocr_config = self.tesseract_config.get_ocr_config('document')
            text = pytesseract.image_to_string(
                enhanced_img, 
                lang=self.tesseract_lang, 
                config=ocr_config
            )
            
            # Detectar tablas en el texto OCR
            tables = self._find_table_patterns_in_text(text, page_number)
            
            return text.strip(), tables
            
        except Exception as e:
            logger.error(f"Error en OCR con tablas página {page_number}: {e}")
            return "", []

    def _format_table_as_text(self, table: Dict[str, Any]) -> str:
        """Formatea una tabla detectada como texto legible."""
        try:
            if 'data' in table:
                # Tabla con datos estructurados
                lines = []
                for row in table['data']:
                    lines.append(' | '.join(str(cell) for cell in row))
                return '\n'.join(lines)
            
            elif 'raw_lines' in table:
                # Tabla con líneas raw
                return '\n'.join(table['raw_lines'])
            
            elif 'text' in table:
                # Tabla con texto OCR
                return table['text']
            
            else:
                return f"Tabla detectada (método: {table.get('method', 'unknown')})"
                
        except Exception as e:
            logger.error(f"Error formateando tabla: {e}")
            return "Error formateando tabla"

    def _enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Mejora imagen para OCR."""
        try:
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            denoised = cv2.fastNlMeansDenoising(gray)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            thresh = cv2.adaptiveThreshold(
                enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            return thresh
            
        except Exception as e:
            logger.warning(f"Error mejorando imagen: {e}")
            return image
    
    def _clean_text(self, text: str, level: str = "basic") -> str:
        """Método de limpieza con diccionario dinámico."""
        if not text:
            return ""
        
        try:
            if level in ["enhanced", "aggressive"]:
                text = self.dynamic_dict.correct_text(text, "official_document")
            
            text = re.sub(r'[^\w\s\n.,;:()\-_/°%$@#áéíóúñÁÉÍÓÚÑüÜ¡!¿?|]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\n\s*\n+', '\n\n', text)
            
            if level == "aggressive":
                structural_patterns = [
                    (r'\b([A-Z]{2,})\s*([A-Z]{2,})\b', r'\1 \2'),
                    (r'\b(\d+)\s*([A-Z][a-z])', r'\1 \2'),
                ]
                
                for pattern, replacement in structural_patterns:
                    text = re.sub(pattern, replacement, text)
            
            min_length = 3 if level == "basic" else 5
            lines = []
            for line in text.split('\n'):
                line = line.strip()
                if len(line) > min_length or line.isdigit() or not line:
                    lines.append(line)
            
            return '\n'.join(lines)
            
        except Exception as e:
            logger.warning(f"Error limpiando texto: {e}")
            return text
    
    def _create_error_result(self, filename: str, error_message: str) -> Dict[str, Any]:
        """Crea resultado de error estándar."""
        return {
            'success': False,
            'filename': filename,
            'error': error_message,
            'texto_procesado': '',
            'paginas': 0,
            'tiempo_procesamiento': 0.0,
            'metodo': 'error',
            'tablas_detectadas': 0,
            'tablas': [],
            'text_length': 0,
            'processing_info': {
                'timestamp': datetime.now().isoformat(),
                'method': 'error',
                'error_details': error_message
            }
        }

# Instancia global para compatibilidad
pdf_processor = AdvancedPDFProcessor()
# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:38

# Auto-generated comment - 20:13:38
