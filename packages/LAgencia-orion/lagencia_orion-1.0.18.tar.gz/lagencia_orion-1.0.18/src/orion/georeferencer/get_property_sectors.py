# from typing import Tuple, Union

# import geopandas as gpd
# import pandas as pd
# from shapely.geometry import Point

# from orion.databases.db_empatia.models.model_searcher import PropertySector
# from orion.databases.db_empatia.repositories.querys_searcher import (
#     QuerysProperty,
#     QuerysPropertySector,
#     QuerysSector,
# )
# from orion.georeferencer.processing_data import get_georeferenced_layers
# from orion.tools import df_to_dicts, list_obj_to_df

# """_summary_: Obtiene todos los inmuebles que están a 500 metros de los puntos de
# interés definidos en la tabla 'sectors'.
# """


# def safe_point(row):
#     try:
#         lat = float(row["Latitud"])
#         lon = float(row["Longitud"])
#         return Point(lon, lat)
#     except (ValueError, TypeError):
#         return None


# def read_data_for_show_geometry_active_by_real_state():
#     """Lee y procesa datos de inmuebles desde la base de datos, convirtiendo los datos en un GeoDataFrame
#     con geometría para análisis geoespacial. También obtiene y procesa capas georreferenciadas de
#     diferentes divisiones territoriales.
#     El proceso incluye:
#     1. Lectura de datos de inmuebles desde la base de datos
#     2. Limpieza y transformación de datos
#     3. Creación de geometrías a partir de coordenadas
#     4. Carga de capas georreferenciadas (puntos de interés, barrios, veredas, etc.)
#     5. Transformación de sistemas de coordenadas
#         tuple: Contiene los siguientes elementos:
#             - inmuebles (GeoDataFrame): DataFrame con geometrías de inmuebles
#             - municipios (GeoDataFrame): Capa de municipios
#             - barrios (GeoDataFrame): Capa de barrios
#             - veredas (GeoDataFrame): Capa de veredas
#             - comunas (GeoDataFrame): Capa de comunas
#             - corregimientos (GeoDataFrame): Capa de corregimientos
#         Todos los GeoDataFrames están proyectados en EPSG:3116
#     """

#     # + prcocesamiento para los inmuebles
#     records = QuerysProperty.select_all()
#     inmuebles = list_obj_to_df(records)
#     if not inmuebles.empty:
#         inmuebles = inmuebles[
#             [
#                 "id",
#                 "code",
#                 "address",
#                 "latitude",
#                 "longitude",
#                 "show_villacruz",
#                 "show_castillo",
#                 "show_estrella",
#                 "show_livin",
#             ]
#         ]

#     inmuebles.rename(
#         columns={
#             "address": "Direccion",
#             "longitude": "Longitud",
#             "latitude": "Latitud",
#         },
#         inplace=True,
#     )

#     inmuebles = inmuebles[inmuebles["Latitud"].notna()]
#     inmuebles = inmuebles[inmuebles["Longitud"].notna()]

#     inmuebles = inmuebles[~inmuebles["Latitud"].isin([None, "None", "null", ""])]
#     inmuebles = inmuebles[~inmuebles["Longitud"].isin([None, "None", "null", ""])]

#     inmuebles["geometry"] = inmuebles.apply(safe_point, axis=1)

#     # inmuebles["geometry"] = inmuebles.apply(
#     #     lambda row: Point(row["Longitud"], row["Latitud"]), axis=1
#     # )

#     # Convertir el DataFrame de pandas en un GeoDataFrame
#     inmuebles = gpd.GeoDataFrame(inmuebles, geometry="geometry")
#     inmuebles.set_index("id")
#     inmuebles.set_crs("EPSG:4326", inplace=True)

#     # + Caegar de capas geometricas
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios = get_georeferenced_layers()

#     # + prepocesamiento capas geometricas
#     puntos_interes.set_index("Name", inplace=True)
#     puntos_interes.drop(columns="Description", inplace=True)

#     municipios.set_index("Name", inplace=True)
#     municipios.drop(columns="Description", inplace=True)

#     barrios.set_index("Name", inplace=True)
#     barrios.drop(columns="Description", inplace=True)

#     comunas.set_index("Name", inplace=True)
#     comunas.drop(columns="Description", inplace=True)

#     corregimientos.set_index("Name", inplace=True)
#     corregimientos.drop(columns="Description", inplace=True)

#     veredas.set_index("Name", inplace=True)
#     veredas.drop(columns="Description", inplace=True)

#     # * Cambio de sistema de cordenadas a EPSG:3116 para realizar calculos
#     puntos_interes.to_crs("EPSG:3116", inplace=True)

#     municipios.to_crs("EPSG:3116", inplace=True)

#     barrios.to_crs("EPSG:3116", inplace=True)

#     comunas.to_crs("EPSG:3116", inplace=True)

#     corregimientos.to_crs("EPSG:3116", inplace=True)

#     veredas.to_crs("EPSG:3116", inplace=True)

#     inmuebles.to_crs("EPSG:3116", inplace=True)

#     # * ===========================
#     inmuebles.rename(columns={"id": "property_id"}, inplace=True)
#     print("Cantidad de inmuebles en properties con latitud y longitud", inmuebles.shape)

#     return (inmuebles, municipios, barrios, veredas, comunas, corregimientos)


# def Relationship_between_properties_and_geometry(
#     properties: Union[pd.DataFrame, gpd.GeoDataFrame],
#     geometry: Union[pd.DataFrame, gpd.GeoDataFrame],
# ) -> Tuple[
#     Union[pd.DataFrame, gpd.GeoDataFrame],
#     Union[pd.DataFrame, gpd.GeoDataFrame],
#     Union[pd.DataFrame, gpd.GeoDataFrame],
# ]:
#     """
#     Relaciona propiedades inmobiliarias con geometrías (sectores) y determina diferentes clasificaciones.
#     Esta función toma dos DataFrames (propiedades y geometrías) y genera tres DataFrames diferentes:
#     1. Sectores activos por inmobiliaria
#     2. Propiedades dentro de geometrías
#     3. Propiedades aisladas (fuera de geometrías)
#     Args:
#         properties (Union[pd.DataFrame, gpd.GeoDataFrame]): DataFrame con la información de las propiedades inmobiliarias.
#             Debe contener las columnas: property_id, code, show_villacruz, show_castillo, show_estrella, show_livin,
#             Direccion, Latitud, Longitud.
#         geometry (Union[pd.DataFrame, gpd.GeoDataFrame]): DataFrame con la información geométrica de los sectores.
#             Debe contener una columna 'Name' que coincida con los nombres de los sectores.
#     Returns:
#         Tuple[Union[pd.DataFrame, gpd.GeoDataFrame], Union[pd.DataFrame, gpd.GeoDataFrame], Union[pd.DataFrame, gpd.GeoDataFrame]]:
#             Una tupla conteniendo tres DataFrames:
#             - show_geometry_active_by_real_state: Sectores que contienen propiedades activas por inmobiliaria
#             - properties_within_geometry: Propiedades que están dentro de alguna geometría/sector
#             - isoluted_properties: Propiedades que no están dentro de ninguna geometría/sector
#     """

#     records = QuerysSector.select_all()
#     sectors = list_obj_to_df(records)[["id", "name"]].rename(columns={"name": "Name"})

#     overlap = gpd.sjoin(properties, geometry, how="left", predicate="within")
#     merged = sectors.merge(overlap, on="Name", how="inner", indicator=True)
#     merged.rename(columns={"id": "sector_id"}, inplace=True)
#     merged = merged[
#         [
#             "Name",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#             "sector_id",
#             "property_id",
#             "code",
#         ]
#     ]

#     # * obtener sectores en los que hay inmubles
#     show_geometry_active_by_real_state = merged.groupby("Name", as_index=False).agg(
#         {
#             "show_villacruz": "max",
#             "show_castillo": "max",
#             "show_estrella": "max",
#             "show_livin": "max",
#         }
#     )
#     show_geometry_active_by_real_state = sectors.merge(show_geometry_active_by_real_state, on="Name", how="inner", indicator=True)
#     show_geometry_active_by_real_state = show_geometry_active_by_real_state[["id", "show_villacruz", "show_castillo", "show_estrella", "show_livin"]]

#     # * obtener dentro de una geometria
#     properties_within_geometry = merged[
#         [
#             "Name",
#             "sector_id",
#             "property_id",
#             "code",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#         ]
#     ]

#     # * inmuebles aislados
#     isoluted_properties = properties[
#         [
#             "property_id",
#             "code",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#             "Direccion",
#             "Latitud",
#             "Longitud",
#         ]
#     ].merge(
#         properties_within_geometry[["property_id"]],
#         on="property_id",
#         how="left",
#         indicator=True,
#     )
#     isoluted_properties = isoluted_properties[
#         [
#             "property_id",
#             "code",
#             "Direccion",
#             "Latitud",
#             "Longitud",
#             "show_villacruz",
#             "show_castillo",
#             "show_estrella",
#             "show_livin",
#             "_merge",
#         ]
#     ]
#     isoluted_properties = isoluted_properties[isoluted_properties["_merge"] == "left_only"].drop(columns=["_merge"])

#     return (
#         show_geometry_active_by_real_state,
#         properties_within_geometry,
#         isoluted_properties,
#     )


# def get_overlapping_properties_by_georeferenced_layers_for_property_sectors_table():
#     """Identifica propiedades que están dentro de un radio de 500 metros de puntos de interés georreferenciados.
#     Esta función realiza los siguientes pasos:
#     1. Obtiene datos de propiedades de la base de datos
#     2. Carga capas georreferenciadas (puntos de interés, barrios, veredas, etc.)
#     3. Realiza transformaciones de coordenadas a EPSG:3116
#     4. Calcula buffers de 500m alrededor de puntos de interés
#     5. Identifica propiedades dentro de estos buffers
#     6. Calcula distancias exactas entre propiedades y puntos de interés
#     7. Asocia sectores con las propiedades encontradas
#     Returns:
#         pandas.DataFrame: DataFrame con las columnas:
#             - property_id (int): ID de la propiedad
#             - sector_id (int): ID del sector asociado al punto de interés
#             - meters (float): Distancia en metros entre la propiedad y el punto de interés
#     Requiere:
#         - Conexión a base de datos con tablas de propiedades y sectores
#         - Archivos de capas georreferenciadas
#         - Bibliotecas: pandas, geopandas, shapely
#     Notas:
#         - Las coordenadas se transforman a EPSG:3116 para cálculos precisos en metros
#         - Solo se consideran propiedades dentro del radio de 500m de puntos de interés
#         - Se filtran resultados para incluir solo distancias válidas (tipo float)
#     """
#     # ! proceso properties_sector para inmuble <-500m-> pi

#     # data de DB
#     records = QuerysProperty.select_all()
#     inmuebles = list_obj_to_df(records)[["id", "address", "latitude", "longitude"]]

#     # + procesamiento de propiedades
#     inmuebles.rename(
#         columns={
#             "id": "Cod",
#             "address": "Direccion",
#             "longitude": "Longitud",
#             "latitude": "Latitud",
#         },
#         inplace=True,
#     )
#     inmuebles.dropna(inplace=True)
#     inmuebles = inmuebles[~inmuebles["Latitud"].isin([None, "None", "null", ""])]
#     inmuebles = inmuebles[~inmuebles["Longitud"].isin([None, "None", "null", ""])]

#     inmuebles["geometry"] = inmuebles.apply(safe_point, axis=1)

#     # inmuebles["geometry"] = inmuebles.apply(
#     #     lambda row: Point(row["Longitud"], row["Latitud"]), axis=1
#     # )

#     # Convertir el DataFrame de pandas en un GeoDataFrame
#     inmuebles = gpd.GeoDataFrame(inmuebles, geometry="geometry")
#     inmuebles.set_index("Cod")
#     inmuebles.set_crs("EPSG:4326", inplace=True)

#     # lectura de capas geograficas
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios = get_georeferenced_layers()

#     # + prepocesamiento de capas geograficas
#     puntos_interes.set_index("Name", inplace=True)
#     puntos_interes.drop(columns="Description", inplace=True)

#     municipios.set_index("Name", inplace=True)
#     municipios.drop(columns="Description", inplace=True)

#     barrios.set_index("Name", inplace=True)
#     barrios.drop(columns="Description", inplace=True)

#     comunas.set_index("Name", inplace=True)
#     comunas.drop(columns="Description", inplace=True)

#     corregimientos.set_index("Name", inplace=True)
#     corregimientos.drop(columns="Description", inplace=True)

#     veredas.set_index("Name", inplace=True)
#     veredas.drop(columns="Description", inplace=True)

#     # Cambio de sistema de cordenadas a EPSG:3116 para realizar calculos
#     puntos_interes.to_crs("EPSG:3116", inplace=True)
#     municipios.to_crs("EPSG:3116", inplace=True)
#     barrios.to_crs("EPSG:3116", inplace=True)
#     comunas.to_crs("EPSG:3116", inplace=True)
#     corregimientos.to_crs("EPSG:3116", inplace=True)
#     veredas.to_crs("EPSG:3116", inplace=True)
#     inmuebles.to_crs("EPSG:3116", inplace=True)

#     # calcular buffer de 500m para los puntos de interes
#     puntos_interes["buffer_500m"] = puntos_interes.geometry.buffer(500)

#     # Crear un GeoDataFrame con los buffers calculados
#     buffers = puntos_interes[["buffer_500m"]].copy()
#     buffers = buffers.set_geometry("buffer_500m")

#     inmuebles_en_buffers = gpd.sjoin(inmuebles, buffers, how="inner", predicate="within")
#     inmuebles_en_buffers.rename(columns={"Name": "PI"}, inplace=True)

#     pi_en_municipio = gpd.sjoin(inmuebles_en_buffers, municipios, how="inner", predicate="within")
#     pi_en_municipio.rename(columns={"Name": "Municipio"}, inplace=True)

#     # Asociar geometría del punto de interés basado en 'PI'
#     pi_en_municipio["geometry_pi"] = pi_en_municipio["PI"].apply(lambda pi_name: puntos_interes.loc[pi_name, "geometry"] if pi_name in puntos_interes.index else None)

#     # Calcular la distancia entre inmuebles y puntos de interés
#     pi_en_municipio["distancia"] = pi_en_municipio.apply(
#         lambda row: row.geometry.distance(row.geometry_pi) if row.geometry_pi is not None else None,
#         axis=1,
#     )

#     property_sectors = pi_en_municipio[["Cod", "distancia", "PI"]].copy().rename(columns={"Cod": "property_id", "PI": "name", "distancia": "meters"})

#     # + lectura de sectores
#     # data de DB
#     records = QuerysSector.select_all()
#     sectors = list_obj_to_df(records)
#     sectors = sectors[["id", "name"]].rename(columns={"id": "sector_id"})

#     # + identificacion de merge

#     merged = property_sectors.merge(sectors, on="name")[["property_id", "sector_id", "meters"]]

#     filter = merged["meters"].apply(lambda x: type(x) is float)
#     merged = merged[filter]

#     return merged


# def get_overlapping_properties_with_georeferenced_layers():
#     """
#     Obtiene las propiedades que se superponen con capas georreferenciadas.
#     Esta función lee datos geométricos de propiedades inmuebles y diferentes divisiones
#     administrativas (municipios, comunas, corregimientos, barrios y veredas), y encuentra
#     las relaciones de superposición entre ellos.
#     Returns:
#         pandas.DataFrame: DataFrame con dos columnas:
#             - sector_id: ID del sector administrativo (municipio, comuna, etc.)
#             - property_id: ID de la propiedad que se encuentra dentro del sector
#     Notas:
#         - La función concatena los resultados de las superposiciones con todas las
#           divisiones administrativas en un solo DataFrame
#         - Solo conserva las columnas sector_id y property_id del resultado final
#         - Utiliza la función auxiliar Relationship_between_properties_and_geometry para
#           calcular las relaciones espaciales
#     """
#     inmuebles, municipios, barrios, veredas, comunas, corregimientos = read_data_for_show_geometry_active_by_real_state()

#     show_municipios, properties_within_muncipios, isoluted_properties_by_municipio = Relationship_between_properties_and_geometry(inmuebles, municipios)

#     show_comunas, properties_within_comunas, isoluted_properties_by_comunas = Relationship_between_properties_and_geometry(inmuebles, comunas)

#     (
#         show_corregimientos,
#         properties_within_corregimientos,
#         isoluted_properties_by_corregimientos,
#     ) = Relationship_between_properties_and_geometry(inmuebles, corregimientos)

#     show_barrios, properties_within_barrios, isoluted_properties_by_barrios = Relationship_between_properties_and_geometry(inmuebles, barrios)

#     show_veredas, properties_within_veredas, isoluted_properties_by_veredas = Relationship_between_properties_and_geometry(inmuebles, veredas)

#     properties_within_muncipios = properties_within_muncipios[["sector_id", "property_id"]]
#     properties_within_comunas = properties_within_comunas[["sector_id", "property_id"]]
#     properties_within_corregimientos = properties_within_corregimientos[["sector_id", "property_id"]]
#     properties_within_barrios = properties_within_barrios[["sector_id", "property_id"]]
#     properties_within_veredas = properties_within_veredas[["sector_id", "property_id"]]

#     properties_within_sector = pd.concat([properties_within_muncipios, properties_within_comunas, properties_within_corregimientos, properties_within_barrios, properties_within_veredas])

#     return properties_within_sector


# def get_georeference_association_for_table_property_sectors() -> pd.DataFrame:
#     """
#     Obtiene la asociación georreferenciada para la tabla de sectores de propiedades.
#     Esta función combina dos conjuntos de datos:
#     1. Propiedades que están dentro de un radio de 500m de puntos de interés
#     2. Propiedades que se superponen con capas georreferenciadas (barrios, veredas, comunas, corregimientos, municipios)
#     Returns:
#         pd.DataFrame: DataFrame combinado que contiene todas las propiedades georreferenciadas
#                      con sus respectivas asociaciones a sectores y puntos de interés.
#     """

#     # obtiene inmuebles a 500m de los puntos de interes
#     properties_within_500m_of_points_of_interest = get_overlapping_properties_by_georeferenced_layers_for_property_sectors_table()

#     # obtiene los inmuebles que estan dentro de (barrios, veredas, comunas, corregimientos, municipios)
#     overlapping_properties_with_georeferenced_layers = get_overlapping_properties_with_georeferenced_layers()

#     return pd.concat([overlapping_properties_with_georeferenced_layers, properties_within_500m_of_points_of_interest])


# def insert_records_in_table_property_sectors_for_properties(properties_ids: pd.Series):
#     """
#     Actualiza las asociaciones entre inmuebles y sectores geográficos utilizando
#     relaciones espaciales. Procesa datos de la base de datos, calcula distancias a
#     puntos de interés y clasifica inmuebles según sectores.

#     Además, asocia inmuebles a municipios, comunas, corregimientos, barrios y veredas,
#     y actualiza la base de datos con estos resultados.
#     """

#     combined_georeferenced_properties = get_georeference_association_for_table_property_sectors()

#     if combined_georeferenced_properties.empty:
#         return

#     to_insert = combined_georeferenced_properties[combined_georeferenced_properties["property_id"].isin(properties_ids)]

#     if not to_insert.empty:
#         print("Registros para insertar en property_sectors para propiedades nuevas: ", to_insert.shape)
#         records = df_to_dicts(to_insert)
#         QuerysPropertySector.bulk_insert(records)
#         return True


# def update_records_table_property_sectors_for_properties(properties_ids: pd.Series):
#     for id_ in properties_ids:
#         QuerysPropertySector.delete_by_filter(PropertySector.property_id == id_)

#     insert_records_in_table_property_sectors_for_properties(properties_ids)
#     return True


# def recalculate_property_sectors_table_records():
#     """
#     Recalcula y actualiza los registros en la tabla property_sectors.
#     Esta función realiza una actualización de la tabla property_sectors comparando los registros
#     existentes con nuevas georeferenciaciones de propiedades. Si se encuentran nuevas asociaciones
#     entre propiedades y sectores, estas son insertadas en la tabla.
#     Returns:
#         bool: Retorna True si se insertaron nuevos registros, None en caso contrario
#     Proceso:
#     1. Obtiene las georeferenciaciones actuales de propiedades
#     2. Si no hay georeferenciaciones, termina la función
#     3. Obtiene los registros actuales de property_sectors
#     4. Realiza un merge para identificar nuevos registros
#     5. Inserta los nuevos registros encontrados en la tabla property_sectors
#     Dependencias:
#         - get_georeference_association_for_table_property_sectors()
#         - QuerysPropertySector
#         - list_obj_to_df()
#         - df_to_dicts()
#     """
#     combined_georeferenced_properties = get_georeference_association_for_table_property_sectors()
#     print(combined_georeferenced_properties)

#     if combined_georeferenced_properties.empty:
#         return True

#     records = QuerysPropertySector.select_all()
#     property_sectors = list_obj_to_df(records)
#     print(combined_georeferenced_properties)
#     if property_sectors.empty:
#         print("Registros para insertar en property_sectors para sectores nuevos: ", property_sectors.shape)
#         records = df_to_dicts(combined_georeferenced_properties)
#         QuerysPropertySector.bulk_insert(records)
#         return True

#     merged = property_sectors.merge(combined_georeferenced_properties, how="outer", on=["sector_id", "property_id"], indicator=True)

#     to_insert = merged[merged["_merge"] == "right_only"].drop(columns=["id", "_merge", "meters_x"]).rename(columns={"meters_y": "meters"})

#     if not to_insert.empty:
#         print("Registros para insertar en property_sectors para sectores nuevos: ", to_insert.shape)
#         records = df_to_dicts(to_insert)
#         QuerysPropertySector.bulk_insert(records)
#         return True


# def reload_property_sectors_table_records():
#     """
#     Recarga todos los registros de la tabla de sectores de propiedades.
#     Esta función realiza dos operaciones principales:
#     1. Elimina todos los registros existentes de la tabla de sectores de propiedades
#     2. Recalcula y vuelve a insertar todos los registros de sectores de propiedades
#     Returns:
#         bool: True si la operación se completa exitosamente
#     Raises:
#         Puede levantar excepciones derivadas de las operaciones de base de datos
#     """

#     QuerysPropertySector.delete_all()

#     recalculate_property_sectors_table_records()
#     return True
