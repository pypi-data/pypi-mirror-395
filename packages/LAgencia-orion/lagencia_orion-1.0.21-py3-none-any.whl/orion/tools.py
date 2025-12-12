import ast
import math
import os
import re
import unicodedata
from datetime import datetime
from typing import Dict, List, Union

import geopandas as gpd
import numpy as np
import pandas as pd
from pandas.io import json


def df_to_dicts(df: pd.DataFrame) -> List[Dict]:
    """Convierte un DataFrame en una lista de diccionarios"""

    df = df.replace("", None).copy()
    df = df.replace(np.nan, None).copy()
    df = df.replace(pd.NaT, None).copy()
    df = df.replace("NaT", None).copy()
    df = df.replace("nan", None).copy()
    df = df.where(pd.notnull(df), None).copy()
    records = df.to_dict("records")
    return records


def gdf_to_dicts(gdf: gpd.GeoDataFrame) -> List[Dict]:
    """
    Convierte un GeoDataFrame en una lista de diccionarios,
    manejando correctamente geometrías y valores nulos.
    """
    # Reemplazar valores vacíos o NaN en columnas no geométricas
    non_geom_columns = gdf.select_dtypes(include=["object", "number"]).columns
    gdf[non_geom_columns] = gdf[non_geom_columns].replace("", None).replace(np.nan, None)

    # Convertir a lista de diccionarios, incluyendo geometrías como WKT (opcional)
    records = gdf.to_dict("records")

    # Si deseas incluir geometrías como WKT (opcional)
    for record in records:
        if "geometry" in record and record["geometry"] is not None:
            record["geometry"] = record["geometry"].wkt

    return records


def list_obj_to_df(records: List[Dict]) -> pd.DataFrame:
    """Convierte una lista de objetos en un DataFrame"""

    if len(records) == 0:
        return pd.DataFrame()

    rows = []
    for row in records:
        dict_ = vars(row)
        del dict_["_sa_instance_state"]
        rows.append(dict_)

    return pd.DataFrame(rows)


def parse_features(x):
    "Parcea un string que tenga forma de dict a un dict ptyhon"
    # NaN / None
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return {}
    # Ya es dict
    if isinstance(x, dict):
        return x
    # String → intenta literal_eval y luego JSON
    if isinstance(x, str):
        s = x.strip()
        try:
            return ast.literal_eval(s)  # para representaciones tipo Python con None, True/False
        except Exception:
            try:
                return json.loads(s)  # por si viene en JSON válido
            except Exception:
                return {}
    # Cualquier otro tipo
    return {}


def get_first_image(image_str: str) -> Union[str, None]:
    """Recibe un string de imagenes con estructura json y retornam la primera imagen"""
    try:
        # Convertir la cadena a lista de diccionarios
        image_list = ast.literal_eval(image_str)
        # Obtener el primer diccionario y extraer 'fotourl'
        return image_list[0]["fotourl"] if image_list else None
    except (ValueError, IndexError, KeyError):
        print("Error al obtener primera imagen")
        return None


def cut_date_str(date: str):
    if isinstance(date, str):
        if date == "" or date == "0000-00-00 00:00:00":
            return "1900-01-01"
        return date[:19]
    if isinstance(date, datetime):
        return date
    if pd.isna(date):
        return "1900-01-01"
    if date is None:
        return "1900-01-01"
    return "1900-01-01"


def convert_iso_to_datetime(iso_date_str: str) -> Union[str, None]:
    """
    Convierte una fecha en formato ISO 8601 o similar a 'yyyy-mm-dd hh:mm:ss'.

    Args:
        iso_date_str (str): Fecha en formato ISO 8601 o similar
                           (ej. '2023-12-19T10:24:59' o '2024-11-27 10:04:53.494356').

    Returns:
        str: Fecha en formato 'yyyy-mm-dd hh:mm:ss', o None si hay un error.
    """
    if isinstance(iso_date_str, datetime):
        return iso_date_str.strftime("%Y-%m-%d %H:%M:%S")

    if not isinstance(iso_date_str, str):
        return None

    try:
        # Si la fecha ya está en el formato deseado, no la cambia
        if " " in iso_date_str and len(iso_date_str.split(".")[0]) == 19:
            return iso_date_str.split(".")[0]

        # Convertir la cadena a un objeto datetime
        dt_obj = datetime.fromisoformat(iso_date_str)
        # Formatear el objeto datetime al formato deseado
        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return None


def robust_convert_to_datetime(date_str):
    """
    Convierte fechas con formatos mixtos en una columna al formato datetime.

    Args:
        date_str (str): Fecha en formato ISO 8601, con o sin milisegundos.

    Returns:
        datetime or NaT: Objeto datetime o NaT si no es posible convertir.
    """
    if isinstance(date_str, datetime):
        return date_str

    if not isinstance(date_str, str):
        return pd.NaT

    try:
        # Formato sin milisegundos
        if " " in date_str and len(date_str.split(".")[0]) == 19:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # Formato con milisegundos
        return datetime.fromisoformat(date_str)
    except ValueError:
        # Devuelve NaT si no se puede convertir
        return pd.NaT


def generate_slug(texto: str):
    try:
        # Crear un diccionario para reemplazar vocales con tilde
        map_letters = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u"}

        # Convertir a minúsculas
        texto = texto.lower()
        # Reemplazar vocales con tilde por su versión sin tilde
        for old, new in map_letters.items():
            texto = texto.replace(old, new)
        # Reemplazar caracteres no alfanuméricos por guiones
        texto = re.sub(r"[^a-z0-9\s-]", "", texto)
        # Reemplazar espacios y guiones consecutivos por un solo guion
        texto = re.sub(r"\s+", "-", texto)
        texto = re.sub(r"-+", "-", texto)
        # Eliminar guiones iniciales o finales
        texto = texto.strip("-").lower()
        return texto
    except Exception:
        print(texto)
        raise


def format_column_name(column_name):
    # Normalizar el string para eliminar acentos y tildes
    normalized_name = unicodedata.normalize("NFD", column_name)
    normalized_name = normalized_name.encode("ascii", "ignore").decode("utf-8")

    # Convertir todo a minúsculas
    formatted_name = normalized_name.lower()

    # Reemplazar "ñ" por "n"
    formatted_name = formatted_name.replace("ñ", "n")

    # Reemplazar espacios por "_"
    formatted_name = re.sub(r"\s+", "_", formatted_name)

    # Eliminar caracteres no alfanuméricos ni "_"
    formatted_name = re.sub(r"[^a-z0-9_]", "", formatted_name)

    return formatted_name


def clear_folder(folder_path: str) -> None:
    """
    Elimina todos los archivos dentro de una carpeta sin eliminar la carpeta.

    Args:
        folder_path (str): La ruta de la carpeta a limpiar.
    """
    try:
        # Iterar sobre el contenido de la carpeta
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            # Eliminar solo los archivos
            if os.path.isfile(item_path):
                os.remove(item_path)
        print(f"Todos los archivos en '{folder_path}' han sido eliminados.")
    except Exception as e:
        print(f"Error al limpiar la carpeta: {e}")


def clean_text(text):
    """Limpia un string eliminando emojis y caracteres especiales,
    solo se mantien caracteres con tilde, 'ñ', 'ü'"""
    if isinstance(text, str):
        return re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s.,;:!?"\'-]', "", text)
    return text


def normalize_commas(input_string: str) -> str:
    """
    Reemplaza múltiples comas consecutivas con una sola coma en un string.

    Args:
        input_string (str): Cadena de texto a procesar.

    Returns:
        str: Cadena procesada con una sola coma por separación.
    """
    if isinstance(input_string, str):
        return re.sub(r",+", ", ", input_string)
    return ""


def remove_leading_comma_space(text: str) -> str:
    """
    Elimina ', ' al inicio del texto si está presente.

    Args:
        text (str): El texto a procesar.

    Returns:
        str: El texto sin ', ' al inicio.
    """
    return re.sub(r"^, ", "", text)


def replace_dot_comma(text: str) -> str:
    """
    Reemplaza todas las ocurrencias de '.,' por ',' en el texto.

    Args:
        text (str): El texto de entrada.

    Returns:
        str: El texto modificado.
    """
    return text.replace(".,", ",")
