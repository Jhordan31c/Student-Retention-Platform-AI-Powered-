#!/bin/bash

# 🚀 Script para ejecutar el servidor en modo desarrollo

echo "============================================"
echo "🚀 INICIANDO SERVIDOR DE DESARROLLO"
echo "============================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Cambiar al directorio backend
cd "$(dirname "$0")/.." || exit

echo ""
echo "${YELLOW}📦 Verificando modelos ML...${NC}"

# Verificar que existen los modelos
if [ ! -d "ml/models" ]; then
    echo "❌ Directorio ml/models no encontrado"
    exit 1
fi

if [ ! -f "ml/models/catboost_optimized.pkl" ] && [ ! -f "ml/models/lightgbm_optimized.pkl" ]; then
    echo "⚠️  ADVERTENCIA: No se encontraron modelos optimizados"
    echo "   Por favor entrena los modelos primero"
fi

echo "${GREEN}✅ Modelos OK${NC}"
echo ""

# Variables de entorno
export ENVIRONMENT=development
export DEBUG=True
export LOG_LEVEL=INFO

echo "${YELLOW}🔧 Configuración:${NC}"
echo "  - Environment: development"
echo "  - Debug: True"
echo "  - Log Level: INFO"
echo ""

echo "${YELLOW}🚀 Iniciando servidor FastAPI...${NC}"
echo "  - URL: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "============================================"
echo ""

# Ejecutar con uvicorn
cd backend || exit
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info