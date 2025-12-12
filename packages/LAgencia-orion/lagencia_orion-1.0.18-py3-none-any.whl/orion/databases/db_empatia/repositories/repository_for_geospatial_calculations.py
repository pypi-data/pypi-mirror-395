from typing import List, Literal, Tuple, Type

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from orion.databases.config_db_empatia import get_session_empatia
from orion.databases.db_empatia.models.model_searcher import Property
from orion.databases.db_empatia.models.models_sectors import Barrio, Comuna, Corregimiento, Lugar, Municipio, Sector, Vereda

"""Respositorio para calculos geoespaciales"""

# distancia_m ≈ distancia_en_grados * 111_320
METERS_PER_DEGREE = 111_320.0

CONTAINMENT_ORDER = {
    Municipio: [],  # raíz
    Comuna: [Municipio],
    Corregimiento: [Municipio],
    Barrio: [Comuna, Corregimiento, Municipio],
    Vereda: [Comuna, Corregimiento, Municipio],
    Lugar: [Barrio, Comuna, Vereda, Corregimiento, Municipio],
}


def test_geometries():
    with get_session_empatia() as s:
        print("props con geom:", s.scalar(select(func.count()).select_from(Property).where(Property.geometry.isnot(None))))
        print("sectors 'Lugar' con geom:", s.scalar(select(func.count()).select_from(Sector).where(Sector.type == "Lugar", Sector.geometry.isnot(None))))
        print("SRID props:", s.execute(select(func.distinct(func.ST_SRID(Property.geometry)))).all())
        print("SRID sects:", s.execute(select(func.distinct(func.ST_SRID(Sector.geometry)))).all())


def trace_containment(
    session: Session,
    model: Type,  # e.g., Barrio, Lugar, etc.
    obj_id: str,
    *,
    inclusive: bool = False,  # True = acepta “en el borde”
) -> List[Tuple[str, object]]:
    """
    Devuelve la lista [("Nivel", objeto)] que contiene al objeto dado.
    Ej.: Barrio -> [("Comuna", c), ("Municipio", m)]
    """
    # 1) Geometría del hijo como subconsulta (evita cartesianos)
    child_geom_sq = select(model.geometry).where(model.id == obj_id).scalar_subquery()

    results: List[Tuple[str, object]] = []

    # Si el modelo no está en el mapa, no hay contenedores definidos
    parents = CONTAINMENT_ORDER.get(model, [])
    if not parents:
        return results

    # 2) Para cada “nivel padre” consulta si contiene al hijo
    for parent in parents:
        if inclusive:
            # “Incluye borde” aproximado:
            #   (ST_Contains) OR (ST_Touches)
            # Nota: si el polígono del hijo comparte interior con el padre, Contains ya bastará.
            predicate = (func.ST_Contains(parent.geometry, child_geom_sq) == 1) | (func.ST_Touches(parent.geometry, child_geom_sq) == 1)
        else:
            # Estricto: hijo completamente dentro del interior del padre
            # (equivalente: ST_Within(child, parent) == 1)
            predicate = func.ST_Contains(parent.geometry, child_geom_sq) == 1

        stmt = select(parent).where(predicate)
        parent_obj = session.execute(stmt).scalars().first()  # .all()  # .first()
        if parent_obj is not None:
            results.append((parent.__name__, parent_obj))
            # No es necesario “subir” la geometría; los niveles superiores
            # también deben contener al hijo (o al menos a su interior).

    return results


def execute_trace_containment(model: Literal[Municipio, Comuna, Corregimiento, Vereda, Barrio, Lugar], sector_id: str):
    with get_session_empatia() as s:
        caminos = trace_containment(s, model, sector_id)

        road = {
            "Municipio": None,
            "Corregimiento": None,
            "Comuna": None,
            "Barrio": None,
            "Vereda": None,
            "Lugar": None,
        }

        for model_, intercepts in caminos:
            if road.get(model_) is None:
                road[model_] = intercepts.name if intercepts else None

        road_list = [value for _, value in road.items() if value is not None]
        road_str = ",".join(road_list)

        return road_str


def execute_trace_for_lugar_within_barrio(model: Barrio, sector_id: str):
    with get_session_empatia() as s:
        caminos = trace_containment(s, model, sector_id)
        return caminos


def property_within_sector(properties_ids: List[int]):
    with get_session_empatia() as session:
        stmt = (
            select(Property.id, Sector.id, Sector.name)
            .select_from(Property)
            .join(Sector, func.ST_Contains(Sector.geometry, func.ST_Centroid(Property.geometry)) == 1)
            .where(
                Sector.type != "Lugar",
                Property.id.in_(properties_ids),
            )
        )
        rows = session.execute(stmt).all()

        return rows


def lugares_a_500m(properties_ids: List[int]):
    with get_session_empatia() as session:
        dist_m = func.ST_Distance(Property.geometry, Sector.geometry) * METERS_PER_DEGREE

        stmt = (
            select(
                Property.id.label("prop_id"),
                Sector.id.label("sect_id"),
                Sector.name,
                dist_m.label("meters"),
            )
            .select_from(Property)
            .join(  # INNER JOIN solo por el tipo; el filtro de distancia va en WHERE
                Sector, Sector.type == "Lugar"
            )
            .where(
                Property.geometry.isnot(None),
                Property.id.in_(properties_ids),
                Sector.geometry.isnot(None),
                dist_m <= 500,  # metros
            )
        )
        rows = session.execute(stmt).all()
        return rows




def lugares_a_x_distancia(properties_ids: List[int], distance: int = 500):
    with get_session_empatia() as session:
        # ST_Distance_Sphere requiere POINT geometries en formato POINT(lng lat)
        # Extraemos el centroide como punto para ambas geometrías

        dist_m = func.ST_Distance(Property.geometry, Sector.geometry) * METERS_PER_DEGREE

        stmt = (
            select(
                Property.id.label("prop_id"),
                Sector.id.label("sect_id"),
                Sector.name,
                dist_m.label("meters"),
            )
            .select_from(Property)
            .join(Sector, Sector.type == "Lugar")
            .where(
                Property.geometry.isnot(None),
                Property.id.in_(properties_ids),
                Sector.geometry.isnot(None),
                dist_m <= distance,
            )
        )
        rows = session.execute(stmt).all()
        return rows
