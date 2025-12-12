# import os
# import re

# import geopandas as gpd
# import pandas as pd

# # * Cargar de archivos KML


# """
# Resumen: Este módulo carga datos de georreferenciación desde archivos KML y Excel,
# realizando procesamiento de datos como la extracción de descripciones y la unificación
# de diversas capas geográficas.
# """


# def extract_description2(description: str) -> str:
#     """
#     Extrae la 'Descripción' de un string en formato 'Descripción: <contenido>'.
#     Si no encuentra 'Descripción:', devuelve None.

#     Args:
#         description (str): El texto que contiene la descripción.

#     Returns:
#         str: La descripción extraída o None si no existe.
#     """
#     if not isinstance(description, str):
#         return None
#     match = re.search(r"Descripción:\s*(.+?)(<br>|$)", description, re.IGNORECASE)
#     if not match:
#         return None
#     if match.group(1).strip().startswith("<br>"):
#         return None
#     else:
#         return match.group(1).strip()


# def extract_description(text: str):
#     match = re.search(r"Descripción:\s*(.*?)(?=\w+:)", text, re.DOTALL)
#     if match:
#         result = match.group(1).strip()
#         # Reemplazar "<br>" por "," y eliminar comas consecutivas
#         result = result.replace("<br>", ",")
#         result = re.sub(r",+", ",", result)
#         result = result.strip(",")
#         return result.strip() if result else None
#     return text


# def get_georeferenced_layers():
#     """
#     Carga diversas capas geográficas desde archivos KML y una tabla Excel,
#     unificando y procesando los datos para su uso posterior.

#     Capas cargadas:
#         - Puntos de interés.
#         - Municipios (varias regiones).
#         - Barrios (varias localidades).
#         - Comunas.
#         - Corregimientos (varias localidades).
#         - Veredas (varias localidades).

#     Returns:
#         tuple: Contiene las siguientes capas geográficas:
#             - puntos_interes (GeoDataFrame): Datos de puntos de interés.
#             - barrios (GeoDataFrame): Datos de barrios.
#             - veredas (GeoDataFrame): Datos de veredas.
#             - comunas (GeoDataFrame): Datos de comunas.
#             - corregimientos (GeoDataFrame): Datos de corregimientos.
#             - municipios (GeoDataFrame): Datos de municipios.
#     """

#     path_read = os.path.join(os.path.dirname(__file__), "..", "sample_data")

#     # + construir puntos de interes
#     puntos_interes: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Puntos de Interés.kml"), driver="KML")
#     sistema_metros: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Sistema Metro.kml"), driver="KML")
#     colegios: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Colegios.kml"), driver="KML")
#     puntos_interes_20240207: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"puntos_interes_20240207.kml"), driver="KML")
#     puntos_interes = pd.concat([puntos_interes, sistema_metros, colegios, puntos_interes_20240207])

#     category_lugar = pd.read_excel(os.path.join(path_read, "categorias_puntos_interes.xlsx"))[["Name", "Categoria"]]

#     category_lugar.drop_duplicates(subset=["Name"], inplace=True)
#     puntos_interes = puntos_interes.merge(category_lugar, on="Name", how="left")
#     puntos_interes.rename(columns={"Categoria": "category_point_interest"}, inplace=True)

#     # + municipios
#     municipios_n_o: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Municipios Norte y Occidente.kml"), driver="KML")

#     municipios_o: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Municipios Oriente.kml"), driver="KML")

#     municipios_s: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Municipios Sur.kml"), driver="KML")

#     municipios_v_aburra: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Municipios V Aburrá.kml"), driver="KML")

#     municipios = pd.concat([municipios_n_o, municipios_o, municipios_s, municipios_v_aburra])

#     # + barrios
#     barrios_bello = gpd.read_file(os.path.join(path_read, r"Barrios Bello.kml"), driver="KML")
#     barrios_la_estrella = gpd.read_file(os.path.join(path_read, r"Barrios La Estrella.kml"), driver="KML")
#     barrios_sabaneta = gpd.read_file(os.path.join(path_read, r"barrios Sabaneta.kml"), driver="KML")
#     barrios_v_aburra = gpd.read_file(os.path.join(path_read, r"Barrios V Aburrá.kml"), driver="KML")
#     barrios_caldas = gpd.read_file(os.path.join(path_read, r"Barrios Caldas.kml"), driver="KML")
#     barrios_rionegro = gpd.read_file(os.path.join(path_read, r"Barrios Rionegro.kml"), driver="KML")
#     lomas: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"lomas.kml"), driver="KML")

#     # Concatenar los datos de los diferentes barrios
#     barrios: gpd.GeoDataFrame = pd.concat([barrios_bello, barrios_la_estrella, barrios_sabaneta, barrios_v_aburra, barrios_caldas, barrios_rionegro, lomas], ignore_index=True)

#     # Extraer la descripción
#     barrios["Extracted_Description"] = barrios["Description"].apply(lambda x: extract_description(x) if isinstance(x, str) else None)

#     # Filtrar los que tienen descripciones válidas
#     alias = barrios[barrios["Extracted_Description"].notna()].copy()

#     # Separar nombres múltiples en filas individuales
#     alias["Extracted_Description"] = alias["Extracted_Description"].str.split(",")

#     # Expandir nombres en nuevas filas
#     alias = alias.explode("Extracted_Description").reset_index(drop=True)

#     # Renombrar la columna
#     alias.drop("Name", axis=1, inplace=True)
#     alias.rename(columns={"Extracted_Description": "Name"}, inplace=True)

#     # Eliminar la columna temporal del DataFrame original
#     barrios.drop("Extracted_Description", axis=1, inplace=True)

#     # Concatenar nuevamente con los datos originales
#     barrios.reset_index(drop=True, inplace=True)
#     alias.reset_index(drop=True, inplace=True)
#     barrios = pd.concat([barrios, alias], ignore_index=True)

#     # + comunas
#     comunas_1: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"comu_med_1.kml"), driver="KML")
#     comunas_2: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"alias_comunas.kml"), driver="KML")

#     comunas = pd.concat([comunas_1, comunas_2])

#     # + corregimientos
#     corr_med_1: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"corr_med_1.kml"), driver="KML")

#     corr_rionegro: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Corregimientos Rionegro.kml"), driver="KML")

#     corregimientos = pd.concat([corr_med_1, corr_rionegro])

#     # + veredas
#     veredas_v_aburra: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Veredas V Aburrá.kml"), driver="KML")
#     veredas_rionegro: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Veredas Rionegro.kml"), driver="KML")
#     veredas_el_retiro: gpd.GeoDataFrame = gpd.read_file(os.path.join(path_read, r"Veredas El Retiro.kml"), driver="KML")

#     veredas = pd.concat([veredas_v_aburra, veredas_rionegro, veredas_el_retiro])

#     return (
#         puntos_interes,
#         barrios,
#         veredas,
#         comunas,
#         corregimientos,
#         municipios,
#     )
