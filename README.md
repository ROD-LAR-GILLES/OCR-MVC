# Sistema OCR MVC - Procesamiento Avanzado de PDFs

## Descripción del Proyecto

Sistema de reconocimiento óptico de caracteres (OCR) diseñado con arquitectura MVC para el procesamiento de documentos PDF, especialmente optimizado para documentos oficiales chilenos y PDFs escaneados de baja calidad.

## Arquitectura del Sistema

```
OCR-MVC/
├── backend/
│   ├── controllers/
│   │   └── ocr_controller.py          # Controlador principal
│   ├── models/
│   │   ├── pdf_processor.py           # Procesador avanzado de PDFs
│   │   ├── document.py                # Modelo de documento
│   │   ├── validator.py               # Validador de documentos
│   └── result_manager.py          # Gestor de resultados
│   ├── views/
│   │   └── cli/
│   │       └── menu.py                # Interfaz de línea de comandos
│   └── utils/
│       ├── opencv_image_enhancer.py   # Mejorador de imágenes con OpenCV
│       ├── advanced_image_enhancer.py # Mejorador avanzado (scipy/skimage)
│       └── config/
│           └── tesseract_config.py    # Configuración de Tesseract
├── pdfs/                              # Directorio de PDFs a procesar
├── resultado/                         # Resultados de procesamiento
├── Dockerfile                         # Configuración del contenedor
├── docker-compose.yml                 # Orquestación de servicios
├── requirements.txt                   # Dependencias Python
└── README.md                          # Este archivo
```

## Características Principales

### Procesamiento Híbrido de PDFs
- **Extracción digital**: Para PDFs con texto seleccionable
- **OCR avanzado**: Para documentos escaneados
- **Estrategia automática**: Selección inteligente del mejor método
- **Detección de tablas**: Múltiples algoritmos de detección

### Mejora Avanzada de Imágenes
- **Corrección de gamma adaptativa**: Ajuste automático según brillo
- **Eliminación de ruido**: Filtros especializados para documentos
- **Corrección de inclinación**: Detección y corrección automática
- **Binarización múltiple**: Combinación de métodos con votación
- **Sharpening inteligente**: Mejora de nitidez preservando texto

### Optimización para Documentos Chilenos
- **Diccionario de correcciones**: Términos legales y oficiales
- **Limpieza especializada**: Filtros para documentos gubernamentales
- **Detección de palabras clave**: Validación de contenido oficial

## Tecnologías Utilizadas

### Core OCR
- **Tesseract OCR**: Motor principal de reconocimiento
- **pytesseract**: Wrapper Python para Tesseract
- **OpenCV**: Procesamiento de imágenes
- **PIL/Pillow**: Manipulación de imágenes

### Procesamiento de PDFs
- **PyMuPDF (fitz)**: Extracción y conversión de PDFs
- **pdfplumber**: Análisis estructural de PDFs
- **PyPDF2**: Operaciones básicas con PDFs

### Mejora de Imágenes Avanzada
- **scipy**: Algoritmos científicos
- **scikit-image**: Procesamiento avanzado de imágenes
- **imutils**: Utilidades de OpenCV
- **numpy**: Operaciones numéricas

### Infraestructura
- **Docker**: Containerización
- **Python 3.9**: Lenguaje base
- **pandas**: Análisis de datos
- **logging**: Sistema de logs

## Instalación y Configuración

### Prerrequisitos
- Docker y Docker Compose
- Git

### Instalación

```bash
# 1. Clonar el repositorio
git clone <repositorio>
cd OCR-MVC

# 2. Construir y ejecutar el contenedor
docker-compose up --build

# 3. En otra terminal, ejecutar tests
./test.sh
```

### Estructura de Directorios

```bash
# Crear directorios necesarios
mkdir -p pdfs resultado
chmod 755 pdfs resultado
```

## Estado Actual del Proyecto

### Funcionalidades Implementadas

1. **Arquitectura MVC completa**
   - Controlador OCR funcional
   - Modelos de documento y validación
   - Vista CLI interactiva

2. **Procesamiento básico de PDFs**
   - Extracción de texto digital
   - Conversión de páginas a imágenes
   - Gestión de resultados

3. **Mejoras de imagen implementadas**
   - Dos sistemas de mejora (básico y avanzado)
   - Pipeline de preprocesamiento
   - Configuración optimizada de Tesseract

### Problemas Identificados

#### PROBLEMA CRÍTICO: OCR de Baja Calidad en Documentos Escaneados

**Ejemplo de resultado actual:**
```
Input esperado: "REPÚBLICA DE CHILE - MINISTERIO DE OBRAS PÚBLICAS"
Output obtenido: "sontormoconercocmesd , t rojocelzzóoamaE O: . Ñ CIERTO: úl NP"
```

**Diagnóstico:**
- El OCR produce texto completamente ilegible
- Los algoritmos de mejora de imagen no están funcionando efectivamente
- Posible problema en la configuración de Tesseract o pipeline de procesamiento

### Mejoras Implementadas (Sin Éxito Aún)

1. **Sistema de Mejora Dual**:
   ```
   opencv_image_enhancer.py    # Solo OpenCV/PIL
   advanced_image_enhancer.py  # scipy/skimage/imutils
   ```

2. **Pipeline Agresivo de Procesamiento**:
   - Corrección gamma adaptativa
   - Eliminación de ruido con fastNlMeansDenoising
   - CLAHE (Contrast Limited Adaptive Histogram Equalization)
   - Corrección de inclinación con Hough Lines
   - Sharpening con múltiples kernels
   - Binarización por votación múltiple

3. **Configuración Tesseract Optimizada**:
   ```
   --oem 3 --psm 6 -c tessedit_char_whitelist=ABC...áéíóúñ
   ```

## Testing y Ejemplos

### PDF de Prueba Actual
- **Archivo**: `pdf_escan.pdf`
- **Tipo**: Documento oficial escaneado (Decreto chileno)
- **Páginas**: 12
- **Estado**: OCR fallando completamente

### Resultados de Prueba
```
Método: ocr_opencv_enhanced
Tiempo: ~15-20 segundos
Éxito:  Texto ilegible
Confianza: ~0.3-0.5
```

### Comando de Prueba
```bash
./test.sh
# O manualmente:
docker exec -it ocr-mvc-system python backend/views/cli/menu.py
```

## Diagnóstico y Próximos Pasos

### Análisis del Problema

1. **Posibles Causas del Fallo OCR**:
   - Configuración incorrecta de Tesseract en el contenedor
   - Pipeline de mejora de imagen no aplicándose correctamente
   - Calidad de imagen insuficiente después del preprocesamiento
   - Idioma OCR mal configurado

2. **Investigación Necesaria**:
   - Verificar logs detallados del pipeline de procesamiento
   - Guardar imágenes intermedias para análisis visual
   - Probar diferentes configuraciones de Tesseract
   - Validar que las librerías de mejora están funcionando

### Plan de Mejoras Inmediatas

1. **Debugging Detallado**:
   ```python
   # Agregar guardado de imágenes intermedias
   cv2.imwrite(f"/tmp/debug_original_{page}.png", original_image)
   cv2.imwrite(f"/tmp/debug_enhanced_{page}.png", enhanced_image)
   ```

2. **Configuración Tesseract Alternativa**:
   ```bash
   # Probar diferentes PSM (Page Segmentation Mode)
   --psm 4  # Texto en una sola columna uniforme
   --psm 6  # Bloque uniforme de texto (actual)
   --psm 8  # Tratar imagen como una sola palabra
   ```

3. **Validación de Dependencias**:
   ```bash
   # Verificar instalación correcta en contenedor
   tesseract --version
   tesseract --list-langs
   ```

## Métricas de Calidad

### Objetivos de Calidad
- **Precisión OCR**: >85% para documentos oficiales
- **Tiempo de procesamiento**: <30 segundos por página
- **Detección de estructura**: Identificar correctamente encabezados y párrafos
- **Extracción de tablas**: >70% de precisión

### Métricas Actuales
- **Precisión OCR**: <10% (CRÍTICO)
- **Tiempo de procesamiento**: 15-20 segundos 
- **Detección de estructura**: No funcional
- **Extracción de tablas**: No funcional

## Configuración Avanzada

### Variables de Entorno

```dockerfile
ENV TESSERACT_CMD=/usr/bin/tesseract
ENV OMP_THREAD_LIMIT=1
ENV PYTHONUNBUFFERED=1
```

### Configuración Docker

```yaml
# docker-compose.yml
services:
  ocr-system:
    build: .
    volumes:
      - ./pdfs:/app/pdfs
      - ./resultado:/app/resultado
    environment:
      - TESSERACT_CMD=/usr/bin/tesseract
```

## Documentación Técnica

### Clases Principales

1. **OCRController**: Controlador principal del sistema
2. **AdvancedPDFProcessor**: Procesador híbrido de PDFs
3. **OpenCVImageEnhancer**: Mejorador de imágenes
4. **DocumentValidator**: Validador de archivos
5. **ResultManager**: Gestor de resultados

### Flujo de Procesamiento

```
PDF Input → Validation → Strategy Selection → Image Enhancement → OCR → Text Cleaning → Output
```

## API y Uso

### Interfaz de Línea de Comandos

```bash
# Ejecutar el sistema interactivo
python backend/views/cli/menu.py

# Opciones disponibles:
# 1. Procesar PDF individual
# 2. Procesamiento por lotes
# 3. Configuración de parámetros
# 4. Ver resultados anteriores
```

### Uso Programático

```python
from backend.controllers.ocr_controller import OCRController

# Inicializar controlador
controller = OCRController()

# Procesar un PDF
result = controller.process_pdf("pdfs/documento.pdf")

# Obtener texto extraído
text = result.get_text()
confidence = result.get_confidence()
```

## Gestión de Resultados

### Estructura de Salida

```
resultado/
├── documento_nombre/
│   ├── texto_extraido.txt
│   ├── metadata.json
│   ├── logs/
│   │   └── processing.log
│   └── images/
│       ├── page_001_original.png
│       └── page_001_enhanced.png
```

### Formato de Metadata

```json
{
  "filename": "documento.pdf",
  "pages_processed": 12,
  "processing_time": 180.5,
  "ocr_method": "ocr_opencv_enhanced",
  "average_confidence": 0.75,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Problemas Conocidos

1. **OCR Ilegible**: Problema crítico con documentos escaneados de baja calidad
2. **Dependencias Conflictivas**: scipy/skimage no siempre disponibles en todos los entornos
3. **Configuración Tesseract**: Posible mala configuración en contenedor Docker
4. **Memoria**: Procesamiento intensivo para imágenes grandes puede causar problemas de memoria
5. **Codificación**: Problemas con caracteres especiales en documentos en español

## Roadmap de Desarrollo

### Versión 1.1 (Próximo Release)
- Corrección crítica del OCR para documentos escaneados
- Implementación de debug visual con guardado de imágenes intermedias
- Optimización de configuración de Tesseract
- Mejora en manejo de memoria

### Versión 1.2 (Futuro)
- Interfaz web con Flask/FastAPI
- API REST para integración externa
- Soporte para múltiples idiomas
- Procesamiento en paralelo

### Versión 2.0 (Largo Plazo)
- Integración con modelos de ML modernos (Transformer-based OCR)
- Procesamiento distribuido
- Interfaz gráfica completa
- Análisis semántico de documentos

## Contribución

### Prioridades de Desarrollo

1. **URGENTE**: Arreglar OCR de documentos escaneados
2. **ALTA**: Implementar guardado de imágenes debug
3. **MEDIA**: Optimizar configuración Tesseract
4. **BAJA**: Mejorar interfaz CLI

### Estructura de Commits

```bash
feat(ocr): descripción de nueva funcionalidad
fix(ocr): corrección de bug
chore(deps): cambios en dependencias
docs(readme): actualización de documentación
test(unit): agregar o modificar tests
refactor(models): reestructuración de código
```

### Guías de Contribución

1. **Fork** el repositorio
2. **Crear** rama feature/fix específica
3. **Implementar** cambios con tests correspondientes
4. **Documentar** cambios en README si es necesario
5. **Crear** Pull Request con descripción detallada

## Licencia

MIT License - Ver archivo LICENSE para más detalles

## Contacto y Soporte

Para reportar problemas o contribuir al proyecto:
- Crear issues en el repositorio
- Contactar al equipo de desarrollo
- Revisar documentación técnica en el wiki

**Estado del Proyecto**: En desarrollo activo - OCR crítico requiere atención inmediata

## Changelog

### v1.0.0 (2024-01-15)
- Implementación inicial de arquitectura MVC
- Sistema dual de mejora de imágenes
- Interfaz CLI básica
- Configuración Docker completa
- Problema crítico identificado en OCR de documentos escaneados

### v0.9.0 (2024-01-10)
- Estructura base del proyecto
- Implementación de modelos y controladores
- Configuración inicial de Tesseract
# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37

# Auto-generated comment - 20:13:37
