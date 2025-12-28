# LLM Explainer Module - FIXED VERSION (Dic 2025)
# Usa Gemini 3 Flash (gratis) con fallback a otras alternativas

import os
import asyncio
import google.generativeai as genai
import pandas as pd
from loguru import logger
from typing import List, Optional
from datetime import datetime, timedelta

class GeminiExplainer:
    """
    Explainer usando Gemini API con manejo robusto de cuotas
    y fallbacks automáticos.
    """
    
    # Modelos ordenados por prioridad (Actualizado Dic 2025)
      # ✅ MODELOS ESTABLES (NO preview)
    MODEL_PRIORITY = [
        'gemini-1.5-flash',        # ✅ MÁS ESTABLE (Recomendado)
        'gemini-1.5-flash-latest', # ✅ Versión latest
        'gemini-2.5-flash',        # ⚠️ Si está disponible
        'gemini-1.5-pro',          # Backup (más lento pero mejor)
    ]
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("⚠️ GEMINI_API_KEY no encontrada. Explicaciones LLM deshabilitadas.")
            self.model = None
            self.model_name = None
            return

        try:
            genai.configure(api_key=self.api_key)
            
            # Detectar mejor modelo disponible
            self.model_name = self._select_best_available_model()
            
            if self.model_name:
                self.model = genai.GenerativeModel(self.model_name, safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE_SPEECH': 'BLOCK_NONE',
                'SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                })
                logger.success(f"✅ Gemini Explainer inicializado: {self.model_name}")
            else:
                logger.error("❌ No se encontró ningún modelo Gemini compatible.")
                self.model = None
                
        except Exception as e:
            logger.error(f"❌ Error al inicializar Gemini: {e}")
            self.model = None
    
    def _select_best_available_model(self) -> Optional[str]:
        """
        Selecciona el mejor modelo disponible en la cuenta actual.
        """
        try:
            # Obtener modelos disponibles
            available = set()
            try:
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        name = m.name.replace('models/', '')
                        available.add(name)
                        available.add(f"models/{name}")
            except Exception as list_err:
                logger.warning(f"⚠️ Error listando modelos ({list_err}). Usando default.")
                return 'gemini-2.5-flash' # Default optimista
            
            logger.info(f"🔍 Modelos Gemini detectados: {sorted(list(available))[:5]}...")
            
            # Buscar en orden de prioridad
            for candidate in self.MODEL_PRIORITY:
                if candidate in available or f"models/{candidate}" in available:
                    return candidate
                
                # Búsqueda parcial (ej: encontrar gemini-3.0-flash-001 si buscamos gemini-3.0-flash)
                for avail in available:
                    if candidate in avail and "vision" not in avail:
                        return avail
            
            # Si no encuentra ninguno de la lista, devolver el primero disponible que sea 'flash'
            flash_models = [m for m in available if 'flash' in m.lower()]
            if flash_models:
                return flash_models[0]

            return 'gemini-2.5-flash' # Fallback final
            
        except Exception as e:
            logger.error(f"❌ Error detectando modelos: {e}")
            return 'gemini-2.5-flash'
    
    def _format_student_profile(self, df: pd.DataFrame) -> str:
        """Convierte datos del estudiante a texto legible"""
        try:
            row = df.iloc[0]
            
            # Traducir valores con manejo de errores
            debt = "Sí" if row.get('Debtor', 0) == 1 else "No"
            scholarship = "Sí" if row.get('Scholarship holder', 0) == 1 else "No"
            fees = "Al día" if row.get('Tuition fees up to date', 0) == 1 else "Atrasada"
            gender = "Masculino" if row.get('Gender', 1) == 1 else "Femenino"
            
            profile = f"""
**Perfil del Estudiante:**
-Edad: {row.get('Age at enrollment', 'N/A')} años
- Género: {gender}

**Situación Financiera:**
- Beca: {scholarship}
- Deuda: {debt}
- Matrícula: {fees}

**Rendimiento Académico:**
- Nota 1er Semestre: {row.get('Curricular units 1st sem (grade)', 'N/A')}
- Unidades Aprobadas 1er Sem: {row.get('Curricular units 1st sem (approved)', 'N/A')}
- Nota 2do Semestre: {row.get('Curricular units 2nd sem (grade)', 'N/A')}
- Unidades Aprobadas 2do Sem: {row.get('Curricular units 2nd sem (approved)', 'N/A')}
"""
            return profile.strip()
        except Exception as e:
            logger.error(f"❌ Error formateando perfil: {e}")
            return "Datos del estudiante no disponibles."
    
    async def generate_explanation(
        self, 
        df: pd.DataFrame, 
        prediction_label: str, 
        probability: float,
        max_retries: int = 1
    ) -> List[str]:
        """
        Genera insights narrativos usando Gemini con retry automático
        """
        if not self.model:
            return ["⚠️ Análisis IA no disponible (API key faltante)."]
        
        profile_text = self._format_student_profile(df)
        
        # Prompt optimizado
        prompt = f"""Actúa como consejero académico. Analiza brevemente:

**PREDICCIÓN:** {prediction_label} ({probability:.1%})

{profile_text}

Responde SOLO con 3 puntos numerados, sin introducción:
Formato:
- Insight 1
- Insight 2  
- Insight 3"""
        
        # Intentar con retry
        for attempt in range(max_retries + 1):
            try:
                response = await self.model.generate_content_async(
                    prompt,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 1200,
                    }
                )
                
                if response.text:
                    text = response.text.strip()

                    # 🔴 AGREGAR ESTO PARA DEBUG
                    logger.info(f"📝 RESPUESTA COMPLETA DEL LLM:\n{text}")
                    logger.info(f"📏 Longitud: {len(text)} caracteres")

                    insights = [
                        line.replace('- ', '').strip() 
                        for line in text.split('\n') 
                        if line.strip().startswith('-')
                    ]

                    logger.info(f"📊 Insights extraídos: {len(insights)}")
                    
                    if not insights:
                        # Si no hay bullets, tomar primeras 3 líneas
                        insights = [l.strip() for l in text.split('\n') if l.strip()][:3]
                    
                    if insights:
                        logger.success(f"✅ {len(insights)} insights generados por {self.model_name}")
                        return insights[:3]
                
                return ["✅ Predicción completada. Contacte a un consejero para más detalles."]
                
            except Exception as e:
                error_msg = str(e)
                
                # Detectar error de cuota
                if '429' in error_msg or 'quota' in error_msg.lower():
                    logger.warning(f"⚠️ Cuota excedida en {self.model_name}. Reintentando...")
                    
                    if attempt == max_retries:
                        return [
                            f"⚠️ Límite de API alcanzado ({self.model_name})",
                            "💡 El sistema sigue funcionando con reglas básicas",
                            f"📊 Predicción: {prediction_label}"
                        ]
                    
                    # Backoff
                    await asyncio.sleep(1)
                    continue
                
                else:
                    logger.error(f"❌ Error generando explicación: {error_msg}")
                    return [
                        "❌ Error al generar explicación con IA",
                        f"Predicción: {prediction_label}"
                    ]
        
        return ["⚠️ No se pudo generar explicación después de reintentos."]
