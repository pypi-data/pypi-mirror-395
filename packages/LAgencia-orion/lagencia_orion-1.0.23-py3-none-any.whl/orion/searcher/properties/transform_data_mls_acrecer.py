import ast

import pandas as pd
from loguru import logger

from orion.acrecer.permitted_neighborhoods import BARRIOS
from orion.tools import generate_slug, parse_features

map_name_fields_properties_acrecer = {
    "code": "code",
    "generalDescription": "description",
    "rentValue": "price",
    "propertyType": "property_type",
    "builtArea": "area",
    "propertyImages": "image",
    "propertyVideoUrl": "video",
    "constructionYears": "age",
    "stratum": "stratum",
    "address": "address",
    "lat": "latitude",
    "lng": "longitude",
    "lastUpdate": "modified_date",
    "addedOn": "create_at",
}


def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """Transforma el DataFrame crudo de la API a la estructura interna.

    Realiza:
    - Selección y renombrado de columnas
    - Filtrado por precio mínimo
    - Normalización de identificadores y creación de campos derivados

    No modifica la lógica original, sólo añade trazabilidad.
    """

    def get_garage(value):
        feats = parse_features(value)  # lo calculas una sola vez
        for key in ("garages", "AASimpleparking", "coveredParkingLots"):
            if key in feats and feats[key] is not None:
                return feats[key]
        return None
    #AASimpleparking


    logger.info("transform_data: inicio transformacion, filas antes=%s", len(data))
    data = data.copy()
    data.rename(columns=map_name_fields_properties_acrecer, inplace=True)
    data = data[data["price"] >= 2_000_000]
    data = data[data["prefix_code"] != "494"]

    data["property_type_searcher"] = data["property_type"].copy()
    data["management"] = "Arriendo"
    data["show_livin"] = True
    data["show_rent_livin"] = True
    data["show_mls_lagencia"] = False
    data["slug"] = ""
    data["price_admon"] = ""
    data["active"] = True
    data["featured"] = ""

    data["image"] = data["image"].astype(str)
    data["image"] = data["image"].apply(lambda x: ast.literal_eval(x)[0] if ast.literal_eval(x) else None)

    # +++ Esta parte debe ser activada
    data["bedrooms"] = data["numberOfRooms"].fillna(0).astype(int)
    # data["bathrooms"] = data["rooms"].apply(lambda x: parse_features(x).get("baths"))
    # data["bathrooms"] = data["bathrooms"].fillna(0).astype(int)

    # data["elevator"] = data["inCondominiumFeatures"].apply(lambda x: parse_features(x).get("servedByElevator"))
    # data["elevator"] = data["elevator"].replace("T", True).fillna(False)

    # data["garage"] = data["householdFeatures"].apply(lambda x: parse_features(x).get("garages"))
    # data["garage"] = data["garage"].fillna(0).astype(int)

    data["neighborhood"] = data["locationData"].apply(lambda x: parse_features(x).get("neighborhood"))
    data = data[data["neighborhood"].isin(BARRIOS)]

    data["slug"] = data["property_type"] + "-en" + data["management"] + "-en " + data["neighborhood"] + "-" + data["code"].astype(str)
    data["slug"] = data["slug"].apply(generate_slug)
    #=============================================================
    # +++ Esta parte es solo temporal, debe eliminarse
    data["rooms"] = data["rooms"].fillna({})
    data["features"] = data["features"].fillna({})
    data["householdFeatures"] = data["householdFeatures"].fillna({})
    data["inCondominiumFeatures"] = data["inCondominiumFeatures"].fillna({})

    columns = ["rooms", "features", "householdFeatures", "inCondominiumFeatures"]
    data["full_features"] = {}

    for index, row in data.iterrows():
        combined_dict = {}

        for column in columns:
            if isinstance(row[column], dict):
                combined_dict.update(row[column])

        data.at[index, "full_features"] = combined_dict

    data["bathrooms"] = data["full_features"].apply(lambda x: parse_features(x).get("baths"))
    data["bathrooms"] = data["bathrooms"].fillna(0).astype(int)

    data["elevator"] = data["full_features"].apply(lambda x: parse_features(x).get("servedByElevator"))
    data["elevator"] = data["elevator"].replace("T", True).fillna(False)

    data["garage"] = data["full_features"].apply(lambda x: get_garage(x))
    data["garage"] = data["garage"].fillna(0).astype(int)

    # Elimiar hasta acá =============================================================





    data = data[
        [
            "id",
            "code",
            "description",
            "slug",
            "price",
            "property_type",
            "property_type_searcher",
            "management",
            "area",
            "bedrooms",
            "bathrooms",
            "garage",
            "elevator",
            "image",
            "video",
            "price_admon",
            "show_livin",
            "show_rent_livin",
            "show_mls_lagencia",
            "featured",
            "age",
            "stratum",
            "address",
            "neighborhood",
            "latitude",
            "longitude",
            "modified_date",
            "create_at",
            "prefix_code",
            "source",
        ]
    ]
    data.drop_duplicates(subset=["id"], inplace=True)
    logger.info("transform_data: fin transformacion, filas despues=%s", len(data))
    return data


def transform_mls_acrecer_for_properties(mls_acrecer: pd.DataFrame) -> pd.DataFrame:
    mls_acrecer = transform_data(mls_acrecer)
    return mls_acrecer
