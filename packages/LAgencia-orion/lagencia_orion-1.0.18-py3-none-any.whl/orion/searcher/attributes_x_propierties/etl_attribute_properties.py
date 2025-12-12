import json

import numpy as np
import pandas as pd
from loguru import logger

from orion.databases.db_bellatrix.repositories.query_acrecer import MLSAcrecer, QuerysMLSAcrecer
from orion.databases.db_bellatrix.repositories.querys_mls import MLS, QuerysMLS
from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi, Simi
from orion.databases.db_bellatrix.repositories.querys_softin import QuerysSoftin, Softin
from orion.databases.db_empatia.models.model_searcher import AttributeProperties
from orion.databases.db_empatia.repositories.querys_searcher import (
    QuerysAttributeProperties,
    QuerysAttributes,
)
from orion.searcher.attributes_x_propierties.chain_of_responsibility_mls import map_option as map_option_mls
from orion.searcher.attributes_x_propierties.chain_of_responsibility_simi import map_option as map_option_simi
from orion.tools import df_to_dicts, list_obj_to_df, parse_features


def transform_softin_for_attribute_properties(softin: pd.DataFrame) -> pd.DataFrame:
    if softin.empty:
        logger.info("Softin esta vacio, no hay attributes_properties que obtener")
        return pd.DataFrame()

    def has_kitchen(option: int):
        allowed_options = [1, 2, 3, 4]
        if option in allowed_options:
            return True
        return False

    def has_gas(option: int):
        allowed_options = [2]
        if option in allowed_options:
            return True
        return False

    column_mapping_attributes = {
        "id": "id",
        "alcoba_serv": "Alcoba del servicio",
        "balcon": "Balcón",
        "banosocial": "Baño social",
        "cocina": "Cocina",
        "comedor": "Comedor",
        "comedorauxiliar": "Comedor auxiliar",
        "cuartoutil": "Cuarto útil",
        "garaje_cubierto": "Garaje cubierto",
        "gas": "Gas",
        "gimnasio": "Gimnasio",
        "parqueaderocubierto": "Parqueadero cubierto",
        "piscina": "Piscina",
        "porteria": "Portería",
        "primerpiso": "Primer piso",
        "sala": "Sala",
        "sala_comedor": "Sala comedor",
        "unidad_cerrada": "Unidad cerrada",
    }

    attributes_properties = softin[column_mapping_attributes.keys()]
    attributes_properties = attributes_properties.rename(columns=column_mapping_attributes)

    attributes_properties["Cocina"] = attributes_properties["Cocina"].apply(has_kitchen)
    attributes_properties["Gas"] = attributes_properties["Gas"].apply(has_gas)

    # procesamiento para solo mantener atributos con valor
    attributes_properties = attributes_properties.replace("", None)
    attributes_properties = attributes_properties.replace(np.nan, None)
    attributes_properties = attributes_properties.replace(False, None)
    attributes_properties = attributes_properties.replace(0, None)

    # obtenemos solo los atributos que tienen valor
    records = df_to_dicts(attributes_properties)
    records_ = []
    for record in records:
        records_ += [{key: value for key, value in record.items() if value is not None}]

    # obtenemos los atributos definidos en la tabla attributes
    attributes_db = QuerysAttributes.select_all()
    attributes_properties = []

    # expandimos los atributos
    for record in records_:
        property_id = record.pop("id")
        for key, value in record.items():
            attributes_properties += [
                {
                    "attribute_id": [attribute.id for attribute in attributes_db if attribute.name == key][0],
                    "property_id": property_id,
                    # "value": value,
                }
            ]
    return pd.DataFrame(attributes_properties)


def transform_simi_for_attributes_properties(simi: pd.DataFrame) -> pd.DataFrame:
    if simi.empty:
        logger.info("Simi esta vacio, no hay attributes_properties que obtener")
        return pd.DataFrame()

    attributes_properties = simi[["id", "caracteristicasinternas", "caracteristicasexternas"]]

    attributes_properties.loc[:, "caracteristicasinternas"] = attributes_properties["caracteristicasinternas"].astype(str)
    attributes_properties.loc[:, "caracteristicasinternas"] = attributes_properties["caracteristicasinternas"].apply(lambda x: json.loads(x.replace("'", '"').replace("None", "null")))
    attributes_properties.loc[:, "caracteristicasexternas"] = attributes_properties["caracteristicasexternas"].astype(str)
    attributes_properties.loc[:, "caracteristicasexternas"] = attributes_properties["caracteristicasexternas"].apply(lambda x: json.loads(x.replace("'", '"').replace("None", "null")))
    attributes_properties_ = []

    for index, row in attributes_properties.iterrows():
        property_id = row["id"]
        attributes = row["caracteristicasinternas"]

        for attribute in attributes:
            attributes_properties_ += [{"property_id": property_id, "attribute": attribute.get("Descripcion").strip()}]

        attributes = row["caracteristicasexternas"]
        for attribute in attributes:
            attributes_properties_ += [{"property_id": property_id, "attribute": attribute.get("Descripcion").strip()}]

    attributes_properties_ = pd.DataFrame(attributes_properties_)

    if attributes_properties_.empty:
        return pd.DataFrame(columns=["property_id", "attribute_id"])

    attributes_properties_["name"] = attributes_properties_["attribute"].apply(map_option_simi)
    attributes_properties_ = attributes_properties_[attributes_properties_["name"].notnull()]

    attributes_properties_.drop_duplicates(subset=["property_id", "name"], inplace=True)
    attributes_properties_.drop(columns="attribute", axis=1, inplace=True)

    records = QuerysAttributes.select_all()
    attribute_db = list_obj_to_df(records)

    merged = attributes_properties_.merge(attribute_db, on="name", how="left")
    merged.drop(columns="name", axis=1, inplace=True)
    merged.rename(columns={"id": "attribute_id"}, inplace=True)
    return merged


def transform_mls_for_attributes_properties(mls: pd.DataFrame) -> pd.DataFrame:
    if mls.empty:
        logger.info("MLS esta vacio, no hay attributes_properties que obtener")
        return pd.DataFrame()

    mls = mls[mls["internal_features"].notnull()]
    mls.loc[:, "internal_features"] = mls["internal_features"].astype(str)
    mls.loc[:, "internal_features"] = mls["internal_features"].apply(lambda x: x.split(","))

    attributes_ = []

    for index, row in mls.iterrows():
        property_id = row["id"]
        attributes = row["internal_features"]
        for attribute in attributes:
            attributes_ += [{"property_id": property_id, "attribute": attribute.strip()}]

    attributes_properties_ = pd.DataFrame(attributes_)

    if attributes_properties_.empty:
        return pd.DataFrame(columns=["property_id", "attribute_id"])

    attributes_properties_["name"] = attributes_properties_["attribute"].apply(map_option_mls)
    attributes_properties_ = attributes_properties_[attributes_properties_["name"].notnull()]

    attributes_properties_.drop_duplicates(subset=["property_id", "name"], inplace=True)
    attributes_properties_.drop(columns="attribute", axis=1, inplace=True)

    records = QuerysAttributes.select_all()
    attribute_db = list_obj_to_df(records)

    merged = attributes_properties_.merge(attribute_db, on="name", how="left")
    merged.drop(columns="name", axis=1, inplace=True)
    merged.rename(columns={"id": "attribute_id"}, inplace=True)

    return merged


def transform_mls_acrecer_for_attributes_properties(mls_acrecer: pd.DataFrame) -> pd.DataFrame:
    if mls_acrecer.empty:
        logger.info("mls_acrecer esta vacio, no hay attributes_properties que obtener")
        return pd.DataFrame()

    # def get_attribute_bath_social(x):
    #     if isinstance(x, dict):
    #         return x.get("Baño social")
    #     elif isinstance(x, str):
    #         resp = literal_eval(x).get("Baño social")
    #         return resp.get("Baño social")
    #     else:
    #         return ""

    # attributes_properties_ = pd.DataFrame()
    # # internal features
    # # attributes_properties_[["property_id", "name"]]= mls_acrecer[["id", "householdFeatures"]].apply(lambda x:  get_attribute_bath_social(x["householdFeatures"], axis=1))
    # attributes_properties_[["property_id", "name"]] = mls_acrecer[["id", "householdFeatures"]].apply(lambda r: pd.Series([r["id"], get_attribute_bath_social(r["householdFeatures"])]), axis=1)

    # attributes_properties_["name"] = attributes_properties_["name"].apply(lambda x: str(x).lower())

    # records = QuerysAttributes.select_all()
    # attribute_db = list_obj_to_df(records)
    # attribute_db["name"] = attribute_db["name"].apply(lambda x: str(x).lower())

    # merged = attributes_properties_.merge(attribute_db, on="name", how="left")
    # merged.drop(columns="name", axis=1, inplace=True)
    # merged.rename(columns={"id": "attribute_id"}, inplace=True)

    # return merged

    # print(mls_acrecer.columns)

    # list_attributes_by_properties = []
    # for idex, row in mls_acrecer.iterrows():
    #     id_ = row["id"]
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["inCondominiumFeatures"].apply(lambda x: "Alcoba del servicio" if parse_features(x).get("availableUtilityRooms") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["rooms"].apply(lambda x: "Balcón" if parse_features(x).get("balconies") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["rooms"].apply(lambda x: "Comedor" if parse_features(x).get("comedores") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["householdFeatures"].apply(lambda x: "Baño social" if parse_features(x).get("Baño Social") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["features"].apply(lambda x: "Cocina" if parse_features(x).get("kitchenType") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["features"].apply(lambda x: "Gas" if parse_features(x).get("gasInstallation") else None)})
    #     list_attributes_by_properties.append({"property_id": id_, "name": mls_acrecer["inCondominiumFeatures"].apply(lambda x: "Parqueadero cubierto" if parse_features(x).get("coveredParkingLots") else None)})

    #     print(list_attributes_by_properties)
    #     print()

    FEATURE_SPECS = [
        ("inCondominiumFeatures", "availableUtilityRooms", "Alcoba del servicio"),
        ("rooms", "balconies", "Balcón"),
        ("rooms", "comedores", "Comedor"),
        ("householdFeatures", "Baño Social", "Baño social"),
        ("features", "kitchenType", "Cocina"),
        ("features", "gasInstallation", "Gas"),
        ("inCondominiumFeatures", "coveredParkingLots", "Parqueadero cubierto"),
    ]

    list_attributes_by_properties = []

    for _, row in mls_acrecer.iterrows():
        property_id = row["id"]
        parsed_cache = {}  # para no llamar parse_features varias veces sobre la misma columna

        for col, key, label in FEATURE_SPECS:
            if col not in parsed_cache:
                parsed_cache[col] = parse_features(row[col])

            if parsed_cache[col].get(key):
                # Solo agregamos si la condición es verdadera (nunca se guarda None)
                list_attributes_by_properties.append(
                    {
                        "property_id": property_id,
                        "name": label,
                    }
                )


    attributes_properties_ = pd.DataFrame(list_attributes_by_properties)
    if attributes_properties_.empty:
        return pd.DataFrame()

    records = QuerysAttributes.select_all()
    attribute_db = list_obj_to_df(records)
    attribute_db["name"] = attribute_db["name"].apply(lambda x: str(x))

    merged = attributes_properties_.merge(attribute_db, on="name", how="left")
    merged.drop(columns="name", axis=1, inplace=True)
    merged.rename(columns={"id": "attribute_id"}, inplace=True)
    return merged


def get_attribute_properties_to_insert(sources_attribute_properties: pd.DataFrame, db_attribute_properties: pd.DataFrame) -> pd.DataFrame:
    db_attribute_properties.drop_duplicates(subset=["property_id"], inplace=True)
    db_attribute_properties = pd.DataFrame(db_attribute_properties["property_id"])
    merged = sources_attribute_properties.merge(db_attribute_properties, on="property_id", how="outer", indicator=True)
    merged = merged[merged["_merge"] == "left_only"].drop(columns=["_merge"])

    return merged


def reload_records_in_table_attribute_properties():
    tools_softin = QuerysSoftin()
    softin = tools_softin.select_by_filter(Softin.activo == 1)
    attributes_properties_softin = transform_softin_for_attribute_properties(softin)

    tools_simi = QuerysSimi()
    simi = tools_simi.select_by_filter(Simi.activo == 1)
    attributes_properties_simi = transform_simi_for_attributes_properties(simi)

    tools_mls = QuerysMLS()
    mls = tools_mls.select_by_filter(MLS.active == 1)
    attributes_properties_mls = transform_mls_for_attributes_properties(mls)

    tools_mls_acrecer = QuerysMLSAcrecer()
    mls_acrecer = tools_mls_acrecer.select_by_filter(MLSAcrecer.activo == 1)
    attributes_properties_mls_acrecer = transform_mls_acrecer_for_attributes_properties(mls_acrecer)

    attributes_properties = pd.concat([attributes_properties_softin, attributes_properties_simi, attributes_properties_mls, attributes_properties_mls_acrecer])
    insert_records_in_table_attribute_properties(attributes_properties)


def insert_records_in_table_attribute_properties(attributes_properties: pd.DataFrame):
    if attributes_properties.empty:
        print("No hay atributos para cargar")
        return

    records = df_to_dicts(attributes_properties)
    QuerysAttributeProperties.bulk_insert(records)


def update_records_for_table_attribute_properties(attributes_properties: pd.DataFrame):
    if attributes_properties.empty:
        return
    ids = attributes_properties["property_id"].unique().tolist()
    for id_ in ids:
        QuerysAttributeProperties.delete_by_filter(AttributeProperties.property_id == id_)
        print(f"Se ha eliminado los atributos de la propiedad {id_=}")

    insert_records_in_table_attribute_properties(attributes_properties)
