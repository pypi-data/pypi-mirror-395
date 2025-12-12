from orion.databases.db_empatia.repositories.querys_searcher import QuerysPropertySector  # noqa: F401
from orion.databases.db_empatia.repositories.repository_for_geospatial_calculations import lugares_a_x_distancia  # noqa: F401
from orion.searcher.sectors_x_properties.sectors_x_properties import insert_records_in_table_sectors_properties_by_sectors# noqa: F401

if __name__ == "__main__":
    # records = lugares_a_x_distancia([4010465], 500)
    # print(len(records))
    # print(records[:5])

    print("=======================")
    id_ = 4010046
    records = lugares_a_x_distancia([id_], 500)
    print(len(records))

    print(records)
    for record in records:
        record_ = {"property_id": id_, "sector_id": record[1], "meters": record[3]}
        print(record_)
        QuerysPropertySector.insert(record_)

    insert_records_in_table_sectors_properties_by_sectors([id_])
