#!/bin/bash

# 🧪 Script para ejecutar tests

echo "============================================"
echo "🧪 EJECUTANDO TESTS - Predictor de Deserción"
echo "============================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Cambiar al directorio backend
cd "$(dirname "$0")/.." || exit

echo ""
echo "${YELLOW}📦 Verificando dependencias...${NC}"
if ! command -v pytest &> /dev/null; then
    echo "${RED}❌ pytest no está instalado${NC}"
    echo "Instalando pytest..."
    pip install pytest pytest-cov pytest-asyncio httpx
fi

echo ""
echo "${GREEN}✅ Dependencias OK${NC}"
echo ""

# Ejecutar tests según argumentos
if [ "$1" == "unit" ]; then
    echo "${YELLOW}🧪 Ejecutando tests unitarios...${NC}"
    pytest tests/ -m unit -v
elif [ "$1" == "integration" ]; then
    echo "${YELLOW}🧪 Ejecutando tests de integración...${NC}"
    pytest tests/ -m integration -v
elif [ "$1" == "performance" ]; then
    echo "${YELLOW}🧪 Ejecutando tests de performance...${NC}"
    pytest tests/ -m performance -v --benchmark-only
elif [ "$1" == "coverage" ]; then
    echo "${YELLOW}🧪 Ejecutando tests con coverage...${NC}"
    pytest tests/ --cov=app --cov-report=html --cov-report=term-missing
    echo ""
    echo "${GREEN}📊 Reporte de coverage generado en htmlcov/index.html${NC}"
else
    echo "${YELLOW}🧪 Ejecutando TODOS los tests...${NC}"
    pytest tests/ -v
fi

echo ""
echo "${GREEN}✅ Tests completados${NC}"
echo "============================================"