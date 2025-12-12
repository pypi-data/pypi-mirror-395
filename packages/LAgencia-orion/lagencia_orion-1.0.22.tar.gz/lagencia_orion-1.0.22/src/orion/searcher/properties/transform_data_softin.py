from datetime import datetime

import pandas as pd

from orion.tools import generate_slug, get_first_image


def transform_softin_for_properties(softin: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el DataFrame de propiedades de Softin en un formato estándar
    compatible con las columnas requeridas para la tabla de propiedades.

    Args:
        softin (pd.DataFrame): DataFrame original con los datos de Softin.

    Returns:
        pd.DataFrame: DataFrame transformado y adaptado con las columnas estándar.
    """
    if softin.empty:
        return softin

    column_mapping_properties = {
        "id": "id",
        "consecutivo": "code",
        "resumen": "description",
        "precio": "price",
        "clase": "property_type",
        "tipo_servicio": "management",
        "area": "area",
        "alcobas": "bedrooms",
        "banos": "bathrooms",
        "garaje": "garage",
        "imagenes": "image",
        "video": "video",
        "vlr_admon": "price_admon",
        "show_villacruz": "show_villacruz",
        "show_estrella": "show_estrella",
        "show_castillo": "show_castillo",
        "destacado": "featured",
        "edad": "age",
        "urbanizacion": "urbanization",
        "estrato": "stratum",
        "direccion": "address",
        "barrio": "neighborhood",
        "llaves_en": "keys_in",
        "fechamodificado": "modified_date",
        "latitud": "latitude",
        "longitud": "longitude",
        "ascensor": "elevator",
        "amoblado": "show_furnished",
    }

    softin = softin.rename(columns=column_mapping_properties)
    softin["image"] = softin["image"].apply(get_first_image)

    # Generacion de slug
    softin["slug"] = softin["property_type"] + "-en" + softin["management"] + "-en " + softin["neighborhood"] + "-" + softin["code"].astype(str)
    softin["slug"] = softin["slug"].apply(generate_slug)
    softin["age"] = softin["age"].apply(lambda x: (datetime.now().year - x) if pd.notnull(x) and isinstance(x, (int, float)) and x <= datetime.now().year else None)
    softin["show_mls_lagencia"] = True

    required_columns = list(column_mapping_properties.values()) + ["slug", "show_mls_lagencia", "source"]
    return softin[required_columns]
