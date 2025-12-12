import ast
import json

import pandas as pd

from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi
from orion.databases.db_empatia.models.model_searcher import GalleryProperties
from orion.databases.db_empatia.repositories.querys_searcher import (
    QuerysGalleryProperties,
    QuerysProperty,
)
from orion.tools import df_to_dicts, list_obj_to_df


def transform_softin_for_gallery_propierties(softin: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos de Softin en un formato adecuado para la tabla
    gallery_properties.

    Args:
        softin (pd.DataFrame): DataFrame con datos de Softin, incluyendo las columnas
        'id' e 'imagenes'.

    Returns:
        pd.DataFrame: DataFrame transformado con columnas 'property_id' e 'image',
                      donde cada fila corresponde a una imagen asociada a una propiedad.
    """

    if softin.empty:
        return pd.DataFrame(columns=["property_id", "image"])

    gallery = softin[["id", "imagenes"]].copy()

    gallery["imagenes"] = gallery["imagenes"].apply(lambda x: json.loads(x.replace("'", '"').replace("None", "null")))

    gallery_ = []
    for index, row in gallery.iterrows():
        for image in row["imagenes"]:
            gallery_ += [{"property_id": row["id"], "image": image.get("fotourl")}]

    return pd.DataFrame(gallery_)


def transform_simi_for_gallery_propierties(simi: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma los datos de Simi en un formato adecuado para la tabla
    gallery_properties.

    Args:
        simi (pd.DataFrame): DataFrame con datos de Simi, incluyendo las columnas
        'id' y 'fotos'.

    Returns:
        pd.DataFrame: DataFrame transformado con columnas 'property_id' e 'image',
                      donde cada fila corresponde a una imagen asociada a una propiedad.
    """
    if simi.empty:
        return pd.DataFrame(columns=["property_id", "image"])

    gallery = simi[["id", "fotos"]].copy()

    gallery["fotos"] = gallery["fotos"].apply(lambda x: json.loads(x.replace("'", '"').replace("None", "null")))

    gallery_ = []
    for index, row in gallery.iterrows():
        for image in row["fotos"]:
            gallery_ += [{"property_id": row["id"], "image": image.get("foto")}]

    gallery = pd.DataFrame(gallery_)
    return gallery


def transform_mls_for_gallery_propierties(mls: pd.DataFrame) -> pd.DataFrame:
    if mls.empty:
        return pd.DataFrame(columns=["property_id", "image"])

    mls = mls[mls["listing_photo_count"].notnull()]
    imagenes = []
    for index, row in mls.iterrows():
        unique_id = row["unique_id"]
        quantity = int(row["listing_photo_count"])
        for n in range(1, quantity + 1):
            if n < 10:
                url = f"http://images.realtyserver.com/photo_server.php?btnSubmit=GetPhoto&board=colombia&failover=clear.gif&name={unique_id}.L0{n}"
            else:
                url = f"http://images.realtyserver.com/photo_server.php?btnSubmit=GetPhoto&board=colombia&failover=clear.gif&name={unique_id}.L{n}"

            imagenes.extend([{"property_id": row["id"], "image": url}])

    imagenes = pd.DataFrame(imagenes)
    return imagenes


def transform_mls_acrecer_for_gallery_propertirs(mls_acrecer: pd.DataFrame) -> pd.DataFrame:
    if mls_acrecer.empty:
        return pd.DataFrame(columns=["property_id", "image"])

    mls_acrecer["image"] = mls_acrecer["propertyImages"].apply(lambda x: ast.literal_eval(x) if ast.literal_eval(x) else None)
    gallery = mls_acrecer[["id", "image"]].copy()

    gallery_ = []
    for index, row in gallery.iterrows():
        for image in row["image"]:
            gallery_ += [{"property_id": row["id"], "image": image}]

    gallery = pd.DataFrame(gallery_)

    return gallery


def get_gallery_properties_insert(gallery_source: pd.DataFrame, gallery_db: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica los registros de imágenes que necesitan ser insertados en la tabla
    gallery_properties.

    Args:
        gallery_source (pd.DataFrame): DataFrame con las imágenes actuales (fuente).
        gallery_db (pd.DataFrame): DataFrame con las imágenes existentes en la
        base de datos.

    Returns:
        pd.DataFrame: DataFrame con los nuevos registros de imágenes que deben
        ser insertados.
    """
    all_gallery = gallery_source.copy()
    gallery_db.drop_duplicates(subset=["property_id"], inplace=True)
    gallery_source.drop_duplicates(subset=["property_id"], inplace=True)

    merged = gallery_source.merge(gallery_db, on="property_id", how="outer", indicator=True)

    to_insert_ids = merged[merged["_merge"] == "left_only"]["property_id"]
    new_gallery = all_gallery[all_gallery["property_id"].isin(to_insert_ids)]
    print(
        "por insertar: ",
        to_insert_ids.shape,
        "propiedades con: ",
        new_gallery.shape,
        "imagenes",
    )
    return new_gallery


def delay_to_update_gallery():
    records = QuerysSimi.select_all()
    simi = list_obj_to_df(records)
    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)
    records = QuerysGalleryProperties.select_all()
    gallery = list_obj_to_df(records)
    if gallery.empty:
        return

    print("Propiedades sin fotos")
    without = properties[~properties["id"].isin(gallery["property_id"])].copy()
    if not without.empty:
        without.loc[:, "modified_date"] = without["modified_date"] - pd.Timedelta(minutes=30)

        simi_ = simi[simi["id"].isin(without["id"])].copy()
        if not simi_.empty:
            simi_.loc[:, "fecha_modificacion"] = simi_["fecha_modificacion"] - pd.Timedelta(minutes=30)

        records = df_to_dicts(without)
        for record in records:
            print(record.get("id"))
            QuerysProperty.update_by_id(record, record.get("id"))

        records = df_to_dicts(simi_)
        for record in records:
            print(record.get("id"))
            QuerysSimi.update_by_id(record, record.get("id"))

    print("Propiedades con solo una foto")
    image_counts = gallery.groupby("property_id").size().reset_index(name="image_count")
    filtered_gallery = image_counts[image_counts["image_count"] < 2]

    without = properties[properties["id"].isin(filtered_gallery["property_id"])].copy()
    if not without.empty:
        without.loc[:, "modified_date"] = without["modified_date"] - pd.Timedelta(minutes=30)
        records = df_to_dicts(without)
        for record in records:
            print(record.get("id"))
            QuerysProperty.update_by_id(record, record.get("id"))

    simi_ = simi[simi["id"].isin(filtered_gallery["property_id"])]
    if not simi_.empty:
        simi_.loc[:, "fecha_modificacion"] = simi_["fecha_modificacion"] - pd.Timedelta(minutes=30)
        records = df_to_dicts(simi_)
        for record in records:
            print(record.get("id"))
            QuerysSimi.update_by_id(record, record.get("id"))


def insert_records_in_table_gallery_properties(all_gallery: pd.DataFrame):
    """inserta en la tabla galeria las url de las imagenes de cada pripiedad

    Args:
        all_gallery (pd.DataFrame): df con la estructura de la tabla gallery
    """
    if all_gallery.empty:
        print("No hay urls de galeria para cargar")
        return

    records = df_to_dicts(all_gallery)
    QuerysGalleryProperties.bulk_insert(records)


def update_records_for_table_gallery_properties(gallery: pd.DataFrame):
    if gallery.empty:
        return True
    ids = gallery["property_id"].unique().tolist()
    for id_ in ids:
        QuerysGalleryProperties.delete_by_filter(GalleryProperties.property_id == id_)
        print(f"Se ha eliminado la galeria de la propiedad {id_=}")

    insert_records_in_table_gallery_properties(gallery)
    return True
