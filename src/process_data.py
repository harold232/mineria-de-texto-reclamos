import pandas as pd
import os

def cargar_datos():
    """Carga y une los datasets de diferentes años en un solo DataFrame"""
    archivos = ["data/raw/reclamos_2021.csv", 
                "data/raw/reclamos_2022.csv", 
                "data/raw/reclamos_2023.csv", 
                "data/raw/reclamos_2024.csv"]

    df_list = [pd.read_csv(archivo, encoding="utf-8") for archivo in archivos]
    df = pd.concat(df_list, ignore_index=True)
    
    df['FE_PRESEN_RECLA'] = pd.to_datetime(df['FE_PRESEN_RECLA'], format='%Y%m%d', errors='coerce')
    df['FE_RESULT_RECL'] = pd.to_datetime(df['FE_RESULT_RECL'], format='%Y%m%d', errors='coerce')
    
    # Extraer año y mes
    df["AÑO"] = df["FE_PRESEN_RECLA"].dt.year
    df["MES"] = df["FE_PRESEN_RECLA"].dt.month
    
    return df

if __name__ == "__main__":
    df = cargar_datos()
    df.to_csv("data/processed/reclamos_clean.csv", index=False)
    print("✅ Datos cargados y guardados en data/processed/reclamos_clean.csv")
