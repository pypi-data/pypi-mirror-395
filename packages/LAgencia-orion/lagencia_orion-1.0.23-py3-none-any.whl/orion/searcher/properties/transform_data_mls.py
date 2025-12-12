from datetime import datetime

import pandas as pd

from orion.tools import generate_slug


def transform_mls_for_properties(mls: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el DataFrame de propiedades de MLS en un formato estándar
    compatible con las columnas requeridas para la tabla de propiedades.

    Args:
        mls (pd.DataFrame): DataFrame original con los datos de MLS.

    Returns:
        pd.DataFrame: DataFrame transformado y adaptado con las columnas estándar.
    """

    if mls.empty:
        return mls

    column_mapping_properties = {
        "id": "id",
        "code": "code",
        "remarks_es": "description",
        "price_current": "price",
        "property_type": "property_type",
        "management": "management",
        # "closed_area": "area", #sqft_total, lot_sqft 6396
        "bedrooms": "bedrooms",
        "bathrooms": "bathrooms",
        "image": "image",
        # video
        # "vlr_admon": "price_admon",
        "show_livin": "show_livin",
        "show_castillo": "show_castillo",
        "show_villacruz": "show_villacruz",
        "show_estrella": "show_estrella",
        # "destacado": "featured",
        "year_built": "age",
        "region": "urbanization",
        # "estrato": "stratum",
        "street_name_es": "address",
        "district": "neighborhood",
        # "llaves_en": "keys_in",
        "modification_date": "modified_date",
        "date_listed": "created_at",
        "latitude": "latitude",
        "longitude": "longitude",
        "parking_spaces": "garage",
    }

    mls = mls.rename(columns=column_mapping_properties)
    # mls["image"] = mls["image"].apply(get_first_image)
    mls["management"] = "Venta"

    # Generacion de slug
    mls["slug"] = mls["property_type"] + "-en " + mls["management"] + "-en " + mls["neighborhood"] + "-" + mls["code"].astype(str)

    mls["slug"] = mls["slug"].apply(generate_slug)

    mls["area"] = mls.apply(lambda x: x["sqft_total"] if pd.notnull(x["sqft_total"]) and x["sqft_total"] else x["lot_sqft"], axis=1)
    mls["age"] = mls["age"].apply(lambda x: x if pd.notnull(x) and isinstance(x, (int, float)) and x > 1000 else ((datetime.now().year - x) if isinstance(x, (int, float)) and x <= datetime.now().year else None))
    mls["show_mls_lagencia"] = True

    mls["show_sale_livin"]= mls["show_livin"]==1
    mls["show_sale_estrella"]= mls["show_estrella"]==1
    mls["show_sale_castillo"]= mls["show_castillo"]==1
    mls["show_sale_villacruz"]= mls["show_villacruz"]==1

    required_columns = list(column_mapping_properties.values()) + ["slug", "area", "show_mls_lagencia", "source", "show_sale_livin", "show_sale_estrella", "show_sale_castillo", "show_sale_villacruz"]

    return mls[required_columns]
