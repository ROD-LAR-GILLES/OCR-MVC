#!/bin/bash

# Detener y eliminar contenedores existentes incluyendo huérfanos
docker compose down --remove-orphans

# Construir la imagen de Docker
docker compose build

# Iniciar los servicios de Docker
docker compose up -d

# Esperar a que los servicios estén listos
echo "Esperando a que los servicios se inicien..."
sleep 5

docker exec -it ocr-mvc-system python backend/views/cli/menu.py