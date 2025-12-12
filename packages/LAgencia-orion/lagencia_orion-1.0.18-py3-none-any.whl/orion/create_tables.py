# import os
# from datetime import datetime

# import numpy as np
# import pandas as pd
# import json


# from src.searcher.etl_attribute_properties import reload_records_in_table_attribute_properties
# from src.georeferencer.get_property_sectors import reload_property_sectors_table_records
# from src.database.config_db import engine
# from src.database.config_db_bellatrix import engine as engine_bellatrix

# from src.database.models.model_simi import Base as base_simi
# from src.database.models.model_softin import Base as base_softin
# from src.database.models.model_mls import Base as base_mls
# from src.database.models.model_leech import Base as base_leech
# from src.database.models.model_searcher import Base as base_searcher, NewRevenues, Property, Subscriptions
# from src.database.models.model_acrecer import Base as base_acrecer

# from src.database.repository.querys_softin import QuerysSoftin
# from src.database.repository.querys_searcher import QuerysProperty
# from src.database.repository.querys_searcher import QuerysAttributes
# from src.database.repository.querys_searcher import QuerysAttributeProperties
# from src.database.repository.querys_searcher import QuerysGalleryProperties


# from src.softin.etl_softin import etl as etl_softin
# from src.simi.etl_simi import etl as etl_simi
# from src.mls.etl_mls import etl as etl_mls

# from src.searcher.etl_attributes import load_attributes
# from src.searcher.etl_properties import update_properties
# from src.georeferencer.get_sectors import load_sectors, update_category_name_from_sectors, update_sectors, update_sectors_, update_shows_from_table_sectors





# from src.georeferencer.get_sectors import update_shows_from_table_sectors
# from src.subscriber_matching.suscribers import get_all_Subscriptions, match
# from src.subscriber_matching.shipments_api import requests_async, send_messages

# import time

# # ! control de ids
# # 1000000 rango softin villacruz
# # 2000000 rango softin castillo
# # 3000000 rango softin alquivnetas
# # 4000000 rango simi livin
# # 7000000 rango mls
# # 10000000 rango softin duplicados


# base_softin.metadata.create_all(engine_bellatrix)
# # base_simi.metadata.create_all(engine_bellatrix)
# # base_mls.metadata.create_all(engine_bellatrix)

# # base_searcher.metadata.create_all(engine)
# # base_leech.metadata.create_all(engine)
# #base_acrecer.metadata.create_all(engine)

# start_time = time.time()
# # + Carga tablas padre
# # * Actualiza la fuentes
# # etl_softin()
# # etl_simi()
# #etl_mls()

# # crear metodos de update para loads
# # load_attributes()
# #load_sectors()
# #update_sectors()

# #update_properties()

# #update_shows_from_table_sectors()

# # Para insertar nuevos sectores y recalcular property_sectors ejecutar update_sectors_()
# # update_sectors_()
# # update_category_name_from_sectors()
# # update_shows_from_table_sectors()


# # si la tabla property_sectors esta vacia ejecutar reload_property_sectors_table_records
# # esto permite eliminar y recalcular todos los valores de property_sectors
# # reload_property_sectors_table_records()
# # reload_records_in_table_attribute_properties()
# end_time = time.time()

# print(f"Tiempo de ejecución: {end_time - start_time}")


# # # + Limpiar tablas
# # QuerysSoftin.delete_all()
# # QuerysProperty.delete_all()
# # QuerysAttributes.delete_all()
# # QuerysAttributeProperties.delete_all()
# # QuerysGalleryProperties.delete_all()


