import pandas as pd

from orion.databases.db_bellatrix.repositories.query_acrecer import QuerysMLSAcrecer
from orion.databases.db_bellatrix.repositories.querys_mls import MLS, QuerysMLS
from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi, Simi
from orion.databases.db_bellatrix.repositories.querys_softin import QuerysSoftin, Softin
from orion.searcher.attributes_x_propierties.etl_attribute_properties import transform_mls_acrecer_for_attributes_properties, transform_mls_for_attributes_properties, transform_simi_for_attributes_properties, transform_softin_for_attribute_properties
from orion.searcher.gallery_x_properties.etl_gallery import transform_mls_acrecer_for_gallery_propertirs, transform_mls_for_gallery_propierties, transform_simi_for_gallery_propierties, transform_softin_for_gallery_propierties
from orion.searcher.properties.transform_data_mls import transform_mls_for_properties
from orion.searcher.properties.transform_data_mls_acrecer import transform_mls_acrecer_for_properties
from orion.searcher.properties.transform_data_simi import transform_simi_for_properties
from orion.searcher.properties.transform_data_softin import transform_softin_for_properties
from orion.searcher.properties.utils_properties import add_shows, convert_property_type_name_to_plural, set_type_management_to_furnished
from orion.tools import list_obj_to_df
from orion.utils.georeferencing_tools import create_geometry_from_coordinates

"""_summary_: reune todas las fuentes de datos, hacer las transormaciones pertinentes para terminar de ajustar la data a
    la tabla properties
"""


def get_softin_full() -> pd.DataFrame:
    records = QuerysSoftin.select_by_filter(Softin.activo == 1)
    softin_full = list_obj_to_df(records)
    print(f"** Propedades de Softin activas: {softin_full.shape} **")
    return softin_full


def get_simi_full() -> pd.DataFrame:
    records = QuerysSimi.select_by_filter(Simi.activo == 1)
    simi_full = list_obj_to_df(records)
    print(f"** Propedades de Simi activas: {simi_full.shape}**")
    return simi_full


def get_mls_full() -> pd.DataFrame:
    records = QuerysMLS.select_by_filter(MLS.active == 1)
    mls_full = list_obj_to_df(records)
    print(f"** Propedades de MLS activas: {mls_full.shape} **")
    return mls_full


def get_mls_acrecer_full() -> pd.DataFrame:
    records = QuerysMLSAcrecer.select_all()
    mls_acrecer_full = list_obj_to_df(records)
    print(f"** Propedades de MLS acrecer activas: {mls_acrecer_full.shape} **")
    return mls_acrecer_full


# get_all_assets_from_sources
def integrate_sources_to_get_properties(
    softin_full: pd.DataFrame,
    simi_full: pd.DataFrame,
    mls_full: pd.DataFrame,
    mls_acrecer_full: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combina las propiedades activas de Softin, Simi, MLS, MLS_acrecer en un único DataFrame.

    Returns:
        pd.DataFrame: DataFrame combinado con todas las propiedades activas que cumple
        con el schema de la tabla properties.
    """
    softin_full = softin_full.copy()
    simi_full = simi_full.copy()
    mls_full = mls_full.copy()
    mls_acrecer_full = mls_acrecer_full.copy()

    softin_full = transform_softin_for_properties(softin_full)
    simi_full = transform_simi_for_properties(simi_full)
    mls_full = transform_mls_for_properties(mls_full)
    mls_acrecer_full = transform_mls_acrecer_for_properties(mls_acrecer_full)

    sources = pd.concat([softin_full, simi_full, mls_full, mls_acrecer_full])
    sources = sources[sources["latitude"].notnull()]
    sources = sources[sources["longitude"].notnull()]
    sources["latitude"] = sources["latitude"].apply(lambda x: float(str(x).replace(",", "")))
    sources["longitude"] = sources["longitude"].apply(lambda x: float(str(x).replace(",", "")))
    sources["geometry"] = sources.apply(lambda x: create_geometry_from_coordinates(x["latitude"], x["longitude"]), axis=1)

    sources = add_shows(sources)
    sources = convert_property_type_name_to_plural(sources)
    sources = set_type_management_to_furnished(sources)
    sources["description"] = sources["description"].apply(lambda x: x.replace("</p>", "").replace("<p>", "") if x else x)

    sources.drop(columns=["create_at"], inplace=True)
    print(f"** Total propiedades procesadas activas: {sources.shape} **")

    return sources


def integrate_sources_to_get_attributes_properties(
    softin_full: pd.DataFrame,
    simi_full: pd.DataFrame,
    mls_full: pd.DataFrame,
    mls_acrecer_full: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combina las propiedades activas de Softin, Simi, MLS, MLS_acrecer en un único DataFrame.

    Returns:
        pd.DataFrame: DataFrame combinado que cumple con el schema de la tabla attributes_properties.
    """

    softin_full = softin_full.copy() if not softin_full.empty else pd.DataFrame()
    simi_full = simi_full.copy() if not simi_full.empty else pd.DataFrame()
    mls_full = mls_full.copy() if not mls_full.empty else pd.DataFrame()
    mls_acrecer_full = mls_acrecer_full.copy() if not mls_acrecer_full.empty else pd.DataFrame()

    attributes_properties_softin = transform_softin_for_attribute_properties(softin_full)
    attributes_properties_simi = transform_simi_for_attributes_properties(simi_full)
    attributes_properties_mls = transform_mls_for_attributes_properties(mls_full)
    attributes_properties_mls_acrecer = transform_mls_acrecer_for_attributes_properties(mls_acrecer_full)

    print(type(attributes_properties_softin))
    print(type(attributes_properties_simi))
    print(type(attributes_properties_mls))
    print(type(attributes_properties_mls_acrecer))

    attributes_properties = pd.concat([attributes_properties_softin, attributes_properties_simi, attributes_properties_mls, attributes_properties_mls_acrecer])

    return attributes_properties


def integrate_sources_to_get_gallery_properties(
    softin_full: pd.DataFrame,
    simi_full: pd.DataFrame,
    mls_full: pd.DataFrame,
    mls_acrecer_full: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combina las propiedades activas de Softin, Simi, MLS, MLS_acrecer en un único DataFrame.

    Returns:
        pd.DataFrame: DataFrame combinado que cumple con el schema de la tabla gallery.
    """

    softin_full = softin_full.copy()
    simi_full = simi_full.copy()
    mls_full = mls_full.copy()
    mls_acrecer_full = mls_acrecer_full.copy()
    gallery_properties_softin = transform_softin_for_gallery_propierties(softin_full)
    gallery_properties_simi = transform_simi_for_gallery_propierties(simi_full)
    gallery_properties_mls = transform_mls_for_gallery_propierties(mls_full)
    gallery_properties_mls_acrecer = transform_mls_acrecer_for_gallery_propertirs(mls_acrecer_full)

    gallery_properties = pd.concat([gallery_properties_softin, gallery_properties_simi, gallery_properties_mls, gallery_properties_mls_acrecer])

    return gallery_properties
