#!/bin/bash

# Script de verificación rápida de servicios
# Usage: ./verify.sh

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Verificando servicios del Predictor de Deserción...${NC}\n"

# Backend
echo -n "Backend API: "
if curl -s http://localhost:8000/api/v1/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

# Frontend
echo -n "Frontend: "
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

# PostgreSQL
echo -n "PostgreSQL: "
if docker exec predictor-postgres pg_isready > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

# Redis
echo -n "Redis: "
if docker exec predictor-redis redis-cli -a redis123 PING 2>/dev/null | grep -q PONG; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

# MLflow
echo -n "MLflow: "
if curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAIL${NC}"
fi

# Docker containers
echo -n "Containers: "
RUNNING=$(docker-compose ps | grep -c "Up" || true)
echo -e "${GREEN}$RUNNING/5 running${NC}"

echo -e "\n${BLUE}Verificación completada${NC}"
