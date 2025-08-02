FROM python:3.9-slim

# Instalar dependencias del sistema OPTIMIZADAS para OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    tesseract-ocr-osd \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Configurar variables de entorno para Tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
ENV TESSERACT_CMD=/usr/bin/tesseract
ENV OMP_THREAD_LIMIT=1
ENV PYTHONUNBUFFERED=1

# Establecer directorio de trabajo y Python path
WORKDIR /app
ENV PYTHONPATH=/app:/app/backend
ENV PYTHONUNBUFFERED=1

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/pdfs /app/resultado && \
    chmod 755 /app/pdfs /app/resultado

# Comando actualizado para usar el nuevo archivo
CMD ["python", "-u", "backend/views/cli/menu.py"]