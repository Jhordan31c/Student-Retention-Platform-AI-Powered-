# 🚀 QUICK START - DÍA 1

## ⚡ Setup Rápido (15 minutos)

Si tienes Docker instalado, puedes tener todo corriendo en minutos:

```bash
# 1. Descargar y extraer el proyecto
cd predictor-desercion

# 2. Ejecutar script de setup
chmod +x setup.sh
./setup.sh

# 3. ¡Listo! Accede a:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000/docs
# - MLflow: http://localhost:5000
```

---

## 📋 Prerequisitos Mínimos

- ✅ Docker Desktop (con Docker Compose)
- ✅ 8GB RAM disponible
- ✅ 10GB espacio en disco
- ✅ Conexión a internet

---

## 🎯 Paso a Paso Manual

### 1. Configurar Variables de Entorno (2 min)

```bash
# Copiar template
cp .env.example .env

# Generar SECRET_KEY seguro
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Editar .env y pegar el SECRET_KEY generado
nano .env  # o usa tu editor favorito
```

### 2. Iniciar Docker Compose (5 min)

```bash
# Build las imágenes (primera vez tarda ~10 min)
docker-compose build

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3. Verificar que Todo Funciona (3 min)

```bash
# Backend health check
curl http://localhost:8000/api/v1/health

# Frontend (debería devolver HTML)
curl http://localhost:3000

# PostgreSQL
docker exec predictor-postgres pg_isready

# Redis
docker exec predictor-redis redis-cli -a redis123 PING
```

Si todos responden correctamente: **✅ ¡Setup completo!**

---

## 🔧 Desarrollo Local (Opcional)

Si prefieres desarrollo sin Docker:

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📚 Próximos Pasos

Ahora que todo está funcionando:

1. **Revisa el checklist detallado:** `docs/DAY1_CHECKLIST.md`
2. **Explora los comandos útiles:** `docs/USEFUL_COMMANDS.md`
3. **Lee la documentación completa:** `README.md`

---

## 🆘 Troubleshooting

### Puerto ya en uso
```bash
# Ver qué usa el puerto
lsof -i :8000
# Matar el proceso
kill -9 <PID>
```

### Docker no inicia
```bash
# Rebuild desde cero
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Ver logs de errores
```bash
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep error
```

---

## 💡 Tips

- **Primera vez:** El build tarda ~10-15 minutos
- **Siguientes veces:** Solo `docker-compose up -d` (segundos)
- **Hot reload:** Los cambios en código se reflejan automáticamente
- **Debugging:** Usa `docker-compose logs -f [servicio]`

---

## ✅ Verificación Final

Ejecuta este one-liner para verificar todo:

```bash
echo "🔍 Verificando servicios..." && \
curl -s http://localhost:8000/api/v1/health | grep -q healthy && echo "✅ Backend OK" || echo "❌ Backend FAIL" && \
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend FAIL" && \
docker exec predictor-postgres pg_isready > /dev/null 2>&1 && echo "✅ PostgreSQL OK" || echo "❌ PostgreSQL FAIL" && \
docker exec predictor-redis redis-cli -a redis123 PING 2>/dev/null | grep -q PONG && echo "✅ Redis OK" || echo "❌ Redis FAIL"
```

Si ves todos ✅: **¡Estás listo para el Día 2!**

---

## 📞 Soporte

- 📖 Docs completas: `README.md`
- ✅ Checklist: `docs/DAY1_CHECKLIST.md`
- 🔧 Comandos: `docs/USEFUL_COMMANDS.md`
- 🏗️ Arquitectura: `docs/ARCHITECTURE.md`

---

**¿Listo para comenzar?** 🚀

Siguiente paso: `docs/DAY1_CHECKLIST.md` para el plan detallado del día.
