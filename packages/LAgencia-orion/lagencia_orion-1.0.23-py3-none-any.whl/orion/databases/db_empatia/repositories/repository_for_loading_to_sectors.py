from typing import List

import geopandas as gpd
import pandas as pd
from loguru import logger
from sqlalchemy import and_, bindparam, func, insert, select, text, update

from orion.databases.config_db_empatia import get_session_empatia
from orion.databases.db_empatia.models.models_sectors import Alias, Barrio, Comuna, Corregimiento, Lugar, Municipio, RelatedNeighborhoods, Sector, Vereda
from orion.databases.db_empatia.repositories.repository_for_geospatial_calculations import execute_trace_containment, execute_trace_for_lugar_within_barrio
from orion.databases.db_empatia.utils import OrderBySector, generate_searcher, generate_slug
from orion.sectors.reader_files_kml import read_file_barrios_relacionados, read_files_barrio, read_files_comunas, read_files_corregimientos, read_files_lugares, read_files_municipio, read_files_veredas

"""repositorio para cargar datos en el esquema de sectores"""


def to_dict(obj):
    return {key: value for key, value in obj.__dict__.items() if not key.startswith("_")}


def load_data_to_table_municipios(gdf: gpd.GeoDataFrame) -> List[Municipio]:
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()

    rows = [{"name": n, "geometry": w, "formatted_name": fn} for n, w, fn in zip(names, wkts, formatted_name)]

    # Consulta a ejecutar
    stmt = insert(Municipio).values(
        name=bindparam("name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
    )

    # ejecucion de la consulta
    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Municipio).all()

        logger.info(f"Se han insertado {len(records)} municipios")
        return records

    logger.warning("No se logró insertar los municipios")
    return []


def load_data_to_table_corregimientos(gdf: gpd.GeoDataFrame) -> List[Corregimiento]:
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()

    rows = [{"name": n, "geometry": w, "formatted_name": fn} for n, w, fn in zip(names, wkts, formatted_name)]

    # Consulta a ejecutar
    stmt = insert(Corregimiento).values(
        name=bindparam("name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
    )

    # ejecucion de la consulta
    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Corregimiento).all()

        logger.info(f"Se han insertado {len(records)} corregimientos")
        return records

    logger.warning("No se logró insertar los corregimientos")
    return []


def load_data_to_table_veredas(gdf: gpd.GeoDataFrame) -> List[Vereda]:
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()

    rows = [{"name": n, "geometry": w, "formatted_name": fn} for n, w, fn in zip(names, wkts, formatted_name)]
    print(f"{len(rows)=}")

    stmt = insert(Vereda).values(
        name=bindparam("name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
    )

    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Vereda).all()
        logger.info(f"Se han insertado {len(records)} veredas")
        return records

    logger.warning("No se logró insertar las veredas")
    return []


def load_data_to_table_comuna(gdf: gpd.GeoDataFrame) -> List[Comuna]:
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()

    rows = [{"name": n, "geometry": w, "formatted_name": fn} for n, w, fn in zip(names, wkts, formatted_name)]
    print(f"{len(rows)=}")

    stmt = insert(Comuna).values(
        name=bindparam("name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
    )

    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Comuna).all()
        logger.info(f"Se han insertado {len(records)} comunas")
        return records

    logger.warning("No se logró insertar las comunas")
    return []


def load_data_to_table_barrio(gdf: gpd.GeoDataFrame) -> List[Barrio]:
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()

    rows = [{"name": n, "geometry": w, "formatted_name": fn} for n, w, fn in zip(names, wkts, formatted_name)]
    print(f"{len(rows)=}")

    stmt = insert(Barrio).values(
        name=bindparam("name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
    )

    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Barrio).all()
        logger.info(f"Se han insertado {len(records)} barrios")
        return records

    logger.warning("No se logró insertar los barrios")
    return []


def load_data_to_table_lugares(gdf: gpd.GeoDataFrame):
    """recibe un geodataframe el cual debe tener las columnas:
    <name>: nombre del municipio
    <geometry>: geometria (POINT/LINESTRING/POLYGON/MULTIPOLYGON) que representa el poligono
    """

    wkts = gdf.geometry.to_wkt().tolist()
    names = gdf["name"].astype(str).tolist()
    formatted_name = gdf["formatted_name"].to_list()
    categories = gdf.category_point_interest

    rows = [{"name": n, "geometry": w, "formatted_name": fn, "category_point_interest": c} for n, w, fn, c in zip(names, wkts, formatted_name, categories)]
    print(f"{len(rows)=}")

    stmt = insert(Lugar).values(
        name=bindparam("name"),
        formatted_name=bindparam("formatted_name"),
        geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),  # Convertir WKT a geometría válida
        category_point_interest=bindparam("category_point_interest"),
    )

    with get_session_empatia() as session:
        session.execute(stmt, rows)
        session.commit()

        records = session.query(Lugar).all()
        logger.info(f"Se han insertado {len(records)} lugares")
        return records

    logger.warning("No se logró insertar los lugares")
    return []


def load_data_to_table_related_neighborhoods(df: pd.DataFrame):
    records = df.to_dict(orient="records")

    for record in records:
        rn_origin_name = record.get("name_origin")
        rn_related_name = record.get("name_related")

        with get_session_empatia() as session:
            # Consultamos el id del sector <padre>
            stmt = select(Sector.id).where(Sector.name == rn_origin_name)
            result_origin_id: Sector = session.scalars(statement=stmt).first()
            # Consultamos el id del sector relacionado
            stmt = select(Sector.id).where(Sector.name == rn_related_name)
            result_related_id: Sector = session.scalars(statement=stmt).first()
            # insertamos/actualizamos el registro

            if not (result_origin_id and result_related_id):
                logger.info(f"No se encontro en la tabla sectors {result_origin_id=} {result_related_id=}")
                continue

            row = {"origin_id": result_origin_id, "origin_name": rn_origin_name, "related_id": result_related_id, "related_name": rn_related_name}
            session.add(RelatedNeighborhoods(**row))
            session.commit()
            logger.info(f"Se agrego la relacion {result_origin_id=} {result_related_id=} en  la tabla barrios_relacionados")


# ============================ FUNCIONES PARA CARGAR DATOS A LAS TABLAS SOURCE============================


def execute_load_data_table_municipios():
    data = read_files_municipio()
    load_data_to_table_municipios(data)


def execute_load_data_table_corregimientos():
    data = read_files_corregimientos()
    load_data_to_table_corregimientos(data)


def execute_load_data_table_veredas():
    data = read_files_veredas()
    load_data_to_table_veredas(data)


def execute_load_data_table_comunas():
    data = read_files_comunas()
    load_data_to_table_comuna(data)


def execute_load_data_table_barrios():
    data = read_files_barrio()
    load_data_to_table_barrio(data)


def execute_load_data_table_lugares():
    data = read_files_lugares()
    print(data.head())
    load_data_to_table_lugares(data)


def execute_load_data_table_related_neighborhoods():
    data = read_file_barrios_relacionados()
    print(data.head())
    load_data_to_table_related_neighborhoods(data)


# ============================ FUNCIONES PARA CARGAR DATOS DESDE SOURCE A LA TABLA SECTORS ============================


def load_municipios_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia municipios -> sectors2 preservando el mismo id.
      - Sector.id = Municipio.id
      - name = Municipio.name
      - searcher/slug = Municipio.formatted_name
      - sector/type = 'municipio'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
    Devuelve el número de filas insertadas.
    """
    # 1) Leemos de municipios como WKT
    sel = select(
        Municipio.id,
        Municipio.name,
        Municipio.formatted_name,
        func.ST_AsText(Municipio.geometry),
    )
    if only_active and hasattr(Municipio, "active"):
        sel = sel.where(Municipio.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt in session.execute(sel):
            # mp_wkt = _to_multipolygon_wkt(wkt)
            rows.append(
                {
                    "id": mid,  # ⬅️ mismo id
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="municipio", name_sector=name),
                    "sector": "",
                    "type": "Municipio",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "order": OrderBySector.MUNICIPIO.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        # 2) Insert explícito con el id del municipio
        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_corregimientos_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia corregimientos -> sectors2 preservando el mismo id.
      - Sector.id = Corregimiento.id
      - name = Corregimiento.name
      - searcher/slug = Corregimiento.formatted_name
      - sector/type = 'corregimiento'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
    Devuelve el número de filas insertadas.
    """
    sel = select(
        Corregimiento.id,
        Corregimiento.name,
        Corregimiento.formatted_name,
        func.ST_AsText(Corregimiento.geometry),
    )
    if only_active and hasattr(Corregimiento, "active"):
        sel = sel.where(Corregimiento.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt in session.execute(sel):
            rows.append(
                {
                    "id": mid,  # ⬅️ mismo id
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="corregimiento", name_sector=name),
                    "sector": "",
                    "type": "Corregimiento",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "order": OrderBySector.CORREGIMIENTO.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_veredas_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia veredas -> sectors2 preservando el mismo id.
      - Sector.id = Vereda.id
      - name = Vereda.name
      - searcher/slug = Vereda.formatted_name
      - sector/type = 'vereda'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
    Devuelve el número de filas insertadas.
    """
    sel = select(
        Vereda.id,
        Vereda.name,
        Vereda.formatted_name,
        func.ST_AsText(Vereda.geometry),
    )
    if only_active and hasattr(Vereda, "active"):
        sel = sel.where(Vereda.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt in session.execute(sel):
            rows.append(
                {
                    "id": mid,  # ⬅️ mismo id
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="vereda", name_sector=name),
                    "sector": "",
                    "type": "Vereda",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "order": OrderBySector.VEREDA.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_comunas_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia comunas -> sectors2 preservando el mismo id.
      - Sector.id = Comuna.id
      - name = Comuna.name
      - searcher/slug = Comuna.formatted_name
      - sector/type = 'comuna'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
    Devuelve el número de filas insertadas.
    """
    sel = select(
        Comuna.id,
        Comuna.name,
        Comuna.formatted_name,
        func.ST_AsText(Comuna.geometry),
    )
    if only_active and hasattr(Comuna, "active"):
        sel = sel.where(Comuna.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt in session.execute(sel):
            rows.append(
                {
                    "id": mid,  # ⬅️ mismo id
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="comuna", name_sector=name),
                    "sector": "",
                    "type": "Comuna",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "order": OrderBySector.COMUNA.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_barrios_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia barrios -> sectors2 preservando el mismo id.
      - Sector.id = Barrio.id
      - name = Barrio.name
      - searcher/slug = Barrio.formatted_name
      - sector/type = 'barrio'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
    Devuelve el número de filas insertadas.
    """
    sel = select(
        Barrio.id,
        Barrio.name,
        Barrio.formatted_name,
        func.ST_AsText(Barrio.geometry),
    )
    if only_active and hasattr(Barrio, "active"):
        sel = sel.where(Barrio.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt in session.execute(sel):
            rows.append(
                {
                    "id": mid,  # ⬅️ mismo id
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="barrio", name_sector=name),
                    "sector": "",
                    "type": "Barrio",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "order": OrderBySector.BARRIO.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_lugares_into_sectors2_preserve_ids(
    truncate: bool = False,
    only_active: bool = True,
) -> int:
    """
    Copia lugares -> sectors2 preservando el mismo id.
      - Sector.id = Lugar.id
      - name = Lugar.name
      - searcher/slug = Lugar.formatted_name
      - sector/type = 'lugar'
      - geometry: POLYGON -> MULTIPOLYGON (WKT) -> ST_GeomFromText(..., 4326)
      - Incluye la categoría de lugar
    Devuelve el número de filas insertadas.
    """
    sel = select(
        Lugar.id,
        Lugar.name,
        Lugar.formatted_name,
        func.ST_AsText(Lugar.geometry),
        Lugar.category_point_interest,  # Agregado para la categoría
    )
    if only_active and hasattr(Lugar, "active"):
        sel = sel.where(Lugar.active.is_(True))

    with get_session_empatia() as session:
        if truncate:
            session.execute(text("TRUNCATE TABLE sectors2"))

        rows: List[dict] = []
        for mid, name, formatted_name, wkt, category in session.execute(sel):
            rows.append(
                {
                    "id": mid,
                    "name": name,
                    "searcher": generate_searcher(name),
                    "slug": generate_slug(type_sector="lugar", name_sector=name),
                    "sector": "",
                    "type": "Lugar",
                    "geometry": wkt,  # será convertido con ST_GeomFromText
                    "category_point_interest": category,  # Incluye la categoría
                    "order": OrderBySector.LUGAR.value,
                }
            )

        if not rows:
            session.commit()
            return 0

        stmt = insert(Sector).values(
            id=bindparam("id"),
            name=bindparam("name"),
            searcher=bindparam("searcher"),
            slug=bindparam("slug"),
            sector=bindparam("sector"),
            type=bindparam("type"),
            geometry=func.ST_GeomFromText(bindparam("geometry"), 4326),
            category_point_interest=bindparam("category_point_interest"),
        )

        result = session.execute(stmt, rows)
        session.commit()
        return result.rowcount


def load_alias_into_sectors2_preserve_ids() -> List[Alias]:
    with get_session_empatia() as session:
        stmt = select(Alias)
        alias: List[Alias] = session.scalars(stmt).all()

        for alias_ in alias:
            stmt = select(Sector).where(and_(Sector.name == alias_.name, Sector.type == alias_.type))
            res = session.scalars(stmt).all()
            if res:
                logger.info(f"El alias {alias_.name=}, {alias_.type=} ya se encuentra registrado en la tabla sectors")
                continue

            stmt = select(Sector).where(Sector.id == alias_.origin_id)
            sector: Sector = session.scalars(stmt).first()

            if not sector:
                continue

            new_sector_alias = to_dict(sector)
            new_sector_alias["id"] = alias_.id
            new_sector_alias["name"] = alias_.name
            new_sector_alias["searcher"] = generate_searcher(alias_.name)
            new_sector_alias["slug"] = generate_slug(type_sector=alias_.type, name_sector=alias_.name)

            session.add(Sector(**new_sector_alias))
            session.commit()
            logger.info(f"Alias {new_sector_alias.get('name')} creado existosamente")

        return alias


def load_data_into_all_sector_source_tables():
    execute_load_data_table_municipios()

    execute_load_data_table_corregimientos()

    execute_load_data_table_veredas()

    execute_load_data_table_comunas()

    execute_load_data_table_barrios()

    execute_load_data_table_lugares()

    load_alias_into_sectors2_preserve_ids()

    execute_load_data_table_related_neighborhoods()


def load_source_sectors_into_table_sectors():
    load_municipios_into_sectors2_preserve_ids()
    load_corregimientos_into_sectors2_preserve_ids()
    load_veredas_into_sectors2_preserve_ids()
    load_comunas_into_sectors2_preserve_ids()
    load_barrios_into_sectors2_preserve_ids()
    load_lugares_into_sectors2_preserve_ids()


# ============================ ACTUALIZAR CAMPO SECTOR DE LA TABLAS SECTORS ============================


def update_field_sector_from_table_sectors_by_comuna():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Comuna")
        comuna_ids = session.scalars(stmt).all()

        for id_ in comuna_ids:
            road = execute_trace_containment(Comuna, id_)
            stmt = select(Sector).where(Sector.id == id_)
            row: Sector = session.scalars(stmt).first()
            row.sector = road
            session.commit()
            #print(f"{road=}")


def update_field_sector_from_table_sectors_by_corregimiento():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Corregimiento")
        ids = session.scalars(stmt).all()

        for id_ in ids:
            road = execute_trace_containment(Corregimiento, id_)
            stmt = select(Sector).where(Sector.id == id_)
            row: Sector = session.scalars(stmt).first()
            row.sector = road
            session.commit()
            print(f"{road=}")


def update_field_sector_from_table_sectors_by_veredas():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Vereda")
        ids = session.scalars(stmt).all()

        for id_ in ids:
            road = execute_trace_containment(Vereda, id_)
            stmt = select(Sector).where(Sector.id == id_)
            row: Sector = session.scalars(stmt).first()
            row.sector = road
            session.commit()
            print(f"{road=}")


def update_field_sector_from_table_sectors_by_barrios():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Barrio")
        ids = session.scalars(stmt).all()

        for id_ in ids:
            road = execute_trace_containment(Barrio, id_)
            stmt = select(Sector).where(Sector.id == id_)
            row: Sector = session.scalars(stmt).first()
            row.sector = road
            session.commit()
            print(f"{road=}")


def update_field_sector_from_table_sectors_by_lugares():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Lugar")
        ids = session.scalars(stmt).all()

        for id_ in ids:
            road = execute_trace_containment(Lugar, id_)
            stmt = select(Sector).where(Sector.id == id_)
            row: Sector = session.scalars(stmt).first()
            row.sector = road
            session.commit()
            print(f"{road=}")


# ============================ CREAR CAMPO SECTOR_REFERENCE ==========================================


def update_field_reference_sector():
    with get_session_empatia() as session:
        stmt = select(Sector.id).where(Sector.type == "Lugar")
        ids: List[Sector] = session.scalars(stmt).all()

        for id_ in ids:
            roads = execute_trace_for_lugar_within_barrio(Lugar, id_)

            for type_, obj in roads:
                if type_ != "Barrio":
                    continue

                session.execute(
                    update(Sector).where(Sector.id == id_).values(reference_sector=obj.id)  # valor de prueba
                )

                session.commit()


