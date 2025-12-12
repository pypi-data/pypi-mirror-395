import pandas as pd
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon, Polygon

from orion.databases.db_empatia.repositories.querys_searcher import QuerysProperty

# from orion.searcher.gallery.etl_gallery import insert_records_in_table_gallery_properties, update_records_for_table_gallery_properties
from orion.tools import df_to_dicts

"""_summary_: permite actualizar la tabla de propiedades con la informacion
            actual de las tablas de softin, simi y mls
"""


# def add_shows(sources: pd.DataFrame) -> pd.DataFrame:
#     sources = sources.copy()

#     sources["show_rent_villacruz"] = 0
#     sources["show_sale_villacruz"] = 0
#     sources["show_furnished_villacruz"] = 0
#     sources.loc[(sources["management"] == "Venta") & (sources["show_villacruz"] == 1), "show_sale_villacruz"] = 1
#     sources.loc[(sources["management"] == "Arriendo") & (sources["show_villacruz"] == 1), "show_rent_villacruz"] = 1
#     sources.loc[(sources["show_furnished"] == 1) & (sources["show_villacruz"] == 1), "show_furnished_villacruz"] = 1

#     sources["show_rent_castillo"] = 0
#     sources["show_sale_castillo"] = 0
#     sources["show_furnished_castillo"] = 0
#     sources.loc[(sources["management"] == "Venta") & (sources["show_castillo"] == 1), "show_sale_castillo"] = 1
#     sources.loc[(sources["management"] == "Arriendo") & (sources["show_castillo"] == 1), "show_rent_castillo"] = 1
#     sources.loc[(sources["show_furnished"] == 1) & (sources["show_castillo"] == 1), "show_furnished_castillo"] = 1

#     sources["show_rent_estrella"] = 0
#     sources["show_sale_estrella"] = 0
#     sources["show_furnished_estrella"] = 0
#     sources.loc[(sources["management"] == "Venta") & (sources["show_estrella"] == 1), "show_sale_estrella"] = 1
#     sources.loc[(sources["management"] == "Arriendo") & (sources["show_estrella"] == 1), "show_rent_estrella"] = 1
#     sources.loc[(sources["show_furnished"] == 1) & (sources["show_estrella"] == 1), "show_furnished_estrella"] = 1

#     sources["show_rent_livin"] = 0
#     sources["show_sale_livin"] = 0
#     sources["show_furnished_livin"] = 0
#     sources.loc[(sources["management"] == "Venta") & (sources["show_livin"] == 1), "show_sale_livin"] = 1
#     sources.loc[(sources["management"] == "Arriendo") & (sources["show_livin"] == 1), "show_rent_livin"] = 1
#     sources.loc[(sources["show_furnished"] == 1) & (sources["show_livin"] == 1), "show_furnished_livin"] = 1

#     return sources


# def deactivate_properties():
#     properties_records = QuerysProperty.select_all()
#     properties_db = list_obj_to_df(properties_records)

#     if properties_db.empty:
#         return

#     records_softin = QuerysSoftin.select_by_filter(Softin.activo == 0)
#     softin_ = pd.DataFrame(list_obj_to_df(records_softin)["id"])
#     records_simi = QuerysSimi.select_by_filter(Simi.activo == 0)
#     simi_ = pd.DataFrame(list_obj_to_df(records_simi)["id"])
#     records_mls = QuerysMLS.select_by_filter(MLS.active == 0)
#     mls_ = pd.DataFrame(list_obj_to_df(records_mls)["id"])

#     sources = pd.concat([softin_, simi_, mls_])

#     merged = properties_db.merge(sources, how="inner", on="id")
#     records = df_to_dicts(merged)

#     for record in records:
#         print(f"Eliminar propiedad: {record.get('id')}")
#         QuerysProperty.delete_by_id(record.get("id"))


# def convert_property_type_name_to_plural(source: pd.DataFrame) -> pd.DataFrame:
#     source = source.copy()
#     # property_type_dict = {
#     #     "Apartaestudio": "Apartaestudios",
#     #     "Apartamento": "Apartamentos",
#     #     "Apto-Loft": "Apto-Lofts",
#     #     "Bodega": "Bodegas",
#     #     "Casa": "Casas",
#     #     "Casa Campestre": "Casas Campestres",
#     #     "Casa-Finca": "Casas Fincas",
#     #     "Casa-local": "Casas Locales",
#     #     "Casa Comercial": "Casas Comerciales",
#     #     "Casa Residencial": "Casas Residenciales",
#     #     "Consultorio": "Consultorios",
#     #     "Cuarto Util": "Cuartos Utiles",
#     #     "Edificio": "Edificios",
#     #     "Finca": "Fincas",
#     #     "Finca Productiva": "Fincas Productivas",
#     #     "Finca Recreativa": "Fincas Recreativas",
#     #     "Hotel": "Hoteles",
#     #     "Hotel/Apart Hotel": "Hoteles/Aparta Hoteles",
#     #     "Local": "Locales",
#     #     "Local Comercial": "Locales Comerciales",
#     #     "Lote": "Lotes",
#     #     "Lote Comercial": "Lotes Comerciales",
#     #     "Lote Residencial": "Lotes Residenciales",
#     #     "Oficina": "Oficinas",
#     #     "Oficina-Consultorio": "Oficinas-Consutorios",
#     #     "Oficina-Local": "Oficinas-Locales",
#     #     "Parqueadero": "Parqueaderos",
#     #     "Terreno": "Terrenos"
#     # }

#     records = QuerysMapPropertyType.select_all()
#     property_type_dict = {}
#     for record in records:
#         property_type_dict.update({record.singular: record.plural})

#     print(property_type_dict)
#     source["property_type_searcher"] = source["property_type"].apply(lambda x: property_type_dict.get(x))

#     return source


# def get_year_build(sources: pd.DataFrame) -> pd.DataFrame:
#     sources = sources.copy()
#     sources["age"] = sources["age"].apply(lambda x: (datetime.now().year - x) if pd.notnull(x) and isinstance(x, (int, float)) and x > 0 and x <= datetime.now().year else None)
#     return sources


# def set_type_management_to_furnished(source: pd.DataFrame) -> pd.DataFrame:
#     source = source.copy()
#     source["management"] = source.apply(lambda x: "Amoblado" if x["management"] == "Arriendo" and x["show_furnished"] == 1 else x["management"], axis=1)
#     return source


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

SRID = 4326


def to_model_dict(d: dict) -> dict:
    d = dict(d)  # copia
    geom = d.get("geometry")

    if geom is None:
        return d

    # Caso 1: viene como texto WKT
    if isinstance(geom, str):
        d["geometry"] = WKTElement(geom, srid=SRID)
        return d

    # Caso 2: viene como Shapely geometry
    # Si es Polygon, lo envolvemos como MultiPolygon para que coincida con tu columna
    if isinstance(geom, Polygon):
        geom = MultiPolygon([geom])

    # Asegúrate de que sea MultiPolygon
    if isinstance(geom, MultiPolygon):
        d["geometry"] = from_shape(geom, srid=SRID)  # <-- correcto para Shapely
        return d

    # (Opcional) si viniera WKB (bytes), podrías usar from_wkb
    # else: lanzar error explícito para detectar casos no contemplados
    raise TypeError(f"geometry no soportada: {type(geom)}")


def insert_new_properties(new_properties: pd.DataFrame):
    if new_properties.empty:
        return

    records = df_to_dicts(new_properties)
    print(f"Insertando nuevas propiedades: {len(records)}")
    records = [to_model_dict(record) for record in records]

    QuerysProperty.insert_all(records)


def update_properties(properties: pd.DataFrame):
    if properties.empty:
        return
    records = df_to_dicts(properties)
    print(f"Actualizando propiedades: {len(records)}")
    for record in records:
        QuerysProperty.update_by_id(record, record.get("id"))


def delete_properties(properties: pd.DataFrame):
    if properties.empty:
        return
    records = df_to_dicts(properties)
    print(f"Eliminando propiedades: {len(records)}")
    for record in records:
        QuerysProperty.delete_by_id(record.get("id"))
