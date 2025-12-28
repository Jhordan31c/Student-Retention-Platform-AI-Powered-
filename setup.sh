#!/bin/bash

echo "============================================"
echo "🚀 SETUP - Predictor de Deserción"
echo "============================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "${YELLOW}📦 Verificando prerrequisitos...${NC}"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo "${GREEN}✅ Docker OK${NC}"

# Crear .env si no existe
if [ ! -f .env ]; then
    echo ""
    echo "${YELLOW}📝 Creando archivo .env desde .env.example...${NC}"
    cp .env.example .env
    echo "${GREEN}✅ Archivo .env creado. Por favor revisa y ajusta las variables.${NC}"
fi

# Verificar que existen los modelos
if [ ! -d "ml/models" ] || [ -z "$(ls -A ml/models)" ]; then
    echo ""
    echo "${RED}⚠️  ADVERTENCIA: No se encontraron modelos ML en ml/models/${NC}"
    echo "   Por favor entrena los modelos antes de continuar."
    read -p "¿Deseas continuar de todas formas? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "${YELLOW}🐳 Construyendo imágenes Docker...${NC}"
docker-compose build

echo ""
echo "${GREEN}✅ Setup completado!${NC}"
echo ""
echo "Para iniciar los servicios ejecuta:"
echo "  ${YELLOW}docker-compose up -d${NC}"
echo ""
echo "Para ver logs:"
echo "  ${YELLOW}docker-compose logs -f backend${NC}"
echo ""
echo "============================================"