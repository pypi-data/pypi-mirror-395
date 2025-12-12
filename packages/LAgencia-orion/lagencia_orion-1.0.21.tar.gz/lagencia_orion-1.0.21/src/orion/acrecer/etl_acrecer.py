from datetime import datetime, timezone
from typing import List

import pandas as pd
from loguru import logger

from orion.acrecer.acrecer import get_all_properties_acrecer_by_city_sync
from orion.databases.config_db_bellatrix import get_session_bellatrix
from orion.databases.db_bellatrix.models.model_acrecer import MLSAcrecer
from orion.databases.db_bellatrix.repositories.query_acrecer import QuerysMLSAcrecer
from orion.definition_ids import ID_BASE_MLS_ACRECER
from orion.tools import df_to_dicts, list_obj_to_df

"""Módulo ETL para el servicio MLS Acrecer.

Este módulo contiene el proceso completo de Extracción, Transformación y Carga (ETL)
para los datos de propiedades provenientes de la API de MLS Acrecer.

El flujo principal (`load_data_for_table_acrecer`) se encarga de:
1.  **Extraer**: Obtener todas las propiedades de la API.
2.  **Transformar**: Limpiar y formatear los datos, generando un ID único y
    ajustando campos como fechas y códigos.
3.  **Cargar**: Comparar los datos nuevos con los existentes en la base de datos
    para determinar qué registros insertar, actualizar o marcar como inactivos.
    Finalmente, aplica estos cambios en la base de datos.
"""




def format_dates(date: str) -> str:
    """Formatea una fecha en formato ISO a 'YYYY-MM-DD HH:MM:SS'.

    Nota:
        Esta función parece no estar en uso actualmente en el flujo principal.

    Parameters
    ----------
    date : str
        Fecha en formato string (ej. '2023-10-26T10:00:00Z').

    Returns
    -------
    str
        Fecha formateada como 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromisoformat(date.replace("T", " ")).date().strftime("%Y-%m-%d %H:%M:%S")


def to_mysql_dt(s: str) -> datetime | None:
    """Convierte una cadena de fecha ISO 8601 a un objeto datetime compatible con MySQL.

    La función maneja el indicador de zona horaria 'Z' (UTC), convierte la fecha a UTC
    y luego la devuelve como un objeto `datetime` "naive" (sin información de zona horaria),
    que es el formato esperado por las columnas DATETIME de MySQL.

    Parameters
    ----------
    s : str
        La cadena de fecha en formato ISO 8601.

    Returns
    -------
    datetime | None
        Un objeto `datetime` naive en UTC, o `None` si la entrada es nula o vacía.
    """
    if s is None or str(s).strip() == "":
        return None
    # Interpreta el string como ISO, tratando 'Z' como UTC (+00:00)
    dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    # Convierte a UTC y elimina la información de tzinfo para compatibilidad con MySQL
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


def load_data_for_table_acrecer():
    """
    Proceso ETL completo para sincronizar propiedades de MLS Acrecer con la base de datos.

    Extrae propiedades de la API, las transforma a un formato estándar y las carga
    en la tabla `mls_acrecer`, gestionando inserciones, actualizaciones y eliminaciones.
    """
    logger.info("load_data_for_table_acrecer: inicio")

    # 1. EXTRACCIÓN: Obtener datos de la API de Acrecer.
    new_data_acrecer = get_all_properties_acrecer_by_city_sync()
    if new_data_acrecer is None or new_data_acrecer.empty:
        logger.warning("load_data_for_table_acrecer: no se obtuvo nueva data, abortando carga")
        return

    # 2. TRANSFORMACIÓN: Limpieza y preparación de los datos.
    # Separar el prefijo y el código numérico de la propiedad.
    new_data_acrecer["prefix_code"] = new_data_acrecer["code"].apply(lambda x: str(x).split("-")[0] if "-" in str(x) else None)
    new_data_acrecer["code"] = new_data_acrecer["code"].apply(lambda x: str(x).split("-")[1] if "-" in str(x) else x)
    new_data_acrecer["ciudad"]= new_data_acrecer["ciudad"].apply(lambda x: x.get("city") if isinstance(x, dict) else None)

    # Generar un ID único sumando una base al código numérico.
    new_data_acrecer["id"] = new_data_acrecer["code"].astype(int).copy()
    new_data_acrecer["id"] = new_data_acrecer["id"] + ID_BASE_MLS_ACRECER

    # Estandarizar tipos de datos y añadir metadatos.
    new_data_acrecer["propertyImages"] = new_data_acrecer["propertyImages"].astype(str)
    new_data_acrecer["active"] = True
    new_data_acrecer["source"] = "mls_acrecer"
    new_data_acrecer.drop_duplicates(subset=["id"], inplace=True)
    new_data_acrecer = new_data_acrecer[new_data_acrecer["id"].notnull()]

    # Formatear columnas de fecha para compatibilidad con la base de datos.
    new_data_acrecer["addedOn"] = new_data_acrecer["addedOn"].map(to_mysql_dt)
    new_data_acrecer["lastUpdate"] = new_data_acrecer["lastUpdate"].map(to_mysql_dt)

    new_data_acrecer_t = new_data_acrecer.copy()

    # 3. CARGA: Comparar con datos existentes y aplicar cambios.
    # Obtener los registros activos actuales de la base de datos.
    with get_session_bellatrix() as session:
        result: List[MLSAcrecer] = session.query(MLSAcrecer).where(MLSAcrecer.active == 1).all()
        table_acrecer = list_obj_to_df(result)

    # Si hay datos tanto de la API como de la BD, se calcula el delta.
    if not table_acrecer.empty and not new_data_acrecer_t.empty:
        # Se realiza un "outer join" para encontrar registros que están en una fuente pero no en la otra.
        # `indicator=True` añade la columna `_merge` que indica la fuente de cada fila.
        merge = table_acrecer.merge(new_data_acrecer_t, on="id", how="outer", suffixes=("_db", "_api"), indicator=True)

        # Normalizar columnas de fecha para una comparación correcta.
        date_cols = ["lastUpdate_db", "lastUpdate_api", "addedOn_db", "addedOn_api"]
        for col in date_cols:
            merge.loc[:, col] = pd.to_datetime(merge[col], errors="coerce").dt.tz_localize(None)

        # --- Identificar registros para ACTUALIZAR ---
        # Son los que existen en ambas fuentes (`_merge` == 'both').
        merge_inner = merge[merge["_merge"] == "both"]
        # Se actualiza si la fecha `lastUpdate` de la API es más reciente que la de la BD.
        ids_by_update = merge_inner.loc[merge_inner["lastUpdate_api"] > merge_inner["lastUpdate_db"], "id"]
        merge_update = new_data_acrecer_t[new_data_acrecer_t["id"].isin(set(ids_by_update))]

        # --- Identificar registros para ELIMINAR (marcar como inactivos) ---
        # Son los que solo existen en la base de datos (`_merge` == 'left_only').
        # Esto significa que ya no vienen de la API.
        merge_left_only = merge[merge["_merge"] == "left_only"]
        ids_by_delete = merge_left_only["id"]
        merge_delete = table_acrecer[table_acrecer["id"].isin(ids_by_delete.to_list())]

        # --- Identificar registros para INSERTAR ---
        # Son los que solo existen en la API (`_merge` == 'right_only').
        merge_right_only = merge[merge["_merge"] == "right_only"]
        ids_by_insert = merge_right_only["id"]
        merge_insert = new_data_acrecer_t[new_data_acrecer_t["id"].isin(ids_by_insert.to_list())]

    elif table_acrecer.empty:
        # Si la tabla de la BD está vacía, todos los registros de la API son nuevos.
        merge_update = pd.DataFrame()
        merge_delete = pd.DataFrame()
        merge_insert = new_data_acrecer_t.copy()

    elif new_data_acrecer_t.empty:
        # Si la API no devuelve datos, no hay nada que insertar o actualizar.
        # Potencialmente, todos los registros existentes podrían ser marcados como inactivos.
        # (Nota: la lógica actual no los elimina a todos en este caso, solo si `table_acrecer` no está vacía).
        merge_update = pd.DataFrame()
        merge_delete = pd.DataFrame()  # Opcionalmente: merge_delete = table_acrecer.copy()
        merge_insert = pd.DataFrame()

    logger.info(
        "load_data_for_table_acrecer: merge_update filas=%s merge_delete filas=%s merge_insert filas=%s",
        len(merge_update), len(merge_delete), len(merge_insert)
    )

    # Aplicar los cambios a la base de datos.
    if not merge_update.empty:
        records = df_to_dicts(merge_update)
        QuerysMLSAcrecer.upsert_all(records)

    if not merge_delete.empty:
        # En lugar de borrar, se marcan como inactivos.
        records = df_to_dicts(merge_delete)
        for record in records:
            QuerysMLSAcrecer.delete_by_id(record.get("id"))  # Asumiendo que esto hace un soft-delete.

    if not merge_insert.empty:
        records = df_to_dicts(merge_insert)
        QuerysMLSAcrecer.bulk_insert(records)


if __name__ == "__main__":
    # Bloque para pruebas o ejecución directa del script.
    ...
