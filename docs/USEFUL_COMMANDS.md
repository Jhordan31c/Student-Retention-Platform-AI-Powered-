# 🔧 COMANDOS ÚTILES - PREDICTOR DE DESERCIÓN

## 🐳 Docker Commands

### Gestión de Servicios
```bash
# Iniciar todos los servicios
docker-compose up -d

# Iniciar y ver logs en tiempo real
docker-compose up

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra datos)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart backend

# Ver estado de servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild y Cleanup
```bash
# Rebuild todos los servicios
docker-compose build

# Rebuild sin cache (desde cero)
docker-compose build --no-cache

# Rebuild un servicio específico
docker-compose build backend

# Eliminar imágenes no usadas
docker image prune -a

# Eliminar volúmenes no usados
docker volume prune
```

### Acceso a Contenedores
```bash
# Entrar al contenedor del backend
docker exec -it predictor-backend bash

# Entrar al contenedor del frontend
docker exec -it predictor-frontend sh

# Entrar a PostgreSQL
docker exec -it predictor-postgres psql -U postgres -d predictor_db

# Entrar a Redis
docker exec -it predictor-redis redis-cli -a redis123
```

---

## 🐍 Backend Commands

### Dentro del contenedor o venv local
```bash
# Activar virtual environment (local)
cd backend && source venv/bin/activate

# Correr servidor en desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ejecutar tests
pytest tests/ -v

# Tests con coverage
pytest --cov=app tests/

# Generar reporte de coverage HTML
pytest --cov=app --cov-report=html tests/

# Linting
black app/
flake8 app/
isort app/

# Type checking
mypy app/
```

### Migraciones de Base de Datos (Alembic)
```bash
# Crear una nueva migración
alembic revision --autogenerate -m "descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current
```

---

## ⚛️ Frontend Commands

### Dentro del contenedor o local
```bash
# Desarrollo local
npm run dev

# Build para producción
npm run build

# Iniciar producción
npm run start

# Linting
npm run lint

# Ejecutar tests
npm run test

# Tests con UI
npm run test:ui

# Tests con coverage
npm run test:coverage

# Type checking
npm run type-check

# Format code
npm run format
```

---

## 🗄️ Database Commands

### PostgreSQL
```bash
# Conectar a la base de datos
psql -h localhost -U postgres -d predictor_db

# Backup de base de datos
docker exec predictor-postgres pg_dump -U postgres predictor_db > backup.sql

# Restore de backup
docker exec -i predictor-postgres psql -U postgres -d predictor_db < backup.sql

# Ver todas las tablas
\dt

# Describir una tabla
\d nombre_tabla

# Ejecutar query desde archivo
psql -h localhost -U postgres -d predictor_db -f query.sql
```

### Redis
```bash
# Conectar a Redis
docker exec -it predictor-redis redis-cli -a redis123

# Dentro de redis-cli:
# Ver todas las keys
KEYS *

# Ver valor de una key
GET key_name

# Eliminar una key
DEL key_name

# Limpiar toda la base de datos (CUIDADO)
FLUSHDB

# Ver info del servidor
INFO

# Monitorear comandos en tiempo real
MONITOR
```

---

## 🧪 Testing Commands

### Backend Testing
```bash
# Test un archivo específico
pytest tests/test_health.py -v

# Test con markers
pytest -m "slow" tests/

# Test con keyword
pytest -k "health" tests/

# Test con print output
pytest tests/ -v -s

# Test coverage por módulo
pytest --cov=app.api tests/ --cov-report=term-missing
```

### Frontend Testing
```bash
# Run all tests
npm test

# Run specific test file
npm test src/components/Dashboard.test.tsx

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm run test:coverage

# Update snapshots
npm test -- --update
```

---

## 📊 MLflow Commands

### CLI Commands
```bash
# Iniciar servidor MLflow
mlflow server \
  --backend-store-uri postgresql://postgres:postgres@localhost:5432/predictor_db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000

# Listar experimentos
mlflow experiments list

# Crear experimento
mlflow experiments create --experiment-name "nuevo-experimento"

# Eliminar experimento
mlflow experiments delete --experiment-id 1

# Ver runs de un experimento
mlflow runs list --experiment-id 1
```

---

## 🔍 Debugging & Monitoring

### Ver logs en tiempo real
```bash
# Backend logs
docker-compose logs -f backend | grep ERROR

# Frontend logs
docker-compose logs -f frontend | grep -i error

# PostgreSQL logs
docker-compose logs -f postgres

# Todos los servicios con timestamp
docker-compose logs -f --tail=100 --timestamps
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/api/v1/health | jq

# Backend status
curl http://localhost:8000/api/v1/status | jq

# Frontend (debe devolver HTML)
curl -I http://localhost:3000

# PostgreSQL
docker exec predictor-postgres pg_isready -U postgres

# Redis
docker exec predictor-redis redis-cli -a redis123 PING
```

### Performance Monitoring
```bash
# Ver uso de recursos por contenedor
docker stats

# Ver solo un contenedor
docker stats predictor-backend

# Inspeccionar un contenedor
docker inspect predictor-backend

# Ver procesos dentro del contenedor
docker top predictor-backend
```

---

## 🛠️ Development Workflow

### Workflow típico del día:
```bash
# 1. Iniciar servicios
docker-compose up -d

# 2. Ver logs
docker-compose logs -f backend frontend

# 3. Hacer cambios en código
# (los cambios se reflejan automáticamente con hot-reload)

# 4. Ejecutar tests
docker exec predictor-backend pytest tests/ -v

# 5. Si necesitas rebuild
docker-compose down
docker-compose build
docker-compose up -d

# 6. Al final del día
docker-compose down
```

### Git Workflow
```bash
# Feature workflow
git checkout -b feature/nombre-feature
# hacer cambios
git add .
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-feature

# Conventional commits
git commit -m "feat: nueva feature"
git commit -m "fix: corregir bug"
git commit -m "docs: actualizar documentación"
git commit -m "test: añadir tests"
git commit -m "refactor: refactorizar código"
```

---

## 🚨 Troubleshooting

### Port already in use
```bash
# Ver qué está usando el puerto
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Matar proceso
kill -9 <PID>
```

### Container won't start
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar variables de entorno
docker-compose config

# Entrar al contenedor manualmente
docker run -it predictor-backend bash
```

### Database issues
```bash
# Recrear base de datos
docker-compose down -v
docker-compose up -d postgres
# Esperar 10 segundos
docker-compose up -d backend
```

### Clean slate (empezar de cero)
```bash
# ADVERTENCIA: Esto elimina TODO
docker-compose down -v
docker system prune -a
rm -rf ml/data/processed/*
rm -rf ml/models/*
docker-compose up -d --build
```

---

## 📝 Quick Reference

### URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- API ReDoc: http://localhost:8000/redoc
- MLflow: http://localhost:5000
- pgAdmin: http://localhost:5050

### Default Credentials
- PostgreSQL: postgres / postgres
- Redis: redis123
- pgAdmin: admin@predictor.com / admin

---

## 💡 Tips & Best Practices

1. **Siempre usa docker-compose** para desarrollo local
2. **Commit frecuentemente** con mensajes descriptivos
3. **Ejecuta tests** antes de hacer commit
4. **Revisa logs** cuando algo no funciona
5. **Usa branches** para features nuevas
6. **Documenta** cambios importantes
7. **Haz backup** de la base de datos antes de cambios grandes
8. **Monitorea recursos** con `docker stats`

---

¿Necesitas ayuda? Revisa:
- README.md
- docs/DEVELOPMENT.md
- docs/ARCHITECTURE.md
