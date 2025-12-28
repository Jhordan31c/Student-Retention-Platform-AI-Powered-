# 🎓 Student Retention Platform (AI-Powered)

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Version](https://img.shields.io/badge/Version-2.0-blue)
![Docker](https://img.shields.io/badge/Docker-Optimized-2496ED)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Next.js%20%7C%20PostgreSQL-black)

Una plataforma integral para la detección temprana, gestión y prevención de la deserción estudiantil. Combina modelos de Machine Learning avanzados (CatBoost) con herramientas de gestión (CRM) y simulación de escenarios para empoderar a las instituciones educativas.

---

## ✨ Características Principales

### 🧠 Predicción & Diagnóstico
- **Motor ML de Alta Precisión:** Modelo CatBoost optimizado con >85% de accuracy.
- **Detección de Factores de Riesgo:** Identifica causas críticas (financieras, académicas, sociales) automáticamente.
- **Feedback Visual:** Indicadores de riesgo intuitivos y semáforos de alerta.

### 🛠️ Herramientas de Intervención (NUEVO)
- **🤖 Generador de Planes con IA:** Crea hojas de ruta personalizadas para cada estudiante en segundos.
- **📋 Tablero Kanban de Gestión:** Sistema de triaje integrado para monitorear casos desde la detección hasta la resolución.
- **🎛️ Simulador de Escenarios "What-If":** Permite a los rectores modificar variables en tiempo real (ej. "¿Qué pasa si damos una beca?") para ver el impacto inmediato en el riesgo.

### 🚀 Infraestructura & UX
- **Docker Optimizado:** Imágenes de producción ligeras (Multi-stage builds) separando dependencias de entrenamiento vs. inferencia.
- **UI Moderna:** Interfaz Dark Mode con animaciones fluidas (Framer Motion), glassmorphism y componentes interactivos.
- **Arquitectura Escalable:** Backend asíncrono (FastAPI) + Frontend estático optimizado (Next.js).

---

## 🏗️ Arquitectura del Sistema

```mermaid
graph TD
    User[Usuario / Rector] -->|Interactúa| Frontend[Next.js 14 Client]
    Frontend -->|API Request| Backend[FastAPI Backend]
    
    subgraph "Core Logic"
        Backend -->|Cache| Redis
        Backend -->|Persistencia| Postgres[(PostgreSQL)]
        Backend -->|Inferencia| ML[ML Engine (CatBoost)]
    end
    
    subgraph "Features"
        Frontend --> Simulator[Simulador Escenarios]
        Frontend --> Kanban[Gestor de Casos]
        ML --> Explainer[AI Plan Generator]
    end
```

## 🚀 Guía de Inicio Rápido

### Prerrequisitos
- Docker Desktop
- Git

### Instalación (Producción)

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-repo-url>
   cd predictor-desercion
   ```

2. **Configurar entorno:**
   ```bash
   cp .env.example .env
   # Editar .env si es necesario (credenciales por defecto son seguras para local)
   ```

3. **Desplegar con Docker:**
   ```bash
   docker-compose up -d
   ```
   
   Esto levantará:
   - **Frontend:** [http://localhost:3000](http://localhost:3000)
   - **Backend API:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Base de Datos & Cache:** (PostgreSQL + Redis)

## 💻 Desarrollo Local

Para contribuir o modificar el código:

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
```

## 📁 Estructura del Proyecto

```
/
├── backend/           # API FastAPI & Lógica ML
│   ├── app/           # Endpoints, Modelos Pydantic
│   └── ml/            # Scripts de inferencia y carga de modelos
├── frontend/          # Next.js App Router
│   ├── app/           # Páginas y Layouts
│   ├── components/    # UI Kit (MagicButton, Boards, Charts)
│   └── types/         # Definiciones TypeScript
├── ml/                # Notebooks de entrenamiento y datos
└── docker/            # Dockerfiles optimizados
```

## 🛡️ Licencia

Este proyecto está bajo la Licencia MIT.