#!/bin/bash

# 🚀 Script para ejecutar el servidor en modo producción

echo "============================================"
echo "🚀 INICIANDO SERVIDOR EN PRODUCCIÓN"
echo "============================================"

# Cambiar al directorio backend
cd "$(dirname "$0")/.." || exit

# Variables de entorno
export ENVIRONMENT=production
export DEBUG=False
export LOG_LEVEL=WARNING
export SHOW_DOCS=False

echo "🔧 Configuración:"
echo "  - Environment: production"
echo "  - Debug: False"
echo "  - Log Level: WARNING"
echo "  - Docs: Disabled"
echo ""

echo "🚀 Iniciando servidor con Gunicorn..."
echo "============================================"
echo ""

# Ejecutar con gunicorn + uvicorn workers
cd backend || exit
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 5 \
    --log-level warning \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log