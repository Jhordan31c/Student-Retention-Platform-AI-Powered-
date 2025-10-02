# ✅ CHECKLIST DÍA 1: SETUP PROFESIONAL

**Fecha:** _________  
**Inicio:** _____  **Fin:** _____  
**Duración estimada:** 6-8 horas

---

## 🎯 OBJETIVOS DEL DÍA

- [ ] Configurar entorno de desarrollo completo
- [ ] Definir arquitectura del sistema
- [ ] Setup de repositorio con mejores prácticas
- [ ] Docker Compose funcionando con todos los servicios

---

## ⏱️ HORA 1-2: ARQUITECTURA Y DISEÑO (2 horas)

### ✅ Prerequisitos
- [ ] Docker Desktop instalado y corriendo
- [ ] Python 3.12+ instalado
- [ ] Node.js 20+ instalado
- [ ] Git configurado
- [ ] VSCode (o IDE preferido) instalado

### 📁 Estructura del Proyecto
- [ ] Clonar o crear repositorio nuevo
- [ ] Copiar estructura de carpetas del template
- [ ] Verificar que todas las carpetas existen:
  ```
  predictor-desercion/
  ├── frontend/
  ├── backend/
  │   ├── app/
  │   │   ├── api/v1/
  │   │   ├── core/
  │   │   ├── models/
  │   │   ├── schemas/
  │   │   └── ml/
  │   └── tests/
  ├── ml/
  │   ├── notebooks/
  │   ├── data/
  │   └── models/
  ├── docker/
  ├── docs/
  └── .github/workflows/
  ```

### 🎨 Diseño de Arquitectura
- [ ] Revisar diagrama de arquitectura en README
- [ ] Entender flujo de datos: Frontend → Backend → ML Model
- [ ] Identificar puntos de integración
- [ ] Documentar decisiones técnicas iniciales

### 🔧 Configuración de Git
- [ ] `git init` (si es nuevo repo)
- [ ] Copiar `.gitignore`
- [ ] Hacer primer commit: `git add . && git commit -m "Initial project structure"`
- [ ] Crear ramas: `git checkout -b develop`
- [ ] (Opcional) Conectar con GitHub/GitLab remoto

**✓ CHECKPOINT 1:** Estructura de proyecto creada y versionada en Git

---

## ⏱️ HORA 3-4: SETUP DESARROLLO LOCAL (2 horas)

### 🐍 Python Setup
- [ ] Verificar versión: `python3 --version` (debe ser 3.12+)
- [ ] Navegar a backend: `cd backend`
- [ ] Crear virtual environment: `python3 -m venv venv`
- [ ] Activar venv:
  - Linux/Mac: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [ ] Actualizar pip: `pip install --upgrade pip`
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Verificar instalación: `pip list | grep fastapi`

### 📦 Node.js Setup
- [ ] Verificar versión: `node --version` (debe ser 20+)
- [ ] Verificar npm: `npm --version`
- [ ] Considerar usar pnpm (más rápido): `npm install -g pnpm`
- [ ] Navegar a frontend: `cd frontend`
- [ ] Instalar dependencias: `npm install` o `pnpm install`
- [ ] Verificar instalación: `npm list next`

### 🔌 VSCode Extensions
- [ ] Python (Microsoft)
- [ ] Pylance (Microsoft)
- [ ] ESLint (Microsoft)
- [ ] Prettier (Prettier)
- [ ] Tailwind CSS IntelliSense (Tailwind Labs)
- [ ] Docker (Microsoft)
- [ ] GitLens (GitKraken)
- [ ] Thunder Client o REST Client
- [ ] (Opcional) GitHub Copilot

### ⚙️ VSCode Settings
- [ ] Configurar format on save
- [ ] Configurar Python interpreter (venv)
- [ ] Configurar ESLint auto-fix
- [ ] Configurar Prettier como default formatter

**✓ CHECKPOINT 2:** Entorno local configurado, dependencias instaladas

---

## ⏱️ HORA 5-6: DOCKER COMPOSE BASE (2 horas)

### 📋 Variables de Entorno
- [ ] Copiar `.env.example` a `.env`: `cp .env.example .env`
- [ ] Revisar y personalizar variables en `.env`:
  ```bash
  POSTGRES_USER=postgres
  POSTGRES_PASSWORD=tu_password_seguro
  SECRET_KEY=generar_key_aleatorio_32_chars
  REDIS_PASSWORD=tu_redis_password
  ```
- [ ] Generar SECRET_KEY seguro:
  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 🐳 Docker Files
- [ ] Revisar `docker-compose.yml`
- [ ] Revisar `docker/Dockerfile.backend`
- [ ] Revisar `docker/Dockerfile.frontend`
- [ ] Verificar configuración de puertos:
  - 3000: Frontend
  - 8000: Backend
  - 5432: PostgreSQL
  - 6379: Redis
  - 5000: MLflow
  - 5050: pgAdmin (opcional)

### 🚀 Primer Build
- [ ] Construir imágenes: `docker-compose build`
- [ ] Tiempo estimado: 10-15 minutos
- [ ] Revisar logs de build para errores
- [ ] Verificar imágenes creadas: `docker images`

### 🏃 Iniciar Servicios
- [ ] Levantar contenedores: `docker-compose up -d`
- [ ] Verificar servicios corriendo: `docker-compose ps`
- [ ] Todos los servicios deben estar en estado "Up"
- [ ] Revisar logs: `docker-compose logs -f`

**✓ CHECKPOINT 3:** Docker Compose levantado exitosamente

---

## ⏱️ HORA 7-8: VERIFICACIÓN Y TESTING (2 horas)

### 🔍 Verificación de Servicios

#### PostgreSQL
- [ ] Conectar con cliente (TablePlus, DBeaver, o psql):
  ```bash
  psql -h localhost -U postgres -d predictor_db
  ```
- [ ] Verificar que la BD está vacía (sin tablas aún)
- [ ] Ejecutar query de prueba: `SELECT version();`

#### Redis
- [ ] Conectar con redis-cli:
  ```bash
  docker exec -it predictor-redis redis-cli
  AUTH redis123
  PING
  ```
- [ ] Debe responder: PONG

#### Backend API
- [ ] Abrir navegador: http://localhost:8000
- [ ] Debe mostrar mensaje de bienvenida con version
- [ ] Abrir documentación: http://localhost:8000/docs
- [ ] Debe mostrar Swagger UI
- [ ] Probar endpoint: GET /api/v1/health
- [ ] Respuesta esperada:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-xx-xx...",
    "version": "1.0.0",
    "environment": "development",
    "python_version": "3.12.x"
  }
  ```

#### MLflow
- [ ] Abrir: http://localhost:5000
- [ ] Debe mostrar UI de MLflow
- [ ] Verificar que no hay experimentos aún

#### Frontend
- [ ] Abrir: http://localhost:3000
- [ ] Debe cargar página de Next.js (aunque esté vacía)
- [ ] Verificar que no hay errores en consola del navegador
- [ ] Verificar hot-reload: editar algún archivo y ver si recarga

### 🧪 Testing Básico

#### Backend Tests
- [ ] Entrar al contenedor: `docker exec -it predictor-backend bash`
- [ ] Correr tests: `pytest tests/ -v`
- [ ] (Pueden fallar si no hay tests aún, pero comando debe funcionar)

#### Frontend Tests
- [ ] Entrar al contenedor: `docker exec -it predictor-frontend sh`
- [ ] Correr tests: `npm test`
- [ ] (Pueden fallar si no hay tests aún, pero comando debe funcionar)

### 📊 Health Check Completo
- [ ] Backend: ✅ http://localhost:8000/api/v1/health
- [ ] Frontend: ✅ http://localhost:3000
- [ ] PostgreSQL: ✅ Conexión exitosa
- [ ] Redis: ✅ PING → PONG
- [ ] MLflow: ✅ http://localhost:5000
- [ ] Todos los contenedores "Up": ✅ `docker-compose ps`

### 🐛 Troubleshooting
Si algo falla:
- [ ] Revisar logs: `docker-compose logs [service]`
- [ ] Verificar .env variables
- [ ] Verificar puertos no estén ocupados: `lsof -i :8000`
- [ ] Reintentar: `docker-compose down && docker-compose up -d`
- [ ] Rebuild si necesario: `docker-compose build --no-cache`

**✓ CHECKPOINT 4:** Todos los servicios verificados y funcionando

---

## ⏱️ HORA EXTRA: DOCUMENTACIÓN (opcional, 30 min)

### 📝 Actualizar Documentación
- [ ] Actualizar README con tu información
- [ ] Documentar problemas encontrados y soluciones
- [ ] Crear DEVELOPMENT.md con setup instructions
- [ ] Tomar screenshots del dashboard funcionando
- [ ] Commit de avances: `git add . && git commit -m "Day 1: Setup complete"`

---

## 🎯 ENTREGABLES DEL DÍA 1

### ✅ Debe estar funcionando:
- [x] Repositorio Git inicializado
- [x] Estructura de carpetas completa
- [x] Docker Compose con 5-6 servicios levantados
- [x] Backend API respondiendo en /docs
- [x] Frontend cargando en localhost:3000
- [x] PostgreSQL conectado
- [x] Redis funcionando
- [x] MLflow UI accesible
- [x] Variables de entorno configuradas

### 📸 Capturas requeridas:
- [ ] Screenshot: Docker Desktop con todos los contenedores corriendo
- [ ] Screenshot: http://localhost:8000/docs (Swagger UI)
- [ ] Screenshot: http://localhost:5000 (MLflow)
- [ ] Screenshot: http://localhost:3000 (Frontend)
- [ ] Screenshot: docker-compose ps output

---

## 🚨 VALIDACIÓN FINAL

Ejecuta este comando para validar todo:
```bash
# Backend health
curl http://localhost:8000/api/v1/health | jq

# Frontend (debe devolver HTML)
curl http://localhost:3000

# MLflow (debe devolver HTML)
curl http://localhost:5000

# PostgreSQL (debe conectar)
docker exec predictor-postgres psql -U postgres -c "SELECT 1"

# Redis (debe responder PONG)
docker exec predictor-redis redis-cli -a redis123 PING
```

### ✅ Todo OK si:
- [x] Todos los curl devuelven respuestas válidas
- [x] PostgreSQL consulta exitosa
- [x] Redis responde PONG
- [x] No hay errores en logs: `docker-compose logs`

---

## 📊 MÉTRICAS DEL DÍA 1

| Métrica | Objetivo | Real | Status |
|---------|----------|------|--------|
| Tiempo total | 6-8h | ___h | ⏳ |
| Servicios funcionando | 6/6 | ___/6 | ⏳ |
| Tests de integración | Pass | ___ | ⏳ |
| Commits realizados | 2+ | ___ | ⏳ |

---

## 🎉 ¡DÍA 1 COMPLETADO!

### Próximos pasos (Día 2):
- [ ] Descargar dataset UCI
- [ ] Análisis exploratorio de datos (EDA)
- [ ] Crear primer notebook de Jupyter
- [ ] Identificar features clave

### 💡 Tips para mañana:
1. Deja Docker corriendo overnight si es posible
2. Si apagas, recuerda: `docker-compose up -d` para reiniciar
3. Prepara tu café ☕ - Día 2 es intenso con data

---

**Firma:** _______________  
**Fecha completada:** _______________  
**Comentarios/Notas:**

_______________________________________________
_______________________________________________
_______________________________________________

