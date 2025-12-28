"""
Script para descargar el dataset de predicción de deserción estudiantil
Dataset: Predict students' dropout and academic success
Source: UCI Machine Learning Repository
URL: https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success
"""

import os
import requests
import zipfile
import pandas as pd
from pathlib import Path

# Configuración
DATASET_URL = "https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip"
BASE_DIR = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Crear directorios si no existen
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def download_dataset():
    """Descarga el dataset del UCI Repository"""
    print("🔽 Descargando dataset del UCI Repository...")
    print(f"📍 URL: {DATASET_URL}")
    
    zip_path = RAW_DIR / "dataset.zip"
    
    try:
        # Descargar archivo
        response = requests.get(DATASET_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(zip_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                    f.write(chunk)
                    done = int(50 * downloaded / total_size)
                    print(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes", end='')
        
        print("\n✅ Descarga completada!")
        return zip_path
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error al descargar: {e}")
        return None

def extract_dataset(zip_path):
    """Extrae el archivo ZIP"""
    print("\n📦 Extrayendo archivos...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(RAW_DIR)
        
        print("✅ Extracción completada!")
        
        # Listar archivos extraídos
        print("\n📁 Archivos extraídos:")
        for file in RAW_DIR.iterdir():
            if file.is_file() and file.suffix == '.csv':
                print(f"  - {file.name} ({file.stat().st_size / 1024:.2f} KB)")
        
        return True
        
    except zipfile.BadZipFile as e:
        print(f"❌ Error al extraer: {e}")
        return False

def validate_dataset():
    """Valida el dataset descargado"""
    print("\n🔍 Validando dataset...")
    
    # Buscar archivo CSV principal
    csv_files = list(RAW_DIR.glob("*.csv"))
    
    if not csv_files:
        print("❌ No se encontró ningún archivo CSV")
        return None
    
    # Tomar el primer CSV encontrado
    csv_path = csv_files[0]
    print(f"📄 Archivo encontrado: {csv_path.name}")
    
    try:
        # Cargar y validar
        df = pd.read_csv(csv_path, sep=';')  # El dataset usa punto y coma como separador
        
        print(f"\n✅ Dataset válido!")
        print(f"📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
        print(f"\n📋 Primeras columnas:")
        for i, col in enumerate(df.columns[:10], 1):
            print(f"  {i}. {col}")
        if len(df.columns) > 10:
            print(f"  ... y {len(df.columns) - 10} columnas más")
        
        # Renombrar a student_data.csv para consistencia
        target_path = RAW_DIR / "student_data.csv"
        if csv_path != target_path:
            df.to_csv(target_path, index=False)
            print(f"\n✅ Dataset guardado como: student_data.csv")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al validar: {e}")
        return None

def main():
    """Función principal"""
    print("=" * 60)
    print("📚 DESCARGA DE DATASET - PREDICCIÓN DE DESERCIÓN ESTUDIANTIL")
    print("=" * 60)
    
    # Verificar si ya existe
    existing_csv = RAW_DIR / "student_data.csv"
    if existing_csv.exists():
        print(f"\n⚠️  El dataset ya existe en: {existing_csv}")
        response = input("¿Deseas descargarlo nuevamente? (s/n): ").lower()
        if response != 's':
            print("✅ Usando dataset existente")
            df = pd.read_csv(existing_csv)
            print(f"📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")
            return
    
    # Descargar
    zip_path = download_dataset()
    if not zip_path:
        return
    
    # Extraer
    if not extract_dataset(zip_path):
        return
    
    # Validar
    df = validate_dataset()
    if df is None:
        return
    
    # Limpiar archivo ZIP
    if zip_path.exists():
        zip_path.unlink()
        print("\n🗑️  Archivo ZIP eliminado (ya no es necesario)")
    
    print("\n" + "=" * 60)
    print("✅ ¡PROCESO COMPLETADO EXITOSAMENTE!")
    print("=" * 60)
    print(f"\n📁 Dataset disponible en: {RAW_DIR / 'student_data.csv'}")
    print("\n🚀 Siguiente paso: Abre tu notebook y ejecuta las celdas de análisis")

if __name__ == "__main__":
    main()