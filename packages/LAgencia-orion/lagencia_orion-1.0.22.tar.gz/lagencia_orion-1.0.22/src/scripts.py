from datetime import datetime  # noqa: F401

from orion.databases.db_empatia.repositories.querys_searcher import QuerysProperty
from orion.databases.db_empatia.repositories.repository_for_loading_to_sectors import execute_load_data_table_related_neighborhoods
from orion.searcher.sectors_x_properties.sectors_x_properties import insert_records_in_table_sectors_properties_by_lugar, insert_records_in_table_sectors_properties_by_sectors

if __name__ == "__main__":
    records = QuerysProperty.select_all()
    ids_ = [record.id for record in records]
    # insert_records_in_table_sectors_properties_by_sectors(properties_ids=ids_)
    # insert_records_in_table_sectors_properties_by_lugar(properties_ids=ids_)

    execute_load_data_table_related_neighborhoods()
