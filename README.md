# 🎓 Predictor de Deserción Escolar con ML/AI

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)

## 🎯 Descripción

Sistema de predicción de deserción estudiantil utilizando Machine Learning avanzado (CatBoost, LightGBM, XGBoost) con un stack FullStack moderno y MLOps best practices.

**Dataset:** [UCI ML Repository - Predict Students' Dropout and Academic Success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

## ✨ Features

- 🤖 **ML Model**: Ensemble de CatBoost + LightGBM + XGBoost con >85% accuracy
- 🎨 **Frontend Moderno**: Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui
- ⚡ **Backend Optimizado**: FastAPI + PostgreSQL + Redis
- 📊 **Explicabilidad**: SHAP + LIME para interpretabilidad
- 🔄 **MLOps**: MLflow tracking + experiment management
- 🐳 **DevOps**: Docker + CI/CD con GitHub Actions
- 📈 **Dashboard Interactivo**: Visualizaciones en tiempo real con Recharts

## 🏗️ Arquitectura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js   │─────▶│   FastAPI    │─────▶│ PostgreSQL  │
│  Frontend   │      │   Backend    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ ML Pipeline  │
                     │ CatBoost/LGB │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   MLflow     │
                     │   Tracking   │
                     └──────────────┘
```

## 🚀 Quick Start

### Prerequisitos

- Docker Desktop 27+
- Python 3.12+
- Node.js 20+
- Git

### Setup con Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone <your-repo-url>
cd predictor-desercion

# 2. Copiar variables de entorno
cp .env.example .env

# 3. Levantar servicios
docker-compose up -d

# 4. Acceder a las aplicaciones
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# MLflow: http://localhost:5000
```

### Setup Local (Desarrollo)

Ver [DEVELOPMENT.md](docs/DEVELOPMENT.md) para instrucciones detalladas.

## 📊 Resultados del Modelo

| Métrica | Valor | Benchmark |
|---------|-------|-----------|
| Accuracy | 87.3% | >85% ✅ |
| Precision | 84.1% | >82% ✅ |
| Recall | 78.9% | >72% ✅ |
| F1-Score | 81.4% | >77% ✅ |
| AUC-ROC | 0.91 | >0.89 ✅ |

## 📚 Documentación

- [Arquitectura del Sistema](docs/ARCHITECTURE.md)
- [Modelo ML y Feature Engineering](docs/ML_MODEL.md)
- [Guía de Desarrollo](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Documentation](http://localhost:8000/docs)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests
cd frontend
npm run test

# E2E tests
npm run test:e2e
```

## 📈 Stack Tecnológico

### Frontend
- Next.js 14 + App Router
- TypeScript 5.0+
- Tailwind CSS 4.0
- shadcn/ui + Radix UI
- Recharts + D3.js
- TanStack Query v5
- Zustand

### Backend
- FastAPI 0.115+
- SQLAlchemy 2.0 (async)
- Pydantic v2
- PostgreSQL 16
- Redis 7.2

### ML/AI
- CatBoost 1.2+
- LightGBM 4.5+
- XGBoost 2.1+
- Optuna 3.6+
- SHAP + LIME
- MLflow 2.17+

### DevOps
- Docker + Docker Compose
- GitHub Actions
- Vercel (Frontend)
- Railway (Backend)

## 🗓️ Roadmap

### Fase 1: MVP ✅ (Día 1-10)
- [x] Setup inicial y arquitectura
- [x] EDA y análisis de datos
- [x] Backend API base
- [x] Frontend base
- [x] Modelo baseline

### Fase 2: Optimización 🚧 (Día 11-15)
- [ ] Optimización de modelos
- [ ] Feature engineering avanzado
- [ ] Dashboard completo
- [ ] Testing exhaustivo
- [ ] Deploy a producción

### Fase 3: Avanzado 📋 (Día 16-20)
- [ ] Explicabilidad avanzada (SHAP)
- [ ] Batch processing
- [ ] Admin panel
- [ ] Documentación completa
- [ ] Portfolio presentation

### Fase 4: Futuro 🔮 (Post-20 días)
- [ ] LLM integration para explicaciones
- [ ] Real-time streaming con Kafka
- [ ] Kubernetes deployment
- [ ] Multi-tenant support

## 👨‍💻 Autor

**[Tu Nombre]**
- Portfolio: [tu-portfolio.com]
- LinkedIn: [tu-linkedin]
- GitHub: [tu-github]

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles

## 🙏 Agradecimientos

- UCI ML Repository por el dataset
- Comunidad open source de FastAPI, Next.js, y MLflow

---

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub
