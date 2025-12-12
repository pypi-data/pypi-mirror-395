# insert
# update
# active (update)
# deactive (update)

# def insert_new_record():
#     insert_new_property_record()
#     insert_new_attributes_property()
#     insert_new_sectors_property()
#     insert_new_gallery_property()
#     ...

# def update_record():
#     update_properties()
#     update_property_attributes()
#     update_property_sectors()
#     update_property_gallery()


import pandas as pd

from orion.databases.db_empatia.repositories.querys_searcher import QuerysGalleryProperties, QuerysProperty, QuerysPropertySector
from orion.searcher.attributes_x_propierties.etl_attribute_properties import QuerysAttributeProperties
from orion.searcher.properties.integrations import integrate_sources_to_get_properties
from orion.searcher.properties.utils_properties import get_properties_to_delete, get_properties_to_insert, get_properties_to_update
from orion.tools import df_to_dicts, list_obj_to_df

list_obj_to_df


# def update_properties() -> bool:
#     """
#     Actualiza la tabla de propiedades con los datos más recientes de Softin, Simi y MLS.

#     Returns:
#         bool: True si la actualización fue exitosa, False en caso de error.
#     """

#     # path_save = os.path.join(os.path.dirname(__file__), "..", "..", "outputs", "properties")
#     try:
#         # deactivate_properties()

#         # Cargamos propiedades de la base de datos
#         records = QuerysProperty.select_all()
#         properties_db = list_obj_to_df(records)

#         # Cargamos datos de las fuentes Softin/Simi/MLS
#         source = get_all_assets_from_sources()

#         # Procesamiento adicional
#         print("Procesar propiedades")
#         source = add_shows(source)
#         source = convert_property_type_name_to_plural(source)
#         source = set_type_management_to_furnished(source)
#         source["description"] = source["description"].apply(lambda x: x.replace("</p>", "").replace("<p>", "") if x else x)

#         # Cargar propiedades de las fuentes si no hay registros en propities
#         if properties_db.empty:
#             print("**Cargamos todos los activos de las fuentes.")
#             id_properties = source["id"]
#             records = df_to_dicts(source)
#             if records:
#                 QuerysProperty.bulk_insert(records)
#                 print("Insertando atributos de nuevas propiedades")
#                 insert_records_in_table_attribute_properties(id_properties)
#                 print("Insertando imagenes de nuevas propiedades")
#                 insert_records_in_table_gallery_properties(id_properties)
#                 print("Insertando propedades por sector")
#                 insert_records_in_table_property_sectors_for_properties(id_properties)
#                 return True
#             return False

#         # Determinar las propiedades a insertar, eliminar y actualizar
#         to_insert = get_properties_to_insert(source, properties_db)
#         to_delete_ids = get_properties_to_delete(source, properties_db)
#         to_update = get_properties_to_update(source, properties_db)

#         # to_insert.to_excel(os.path.join(path_save, "to_insert_properties.xlsx"), index=False)
#         # to_delete_ids.to_excel(os.path.join(path_save, "to_delete_ids_properties.xlsx"), index=False)
#         # to_update.to_excel(os.path.join(path_save, "to_update_proerties.xlsx"), index=False)

#         print("**Propiedades para insertar: ", to_insert.shape)
#         print("**Propiedades para eliminar: ", to_delete_ids.shape)
#         print("**Propiedades para actualizar: ", to_update.shape)

#         # Eliminar propiedades no activas
#         for property_id in to_delete_ids:
#             QuerysProperty.delete_by_id(property_id)

#         # Insertar nuevas propiedades
#         if not to_insert.empty:
#             id_properties = to_insert["id"]
#             records = df_to_dicts(to_insert)
#             print("Insertando nuevas propiedades")
#             QuerysProperty.bulk_insert(records)
#             print("Insertando atributos de nuevas propiedades")
#             insert_records_in_table_attribute_properties(id_properties)
#             print("Insertando imagenes de nuevas propiedades")
#             insert_records_in_table_gallery_properties(id_properties)
#             print("Insertando propedades por sector")
#             insert_records_in_table_property_sectors_for_properties(id_properties)

#         # Actualizar propiedades
#         if not to_update.empty:
#             id_properties = to_update["id"]
#             records = df_to_dicts(to_update)
#             print("Actualizando propiedades")
#             for record in records:
#                 print(f"property: {record.get('id')}")
#                 rec = QuerysProperty.select_by_filter(Property.id == record.get("id"))
#                 if record["old_price"] != rec[0].price:
#                     record["old_price"] = rec[0].price
#                 QuerysProperty.update_by_id(record, record.get("id"))
#             print("Actualizando atributos de propiedades")
#             update_records_for_table_attribute_properties(id_properties)
#             print("Actualizando galeria de propiedades")
#             update_records_for_table_gallery_properties(id_properties)
#             print("Actualizando propiedades por sector")
#             update_records_table_property_sectors_for_properties(id_properties)

#         return True

#     except Exception as e:
#         print(f"Error actualizando propiedades: {e}")
#         print(traceback.format_exc())
#         print(sys.exc_info()[2])
#         return False


def insert_new_record(df: pd.DataFrame):
    records = df_to_dicts(df)
    tools_properties = QuerysProperty()
    # tools_attributes =QuerysAttributes()
    tools_attributes_properties = QuerysAttributeProperties()
    tools_gallery_properties = QuerysGalleryProperties()
    tools_sectors_properties = QuerysPropertySector()

    for record in records:
        tools_properties.bulk_insert()


def etl():
    properties_sources = integrate_sources_to_get_properties()

    records = QuerysProperty.select_all()
    properties_db = list_obj_to_df(records)

    result_insert = get_properties_to_insert(properties_sources, properties_db)
    result_delete = get_properties_to_delete(properties_sources, properties_db)
    result_update = get_properties_to_update(properties_sources, properties_db)

    print(f"para insertar: {result_insert.shape[0]}")
    print(result_insert)
    print(f"para eliminar: {result_delete.shape[0]}")
    print(result_delete)
    print(f"para actualizar: {result_update.shape[0]}")
    print(result_update)

    insert_new_record(result_insert)
