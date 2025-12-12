from datetime import datetime
from typing import Tuple

import pandas as pd

from orion.databases.db_bellatrix.repositories.querys_mls import QuerysMLS
from orion.mls.mls import get_all_mls
from orion.tools import cut_date_str, df_to_dicts, list_obj_to_df

"""_summary_: hace un upsert a la tabla MLS dada la informacion del servidor FTP
"""


def split_by_transaction(mls_api: pd.DataFrame, mls_db: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Divide las propiedades en propiedades para insertar, actualizar y desactivar"""

    # + Si la tabla MLS esta vacia cargamos todos los registros del API de MLS
    if mls_db.empty:
        columns = mls_api.columns
        return mls_api, pd.DataFrame(columns=columns), pd.DataFrame(columns=columns), pd.DataFrame(columns=columns)

    # + Conevertir fechas string a datetime[64]
    mls_api["modification_date"] = pd.to_datetime(mls_api["modification_date"].apply(cut_date_str), errors="coerce")
    mls_db["modification_date"] = pd.to_datetime(mls_db["modification_date"].apply(cut_date_str), errors="coerce")

    # + separar la data por tipo de transacción (insert, update, delete(deactivate))
    mls_api_id = pd.DataFrame(mls_api["id"], columns=["id"])
    mls_db_id = pd.DataFrame(mls_db.loc[mls_db["active"] == False, "id"])

    # activar propiedades
    merged = mls_api_id.merge(mls_db_id, how="outer", on="id", indicator=True)
    to_activate_ids = merged.loc[merged["_merge"] == "both", "id"].copy()
    to_activate = mls_api[mls_api["id"].isin(to_activate_ids)].copy()
    if not to_activate.empty:
        to_activate.loc[:, "active"] = True

    # (insert(activate), update, delete(deactivate))
    mls_db_id = pd.DataFrame(mls_db["id"], columns=["id"])
    merged = mls_api_id.merge(mls_db_id, how="outer", on="id", indicator=True)

    # 1. Nuevos registros en mls_api_id
    to_insert_ids = merged[merged["_merge"] == "left_only"]["id"].copy()
    to_insert = mls_api[mls_api_id["id"].isin(to_insert_ids)].copy()

    # 2. Registros en mls_db_id que deben ser desactivados
    to_deactivate_ids = merged[merged["_merge"] == "right_only"]["id"].copy()
    to_deactivate = mls_db.loc[mls_db_id["id"].isin(to_deactivate_ids) & mls_db["active"] == True].copy()
    to_deactivate.loc[:, "active"] = False

    # 3. Registros en la unión (Deben ser actualizados)
    to_update_ids = merged[merged["_merge"] == "both"]["id"].copy()
    to_update_from_api = mls_api[mls_api_id["id"].isin(to_update_ids)][["id", "modification_date"]].rename(columns={"modification_date": "modification_date_api"})
    to_update_from_db = mls_db[mls_db_id["id"].isin(to_update_ids)][["id", "modification_date"]].rename(columns={"modification_date": "modification_date_db"})
    to_update_ = to_update_from_api.merge(to_update_from_db, on="id", how="inner")
    to_update_["update"] = to_update_["modification_date_api"] > to_update_["modification_date_db"]
    to_update_ids = to_update_[to_update_["update"]]["id"]
    to_update = mls_api[mls_api_id["id"].isin(to_update_ids)]

    return to_insert, to_deactivate, to_update, to_activate


def upsert_mls(to_insert: pd.DataFrame, to_deactivate: pd.DataFrame, to_update: pd.DataFrame, to_activate: pd.DataFrame):
    """Realiza operaciones de inserción, actualizacion y eliminacion(desactivar)
    sobre la tabla MLS"""

    to_insert = to_insert.copy()
    to_deactivate = to_deactivate.copy()
    to_update = to_update.copy()

    to_insert["modification_date"] = to_insert["modification_date"].astype(str)
    to_deactivate["modification_date"] = to_deactivate["modification_date"].astype(str)
    to_update["modification_date"] = to_update["modification_date"].astype(str)
    to_activate["modification_date"] = to_activate["modification_date"].astype(str)
    to_insert = to_insert.replace("NaT", None)
    to_deactivate = to_deactivate.replace("NaT", None)
    to_update = to_update.replace("NaT", None)
    to_activate = to_activate.replace("NaT", None)

    date_insertion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # + *transacciones
    # insertar nuevas propiedades
    if not to_insert.empty:
        to_insert.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_insert)
        # Querysmls.insert_all(records)
        QuerysMLS.bulk_insert(records)

    # desactivar propiedades
    if not to_deactivate.empty:
        to_deactivate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_deactivate)
        for record in records:
            QuerysMLS.update_by_id(record, record.get("id"))

    # actualizar propiedades
    if not to_update.empty:
        to_update.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_update)
        for record in records:
            QuerysMLS.update_by_id(record, record.get("id"))

    # activar propiedades
    if not to_activate.empty:
        to_activate.loc[:, "date_insertion"] = date_insertion
        records = df_to_dicts(to_activate)
        for record in records:
            QuerysMLS.update_by_id(record, record.get("id"))


def etl():
    """Mantiene la tabla de mls actualizada"""

    mls_api = get_all_mls()
    #mls_api.to_excel("mls_api.xlsx", index=False)

    # + Consultar MLS de base de datos
    records = QuerysMLS.select_all()
    mls_db = list_obj_to_df(records)

    to_insert, to_deactivate, to_update, to_activate = split_by_transaction(mls_api, mls_db)

    upsert_mls(to_insert, to_deactivate, to_update, to_activate)

    if not mls_db.empty:
        print("\nRegistros DB activo:")
        print(mls_db[mls_db["active"] == 1].shape)

        print("\nRegistros DB inactivo:")
        print(mls_db[mls_db["active"] == 0].shape)

    print("\nRegistros API:")
    print(mls_api.shape)

    print("\nRegistros para insertar:")
    print(to_insert.shape)

    print("\nRegistros para activar:")
    print(to_activate.shape)

    print("\nRegistros para desactivar:")
    print(to_deactivate.shape)

    print("\nRegistros para actualizar:")
    print(to_update.shape)
