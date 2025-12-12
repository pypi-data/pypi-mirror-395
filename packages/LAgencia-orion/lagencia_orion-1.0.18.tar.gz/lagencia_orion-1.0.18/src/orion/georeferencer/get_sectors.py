# import os
# from typing import Union

# import geopandas as gpd
# import pandas as pd

# from orion.databases.db_empatia.models.model_searcher import Sector
# from orion.databases.db_empatia.repositories.querys_searcher import (
#     QuerysProperty,
#     QuerysPropertySector,
#     QuerysSector,
# )
# from orion.georeferencer.get_property_sectors import reload_property_sectors_table_records
# from orion.georeferencer.get_surname_sector import (
#     get_field_sector_reference_barrio,
#     get_field_sector_reference_vereda,
#     get_reference_for_barrio,
#     get_reference_for_comuna,
#     get_reference_for_corregimiento,
#     get_reference_for_lugar,
#     get_reference_for_vereda,
# )
# from orion.georeferencer.processing_data import get_georeferenced_layers
# from orion.tools import df_to_dicts, generate_slug, list_obj_to_df

# """
# Resumen: Este módulo carga y transforma datos de capas de georreferenciación,
# permitiendo gestionar sectores geográficos y su asociación con propiedades.
# """


# def concat_sectors(puntos_interes, barrios, veredas, comunas, corregimientos, municipios) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
#     """
#     Combina diferentes capas geográficas en un solo DataFrame con la información
#     unificada de sectores.

#     Args:
#         puntos_interes (GeoDataFrame): Puntos de interés.
#         barrios (GeoDataFrame): Barrios.
#         veredas (GeoDataFrame): Veredas.
#         comunas (GeoDataFrame): Comunas.
#         corregimientos (GeoDataFrame): Corregimientos.
#         municipios (GeoDataFrame): Municipios.

#     Returns:
#         Union[pd.DataFrame, gpd.GeoDataFrame]: DataFrame combinado con los sectores.
#     """

#     # + puntos de interes
#     data = {
#         "name": puntos_interes["Name"],
#         "category_point_interest": puntos_interes["Categoria"],
#     }
#     sectores_punto_interes = pd.DataFrame(data)
#     sectores_punto_interes["type"] = "Lugar"

#     # + municipios
#     data = {"name": municipios["Name"]}
#     sectores_municipio = pd.DataFrame(data)
#     sectores_municipio["type"] = "Municipio"

#     # + barrios
#     data = {"name": barrios["Name"]}
#     sectores_barrios = pd.DataFrame(data)
#     sectores_barrios["type"] = "Barrio"

#     # + comunas
#     data = {"name": comunas["Name"]}
#     sectores_comunas_med_1 = pd.DataFrame(data)
#     sectores_comunas_med_1["type"] = "Comuna"

#     # + corregimientos
#     data = {"name": corregimientos["Name"]}
#     sectores_corr_med_1 = pd.DataFrame(data)
#     sectores_corr_med_1["type"] = "Corregimiento"

#     # + veredas
#     data = {"name": veredas["Name"]}
#     sectores_veredas_v_aburra = pd.DataFrame(data)
#     sectores_veredas_v_aburra["type"] = "Vereda"

#     sectores = pd.concat(
#         [
#             sectores_punto_interes,
#             sectores_municipio,
#             sectores_barrios,
#             sectores_comunas_med_1,
#             sectores_corr_med_1,
#             sectores_veredas_v_aburra,
#         ]
#     )
#     # sectores.drop_duplicates(subset=["name"], inplace=True)

#     return sectores


# def get_order(type_sector: str):
#     """
#     Devuelve el orden asociado a un tipo de sector.

#     Args:
#         type_sector (str): Tipo de sector (e.g., "Municipio", "Barrio").

#     Returns:
#         int: Orden del tipo de sector.
#     """
#     map_order = {
#         "Municipio": 0,
#         "Barrio": 1,
#         "Vereda": 2,
#         "Comuna": 3,
#         "Corregimiento": 4,
#         "Lugar": 5,
#     }
#     return map_order.get(type_sector, None)


# # update_field_reference_sector
# def get_field_reference_sector() -> Union[pd.DataFrame, gpd.GeoDataFrame]:
#     """
#     Asocia puntos de interes de tabla sectors con un barrio, manteniendo
#     el id del barrio al que pertenece cada punto de interes.
#     """
#     puntos_interes, barrios, veredas, _, _, _ = get_georeferenced_layers()
#     sectors = QuerysSector.select_all()
#     sectors = list_obj_to_df(sectors)

#     # obtener referencia de secrot para barrios
#     field_sector_reference = get_field_sector_reference_barrio(puntos_interes, barrios).drop_duplicates(subset=["Name"]).dropna(subset=["Barrio"])

#     field_sector_reference = field_sector_reference.merge(sectors, left_on="Barrio", right_on="name", how="left").rename(columns={"id": "reference_sector_1", "type": "type_reference"})

#     field_sector_reference = field_sector_reference[field_sector_reference["type_reference"] == "Barrio"]

#     sectors["reference_sector_1"] = None
#     for index, row in field_sector_reference.iterrows():
#         lugar = row["Name"]
#         id_barrio = row["reference_sector_1"]
#         sectors.loc[
#             (sectors["name"] == lugar) & (sectors["type"] == "Lugar"),
#             "reference_sector_1",
#         ] = id_barrio

#     # ===========================
#     # obtener referencia de secrot para veredas
#     field_sector_reference = get_field_sector_reference_vereda(puntos_interes, veredas).drop_duplicates(subset=["Name"]).dropna(subset=["Vereda"])

#     field_sector_reference = field_sector_reference.merge(sectors, left_on="Vereda", right_on="name", how="left").rename(columns={"id": "reference_sector_2", "type": "type_reference"})

#     field_sector_reference = field_sector_reference[field_sector_reference["type_reference"] == "Vereda"]

#     sectors["reference_sector_2"] = None
#     for index, row in field_sector_reference.iterrows():
#         lugar = row["Name"]
#         id_vereda = row["reference_sector_2"]
#         sectors.loc[
#             (sectors["name"] == lugar) & (sectors["type"] == "Lugar"),
#             "reference_sector_2",
#         ] = id_vereda

#     # sectors["reference_sector"] = sectors["reference_sector_1"].fillna(sectors["reference_sector_2"])
#     # sectors.drop(columns=["reference_sector_1", "reference_sector_2"], inplace= True)

#     sectors.loc[:, "reference_sector"] = sectors.apply(lambda x: x["reference_sector_1"] if not pd.isna(x["reference_sector_1"]) else (x["reference_sector_2"] if not pd.isna(x["reference_sector_2"]) else None), axis=1)

#     sectors.drop(columns=["reference_sector_1", "reference_sector_2"], inplace=True)

#     sectors_lugar = sectors[sectors["type"] == "Lugar"]
#     records = df_to_dicts(sectors_lugar)
#     for record in records:
#         QuerysSector.update_by_id(record, record.get("id"))

#     return sectors


# def get_slug(
#     sectors: Union[pd.DataFrame, gpd.GeoDataFrame],
# ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
#     """
#     Genera un identificador único (slug) para cada sector.

#     Args:
#         sectors (Union[pd.DataFrame, gpd.GeoDataFrame]): Datos de los sectores.

#     Returns:
#         Union[pd.DataFrame, gpd.GeoDataFrame]: DataFrame con slugs generados.
#     """
#     sectors["slug"] = (
#         sectors["type"] + " en " + sectors["name"]  # + "-" + sectors["id"].astype(str)
#     )
#     sectors["slug"] = sectors["slug"].apply(generate_slug)

#     return sectors


# def remove_key_words(text: str):
#     if not isinstance(text, str):
#         return text
#     key_words = ["el", "del", "la", "los", "las", "de", "y"]
#     words = text.lower().strip().split(" ")
#     words_ = words.copy()
#     state = False
#     for word in words:
#         if word in key_words:
#             words_.remove(word)
#             state = True
#     if state:
#         new_text = text + "|" + " ".join(words_)
#         return new_text
#     return text


# def transform_data_for_sectors(
#     sectors: Union[pd.DataFrame, gpd.GeoDataFrame],
# ) -> Union[pd.DataFrame, gpd.GeoDataFrame]:
#     """
#     Transforma datos de sectores, asignando identificadores únicos, slugs, y un orden por tipo.

#     Args:
#         sectors (Union[pd.DataFrame, gpd.GeoDataFrame]): Datos de los sectores.

#     Returns:
#         Union[pd.DataFrame, gpd.GeoDataFrame]: Datos transformados de los sectores.
#     """
#     # sectors["id"] = np.arange(1, sectors.shape[0] + 1)  # primary key
#     sectors["searcher"] = sectors["name"].apply(remove_key_words)
#     sectors = get_slug(sectors)
#     sectors["order"] = sectors["type"].apply(get_order)
#     return sectors


# def load_sectors():
#     """
#     Carga y procesa todas las capas geográficas, unifica datos y los inserta en la base
#     de datos como sectores.

#     Returns:
#         bool: Indica si el proceso fue exitoso.
#     """
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios = get_georeferenced_layers()

#     total_reg = puntos_interes.shape[0] + barrios.shape[0] + veredas.shape[0] + comunas.shape[0] + corregimientos.shape[0] + municipios.shape[0]

#     # obtener referencia de sectores
#     reference_lugar = get_reference_for_lugar(puntos_interes, barrios, veredas, comunas, corregimientos, municipios)[["Name", "apellido", "category_point_interest"]]
#     reference_lugar["type"] = "Lugar"

#     reference_barrios = get_reference_for_barrio(barrios, comunas, corregimientos, municipios, veredas)[["Name", "apellido"]]
#     reference_barrios["type"] = "Barrio"

#     reference_veredas = get_reference_for_vereda(veredas, comunas, corregimientos, municipios)[["Name", "apellido"]]
#     reference_veredas["type"] = "Vereda"

#     reference_comunas = get_reference_for_comuna(comunas, municipios)[["Name", "apellido"]]
#     reference_comunas["type"] = "Comuna"

#     reference_corregimientos = get_reference_for_corregimiento(corregimientos, municipios)[["Name", "apellido"]]
#     reference_corregimientos["type"] = "Corregimiento"

#     municipios["apellido"] = ""
#     municipios["type"] = "Municipio"
#     municipios = municipios[["Name", "apellido", "type"]]

#     sectors = pd.concat(
#         [
#             reference_lugar,
#             reference_barrios,
#             reference_veredas,
#             reference_comunas,
#             reference_corregimientos,
#             municipios,
#         ]
#     ).rename(columns={"Name": "name", "apellido": "sector"})

#     sectors = transform_data_for_sectors(sectors)

#     # assert sectors.shape[0] == total_reg

#     records = df_to_dicts(sectors)
#     QuerysSector.bulk_insert(records)

#     get_field_reference_sector()

#     return True


# def update_sectors():
#     """
#     Carga y procesa todas las capas geográficas, unifica datos y los inserta en la base
#     de datos como sectores.

#     Returns:
#         bool: Indica si el proceso fue exitoso.
#     """
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios = get_georeferenced_layers()

#     total_reg = puntos_interes.shape[0] + barrios.shape[0] + veredas.shape[0] + comunas.shape[0] + corregimientos.shape[0] + municipios.shape[0]

#     # obtener referencia de sectores
#     reference_lugar = get_reference_for_lugar(puntos_interes, barrios, veredas, comunas, corregimientos, municipios)[["Name", "apellido", "category_point_interest"]]
#     reference_lugar["type"] = "Lugar"

#     reference_barrios = get_reference_for_barrio(barrios, comunas, corregimientos, municipios, veredas)[["Name", "apellido"]]
#     reference_barrios["type"] = "Barrio"

#     reference_veredas = get_reference_for_vereda(veredas, comunas, corregimientos, municipios)[["Name", "apellido"]]
#     reference_veredas["type"] = "Vereda"

#     reference_comunas = get_reference_for_comuna(comunas, municipios)[["Name", "apellido"]]
#     reference_comunas["type"] = "Comuna"

#     reference_corregimientos = get_reference_for_corregimiento(corregimientos, municipios)[["Name", "apellido"]]
#     reference_corregimientos["type"] = "Corregimiento"

#     municipios["apellido"] = ""
#     municipios["type"] = "Municipio"
#     municipios = municipios[["Name", "apellido", "type"]]

#     sectors = pd.concat(
#         [
#             reference_lugar,
#             reference_barrios,
#             reference_veredas,
#             reference_comunas,
#             reference_corregimientos,
#             municipios,
#         ]
#     ).rename(columns={"Name": "name", "apellido": "sector"})

#     sectors = transform_data_for_sectors(sectors)

#     sectors_new = sectors.copy()
#     sectors_db = QuerysSector.select_all()
#     sectors_db = list_obj_to_df(sectors_db)

#     if sectors_db.empty:
#         records = df_to_dicts(sectors_new)
#         QuerysSector.bulk_insert(records)
#         return

#     sectors_db_lugar = pd.DataFrame(data=sectors_db.loc[(sectors_db["type"] == "Lugar"), "name"], columns=["name"])
#     sectors_new_lugar = sectors_new.loc[(sectors_new["type"] == "Lugar")]
#     merge_lugar = sectors_db_lugar.merge(sectors_new_lugar, on="name", how="outer", indicator=True)
#     merge_lugar = merge_lugar[merge_lugar["_merge"] == "right_only"].drop(columns=["_merge"])
#     merge_lugar = merge_lugar[merge_lugar["name"].notnull()]
#     merge_lugar = merge_lugar[(merge_lugar["name"] != "")]
#     records = df_to_dicts(merge_lugar)
#     QuerysSector.bulk_insert(records)

#     sectors_db_barrio = pd.DataFrame(data=sectors_db.loc[(sectors_db["type"] == "Barrio"), "name"], columns=["name"])
#     sectors_new_barrio = sectors_new.loc[(sectors_new["type"] == "Barrio")]
#     merge_barrio = sectors_db_barrio.merge(sectors_new_barrio, on="name", how="outer", indicator=True)
#     merge_barrio = merge_barrio[merge_barrio["_merge"] == "right_only"].drop(columns=["_merge"])
#     merge_barrio = merge_barrio[merge_barrio["name"].notnull()]
#     merge_barrio = merge_barrio[(merge_barrio["name"] != "")]
#     records = df_to_dicts(merge_barrio)
#     QuerysSector.bulk_insert(records)

#     get_field_reference_sector()

#     sectors.to_excel("merge_name.xlsx", index=False)

#     return True


# def update_shows_from_table_sectors():
#     """
#     Actualiza los shows de las tablas de sectores con los datos de visualización asociados a
#     propiedades disponibles en zonas georeferenciadas.
#     """

#     records = QuerysPropertySector.select_all()
#     property_sector = list_obj_to_df(records)
#     records = QuerysProperty.select_all()
#     property = list_obj_to_df(records)[
#         [
#             "id",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#             "show_rent_villacruz",
#             "show_sale_villacruz",
#             "show_furnished_villacruz",
#             "show_rent_castillo",
#             "show_sale_castillo",
#             "show_furnished_castillo",
#             "show_rent_estrella",
#             "show_sale_estrella",
#             "show_furnished_estrella",
#             "show_rent_livin",
#             "show_sale_livin",
#             "show_furnished_livin",
#         ]
#     ].rename(columns={"id": "property_id"})
#     records = QuerysSector.select_all()
#     sectors = list_obj_to_df(records)[["id", "name"]].rename(columns={"id": "sector_id"})

#     # Solo llenamos los show missinf con False
#     property = property.fillna(False)

#     merge = property.merge(property_sector, on="property_id", how="inner").merge(sectors, on="sector_id", how="inner")[
#         [
#             "sector_id",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#             "show_rent_villacruz",
#             "show_sale_villacruz",
#             "show_furnished_villacruz",
#             "show_rent_castillo",
#             "show_sale_castillo",
#             "show_furnished_castillo",
#             "show_rent_estrella",
#             "show_sale_estrella",
#             "show_furnished_estrella",
#             "show_rent_livin",
#             "show_sale_livin",
#             "show_furnished_livin",
#         ]
#     ]

#     sectors_update = merge.groupby("sector_id", as_index=False).agg(
#         {
#             "show_villacruz": "max",
#             "show_castillo": "max",
#             "show_estrella": "max",
#             "show_livin": "max",
#             "show_rent_villacruz": "max",
#             "show_sale_villacruz": "max",
#             "show_furnished_villacruz": "max",
#             "show_rent_castillo": "max",
#             "show_sale_castillo": "max",
#             "show_furnished_castillo": "max",
#             "show_rent_estrella": "max",
#             "show_sale_estrella": "max",
#             "show_furnished_estrella": "max",
#             "show_rent_livin": "max",
#             "show_sale_livin": "max",
#             "show_furnished_livin": "max",
#         }
#     )

#     update_villacruz = sectors_update[sectors_update["show_villacruz"]]
#     update_castillo = sectors_update[sectors_update["show_castillo"]]
#     update_estrella = sectors_update[sectors_update["show_estrella"]]
#     update_livin = sectors_update[sectors_update["show_livin"]]
#     show_rent_villacruz = sectors_update[sectors_update["show_rent_villacruz"]]
#     show_sale_villacruz = sectors_update[sectors_update["show_sale_villacruz"]]
#     show_furnished_villacruz = sectors_update[sectors_update["show_furnished_villacruz"]]
#     show_rent_castillo = sectors_update[sectors_update["show_rent_castillo"]]
#     show_sale_castillo = sectors_update[sectors_update["show_sale_castillo"]]
#     show_furnished_castillo = sectors_update[sectors_update["show_furnished_castillo"]]
#     show_rent_estrella = sectors_update[sectors_update["show_rent_estrella"]]
#     show_sale_estrella = sectors_update[sectors_update["show_sale_estrella"]]
#     show_furnished_estrella = sectors_update[sectors_update["show_furnished_estrella"]]
#     show_rent_livin = sectors_update[sectors_update["show_rent_livin"]]
#     show_sale_livin = sectors_update[sectors_update["show_sale_livin"]]
#     show_furnished_livin = sectors_update[sectors_update["show_furnished_livin"]]

#     QuerysSector.update_all_by_filter(Sector.show_villacruz == 1, {"show_villacruz": 0})
#     QuerysSector.update_all_by_filter(Sector.show_castillo == 1, {"show_castillo": 0})
#     QuerysSector.update_all_by_filter(Sector.show_estrella == 1, {"show_estrella": 0})
#     QuerysSector.update_all_by_filter(Sector.show_livin == 1, {"show_livin": 0})

#     QuerysSector.update_all_by_filter(Sector.show_rent_villacruz == 1, {"show_rent_villacruz": 0})
#     QuerysSector.update_all_by_filter(Sector.show_sale_villacruz == 1, {"show_sale_villacruz": 0})
#     QuerysSector.update_all_by_filter(Sector.show_furnished_villacruz == 1, {"show_furnished_villacruz": 0})
#     QuerysSector.update_all_by_filter(Sector.show_rent_castillo == 1, {"show_rent_castillo": 0})
#     QuerysSector.update_all_by_filter(Sector.show_sale_castillo == 1, {"show_sale_castillo": 0})
#     QuerysSector.update_all_by_filter(Sector.show_furnished_castillo == 1, {"show_furnished_castillo": 0})
#     QuerysSector.update_all_by_filter(Sector.show_rent_estrella == 1, {"show_rent_estrella": 0})
#     QuerysSector.update_all_by_filter(Sector.show_sale_estrella == 1, {"show_sale_estrella": 0})
#     QuerysSector.update_all_by_filter(Sector.show_furnished_estrella == 1, {"show_furnished_estrella": 0})
#     QuerysSector.update_all_by_filter(Sector.show_rent_livin == 1, {"show_rent_livin": 0})
#     QuerysSector.update_all_by_filter(Sector.show_sale_livin == 1, {"show_sale_livin": 0})
#     QuerysSector.update_all_by_filter(Sector.show_furnished_livin == 1, {"show_furnished_livin": 0})

#     QuerysSector.update_all_by_ids(update_villacruz["sector_id"], {"show_villacruz": True})
#     QuerysSector.update_all_by_ids(update_castillo["sector_id"], {"show_castillo": True})
#     QuerysSector.update_all_by_ids(update_estrella["sector_id"], {"show_estrella": True})
#     QuerysSector.update_all_by_ids(update_livin["sector_id"], {"show_livin": True})

#     QuerysSector.update_all_by_ids(show_rent_villacruz["sector_id"], {"show_rent_villacruz": True})
#     QuerysSector.update_all_by_ids(show_sale_villacruz["sector_id"], {"show_sale_villacruz": True})
#     QuerysSector.update_all_by_ids(show_furnished_villacruz["sector_id"], {"show_furnished_villacruz": True})
#     QuerysSector.update_all_by_ids(show_rent_castillo["sector_id"], {"show_rent_castillo": True})
#     QuerysSector.update_all_by_ids(show_sale_castillo["sector_id"], {"show_sale_castillo": True})
#     QuerysSector.update_all_by_ids(show_furnished_castillo["sector_id"], {"show_furnished_castillo": True})
#     QuerysSector.update_all_by_ids(show_rent_estrella["sector_id"], {"show_rent_estrella": True})
#     QuerysSector.update_all_by_ids(show_sale_estrella["sector_id"], {"show_sale_estrella": True})
#     QuerysSector.update_all_by_ids(show_furnished_estrella["sector_id"], {"show_furnished_estrella": True})
#     QuerysSector.update_all_by_ids(show_rent_livin["sector_id"], {"show_rent_livin": True})
#     QuerysSector.update_all_by_ids(show_sale_livin["sector_id"], {"show_sale_livin": True})
#     QuerysSector.update_all_by_ids(show_furnished_livin["sector_id"], {"show_furnished_livin": True})


# def update_category_name_from_sectors():
#     path_local = os.path.dirname(__file__)
#     path__file_category_point_interest = os.path.join(path_local, "..", "..", "sample_data", "categorias_puntos_interes.xlsx")
#     category_point_interest = pd.read_excel(path__file_category_point_interest)
#     if category_point_interest.empty:
#         return
#     filter_category_point_interest = category_point_interest[["Name", "Categoria"]]

#     records = QuerysSector.select_all()
#     sectors = list_obj_to_df(records)
#     filter_sectors = sectors.loc[sectors["type"] == "Lugar"]

#     merged = filter_category_point_interest.merge(filter_sectors, how="inner", left_on="Name", right_on="name", indicator=True)
#     merged.drop(columns=["Name", "category_point_interest"], inplace=True)
#     merged.rename(columns={"Categoria": "category_point_interest"}, inplace=True)

#     # podemos aca añadir filtros al df para obtener solo los secotores que queremos actualizar

#     if not merged.empty:
#         records = df_to_dicts(merged)
#         for record in records:
#             QuerysSector.update_by_id(record, record.get("id"))

#         print("Categorias de sectores type= 'Lugar' actualizadas")
#         return


# def get_processed_sectors() -> pd.DataFrame:
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios = get_georeferenced_layers()

#     # obtener referencia de sectores
#     reference_lugar = get_reference_for_lugar(puntos_interes, barrios, veredas, comunas, corregimientos, municipios)[["Name", "apellido", "category_point_interest"]]
#     reference_lugar["type"] = "Lugar"

#     reference_barrios = get_reference_for_barrio(barrios, comunas, corregimientos, municipios, veredas)[["Name", "apellido"]]
#     reference_barrios["type"] = "Barrio"

#     reference_veredas = get_reference_for_vereda(veredas, comunas, corregimientos, municipios)[["Name", "apellido"]]
#     reference_veredas["type"] = "Vereda"

#     reference_comunas = get_reference_for_comuna(comunas, municipios)[["Name", "apellido"]]
#     reference_comunas["type"] = "Comuna"

#     reference_corregimientos = get_reference_for_corregimiento(corregimientos, municipios)[["Name", "apellido"]]
#     reference_corregimientos["type"] = "Corregimiento"

#     municipios["apellido"] = ""
#     municipios["type"] = "Municipio"
#     municipios = municipios[["Name", "apellido", "type"]]

#     sectors = pd.concat(
#         [
#             reference_lugar,
#             reference_barrios,
#             reference_veredas,
#             reference_comunas,
#             reference_corregimientos,
#             municipios,
#         ]
#     ).rename(columns={"Name": "name", "apellido": "sector"})

#     sectors = transform_data_for_sectors(sectors)

#     return sectors


# def update_sectors_():
#     """
#     Actualiza la tabla de sectores comparando los sectores existentes en la base de datos con los nuevos sectores de origen.
#     Esta función realiza las siguientes operaciones:
#     1. Recupera todos los sectores existentes en la base de datos
#     2. Obtiene los sectores procesados de la fuente
#     3. Limpia los datos eliminando los nombres de sectores vacíos/nulos
#     4. Identifica nuevos sectores comparando la fuente con la base de datos
#     5. Inserta nuevos sectores si los encuentra
#     6. Recalcula la tabla de sectores de propiedad si se han realizado cambios
#     7. Devuelve:
#         Ninguno
#     Efectos secundarios:
#         - Inserta nuevos registros en la tabla sectores si se encuentran nuevos sectores
#         - Actualiza los registros de la tabla sectores_propiedad mediante el recálculo
#     """

#     records = QuerysSector.select_all()
#     db_sectors = list_obj_to_df(records)
#     source_sectors = get_processed_sectors()

#     db_sectors = db_sectors[db_sectors["name"].notna()].copy()
#     source_sectors = source_sectors[source_sectors["name"].notna()].copy()
#     db_sectors = db_sectors[db_sectors["name"] != ""].copy()
#     source_sectors = source_sectors[source_sectors["name"] != ""].copy()

#     merged = db_sectors.merge(source_sectors, how="outer", on=["name", "type"], indicator=True)

#     to_insert = merged[merged["_merge"] == "right_only"]
#     print(to_insert)
#     to_insert.to_excel("new_sectors_insert.xlsx")
#     if not to_insert.empty:
#         # insertar nuevos sectores
#         to_insert = source_sectors.loc[source_sectors["name"].isin(to_insert["name"]) & source_sectors["type"].isin(to_insert["type"])]
#         records = df_to_dicts(to_insert)
#         QuerysSector.bulk_insert(records)
#         # recalcular property_sectors
#         reload_property_sectors_table_records()
