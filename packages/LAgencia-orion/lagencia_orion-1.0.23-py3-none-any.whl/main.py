from datetime import datetime  # noqa: F401

import pandas as pd  # noqa: F401

from orion.acrecer.etl_acrecer import load_data_for_table_acrecer  # noqa: F401
from orion.databases.db_bellatrix.repositories.query_acrecer import QuerysMLSAcrecer
from orion.databases.db_bellatrix.repositories.querys_simi import QuerysSimi
from orion.databases.db_bellatrix.repositories.querys_softin import QuerysSoftin
from orion.databases.db_empatia.repositories.querys_searcher import QuerysProperty  # noqa: F401
from orion.databases.db_empatia.repositories.repository_for_geospatial_calculations import lugares_a_500m, property_within_sector, test_geometries  # noqa: F401
from orion.databases.db_empatia.repositories.repository_for_loading_to_sectors import (  # noqa: F401
    execute_load_data_table_related_neighborhoods,
    load_alias_into_sectors2_preserve_ids,
    load_barrios_into_sectors2_preserve_ids,
    load_comunas_into_sectors2_preserve_ids,
    load_corregimientos_into_sectors2_preserve_ids,
    load_data_into_all_sector_source_tables,
    load_data_to_table_related_neighborhoods,
    load_lugares_into_sectors2_preserve_ids,
    load_municipios_into_sectors2_preserve_ids,
    load_source_sectors_into_table_sectors,
    load_veredas_into_sectors2_preserve_ids,
    update_field_reference_sector,
    update_field_sector_from_table_sectors_by_barrios,
    update_field_sector_from_table_sectors_by_comuna,
    update_field_sector_from_table_sectors_by_corregimiento,
    update_field_sector_from_table_sectors_by_lugares,
    update_field_sector_from_table_sectors_by_veredas,
)
from orion.databases.db_empatia.sp.sp import create_sp_and_trigers_from_sectors_control, execute_all_sp  # noqa: F401
from orion.mls.etl_mls import QuerysMLS  # noqa: F401
from orion.mls.etl_mls import etl as etl_mls  # noqa: F401
from orion.mls.mls import get_all_mls, get_full_data_mls  # noqa: F401

# from orion.searcher.etl_properties import update_properties  # # noqa: F401
# from orion.searcher.etl_properties import get_all_assets_from_sources  # noqa: F401
from orion.scripts.init_dbs import create_schemas_empatia  # noqa: F401
from orion.searcher.attributes_x_propierties.etl_attribute_properties import insert_records_in_table_attribute_properties, reload_records_in_table_attribute_properties, transform_mls_acrecer_for_attributes_properties, update_records_for_table_attribute_properties  # noqa: F401
from orion.searcher.etl_main import get_properties_to_insert  # noqa: F401
from orion.searcher.gallery_x_properties.etl_gallery import insert_records_in_table_gallery_properties, transform_mls_acrecer_for_gallery_propertirs, transform_mls_for_gallery_propierties, update_records_for_table_gallery_properties  # noqa: F401
from orion.searcher.properties.etl_properties import delete_properties, insert_new_properties, update_properties  # noqa: F401
from orion.searcher.properties.integrations import get_mls_acrecer_full, get_mls_full, get_simi_full, get_softin_full, integrate_sources_to_get_attributes_properties, integrate_sources_to_get_gallery_properties, integrate_sources_to_get_properties  # noqa: F401
from orion.searcher.properties.transform_data_mls import transform_mls_for_properties
from orion.searcher.properties.transform_data_mls_acrecer import transform_mls_acrecer_for_properties
from orion.searcher.properties.transform_data_simi import transform_simi_for_properties
from orion.searcher.properties.transform_data_softin import transform_softin_for_properties
from orion.searcher.properties.utils_properties import get_properties_to_delete, get_properties_to_update  # noqa: F401
from orion.searcher.sectors_x_properties.sectors_x_properties import insert_records_in_table_sectors_properties_by_lugar, insert_records_in_table_sectors_properties_by_sectors, update_records_for_table_sectors_properties, update_records_for_table_sectors_properties_by_lugar  # noqa: F401
from orion.simi.etl_simi import etl as etl_simi  # noqa: F401
from orion.softin.etl_softin import etl as etl_softin  # noqa: F401
from orion.tools import list_obj_to_df


def _test_load_data_sectors_source():
    # Solo se ejecutan una vez, en la carga de datos
    load_data_into_all_sector_source_tables()
    load_source_sectors_into_table_sectors()
    update_field_sector_from_table_sectors_by_comuna()
    update_field_sector_from_table_sectors_by_corregimiento()
    update_field_sector_from_table_sectors_by_veredas()
    update_field_sector_from_table_sectors_by_barrios()
    update_field_sector_from_table_sectors_by_lugares()
    update_field_reference_sector()

    # se ejecuta cada 30m o una vez al dia (en la noche)
    # create_sp_and_trigers_from_sectors_control()


def _test_sources_transfor_for_propertirs():
    # + PROBANDO LA TRANSFORMACION DE LAS FUENTES PARA CARGAR A PROPIEDADES
    records = QuerysSimi.select_all()
    simi_db = list_obj_to_df(records)
    result = transform_simi_for_properties(simi_db)
    print(result)

    records = QuerysSoftin.select_all()
    simi_db = list_obj_to_df(records)
    result = transform_softin_for_properties(simi_db)
    print(result)

    records = QuerysMLS.select_all()
    simi_db = list_obj_to_df(records)
    result = transform_mls_for_properties(simi_db)
    print(result)

    records = QuerysMLSAcrecer.select_all()
    simi_db = list_obj_to_df(records)
    result = transform_mls_acrecer_for_properties(simi_db)
    print(result)


def _test_etls_sources():
    etl_softin()
    etl_simi()
    etl_mls()
    load_data_for_table_acrecer()


def main():
    # load_data_for_table_acrecer()
    # mls_acrecer_full = get_mls_acrecer_full()

    # print(mls_acrecer_full.columns)
    # print(mls_acrecer_full[["rooms", "features", "householdFeatures", "inCondominiumFeatures"]])

    # mls_acrecer_full["rooms"] = mls_acrecer_full["rooms"].fillna({})
    # mls_acrecer_full["features"] = mls_acrecer_full["features"].fillna({})
    # mls_acrecer_full["householdFeatures"] = mls_acrecer_full["householdFeatures"].fillna({})
    # mls_acrecer_full["inCondominiumFeatures"] = mls_acrecer_full["inCondominiumFeatures"].fillna({})

    # columns = ["rooms", "features", "householdFeatures", "inCondominiumFeatures"]
    # mls_acrecer_full["full"] = {}

    # for index, row in mls_acrecer_full.iterrows():
    #     combined_dict = {}

    #     for column in columns:
    #         if isinstance(row[column], dict):
    #             combined_dict.update(row[column])

    #     mls_acrecer_full.at[index, "full"] = combined_dict

    # print(mls_acrecer_full[["rooms", "features"]])
    # print(mls_acrecer_full[["householdFeatures", "inCondominiumFeatures"]])
    # print(mls_acrecer_full[["full"]])

    # mls_acrecer_full[["id", "rooms", "features", "householdFeatures", "inCondominiumFeatures", "full"]].to_excel("mls_acrecer_full_new.xlsx", index=False)

    # result = transform_mls_acrecer_for_properties(mls_acrecer=mls_acrecer_full)
    # print(result)
    # print(result.columns)
    # print(len(result.columns))

    # ===========================================
    # etl_mls()
    # load_data_for_table_acrecer()
    # reload_records_in_table_attribute_properties()

    # records = QuerysMLSAcrecer.select_all()
    # mls_acrecer = list_obj_to_df(records)
    # result = transform_mls_acrecer_for_attributes_properties(mls_acrecer)
    # print(result)

    # + Cargar datos a softin, simi, mls, acrecer
    # _test_etls_sources()

    # + Crear esquemas, triggers y sp
    # create_schemas_bellatrix()
    create_schemas_empatia()
    # create_sp_and_trigers_from_sectors_control()

    # + cargar datos a las fuentes de sectores y a sectores
    # _test_load_data_sectors_source()

    # + funciones para tablas base

    # + Ejecutar los procedimientos almacenados
    # execute_all_sp()

    # + ======================================================Sincronizacion

    # # obtenemos las propiedades activas de cada fuente
    # softin_full = get_softin_full()
    # simi_full = get_simi_full()
    # mls_full = get_mls_full()
    # mls_acrecer_full = get_mls_acrecer_full()

    # # obtener propiedades
    # new_properties = integrate_sources_to_get_properties(softin_full, simi_full, mls_full, mls_acrecer_full)

    # records = QuerysProperty.select_all()
    # old_properties = list_obj_to_df(records)

    # #new_properties.to_excel("new_properties.xlsx", index=False)
    # #old_properties.to_excel("old_properties.xlsx", index=False)

    # by_insert = get_properties_to_insert(new_properties, old_properties)
    # by_update = get_properties_to_update(new_properties, old_properties)
    # by_delete = get_properties_to_delete(new_properties, old_properties)

    # print(f"{by_insert.shape=}")
    # print(f"{by_update.shape=}")
    # print(f"{by_delete.shape=}")

    # # + para insertar
    # if not by_insert.empty:
    #     properties_ids = by_insert["id"].to_list()
    #     softin_full_ = softin_full[softin_full["id"].isin(by_insert["id"])]
    #     simi_full_ = simi_full[simi_full["id"].isin(by_insert["id"])]
    #     mls_full_ = mls_full[mls_full["id"].isin(by_insert["id"])]
    #     mls_acrecer_full_ = mls_acrecer_full[mls_acrecer_full["id"].isin(by_insert["id"])]

    #     # insertar propiedades nuevas o que estaban desactivadas
    #     insert_new_properties(by_insert)

    #     # obtener atributos de propiedades
    #     result_attributes_properties = integrate_sources_to_get_attributes_properties(softin_full_, simi_full_, mls_full_, mls_acrecer_full_)
    #     print(result_attributes_properties)
    #     insert_records_in_table_attribute_properties(result_attributes_properties)

    #     # obtener galeria de porpiedades
    #     result_gallery_properties = integrate_sources_to_get_gallery_properties(softin_full_, simi_full_, mls_full_, mls_acrecer_full_)
    #     print(result_gallery_properties)
    #     insert_records_in_table_gallery_properties(result_gallery_properties)

    #     # obtener sectores de propiedades
    #     insert_records_in_table_sectors_properties_by_sectors(properties_ids)
    #     insert_records_in_table_sectors_properties_by_lugar(properties_ids)
    #     # ejecutar procedimientos almacenados

    # # # + para actualizar
    # if not by_update.empty:
    #     #by_update.to_excel("by_update.xlsx", index=False)
    #     properties_ids = by_update["id"].to_list()
    #     softin_full_ = softin_full[softin_full["id"].isin(by_update["id"])]
    #     simi_full_ = simi_full[simi_full["id"].isin(by_update["id"])]
    #     mls_full_ = mls_full[mls_full["id"].isin(by_update["id"])]
    #     mls_acrecer_full_ = mls_acrecer_full[mls_acrecer_full["id"].isin(by_update["id"])]

    #     update_properties(by_update)

    #     # obtener atributos de propiedades
    #     result_attributes_properties = integrate_sources_to_get_attributes_properties(softin_full_, simi_full_, mls_full_, mls_acrecer_full_)
    #     print(result_attributes_properties)
    #     update_records_for_table_attribute_properties(result_attributes_properties)

    #     # obtener galeria de porpiedades
    #     result_gallery_properties = integrate_sources_to_get_gallery_properties(softin_full_, simi_full_, mls_full_, mls_acrecer_full_)
    #     print(result_gallery_properties)
    #     update_records_for_table_gallery_properties(result_gallery_properties)

    #     update_records_for_table_sectors_properties(properties_ids)
    #     update_records_for_table_sectors_properties_by_lugar(properties_ids)

    # # by_delete
    # if not by_delete.empty:
    #     delete_properties(by_delete)

    #! ====================================================
    # load_source_sectors_into_table_sectors()
    # result  = property_within_sector()
    # print(result)

    # test_geometries()

    # mls_acrecer_full = get_mls_acrecer_full()
    # result = transform_mls_acrecer_for_properties(mls_acrecer_full)
    # print(result)

    ...


if __name__ == "__main__":
    main()
