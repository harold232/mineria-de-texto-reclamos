import os
import pandas as pd
import logging
from datetime import datetime

# Configuración del logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def cargar_datos(filepath):
    """
    Carga un archivo CSV en un DataFrame de Pandas.
    
    Parámetros:
    ----------
    filepath : str
        Ruta del archivo CSV.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con los datos cargados.
    """
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
        logging.info(f"Archivo cargado exitosamente: {filepath}")
        return df
    except Exception as e:
        logging.error(f"Error al cargar {filepath}: {str(e)}")
        return None


def guardar_datos(df, filepath):
    """
    Guarda un DataFrame como CSV en la ruta especificada.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame a guardar.
    filepath : str
        Ruta donde se guardará el archivo CSV.

    Retorna:
    -------
    None
    """
    try:
        df.to_csv(filepath, index=False, encoding="utf-8")
        logging.info(f"Archivo guardado correctamente en: {filepath}")
    except Exception as e:
        logging.error(f"Error al guardar {filepath}: {str(e)}")


def crear_directorio_si_no_existe(directory):
    """
    Crea un directorio si no existe.

    Parámetros:
    ----------
    directory : str
        Ruta del directorio a crear.

    Retorna:
    -------
    None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directorio creado: {directory}")


def formatear_fecha(fecha_str, formato_entrada="%Y%m%d", formato_salida="%Y-%m-%d"):
    """
    Convierte una fecha de un formato a otro.

    Parámetros:
    ----------
    fecha_str : str
        Fecha en formato de cadena.
    formato_entrada : str
        Formato original de la fecha.
    formato_salida : str
        Formato deseado de salida.

    Retorna:
    -------
    str
        Fecha formateada.
    """
    try:
        fecha = datetime.strptime(str(fecha_str), formato_entrada)
        return fecha.strftime(formato_salida)
    except Exception as e:
        logging.error(f"Error al formatear fecha {fecha_str}: {str(e)}")
        return None


def convertir_a_datetime(df, columna, formato="%Y-%m-%d"):
    """
    Convierte una columna de un DataFrame a formato datetime.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con la columna a convertir.
    columna : str
        Nombre de la columna a convertir.
    formato : str
        Formato deseado de conversión.

    Retorna:
    -------
    pd.DataFrame
        DataFrame con la columna convertida.
    """
    try:
        df[columna] = pd.to_datetime(df[columna], format=formato, errors="coerce")
        return df
    except Exception as e:
        logging.error(f"Error al convertir {columna} a datetime: {str(e)}")
        return df


def filtrar_por_rango_fechas(df, columna, fecha_inicio, fecha_fin):
    """
    Filtra un DataFrame por un rango de fechas.

    Parámetros:
    ----------
    df : pd.DataFrame
        DataFrame con la columna de fechas.
    columna : str
        Nombre de la columna con fechas.
    fecha_inicio : str
        Fecha de inicio en formato YYYY-MM-DD.
    fecha_fin : str
        Fecha de fin en formato YYYY-MM-DD.

    Retorna:
    -------
    pd.DataFrame
        DataFrame filtrado por el rango de fechas.
    """
    df = convertir_a_datetime(df, columna)
    return df[(df[columna] >= fecha_inicio) & (df[columna] <= fecha_fin)]


# Crear directorios base si no existen
crear_directorio_si_no_existe("logs")
crear_directorio_si_no_existe("data/processed")
crear_directorio_si_no_existe("models")

