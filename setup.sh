#!/bin/bash

# Predictor de Deserción Escolar - Setup Script
# Día 1: Configuración completa del proyecto

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

# Check prerequisites
check_prerequisites() {
    print_header "Verificando Prerequisitos"
    
    # Check Docker
    if command -v docker &> /dev/null; then
        print_success "Docker instalado: $(docker --version)"
    else
        print_error "Docker no está instalado. Por favor instala Docker Desktop."
        exit 1
    fi
    
    # Check Docker Compose
    if command -v docker-compose &> /dev/null; then
        print_success "Docker Compose instalado: $(docker-compose --version)"
    else
        print_error "Docker Compose no está instalado."
        exit 1
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python instalado: $PYTHON_VERSION"
    else
        print_error "Python 3 no está instalado."
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        print_success "Node.js instalado: $NODE_VERSION"
    else
        print_error "Node.js no está instalado."
        exit 1
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        print_success "Git instalado: $(git --version)"
    else
        print_warning "Git no está instalado. Recomendado para control de versiones."
    fi
}

# Setup environment variables
setup_env() {
    print_header "Configurando Variables de Entorno"
    
    if [ ! -f .env ]; then
        print_info "Creando archivo .env desde .env.example"
        cp .env.example .env
        print_success "Archivo .env creado"
        print_warning "IMPORTANTE: Actualiza las variables en .env antes de continuar"
    else
        print_info "Archivo .env ya existe"
    fi
}

# Initialize Git repository
init_git() {
    print_header "Inicializando Repositorio Git"
    
    if [ ! -d .git ]; then
        git init
        git add .
        git commit -m "Initial commit: Project structure setup"
        print_success "Repositorio Git inicializado"
    else
        print_info "Repositorio Git ya existe"
    fi
}

# Create necessary directories
create_directories() {
    print_header "Creando Directorios Necesarios"
    
    mkdir -p ml/data/raw
    mkdir -p ml/data/processed
    mkdir -p ml/models
    mkdir -p ml/notebooks
    mkdir -p logs
    mkdir -p backend/logs
    
    # Create .gitkeep files
    touch ml/data/raw/.gitkeep
    touch ml/data/processed/.gitkeep
    touch ml/models/.gitkeep
    touch logs/.gitkeep
    
    print_success "Directorios creados"
}

# Setup Python virtual environment (optional, for local development)
setup_python_venv() {
    print_header "Configurando Entorno Virtual de Python (Opcional)"
    
    read -p "¿Deseas crear un entorno virtual de Python para desarrollo local? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        cd ..
        print_success "Entorno virtual de Python creado en backend/venv"
        print_info "Para activarlo: cd backend && source venv/bin/activate"
    else
        print_info "Saltando creación de entorno virtual"
    fi
}

# Install frontend dependencies (optional, for local development)
setup_frontend() {
    print_header "Instalando Dependencias del Frontend (Opcional)"
    
    read -p "¿Deseas instalar dependencias de Node.js para desarrollo local? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd frontend
        npm install
        cd ..
        print_success "Dependencias de Node.js instaladas"
    else
        print_info "Saltando instalación de dependencias de Node.js"
    fi
}

# Build and start Docker containers
start_docker() {
    print_header "Iniciando Servicios con Docker"
    
    read -p "¿Deseas iniciar los contenedores de Docker ahora? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Construyendo imágenes Docker..."
        docker-compose build
        
        print_info "Iniciando contenedores..."
        docker-compose up -d
        
        print_success "Contenedores iniciados"
        
        # Wait for services to be ready
        print_info "Esperando a que los servicios estén listos..."
        sleep 10
        
        # Check if services are running
        if docker-compose ps | grep -q "Up"; then
            print_success "Servicios corriendo correctamente"
            
            echo ""
            print_info "URLs de acceso:"
            echo "  - Frontend: http://localhost:3000"
            echo "  - Backend API: http://localhost:8000"
            echo "  - API Docs: http://localhost:8000/docs"
            echo "  - MLflow: http://localhost:5000"
            echo "  - pgAdmin: http://localhost:5050 (opcional, perfil debug)"
        else
            print_error "Algunos servicios no están corriendo correctamente"
            print_info "Ejecuta: docker-compose logs para ver los errores"
        fi
    else
        print_info "Puedes iniciar los contenedores más tarde con: docker-compose up -d"
    fi
}

# Print next steps
print_next_steps() {
    print_header "¡Setup Completado!"
    
    echo -e "${GREEN}✓ El proyecto está configurado correctamente${NC}\n"
    
    print_info "Próximos Pasos:"
    echo ""
    echo "1. Revisa y actualiza el archivo .env con tus configuraciones"
    echo ""
    echo "2. Inicia los servicios (si no lo hiciste):"
    echo "   ${BLUE}docker-compose up -d${NC}"
    echo ""
    echo "3. Verifica que todo esté funcionando:"
    echo "   ${BLUE}docker-compose ps${NC}"
    echo ""
    echo "4. Accede a las aplicaciones:"
    echo "   - Frontend: ${BLUE}http://localhost:3000${NC}"
    echo "   - Backend: ${BLUE}http://localhost:8000${NC}"
    echo "   - API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo "   - MLflow: ${BLUE}http://localhost:5000${NC}"
    echo ""
    echo "5. Para detener los servicios:"
    echo "   ${BLUE}docker-compose down${NC}"
    echo ""
    echo "6. Para ver logs:"
    echo "   ${BLUE}docker-compose logs -f [service_name]${NC}"
    echo ""
    
    print_info "Documentación adicional en:"
    echo "   - README.md"
    echo "   - docs/DEVELOPMENT.md"
    echo ""
    
    print_success "¡Listo para empezar a desarrollar! 🚀"
}

# Main execution
main() {
    clear
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║   Predictor de Deserción Escolar - Setup         ║"
    echo "║   Día 1: Configuración del Proyecto              ║"
    echo "╚═══════════════════════════════════════════════════╝"
    echo -e "${NC}\n"
    
    check_prerequisites
    setup_env
    create_directories
    init_git
    setup_python_venv
    setup_frontend
    start_docker
    print_next_steps
}

# Run main function
main
