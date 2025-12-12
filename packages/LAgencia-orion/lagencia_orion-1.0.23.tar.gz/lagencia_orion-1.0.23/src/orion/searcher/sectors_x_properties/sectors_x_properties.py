from typing import List

from orion.databases.db_empatia.repositories.querys_searcher import PropertySector, QuerysPropertySector
from orion.databases.db_empatia.repositories.repository_for_geospatial_calculations import lugares_a_500m, property_within_sector


def insert_records_in_table_sectors_properties_by_sectors(properties_ids: List[int]):
    results = property_within_sector(properties_ids)
    records = [PropertySector(property_id=record[0], sector_id=record[1], meters=None) for record in results]
    print(f"Se calcularon {len(records)} solapes entre propiedades y sectores")
    QuerysPropertySector.bulk_insert(records)


def update_records_for_table_sectors_properties(properties_ids: List[int]):
    for id_ in properties_ids:
        QuerysPropertySector.delete_by_filter(PropertySector.property_id == id_)

    insert_records_in_table_sectors_properties_by_sectors(properties_ids)


def insert_records_in_table_sectors_properties_by_lugar(properties_ids: List[int]):
    results = lugares_a_500m(properties_ids)
    print(results[:10])
    print(f"cantidad de distancias calculadas: {len(results)}")

    records = [PropertySector(property_id=record[0], sector_id=record[1], meters=record[3]) for record in results]
    print(f"Se calcularon {len(records)} solapes entre propiedades y sectores")
    QuerysPropertySector.bulk_insert(records)


def update_records_for_table_sectors_properties_by_lugar(properties_ids: List[int]):
    for id_ in properties_ids:
        QuerysPropertySector.delete_by_filter(PropertySector.property_id == id_)

    insert_records_in_table_sectors_properties_by_lugar(properties_ids)
