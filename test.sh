#!/bin/bash

# Ver logs del contenedor
docker logs ocr-mvc-system

# Ver logs en tiempo real (con -f)
docker logs -f ocr-mvc-system

# Ver últimas 20 líneas
docker logs --tail 20 ocr-mvc-system

# Ver logs con timestamp
docker logs -t ocr-mvc-system

# Ver logs del contenedor
docker logs ocr-mvc-system

# Ver logs en tiempo real (con -f)
docker logs -f ocr-mvc-system

# Ver últimas 20 líneas
docker logs --tail 20 ocr-mvc-system

# Ver logs con timestamp
docker logs -t ocr-mvc-system

# Ver logs del contenedor
docker logs ocr-mvc-system

# Ver logs en tiempo real (con -f)
docker logs -f ocr-mvc-system

# Ver últimas 20 líneas
docker logs --tail 20 ocr-mvc-system

# Ver logs con timestamp
docker logs -t ocr-mvc-system

# Iniciar el contenedor si está parado
docker start ocr-mvc-system

# O usar docker-compose
docker-compose up

# Ver por qué falló
docker logs ocr-mvc-system