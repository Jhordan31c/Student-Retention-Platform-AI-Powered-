#!/bin/bash

echo "============================================"
echo "🔍 VERIFICACIÓN - Sistema Completo"
echo "============================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

FAILED=0

# Función para verificar endpoint
check_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Verificando ${name}... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" == "$expected" ]; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED (HTTP $response)${NC}"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo ""
echo "${YELLOW}🐳 Verificando servicios Docker...${NC}"

# Verificar que están corriendo
services=("predictor-backend" "predictor-postgres" "predictor-redis" "predictor-mlflow")

for service in "${services[@]}"; do
    echo -n "Verificando $service... "
    if docker ps --format "{{.Names}}" | grep -q "^${service}$"; then
        echo -e "${GREEN}✅ Running${NC}"
    else
        echo -e "${RED}❌ Not running${NC}"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "${YELLOW}🌐 Verificando endpoints...${NC}"

# Esperar un poco a que los servicios estén listos
sleep 5

# Verificar endpoints
check_endpoint "Backend Health" "http://localhost:8000/api/v1/health" "200"
check_endpoint "Backend Root" "http://localhost:8000/" "200"
check_endpoint "Backend Docs" "http://localhost:8000/docs" "200"
check_endpoint "MLflow" "http://localhost:5000/health" "200"
check_endpoint "Frontend" "http://localhost:3000/" "200"

echo ""
echo "============================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ TODAS LAS VERIFICACIONES PASARON${NC}"
    echo ""
    echo "URLs disponibles:"
    echo "  - Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - MLflow: http://localhost:5000"
    echo "  - Frontend: http://localhost:3000"
    echo "  - PgAdmin: http://localhost:5050 (si está habilitado)"
    exit 0
else
    echo -e "${RED}❌ $FAILED VERIFICACIONES FALLARON${NC}"
    echo ""
    echo "Para ver logs ejecuta:"
    echo "  docker-compose logs -f"
    exit 1
fi