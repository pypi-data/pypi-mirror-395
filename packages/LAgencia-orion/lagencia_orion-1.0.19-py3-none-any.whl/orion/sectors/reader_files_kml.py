import re
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely import wkb
from shapely.geometry import MultiPolygon, Polygon
from shapely.validation import make_valid

from orion.utils.formaters_string import format_string


def extract_description(text: str):
    match = re.search(r"Descripción:\s*(.*?)(?=\w+:)", text, re.DOTALL)
    if match:
        result = match.group(1).strip()
        # Reemplazar "<br>" por "," y eliminar comas consecutivas
        result = result.replace("<br>", ",")
        result = re.sub(r",+", ",", result)
        result = result.strip(",")
        return result.strip() if result else None
    return text


def to_multipolygon_2d(g):
    """
    Convierte cualquier tipo de geometría a MULTIPOLYGON 2D:
    - POLYGON -> MULTIPOLYGON
    - POINT -> MULTIPOLYGON (se convierte en un pequeño polígono alrededor del punto)
    - MULTIPOLYGON queda igual
    - Cualquier otro tipo se descarta.
    """
    if g is None or g.is_empty:
        return None

    # Reparar geometría (opcional)
    g = make_valid(g)  # Elimina autointersecciones, etc.

    # Elimina la dimensión Z o M (si la tiene)
    g = wkb.loads(wkb.dumps(g, output_dimension=2))

    # Si la geometría es un POLYGON, convertirla a MULTIPOLYGON
    if g.geom_type == "Polygon":
        return MultiPolygon([g])

    # Si es un MULTIPOLYGON, retornarlo tal cual
    if g.geom_type == "MultiPolygon":
        return g

    # Si es un POINT, convertirlo en un MULTIPOLYGON
    if g.geom_type == "Point":
        # Crear un MULTIPOLYGON alrededor del punto (se crea un pequeño polígono alrededor del punto)
        coordinates = [(g.x - 0.00001, g.y - 0.00001), (g.x + 0.00001, g.y - 0.00001), (g.x + 0.00001, g.y + 0.00001), (g.x - 0.00001, g.y + 0.00001), (g.x - 0.00001, g.y - 0.00001)]
        return MultiPolygon([Polygon(coordinates)])

    # Si la geometría es de tipo diferente (LineString, Collection, etc.), devolver None
    return None


def read_files_municipio():
    path_folder = Path("sample_data")
    municipios_n_o: gpd.GeoDataFrame = gpd.read_file(path_folder / "Municipios Norte y Occidente.kml", driver="KML")

    municipios_o: gpd.GeoDataFrame = gpd.read_file(path_folder / "Municipios Oriente.kml", driver="KML")

    municipios_s: gpd.GeoDataFrame = gpd.read_file(path_folder / "Municipios Sur.kml", driver="KML")

    municipios_v_aburra: gpd.GeoDataFrame = gpd.read_file(path_folder / "Municipios V Aburrá.kml", driver="KML")

    municipios = pd.concat([municipios_n_o, municipios_o, municipios_s, municipios_v_aburra])

    gdf = municipios.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    # gdf["geometry"] = gdf.geometry.apply(lambda g: wkb.loads(wkb.dumps(g, output_dimension=2)))
    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)

    return gdf


def read_files_corregimientos():
    path_folder = Path("sample_data")
    corr_med_1: gpd.GeoDataFrame = gpd.read_file(path_folder / "corr_med_1.kml", driver="KML")

    corr_rionegro: gpd.GeoDataFrame = gpd.read_file(path_folder / "Corregimientos Rionegro.kml", driver="KML")

    corregimientos = pd.concat([corr_med_1, corr_rionegro])

    gdf = corregimientos.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    # gdf["geometry"] = gdf.geometry.apply(lambda g: wkb.loads(wkb.dumps(g, output_dimension=2)))
    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)

    return gdf


def read_files_veredas():
    path_folder = Path("sample_data")
    veredas_v_aburra: gpd.GeoDataFrame = gpd.read_file(path_folder / "Veredas V Aburrá.kml", driver="KML")
    veredas_rionegro: gpd.GeoDataFrame = gpd.read_file(path_folder / "Veredas Rionegro.kml", driver="KML")
    veredas_el_retiro: gpd.GeoDataFrame = gpd.read_file(path_folder / "Veredas El Retiro.kml", driver="KML")

    veredas = pd.concat([veredas_v_aburra, veredas_rionegro, veredas_el_retiro])

    gdf = veredas.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)

    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    return gdf


def read_files_comunas():
    path_folder = Path("sample_data")
    comunas_1: gpd.GeoDataFrame = gpd.read_file(path_folder / "comu_med_1.kml", driver="KML")
    comunas_2: gpd.GeoDataFrame = gpd.read_file(path_folder / "alias_comunas.kml", driver="KML")

    comunas = pd.concat([comunas_1, comunas_2])

    gdf = comunas.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)

    return gdf


def read_files_barrio():
    path_folder = Path("sample_data")
    barrios_bello = gpd.read_file(path_folder / "Barrios Bello.kml", driver="KML")
    barrios_la_estrella = gpd.read_file(path_folder / "Barrios La Estrella.kml", driver="KML")
    barrios_sabaneta = gpd.read_file(path_folder / "barrios Sabaneta.kml", driver="KML")
    barrios_v_aburra = gpd.read_file(path_folder / "Barrios V Aburrá.kml", driver="KML")
    barrios_caldas = gpd.read_file(path_folder / "Barrios Caldas.kml", driver="KML")
    barrios_rionegro = gpd.read_file(path_folder / "Barrios Rionegro.kml", driver="KML")
    lomas: gpd.GeoDataFrame = gpd.read_file(path_folder / "lomas.kml", driver="KML")

    # Concatenar los datos de los diferentes barrios
    barrios: gpd.GeoDataFrame = pd.concat([barrios_bello, barrios_la_estrella, barrios_sabaneta, barrios_v_aburra, barrios_caldas, barrios_rionegro, lomas], ignore_index=True)

    # Extraer la descripción
    barrios["Extracted_Description"] = barrios["Description"].apply(lambda x: extract_description(x) if isinstance(x, str) else None)

    # Filtrar los que tienen descripciones válidas
    alias = barrios[barrios["Extracted_Description"].notna()].copy()

    # Separar nombres múltiples en filas individuales
    alias["Extracted_Description"] = alias["Extracted_Description"].str.split(",")

    # Expandir nombres en nuevas filas
    alias = alias.explode("Extracted_Description").reset_index(drop=True)

    # Renombrar la columna
    alias.drop("Name", axis=1, inplace=True)
    alias.rename(columns={"Extracted_Description": "Name"}, inplace=True)

    # Eliminar la columna temporal del DataFrame original
    barrios.drop("Extracted_Description", axis=1, inplace=True)

    # Concatenar nuevamente con los datos originales
    barrios.reset_index(drop=True, inplace=True)
    alias.reset_index(drop=True, inplace=True)
    barrios = pd.concat([barrios, alias], ignore_index=True)

    gdf = barrios.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)
    return gdf


def read_files_lugares():
    path_folder = Path("sample_data")
    puntos_interes: gpd.GeoDataFrame = gpd.read_file(path_folder / "Puntos de Interés.kml", driver="KML")
    sistema_metros: gpd.GeoDataFrame = gpd.read_file(path_folder / "Sistema Metro.kml", driver="KML")
    colegios: gpd.GeoDataFrame = gpd.read_file(path_folder / "Colegios.kml", driver="KML")
    puntos_interes_20240207: gpd.GeoDataFrame = gpd.read_file(path_folder / "puntos_interes_20240207.kml", driver="KML")
    puntos_interes = pd.concat([puntos_interes, sistema_metros, colegios, puntos_interes_20240207])

    category_lugar = pd.read_excel(path_folder / "categorias_puntos_interes.xlsx")[["Name", "Categoria"]]

    category_lugar.drop_duplicates(subset=["Name"], inplace=True)
    puntos_interes = puntos_interes.merge(category_lugar, on="Name", how="left")
    puntos_interes.rename(columns={"Categoria": "category_point_interest"}, inplace=True)
    puntos_interes["category_point_interest"] = puntos_interes["category_point_interest"].fillna("Sin categoría")

    gdf = puntos_interes.rename(columns={"Name": "name"})
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()
    gdf = gdf.drop_duplicates(subset=["name"]).copy()

    names = gdf["name"].astype(str).tolist()
    gdf["formatted_name"] = [format_string(name) for name in names]
    gdf = gdf.drop_duplicates(subset=["formatted_name"]).copy()

    gdf["geometry"] = gdf.geometry.apply(to_multipolygon_2d)

    return gdf


def read_file_barrios_relacionados() -> pd.DataFrame:
    path_folder = Path("sample_data") / "barrios_relacionados.xlsx"
    related_neighborhoods = pd.read_excel(path_folder)
    return related_neighborhoods
