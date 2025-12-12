import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pandas as pd

from orion.databases.db_bellatrix.repositories.querys_softin import QuerysSoftin
from orion.softin.softin import get_all_softin
from orion.tools import convert_iso_to_datetime, df_to_dicts, list_obj_to_df

"""_summary_: hace un upsert a la tabla softin dada la informacion del API softin
"""
# path_save = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "softin")

path_save = Path(__file__).resolve().parent / "outputs" / "softin"


def split_by_transaction(softin_api: pd.DataFrame, softin_db: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Divide las propiedades en propiedades para insertar, actualizar y desactivar"""
    path_save = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "softin")

    # + Si la tabla Softin esta vacia cargamos todos los registros del API de Softin
    if softin_db.empty:
        columns = softin_api.columns
        return softin_api, pd.DataFrame(columns=columns), pd.DataFrame(columns=columns), pd.DataFrame(columns=columns)

    # + Conevertir fechas string a datetime[64]
    softin_api["fechamodificado"] = pd.to_datetime(softin_api["fechamodificado"].apply(convert_iso_to_datetime), errors="coerce")
    softin_db["fechamodificado"] = pd.to_datetime(softin_db["fechamodificado"].apply(convert_iso_to_datetime), errors="coerce")

    # + division por tipo de transacción y procesamiento
    softin_api_id = pd.DataFrame(softin_api["id"], columns=["id"])
    softin_db_id = pd.DataFrame(softin_db.loc[softin_db["activo"] == False, "id"], columns=["id"])

    # # activar propiedades
    merged = softin_api_id.merge(softin_db_id, how="outer", on="id", indicator=True)
    to_activate_ids = merged.loc[merged["_merge"] == "both", "id"].copy()
    to_activate = softin_api[softin_api["id"].isin(to_activate_ids)].copy()
    if not to_activate.empty:
        to_activate.loc[:, "activo"] = True

    # (insert(activate), update, delete(deactivate))
    softin_db_id = pd.DataFrame(softin_db["id"], columns=["id"])
    merged = softin_api_id.merge(softin_db_id, how="outer", on="id", indicator=True)
    # merged.to_excel(os.path.join(path_save, "merged.xlsx"), index=False)

    # 1. Nuevos registros en softin_api_id
    to_insert_ids = merged[merged["_merge"] == "left_only"]["id"]
    to_insert = softin_api[softin_api_id["id"].isin(to_insert_ids)]

    # 2. Registros en softin_db_id que deben ser desactivados
    to_deactivate_ids = merged[merged["_merge"] == "right_only"]["id"]
    to_deactivate = softin_db.loc[softin_db_id["id"].isin(to_deactivate_ids) & softin_db["activo"] == True]
    to_deactivate.loc[:, "activo"] = False

    # 3. Registros en la unión (Deben ser actualizados)
    to_update_ids = merged[merged["_merge"] == "both"]["id"].copy()
    to_update_from_api = softin_api[softin_api_id["id"].isin(to_update_ids)][["id", "fechamodificado"]].rename(columns={"fechamodificado": "fechamodificado_api"})
    to_update_from_db = softin_db[softin_db_id["id"].isin(to_update_ids)][["id", "fechamodificado"]].rename(columns={"fechamodificado": "fechamodificado_db"})
    to_update_ = to_update_from_api.merge(to_update_from_db, on="id", how="inner")
    to_update_["update"] = to_update_["fechamodificado_api"] > to_update_["fechamodificado_db"]
    to_update_ids = to_update_[to_update_["update"]]["id"]
    to_update = softin_api[softin_api_id["id"].isin(to_update_ids)]

    return to_insert, to_deactivate, to_update, to_activate


def upsert_softin(to_insert: pd.DataFrame, to_deactivate: pd.DataFrame, to_update: pd.DataFrame, to_activate: pd.DataFrame):
    """Realiza operaciones de inserción, actualizacion y eliminacion(desactivar)
    sobre la tabla Softin"""

    to_insert = to_insert.copy()
    to_deactivate = to_deactivate.copy()
    to_update = to_update.copy()

    to_insert["fechamodificado"] = to_insert["fechamodificado"].astype(str)
    to_deactivate["fechamodificado"] = to_deactivate["fechamodificado"].astype(str)
    to_update["fechamodificado"] = to_update["fechamodificado"].astype(str)
    to_activate["fechamodificado"] = to_activate["fechamodificado"].astype(str)
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
        # QuerysSoftin.insert_all(records)
        QuerysSoftin.bulk_insert(records)

    # desactivar propiedades
    if not to_deactivate.empty:
        to_deactivate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_deactivate)
        for record in records:
            QuerysSoftin.update_by_id(record, record.get("id"))

    # actualizar propiedades
    if not to_update.empty:
        to_update.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_update)
        for record in records:
            QuerysSoftin.update_by_id(record, record.get("id"))

    # activar propiedades
    if not to_activate.empty:
        to_activate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_activate)
        for record in records:
            QuerysSoftin.update_by_id(record, record.get("id"))


def etl():
    """Mantiene la tabla de softin actualizada"""
    # softin_api = get_all_softin()
    softin_api = asyncio.run(get_all_softin())
    records = QuerysSoftin.select_all()
    softin_db = list_obj_to_df(records)

    to_insert, to_deactivate, to_update, to_activate = split_by_transaction(softin_api, softin_db)

    # to_insert.to_excel(os.path.join(path_save, "por_insertar.xlsx"), index=False)
    # to_deactivate.to_excel(os.path.join(path_save, "por_desactivar.xlsx"), index=False)
    # to_update.to_excel(os.path.join(path_save, "por_actualizar.xlsx"), index=False)
    # to_activate.to_excel(os.path.join(path_save, "por_activar.xlsx"), index=False)

    upsert_softin(to_insert, to_deactivate, to_update, to_activate)

    if not softin_db.empty:
        print("\nRegistros DB activo:")
        print(softin_db[softin_db["activo"] == True].shape)

        print("\nRegistros DB inactivo:")
        print(softin_db[softin_db["activo"] == False].shape)

    print("\nRegistros API:")
    print(softin_api.shape)

    print("\nNuevos registros para insertar:")
    print(to_insert.shape)

    print("\nRegistros para activar:")
    print(to_activate.shape)

    print("\nRegistros para desactivar:")
    print(to_deactivate.shape)

    print("\nRegistros para actualizar:")
    print(to_update.shape)
