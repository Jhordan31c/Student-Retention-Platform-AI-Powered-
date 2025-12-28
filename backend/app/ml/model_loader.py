import pickle
import joblib
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Any
import logging

from app.core.config import settings
from app.ml.feature_engineering import FeatureEngineer

logger = logging.getLogger(__name__)

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'FeatureEngineer':
            return FeatureEngineer
        return super().find_class(module, name)

def load_model() -> Tuple[Any, Any, Any]:
    models_dir = settings.models_dir
    data_dir = Path("/app/ml/data") # Ruta en el contenedor
    logger.info(f"Loading models from: {models_dir}")
    
    try:
        # 1. Cargar Modelo
        model_path = models_dir / "catboost_optimized.pkl"
        if not model_path.exists():
            model_path = models_dir / "model.pkl"
        
        if not model_path.exists():
            logger.error(f"❌ Model file not found at {model_path}")
            raise FileNotFoundError(f"Model file not found")
            
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"✅ Model loaded successfully from {model_path.name}")
        
        # 2. Cargar Pipeline
        pipeline_path = models_dir / "preprocessing_pipeline.pkl"
        pipeline = None
        
        try:
            if pipeline_path.exists():
                with open(pipeline_path, 'rb') as f:
                    pipeline = CustomUnpickler(f).load()
                logger.info(f"✅ Pipeline loaded successfully from {pipeline_path.name}")
            else:
                raise FileNotFoundError("Pipeline pickle missing")
                
        except Exception as e:
            logger.warning(f"⚠️ Pipeline load failed ({e}). RECONSTRUCTING and FITTING from raw data...")
            
            # --- RECONSTRUCCIÓN Y ENTRENAMIENTO DEL PIPELINE ---
            from sklearn.pipeline import Pipeline
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import StandardScaler, OneHotEncoder
            
            # Cargar datos crudos para entrenar el pipeline
            raw_data_path = data_dir / "raw/student_data.csv"
            if not raw_data_path.exists():
                raise FileNotFoundError(f"CRITICAL: Cannot reconstruct pipeline. Raw data not found at {raw_data_path}")
            
            logger.info("📊 Loading raw data for pipeline training...")
            df_raw = pd.read_csv(raw_data_path)
            
            # Definir columnas (mismas que notebook)
            numeric_features = [
                'Age at enrollment', 'Previous qualification (grade)', 'Admission grade',
                'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
                'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
                'Curricular units 1st sem (grade)', 'Curricular units 2nd sem (credited)',
                'Curricular units 2nd sem (enrolled)', 'Curricular units 2nd sem (evaluations)',
                'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)',
                'Unemployment rate', 'Inflation rate', 'GDP'
            ]
            
            engineered_features = [
                'avg_grade_overall', 'approval_rate_overall', 'total_approved',
                'grade_improvement', 'at_risk_1st_sem', 'risk_score',
                'socioeconomic_index', 'age_deviation'
            ]
            
            categorical_features = [
                'Marital status', 'Application mode', 'Application order', 'Course',
                'Daytime/evening attendance\t', 'Previous qualification', 'Nacionality',
                "Mother's qualification", "Father's qualification", 'Gender',
                'Scholarship holder', 'Debtor', 'Tuition fees up to date', 'Displaced'
            ]

            numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_original', numeric_transformer, numeric_features),
                    ('num_engineered', numeric_transformer, engineered_features),
                    ('cat', categorical_transformer, categorical_features)
                ],
                remainder='drop'
            )
            
            pipeline = Pipeline(steps=[
                ('feature_engineer', FeatureEngineer()),
                ('preprocessor', preprocessor)
            ])
            
            # ENTRENAR EL PIPELINE
            logger.info("🔧 Fitting reconstructed pipeline...")
            # Separar target si existe (aunque pipeline solo usa X)
            if 'Target' in df_raw.columns:
                X_raw = df_raw.drop(columns=['Target'])
            else:
                X_raw = df_raw
                
            pipeline.fit(X_raw)
            logger.info("✅ Pipeline reconstructed and FITTED successfully!")

        # 3. Cargar Label Encoder
        encoder_path = models_dir / "label_encoder.pkl"
        if not encoder_path.exists():
             class MockEncoder:
                 classes_ = ['Dropout', 'Enrolled', 'Graduate']
                 def inverse_transform(self, y):
                     return [self.classes_[int(val)] for val in y]
             label_encoder = MockEncoder()
        else:
            try:
                label_encoder = joblib.load(encoder_path)
            except:
                with open(encoder_path, 'rb') as f:
                    label_encoder = pickle.load(f)
            logger.info(f"✅ Label encoder loaded successfully from {encoder_path.name}")
            
        return model, pipeline, label_encoder

    except Exception as e:
        logger.error(f"🔥 CRITICAL ERROR loading models: {e}")
        raise e
