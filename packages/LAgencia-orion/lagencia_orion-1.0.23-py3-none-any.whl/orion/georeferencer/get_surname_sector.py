# import geopandas as gpd
# import pandas as pd

# from orion.tools import normalize_commas, remove_leading_comma_space, replace_dot_comma

# """
# Resumen: Este módulo proporciona funciones para obtener referencias geográficas de
# diferentes capas (lugares, barrios, veredas, comunas, corregimientos, municipios) y
# asignarlas a un campo 'sector' de la tabla sectors. Las funciones incluyen validaciones
# del sistema de coordenadas y procesamiento de geometrías.
# """

# def get_centroide(gdf: gpd.GeoDataFrame):
#     """
#     Calcula el centroide de cada geometría en un GeoDataFrame, transformando el
#     sistema de coordenadas a EPSG:3116 y luego regresándolo a EPSG:4326.

#     Args:
#         gdf (gpd.GeoDataFrame): GeoDataFrame con geometrías.

#     Returns:
#         gpd.GeoDataFrame: GeoDataFrame con centroides calculados.
#     """
#     gdf.to_crs("EPSG:3116", inplace=True)
#     gdf["geometry"] = gdf.geometry.centroid
#     gdf.to_crs("EPSG:4326", inplace=True)
#     return gdf


# def get_reference_for_lugar(
#     puntos_interes, barrios, veredas, comunas, corregimientos, municipios
# ):
#     """
#     Obtiene referencias geográficas asociadas a puntos de interés dentro de diferentes
#     capas como barrios, veredas, comunas, corregimientos y municipios.

#     Args:
#         puntos_interes (gpd.GeoDataFrame): GeoDataFrame de puntos de interés.
#         barrios (gpd.GeoDataFrame): GeoDataFrame de barrios.
#         veredas (gpd.GeoDataFrame): GeoDataFrame de veredas.
#         comunas (gpd.GeoDataFrame): GeoDataFrame de comunas.
#         corregimientos (gpd.GeoDataFrame): GeoDataFrame de corregimientos.
#         municipios (gpd.GeoDataFrame): GeoDataFrame de municipios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias y nombres geográficos procesados.
#     """

#     # barrios
#     ref = gpd.sjoin(puntos_interes, barrios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Barrio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Barrio", "geometry", "category_point_interest"]]

#     # veredas
#     ref = gpd.sjoin(ref, veredas, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Vereda", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Barrio", "Vereda", "geometry", "category_point_interest"]]

#     # comuna
#     ref = gpd.sjoin(ref, comunas, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Comuna", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Barrio", "Vereda", "Comuna", "geometry", "category_point_interest"]]

#     # corregimiento
#     ref = gpd.sjoin(ref, corregimientos, how="left", predicate="within")
#     ref.rename(
#         columns={"Name_right": "Corregimiento", "Name_left": "Name"}, inplace=True
#     )
#     ref = ref[["Name", "Barrio", "Vereda", "Comuna", "Corregimiento", "geometry", "category_point_interest"]]

#     # municipio
#     ref = gpd.sjoin(ref, municipios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Municipio", "Name_left": "Name"}, inplace=True)
#     ref = ref[
#         ["Name", "Barrio", "Vereda", "Comuna", "Corregimiento", "Municipio", "geometry", "category_point_interest"]
#     ]

#     ref["Name"] = ref["Name"].astype(str)
#     ref["Barrio"] = ref["Barrio"].astype(str)
#     ref["Vereda"] = ref["Vereda"].astype(str)
#     ref["Comuna"] = ref["Comuna"].astype(str)
#     ref["Corregimiento"] = ref["Corregimiento"].astype(str)
#     ref["Municipio"] = ref["Municipio"]

#     ref = ref.replace("nan", "")
#     ref["apellido"] = (
#         ref["Barrio"]
#         + ","
#         + ref["Vereda"]
#         + ","
#         + ref["Comuna"]
#         + ","
#         + ref["Corregimiento"]
#         + ","
#         + ref["Municipio"]
#     )

#     ref["apellido"] = pd.DataFrame(ref)["apellido"].apply(normalize_commas)
#     ref["apellido"] = ref["apellido"].apply(remove_leading_comma_space)
#     ref["apellido"] = ref["apellido"].apply(replace_dot_comma)
#     ref.drop_duplicates(subset=["Name"], inplace=True)

#     return ref


# def get_reference_for_barrio(barrios, comunas, corregimientos, municipios, veredas):
#     """
#     Obtiene referencias geográficas para barrios dentro de comunas, corregimientos,
#     municipios y veredas.

#     Args:
#         barrios (gpd.GeoDataFrame): GeoDataFrame de barrios.
#         comunas (gpd.GeoDataFrame): GeoDataFrame de comunas.
#         corregimientos (gpd.GeoDataFrame): GeoDataFrame de corregimientos.
#         municipios (gpd.GeoDataFrame): GeoDataFrame de municipios.
#         veredas (gpd.GeoDataFrame): GeoDataFrame de veredas.

#     Returns:
#         pd.DataFrame: DataFrame con referencias procesadas.
#     """
#     if not (barrios.crs == comunas.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Comunas")
#         return barrios

#     if not (barrios.crs == corregimientos.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Corregimientos")
#         return barrios

#     if not (barrios.crs == municipios.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Municipios")
#         return barrios

#     if not (barrios.crs == veredas.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Veredas")
#         return barrios

#     barrios = get_centroide(barrios)

#     # comuna
#     ref = gpd.sjoin(barrios, comunas, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Comuna", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Comuna", "geometry"]]

#     # corregimiento
#     ref = gpd.sjoin(ref, corregimientos, how="left", predicate="within")
#     ref.rename(
#         columns={"Name_right": "Corregimiento", "Name_left": "Name"}, inplace=True
#     )
#     ref = ref[["Name", "Comuna", "Corregimiento", "geometry"]]

#     # municipio
#     ref = gpd.sjoin(ref, municipios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Municipio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Comuna", "Corregimiento", "Municipio", "geometry"]]

#     # veredas
#     ref = gpd.sjoin(ref, veredas, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Vereda", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Vereda", "Comuna", "Corregimiento", "Municipio", "geometry"]]

#     ref["Name"] = ref["Name"].astype(str)
#     ref["Vereda"] = ref["Vereda"].astype(str)
#     ref["Comuna"] = ref["Comuna"].astype(str)
#     ref["Corregimiento"] = ref["Corregimiento"].astype(str)
#     ref["Municipio"] = ref["Municipio"]

#     ref = ref.replace("nan", "")
#     ref["apellido"] = (
#         ref["Vereda"]
#         + ","
#         + ref["Comuna"]
#         + ","
#         + ref["Corregimiento"]
#         + ","
#         + ref["Municipio"]
#     )
#     ref["apellido"] = pd.DataFrame(ref)["apellido"].apply(normalize_commas)
#     ref["apellido"] = ref["apellido"].apply(remove_leading_comma_space)
#     ref["apellido"] = ref["apellido"].apply(replace_dot_comma)
#     ref.drop_duplicates(subset=["Name"], inplace=True)

#     return ref


# def get_reference_for_vereda(vereda, comunas, corregimientos, municipios):
#     """
#     Obtiene referencias geográficas para veredas dentro de comunas, corregimientos
#     y municipios.

#     Args:
#         vereda (gpd.GeoDataFrame): GeoDataFrame de veredas.
#         comunas (gpd.GeoDataFrame): GeoDataFrame de comunas.
#         corregimientos (gpd.GeoDataFrame): GeoDataFrame de corregimientos.
#         municipios (gpd.GeoDataFrame): GeoDataFrame de municipios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias procesadas.
#     """
#     if not (vereda.crs == comunas.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Comunas")
#         return vereda

#     if not (vereda.crs == corregimientos.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Corregimientos")
#         return vereda

#     if not (vereda.crs == municipios.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Municipios")
#         return vereda

#     vereda = get_centroide(vereda)

#     # comuna
#     ref = gpd.sjoin(vereda, comunas, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Comuna", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Comuna", "geometry"]]

#     # corregimiento
#     ref = gpd.sjoin(ref, corregimientos, how="left", predicate="within")
#     ref.rename(
#         columns={"Name_right": "Corregimiento", "Name_left": "Name"}, inplace=True
#     )
#     ref = ref[["Name", "Comuna", "Corregimiento", "geometry"]]

#     # municipio
#     ref = gpd.sjoin(ref, municipios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Municipio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Comuna", "Corregimiento", "Municipio", "geometry"]]

#     ref["Name"] = ref["Name"].astype(str)
#     ref["Comuna"] = ref["Comuna"].astype(str)
#     ref["Corregimiento"] = ref["Corregimiento"].astype(str)
#     ref["Municipio"] = ref["Municipio"]

#     ref = ref.replace("nan", "")
#     ref["apellido"] = (
#         ref["Comuna"] + "," + ref["Corregimiento"] + "," + ref["Municipio"]
#     )
#     ref["apellido"] = pd.DataFrame(ref)["apellido"].apply(normalize_commas)
#     ref["apellido"] = ref["apellido"].apply(remove_leading_comma_space)
#     ref["apellido"] = ref["apellido"].apply(replace_dot_comma)
#     ref.drop_duplicates(subset=["Name"], inplace=True)

#     return ref


# def get_reference_for_comuna(comunas, municipios):
#     """
#     Obtiene referencias geográficas para comunas dentro de municipios.

#     Args:
#         comunas (gpd.GeoDataFrame): GeoDataFrame de comunas.
#         municipios (gpd.GeoDataFrame): GeoDataFrame de municipios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias procesadas.
#     """
#     if not (comunas.crs == municipios.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Municipios")
#         return comunas

#     comunas = get_centroide(comunas)

#     # municipio
#     ref = gpd.sjoin(comunas, municipios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Municipio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Municipio", "geometry"]]

#     ref["Name"] = ref["Name"].astype(str)
#     ref["Municipio"] = ref["Municipio"]

#     ref = ref.replace("nan", "")
#     ref["apellido"] = ref["Municipio"]

#     ref["apellido"] = pd.DataFrame(ref)["apellido"].apply(normalize_commas)
#     ref["apellido"] = ref["apellido"].apply(remove_leading_comma_space)
#     ref["apellido"] = ref["apellido"].apply(replace_dot_comma)
#     ref.drop_duplicates(subset=["Name"], inplace=True)
#     return ref


# def get_reference_for_corregimiento(corregimientos, municipios):
#     """
#     Obtiene referencias geográficas para corregimientos dentro de municipios.

#     Args:
#         corregimientos (gpd.GeoDataFrame): GeoDataFrame de corregimientos.
#         municipios (gpd.GeoDataFrame): GeoDataFrame de municipios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias procesadas.
#     """
#     if not (corregimientos.crs == municipios.crs):
#         print("Error: No coinciden el sistema de coordenadas Barrios:Municipios")
#         return corregimientos

#     corregimientos = get_centroide(corregimientos)

#     # municipio
#     ref = gpd.sjoin(corregimientos, municipios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Municipio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Municipio", "geometry"]]

#     ref["Name"] = ref["Name"].astype(str)
#     ref["Municipio"] = ref["Municipio"]

#     ref = ref.replace("nan", "")
#     ref["apellido"] = ref["Municipio"]

#     ref["apellido"] = pd.DataFrame(ref)["apellido"].apply(normalize_commas)
#     ref["apellido"] = ref["apellido"].apply(remove_leading_comma_space)
#     ref["apellido"] = ref["apellido"].apply(replace_dot_comma)
#     ref.drop_duplicates(subset=["Name"], inplace=True)

#     return ref


# def get_field_sector_reference_barrio(
#     puntos_interes: gpd.GeoDataFrame, barrios: gpd.GeoDataFrame
# )->pd.DataFrame:
#     """
#     Obtiene referencias de sectores para puntos de interés relacionados con barrios.

#     Args:
#         puntos_interes (gpd.GeoDataFrame): GeoDataFrame de puntos de interés.
#         barrios (gpd.GeoDataFrame): GeoDataFrame de barrios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias de sectores.
#     """

#     # barrios
#     ref = gpd.sjoin(puntos_interes, barrios, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Barrio", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Barrio"]]

#     return ref


# def get_field_sector_reference_vereda(
#     puntos_interes, vereda
# )->pd.DataFrame:
#     """
#     Obtiene referencias de sectores para puntos de interés relacionados con barrios.

#     Args:
#         puntos_interes (gpd.GeoDataFrame): GeoDataFrame de puntos de interés.
#         barrios (gpd.GeoDataFrame): GeoDataFrame de barrios.

#     Returns:
#         pd.DataFrame: DataFrame con referencias de sectores.
#     """

#     # barrios
#     ref = gpd.sjoin(puntos_interes, vereda, how="left", predicate="within")
#     ref.rename(columns={"Name_right": "Vereda", "Name_left": "Name"}, inplace=True)
#     ref = ref[["Name", "Vereda"]]

#     return ref


