"""
🔍 Script de diagnóstico para identificar el problema de features
Ejecuta esto para ver exactamente qué espera el modelo
"""

import pickle
import numpy as np
from pathlib import Path

# Rutas
MODEL_PATH = Path("/Users/jhordancotrina/Desktop/predictor-desercion/ml/models/catboost_optimized.pkl")
X_TRAIN_PATH = Path("/Users/jhordancotrina/Desktop/predictor-desercion/ml/data/processed/X_train.npy")

print("🔍 DIAGNÓSTICO DEL MODELO")
print("=" * 60)

# 1. Cargar modelo
print("\n📦 Cargando modelo...")
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
print(f"✅ Modelo cargado: {type(model).__name__}")

# 2. Ver cuántas features espera
try:
    n_features = model.feature_count_
    print(f"\n🎯 Features esperadas por el modelo: {n_features}")
except:
    try:
        n_features = model.n_features_in_
        print(f"\n🎯 Features esperadas por el modelo: {n_features}")
    except:
        print("\n⚠️ No se pudo determinar n_features del modelo")

# 3. Ver si hay feature names
try:
    feature_names = model.feature_names_
    print(f"\n📝 Feature names disponibles: {len(feature_names)}")
    print("\nPrimeras 10 features:")
    for i, name in enumerate(feature_names[:10]):
        print(f"  {i}: {name}")
    print("  ...")
    print(f"\nÚltimas 5 features:")
    for i, name in enumerate(feature_names[-5:], start=len(feature_names)-5):
        print(f"  {i}: {name}")
except:
    print("\n⚠️ El modelo no tiene feature_names_")

# 4. Cargar X_train si existe
if X_TRAIN_PATH.exists():
    print(f"\n📂 Cargando X_train.npy...")
    X_train = np.load(X_TRAIN_PATH)
    print(f"✅ Shape de X_train: {X_train.shape}")
    print(f"   - Samples: {X_train.shape[0]}")
    print(f"   - Features: {X_train.shape[1]}")
    
    # Comparar
    if X_train.shape[1] == n_features:
        print("\n✅ ¡MATCH! X_train tiene el número correcto de features")
    else:
        print(f"\n❌ MISMATCH: X_train tiene {X_train.shape[1]} features, modelo espera {n_features}")
else:
    print(f"\n⚠️ X_train.npy no encontrado en: {X_TRAIN_PATH}")

print("\n" + "=" * 60)
print("\n💡 RECOMENDACIÓN:")
print("   Si X_train existe y tiene el número correcto de features,")
print("   puedo crear un endpoint que use exactamente ese formato.")
