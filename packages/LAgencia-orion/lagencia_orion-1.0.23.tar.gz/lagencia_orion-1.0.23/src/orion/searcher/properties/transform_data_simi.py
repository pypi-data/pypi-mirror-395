import json
from datetime import datetime
from typing import Dict, List

import pandas as pd

from orion.tools import generate_slug


def search_elevator_simi(data_str: str) -> Dict[str, int]:
    """
    Busca 'Ascensor' en el campo 'Descripcion' y retorna su cantidad.

    Args:
        data_str (str): String con una lista de diccionarios en formato JSON.

    Returns:
        int: cantidad.
    """
    if not data_str:
        return False

    data_str = data_str.strip()
    try:
        # Convertir el string JSON en una lista de diccionarios
        data: List[Dict] = json.loads(data_str.replace("'", '"').replace("None", "null"))

        # Buscar el diccionario con 'Ascensor' en el campo 'Descripcion'
        for item in data:
            if "Ascensor" in item.get("Descripcion", ""):
                return True

        # Si no se encuentra 'Ascensor', retornar un mensaje vacío
        return False

    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON: {e}")
        return {"Descripcion": "Error", "cantidad": 0}


def transform_simi_for_properties(simi: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el DataFrame de propiedades de Simi en un formato estándar
    compatible con las columnas requeridas para la tabla de propiedades.

    Args:
        simi (pd.DataFrame): DataFrame original con los datos de Simi.

    Returns:
        pd.DataFrame: DataFrame transformado y adaptado con las columnas estándar.||
    """
    if simi.empty:
        return simi

    column_mapping_properties = {
        "id": "id",
        "codinm": "code",
        "descripcionst": "description",
        "precio": "price",
        "tipo_inmueble": "property_type",
        "gestion": "management",
        "arealote": "area",
        "alcobas": "bedrooms",
        "banos": "bathrooms",
        "garaje": "garage",
        "fotos": "image",
        "video": "video",
        "administracion": "price_admon",
        "show_livin": "show_livin",
        "descestado": "featured",
        "edadinmueble": "age",
        "estrato": "stratum",
        "direccion": "address",
        "barrio": "neighborhood",
        "fecha_modificacion": "modified_date",
        "latitud": "latitude",
        "longitud": "longitude",
        "amoblado": "show_furnished",
    }

    simi.rename(columns=column_mapping_properties, inplace=True)

    simi["image"] = simi["image"].astype(str)
    simi["image"] = simi["image"].apply(lambda x: json.loads(x.replace("'", '"').replace("None", "null")))
    simi["image"] = simi["image"].apply(lambda x: x[0].get("foto") if x else None)

    simi["slug"] = simi["property_type"] + "-en " + simi["management"] + "-en " + simi["neighborhood"] + "-" + simi["code"].astype(str)
    simi["slug"] = simi["slug"].apply(generate_slug)

    simi["elevator"] = simi["caracteristicasexternas"].apply(search_elevator_simi)
    simi["age"] = simi["age"].apply(lambda x: (datetime.now().year - x) if pd.notnull(x) and isinstance(x, (int, float)) and x <= datetime.now().year else None)
    simi["show_mls_lagencia"] = True

    required_columns = list(column_mapping_properties.values()) + ["slug", "elevator", "show_mls_lagencia", "source"]

    return simi[required_columns]
