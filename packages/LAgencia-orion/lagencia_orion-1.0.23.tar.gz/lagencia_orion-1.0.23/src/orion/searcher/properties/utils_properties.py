from datetime import datetime

import pandas as pd

from orion.databases.db_bellatrix.repositories.querys_mls import MLS, QuerysMLS
from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi, Simi
from orion.databases.db_bellatrix.repositories.querys_softin import QuerysSoftin, Softin
from orion.databases.db_empatia.repositories.querys_searcher import QuerysMapPropertyType, QuerysProperty
from orion.tools import df_to_dicts, list_obj_to_df


def get_properties_to_insert(new: pd.DataFrame, old: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica las propiedades activas en las fuentes (Softin/Simi/MLS)
    que aún no están en la base de datos.

    Args:
        new (pd.DataFrame): DataFrame con las propiedades activas obtenidas
                                  de las fuentes (Softin/Simi/MLS).
        old (pd.DataFrame): DataFrame con las propiedades existentes
                                      en la base de datos.

    Returns:
       pd.DataFrame: DataFrame con las propiedades activas que necesitan ser insertadas.
    """

    if old.empty:
        return new

    if new.empty:
        return pd.DataFrame()

    merged = new.merge(old, on="id", how="outer", indicator=True)
    to_insert_ids = merged[merged["_merge"] == "left_only"]["id"]
    return new[new["id"].isin(to_insert_ids)]


def get_properties_to_delete(new: pd.DataFrame, old: pd.DataFrame) -> pd.DataFrame:
    """

    identifica los registros que estan en old pero no en new

    Args:
        new (pd.DataFrame): DataFrame con las propiedades activas obtenidas
                               de las fuentes (Softin/Simi/MLS).
        old (pd.DataFrame): DataFrame con las propiedades existentes
                                      en la base de datos.

    Returns:
        pd.Series: Serie con los IDs de las propiedades que deben eliminarse.
    """

    if new.empty:
        return pd.DataFrame()

    if old.empty:
        return pd.DataFrame()

    merged = old.merge(new, on="id", how="outer", indicator=True)

    return merged[merged["_merge"] == "left_only"]#["id"]


def get_properties_to_update(source: pd.DataFrame, properties_db: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica las propiedades que ya no están activas en las fuentes
    pero que permanecen en la base de datos.

    Args:
        source (pd.DataFrame): DataFrame con las propiedades activas obtenidas
                               de las fuentes (Softin/Simi/MLS).
        properties_db (pd.DataFrame): DataFrame con las propiedades existentes
                                      en la base de datos.

    Returns:
        pd.DataFrame: DataFrame con las propiedades activas que necesitan ser actualizadas.
    """

    if source.empty or properties_db.empty:
        return pd.DataFrame()

    source_id = pd.DataFrame(source["id"], columns=["id"])
    properties_db_id = pd.DataFrame(properties_db["id"], columns=["id"])

    merged = source_id.merge(properties_db_id, how="outer", on="id", indicator=True)
    to_update_ids = merged[merged["_merge"] == "both"]["id"].copy()

    to_update_from_source = source[source_id["id"].isin(to_update_ids)][["id", "modified_date"]].rename(columns={"modified_date": "modified_date_source"})
    to_update_from_db = properties_db[properties_db_id["id"].isin(to_update_ids)][["id", "modified_date"]].rename(columns={"modified_date": "modified_date_db"})

    to_update_ = to_update_from_source.merge(to_update_from_db, on="id", how="inner")
    to_update_= to_update_[to_update_["modified_date_source"]!='0000-00-00 00:00:00']
    to_update_["modified_date_source"] = pd.to_datetime(to_update_["modified_date_source"])
    to_update_["modified_date_db"] = pd.to_datetime(to_update_["modified_date_db"])
    to_update_["update"] = to_update_["modified_date_source"] > to_update_["modified_date_db"]
    to_update_.to_excel("to_update_.xlsx", index=False) #+

    to_update_ids = to_update_[to_update_["update"]]["id"]
    to_update = source[source_id["id"].isin(to_update_ids)]

    to_update = to_update.merge(properties_db[["id", "price"]], on="id", how="left", suffixes=("", "_old"))
    to_update.rename(columns={"price_old": "old_price"}, inplace=True)

    return to_update


def deactivate_properties():
    properties_records = QuerysProperty.select_all()
    properties_db = list_obj_to_df(properties_records)

    if properties_db.empty:
        return

    records_softin = QuerysSoftin.select_by_filter(Softin.activo == 0)
    softin_ = pd.DataFrame(list_obj_to_df(records_softin)["id"])
    records_simi = QuerysSimi.select_by_filter(Simi.activo == 0)
    simi_ = pd.DataFrame(list_obj_to_df(records_simi)["id"])
    records_mls = QuerysMLS.select_by_filter(MLS.active == 0)
    mls_ = pd.DataFrame(list_obj_to_df(records_mls)["id"])

    sources = pd.concat([softin_, simi_, mls_])

    merged = properties_db.merge(sources, how="inner", on="id")
    records = df_to_dicts(merged)

    for record in records:
        print(f"Eliminar propiedad: {record.get('id')}")
        QuerysProperty.delete_by_id(record.get("id"))


def add_shows(sources: pd.DataFrame) -> pd.DataFrame:
    sources = sources.copy()

    sources["show_rent_villacruz"] = 0
    sources["show_sale_villacruz"] = 0
    sources["show_furnished_villacruz"] = 0
    sources.loc[(sources["management"] == "Venta") & (sources["show_villacruz"] == 1), "show_sale_villacruz"] = 1
    sources.loc[(sources["management"] == "Arriendo") & (sources["show_villacruz"] == 1), "show_rent_villacruz"] = 1
    sources.loc[(sources["show_furnished"] == 1) & (sources["show_villacruz"] == 1), "show_furnished_villacruz"] = 1

    sources["show_rent_castillo"] = 0
    sources["show_sale_castillo"] = 0
    sources["show_furnished_castillo"] = 0
    sources.loc[(sources["management"] == "Venta") & (sources["show_castillo"] == 1), "show_sale_castillo"] = 1
    sources.loc[(sources["management"] == "Arriendo") & (sources["show_castillo"] == 1), "show_rent_castillo"] = 1
    sources.loc[(sources["show_furnished"] == 1) & (sources["show_castillo"] == 1), "show_furnished_castillo"] = 1

    sources["show_rent_estrella"] = 0
    sources["show_sale_estrella"] = 0
    sources["show_furnished_estrella"] = 0
    sources.loc[(sources["management"] == "Venta") & (sources["show_estrella"] == 1), "show_sale_estrella"] = 1
    sources.loc[(sources["management"] == "Arriendo") & (sources["show_estrella"] == 1), "show_rent_estrella"] = 1
    sources.loc[(sources["show_furnished"] == 1) & (sources["show_estrella"] == 1), "show_furnished_estrella"] = 1

    sources["show_rent_livin"] = 0
    sources["show_sale_livin"] = 0
    sources["show_furnished_livin"] = 0
    sources.loc[(sources["management"] == "Venta") & (sources["show_livin"] == 1), "show_sale_livin"] = 1
    sources.loc[(sources["management"] == "Arriendo") & (sources["show_livin"] == 1), "show_rent_livin"] = 1
    sources.loc[(sources["show_furnished"] == 1) & (sources["show_livin"] == 1), "show_furnished_livin"] = 1

    return sources


def convert_property_type_name_to_plural(source: pd.DataFrame) -> pd.DataFrame:
    source = source.copy()
    # property_type_dict = {
    #     "Apartaestudio": "Apartaestudios",
    #     "Apartamento": "Apartamentos",
    #     "Apto-Loft": "Apto-Lofts",
    #     "Bodega": "Bodegas",
    #     "Casa": "Casas",
    #     "Casa Campestre": "Casas Campestres",
    #     "Casa-Finca": "Casas Fincas",
    #     "Casa-local": "Casas Locales",
    #     "Casa Comercial": "Casas Comerciales",
    #     "Casa Residencial": "Casas Residenciales",
    #     "Consultorio": "Consultorios",
    #     "Cuarto Util": "Cuartos Utiles",
    #     "Edificio": "Edificios",
    #     "Finca": "Fincas",
    #     "Finca Productiva": "Fincas Productivas",
    #     "Finca Recreativa": "Fincas Recreativas",
    #     "Hotel": "Hoteles",
    #     "Hotel/Apart Hotel": "Hoteles/Aparta Hoteles",
    #     "Local": "Locales",
    #     "Local Comercial": "Locales Comerciales",
    #     "Lote": "Lotes",
    #     "Lote Comercial": "Lotes Comerciales",
    #     "Lote Residencial": "Lotes Residenciales",
    #     "Oficina": "Oficinas",
    #     "Oficina-Consultorio": "Oficinas-Consutorios",
    #     "Oficina-Local": "Oficinas-Locales",
    #     "Parqueadero": "Parqueaderos",
    #     "Terreno": "Terrenos"
    # }

    records = QuerysMapPropertyType.select_all()
    property_type_dict = {}
    for record in records:
        property_type_dict.update({record.singular: record.plural})

    source["property_type_searcher"] = source["property_type"].apply(lambda x: property_type_dict.get(x))

    return source


def get_year_build(sources: pd.DataFrame) -> pd.DataFrame:
    sources = sources.copy()
    sources["age"] = sources["age"].apply(lambda x: (datetime.now().year - x) if pd.notnull(x) and isinstance(x, (int, float)) and x > 0 and x <= datetime.now().year else None)
    return sources


def set_type_management_to_furnished(source: pd.DataFrame) -> pd.DataFrame:
    source = source.copy()
    source["management"] = source.apply(lambda x: "Amoblado" if x["management"] == "Arriendo" and x["show_furnished"] == 1 else x["management"], axis=1)
    return source
