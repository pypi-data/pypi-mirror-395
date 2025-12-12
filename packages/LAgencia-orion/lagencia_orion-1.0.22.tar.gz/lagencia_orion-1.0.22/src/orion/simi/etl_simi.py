import asyncio
import os
from datetime import datetime
from typing import Tuple

import pandas as pd

from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi
from orion.simi.simi import get_all_simi
from orion.tools import cut_date_str, df_to_dicts, list_obj_to_df

"""_summary_: hace un upsert a la tabla Simi dada la informacion del API Simi
"""


def split_by_transaction(simi_api: pd.DataFrame, simi_db: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Divide las propiedades en propiedades para insertar, actualizar y desactivar"""
    path_save = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "simi")

    # + Si la tabla MLS esta vacia cargamos todos los registros del API de MLS
    if simi_db.empty:
        columns = simi_api.columns
        return simi_api, pd.DataFrame(columns=columns), pd.DataFrame(columns=columns), pd.DataFrame(columns=columns)

    # + Conevertir fechas string a datetime[64]

    simi_api["fecha_modificacion"] = pd.to_datetime(simi_api["fecha_modificacion"].apply(cut_date_str), errors="coerce")
    simi_db["fecha_modificacion"] = pd.to_datetime(simi_db["fecha_modificacion"].apply(cut_date_str), errors="coerce")

    # + separar la data por tipo de transacción (insert(activate), update, delete(deactivate), activate)
    simi_api_id = pd.DataFrame(simi_api["id"], columns=["id"])
    simi_db_id = pd.DataFrame(simi_db.loc[simi_db["activo"] == False, "id"], columns=["id"])

    # # activar propiedades
    merged = simi_api_id.merge(simi_db_id, how="outer", on="id", indicator=True)
    to_activate_ids = merged.loc[merged["_merge"] == "both", "id"].copy()
    to_activate = simi_api[simi_api["id"].isin(to_activate_ids)].copy()
    if not to_activate.empty:
        to_activate.loc[:, "activo"] = True

    # (insert(activate), update, delete(deactivate))
    simi_db_id = pd.DataFrame(simi_db["id"], columns=["id"])
    merged = simi_api_id.merge(simi_db_id, how="outer", on="id", indicator=True)
    # merged.to_excel(os.path.join(path_save, "merged.xlsx"), index=False)

    # 1. Nuevos registros en  para insertar
    to_insert_ids = merged[merged["_merge"] == "left_only"]["id"]
    to_insert = simi_api[simi_api_id["id"].isin(to_insert_ids)]

    # 2. Registros en simi_db_id que deben ser desactivados
    to_deactivate_ids = merged[merged["_merge"] == "right_only"]["id"]
    to_deactivate = simi_db.loc[simi_db_id["id"].isin(to_deactivate_ids) & simi_db["activo"] == True]
    to_deactivate.loc[:, "activo"] = False

    # 3. Registros en la unión (Deben ser actualizados)
    to_update_ids = merged[merged["_merge"] == "both"]["id"].copy()
    to_update_from_api = simi_api[simi_api_id["id"].isin(to_update_ids)][["id", "fecha_modificacion"]].rename(columns={"fecha_modificacion": "fecha_modificacion_api"})
    to_update_from_db = simi_db[simi_db_id["id"].isin(to_update_ids)][["id", "fecha_modificacion"]].rename(columns={"fecha_modificacion": "fecha_modificacion_db"})
    to_update_ = to_update_from_api.merge(to_update_from_db, on="id", how="inner")
    to_update_["update"] = to_update_["fecha_modificacion_api"] > to_update_["fecha_modificacion_db"]
    to_update_ids = to_update_[to_update_["update"]]["id"]
    to_update = simi_api[simi_api_id["id"].isin(to_update_ids)]

    return to_insert, to_deactivate, to_update, to_activate


def upsert_simi(to_insert: pd.DataFrame, to_deactivate: pd.DataFrame, to_update: pd.DataFrame, to_activate: pd.DataFrame):
    """Realiza operaciones de inserción, actualizacion y eliminacion(desactivar)
    sobre la tabla Simi"""

    to_insert = to_insert.copy()
    to_deactivate = to_deactivate.copy()
    to_update = to_update.copy()

    to_insert["fecha_modificacion"] = to_insert["fecha_modificacion"].astype(str)
    to_deactivate["fecha_modificacion"] = to_deactivate["fecha_modificacion"].astype(str)
    to_update["fecha_modificacion"] = to_update["fecha_modificacion"].astype(str)
    to_activate["fecha_modificacion"] = to_activate["fecha_modificacion"].astype(str)
    to_insert = to_insert.replace("NaT", None)
    to_deactivate = to_deactivate.replace("NaT", None)
    to_update = to_update.replace("NaT", None)
    to_activate = to_activate.replace("NaT", None)

    date_insertion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # + transacciones
    # insertar nuevas propiedades
    if not to_insert.empty:
        to_insert.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_insert)
        # QuerysSimi.insert_all(records)
        QuerysSimi.bulk_insert(records)

    # desactivar propiedades
    if not to_deactivate.empty:
        to_deactivate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_deactivate)
        for record in records:
            QuerysSimi.update_by_id(record, record.get("id"))

    # actualizar propiedades
    if not to_update.empty:
        print("Actualizando inmuebles simi")
        to_update.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_update)
        for record in records:
            QuerysSimi.update_by_id(record, record.get("id"))
            # print(record)
            # print()

    # activar propiedades
    if not to_activate.empty:
        to_activate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_activate)
        for record in records:
            QuerysSimi.update_by_id(record, record.get("id"))


def etl():
    """Mantiene la tabla de Simi actualizada"""
    path_save = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "simi")

    simi_api = asyncio.run(get_all_simi())
    # simi_api.to_excel(os.path.join(path_save, "simi_api.xlsx"), index=False)

    records = QuerysSimi.select_all()
    simi_db = list_obj_to_df(records)
    # simi_db.to_excel(os.path.join(path_save, "simi_db.xlsx"), index=False)

    to_insert, to_deactivate, to_update, to_activate = split_by_transaction(simi_api, simi_db)

    # to_insert.to_excel(os.path.join(path_save, "por_insertar.xlsx"), index=False)
    # to_deactivate.to_excel(os.path.join(path_save, "por_desactivar.xlsx"), index=False)
    # to_update.to_excel(os.path.join(path_save, "por_actualizar.xlsx"), index=False)
    # to_activate.to_excel(os.path.join(path_save, "por_activar.xlsx"), index=False)

    upsert_simi(to_insert, to_deactivate, to_update, to_activate)

    if not simi_db.empty:
        print("\nRegistros DB activo:")
        print(simi_db[simi_db["activo"] == True].shape)

        print("\nRegistros DB inactivo:")
        print(simi_db[simi_db["activo"] == False].shape)

    print("\nRegistros API:")
    print(simi_api.shape)

    print("\nRegistros para insertar:")
    print(to_insert.shape)

    print("\nRegistros para activar:")
    print(to_activate.shape)

    print("\nRegistros para desactivar:")
    print(to_deactivate.shape)

    print("\nRegistros para actualizar:")
    print(to_update.shape)
