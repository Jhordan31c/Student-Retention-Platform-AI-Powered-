# 🚀 PLAN DE CIERRE: SPRINT FINAL (5 DÍAS)
## Objetivo: MVP Robusto para el 1 de Diciembre de 2025

---

## 🚨 SITUACIÓN ACTUAL
**Estado:** Sprint de emergencia / Consolidación.
**Fecha Inicio:** 27 Noviembre 2025
**Fecha Entrega:** 1 Diciembre 2025
**Enfoque:** Integración > Nuevos Features. Priorizar que "funcione" end-to-end sobre la perfección teórica.

---

## 🗓️ CRONOGRAMA SPRINT FINAL (5 DÍAS)

### 🏁 **DÍA 1 (27 Nov): CONEXIÓN Y BACKEND CORE**
**Meta:** Lograr que el Backend prediga usando el modelo real y devuelva datos al frontend (vía API Docs).
- [ ] **Limpieza ML:** Asegurar que `ml/models/` tenga el modelo `.cbm` o `.pkl` final (CatBoost es suficiente, no compliques con Ensemble si no está listo).
- [ ] **API Integration:** Verificar que `POST /predict` cargue el modelo y devuelva predicción + probabilidad.
- [ ] **Configuración:** Crear `.env` y asegurar que las variables coincidan en Docker.
- [ ] **DB Check:** Confirmar que PostgreSQL guarda el historial de predicciones.

### 🎨 **DÍA 2 (28 Nov): FRONTEND INTERACTIVO**
**Meta:** Una UI limpia que consuma la API real (No mocks).
- [ ] **Formulario Real:** Construir el formulario en Next.js con los campos exactos que requiere el modelo.
- [ ] **Feedback Visual:** Mostrar "Cargando..." mientras predice y mostrar el resultado con colores (Rojo: Riesgo Alto, Verde: Aprobado).
- [ ] **Gráficos Simples:** Usar Recharts para mostrar la probabilidad (Gauge chart o Barra simple).

### 🧠 **DÍA 3 (29 Nov): EXPLICABILIDAD & VALOR AGREGADO**
**Meta:** Responder "¿Por qué el estudiante desertaría?"
- [ ] **Feature Importance:** El backend debe devolver las 3 variables que más influyeron en la decisión (usando `feature_importances_` del modelo o SHAP ligero).
- [ ] **UI Explicativa:** Mostrar estas 3 variables en el Frontend ("Riesgo alto debido a: Notas semestre 1 bajas, Deuda en matrícula").
- [ ] **Error Handling:** Manejar errores si el usuario mete datos locos.

### 🐳 **DÍA 4 (30 Nov): DOCKER Y ESTABILIDAD**
**Meta:** "It works on any machine".
- [ ] **Docker Compose Polish:** Asegurar que `docker-compose up` levante todo sin errores manuales.
- [ ] **Network Check:** Verificar comunicación interna (Backend -> DB, Frontend -> Backend).
- [ ] **Tests Críticos:** 
    - 1 Test Backend (Endpoint predict funciona).
    - 1 Test Frontend (La página carga).

### 📚 **DÍA 5 (1 Dic): DOCUMENTACIÓN Y ENTREGA**
**Meta:** Portafolio Ready.
- [ ] **Documentación Faltante:** Crear `DEVELOPMENT.md` y llenar los huecos del `README.md`.
- [ ] **Screenshots:** Capturar la UI funcionando para el README.
- [ ] **Limpieza:** Borrar logs, código comentado y archivos temporales.
- [ ] **Video Demo (Opcional):** Grabar 30 segundos del flujo funcionando.

---

## ✂️ RECORTES TÁCTICOS (Lo que dejaremos para la "Fase 2" post-entrega)
Para cumplir la fecha, **sacrificamos** temporalmente:
1.  **Monitorización Avanzada:** (Evidently AI, Prometheus, Grafana). Usaremos logs simples.
2.  **CI/CD Complex:** (GitHub Actions pipelines). Haremos deploy/test local.
3.  **Auth de Usuarios:** La API será pública/abierta para la demo.
4.  **Ensemble Complejo:** Nos quedamos con el mejor modelo individual (probablemente CatBoost) para evitar complejidad de serialización.

---

## 🛠️ STACK FINAL (CONSOLIDADO)
- **Frontend:** Next.js 14 + Tailwind + Recharts.
- **Backend:** FastAPI + Pydantic.
- **ML:** CatBoost (Single Model) + MLflow (solo tracking local).
- **DB:** PostgreSQL.
- **Infra:** Docker Compose.

---
**¡A TRABAJAR! CADA HORA CUENTA.**
