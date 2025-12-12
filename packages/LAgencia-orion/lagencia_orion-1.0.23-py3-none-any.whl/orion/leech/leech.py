import time
import aiohttp
import asyncio
import pandas as pd
from dotenv import load_dotenv

import sys
import os




# sys.path.append(os.path.dirname(__file__))  # agrega 'orion' al path
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))  # agrega 'orion/src' al path

from src.tools import format_column_name
from src.searcher.etl_properties import convert_property_type_name_to_plural, transform_simi_for_properties, transform_softin_for_properties
from src.simi.simi import get_details_property
from src.searcher.etl_attribute_properties import update_records_for_table_attribute_properties
from src.georeferencer.get_property_sectors import update_records_table_property_sectors_for_properties
from src.searcher.etl_gallery import update_records_for_table_gallery_properties
from src.softin.tools import fetch_api_softin, RealState
from src.database.repository.querys_searcher import QuerysProperty, Property

load_dotenv()

username = ""
password = "4NNCuE484n0PMoQRe6QzGZnlQz3JGQfBVFODWeg1-494"
auth = aiohttp.BasicAuth(username, password)


async def run(code: int):
    async with aiohttp.ClientSession(auth=auth, timeout=aiohttp.ClientTimeout(60)) as session:
        result= await get_details_property(session, code)
        return result


def run_leech_for_simi(code: int)-> True:

    # consultar api simi por consecutivo
    response_api= asyncio.run(run(code))

    df= pd.DataFrame([response_api])

    print(df.columns)

    # procesamiento requerido para cargar datos de simi a propiedades
    df.rename(columns={"tpinmu":"property_type",
                    "NombresGestion": "management",
                    "caracteristicasExternas": "caracteristicasexternas",
                    "EdadInmueble": "age",
                    "AreaLote": "area",
                    "Administracion": "price_admon",
                    "Estrato": "stratum",
                    "Direccion": "address",
                    "amobladoInmueble": "show_furnished",
                    "descripcionSt": "descripcionst"
                    }, inplace=True)

    df["codinm"]= df["codinm"].astype(int)
    df["id"]= 4000000 + df["codinm"]
    df["caracteristicasexternas"]= df["caracteristicasexternas"].astype(str)
    df["show_livin"] = True
    df["featured"]= False
    df["precio"] = df["ValorVenta"].astype(float) + df["ValorCanon"].astype(float)
    df["management"]= df["management"].str.replace("ARRIENDO", "Arriendo")
    df["management"]= df["management"].str.replace("VENTA", "Venta")
    df= convert_property_type_name_to_plural(df)

    df= transform_simi_for_properties(df)
    record= df.to_dict("records")[0]


    obj_property= QuerysProperty.select_by_filter(Property.id==record.get("id"))

    if not obj_property:
        print(f"Propiedad no disponible en la tablas propiedades id: {record.get("id")}")
        return False

    print(obj_property)

    record_property= obj_property[0].__dict__
    record_property.pop('_sa_instance_state', None)

    # Debemos mantener la misma modified_date para que la sincronizacion 30m funcione
    modified_date_property= record_property.get("modified_date")
    record_property.update(record)
    record_property["modified_date"]= modified_date_property


    QuerysProperty.update_all_by_ids([record_property.get("id")], record_property)

    start_time = time.time()
    update_records_for_table_attribute_properties([record_property.get("id")])
    print(f"Tiempo total de ejecución update_records_for_table_attribute_properties: {time.time() - start_time:.2f} segundos")

    start_time = time.time()
    update_records_for_table_gallery_properties([record_property.get("id")])
    print(f"Tiempo total de ejecución update_records_for_table_gallery_properties: {time.time() - start_time:.2f} segundos")

    start_time = time.time()
    # update_records_table_property_sectors_for_properties([record_property.get("id")])
    print(f"Tiempo total de ejecución update_records_table_property_sectors_for_properties: {time.time() - start_time:.2f} segundos")

    return True


def run_leech_for_softin_villacruz(code: int, real_state_name: str):

    print("Actualizanvo propiedad: ", code)

    # consultar api simi por consecutivo
    real_state= RealState(real_state_name)
    result= asyncio.run(fetch_api_softin(real_state, code))

    # procesamiento requerido para cargar datos de softin a propiedades
    df= pd.DataFrame(result)
    df["show_villacruz"] = True
    df["show_castillo"] = False
    df["show_estrella"] = False
    df["imagenes"] = df["imagenes"].astype(str)
    df["id"] = 1000000 + df["consecutivo"]
    df.drop_duplicates(subset=["id"], inplace=True)
    df.columns = list(map(format_column_name, df.columns))

    df["activo"] = True

    # propiedades arriendo
    lease = df[df["tipo_servicio"] == "Arriendo"]
    lease.loc[:, "precio"] = lease["precio"]

    # propiedades venta
    sell = df[df["tipo_servicio"] == "Venta"]
    sell.loc[:, "precio"] = sell["precio_venta"]

    # Dividir las propiedades con tipo de servicio "Ambos" en "Arriendo" y "Venta"
    sell_and_lease = df[df["tipo_servicio"] == "Ambos"]

    # Crear DataFrames para "Venta" y "Arriendo"
    lease_ = sell_and_lease.copy()
    lease_.loc[:, "tipo_servicio"] = "Arriendo"
    lease_.loc[:, "precio"] = lease_["precio"]
    lease_.loc[:, "id"] = 10000000 + lease_["id"]

    sell_ = sell_and_lease.copy()
    sell_.loc[:, "tipo_servicio"] = "Venta"
    sell_.loc[:, "precio"] = sell_["precio_venta"]

    df = pd.concat([lease, sell, lease_, sell_])

    df= transform_softin_for_properties(df)

    records_api= df.to_dict("records")

    for record_api_new in records_api:

        record= QuerysProperty.select_by_filter(Property.id==record_api_new.get("id"))

        if not record:
            print(f"Propiedad no disponible en la tablas propiedades id: {record}")
            return False

        record_property_old= record[0].__dict__
        record_property_old.pop('_sa_instance_state', None)

        # Debemos mantener la misma modified_date para que la sincronizacion 30m funcione
        modified_date_property= record_property_old.get("modified_date")

        record_property_old.update(record_api_new)

        record_property_old["modified_date"]= modified_date_property


        QuerysProperty.update_all_by_ids([record_property_old.get("id")], record_property_old)

        start_time = time.time()
        update_records_for_table_attribute_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_attribute_properties: {time.time() - start_time:.2f} segundos")

        start_time = time.time()
        update_records_for_table_gallery_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_gallery_properties: {time.time() - start_time:.2f} segundos")

        # start_time = time.time()
        # update_records_table_property_sectors_for_properties([record_property_old.get("id")])
        # print(f"Tiempo total de ejecución update_records_table_property_sectors_for_properties: {time.time() - start_time:.2f} segundos")

    return True


def run_leech_for_softin_castillo(code: int, real_state_name: str):

    print("Actualizanvo propiedad: ", code)

    # consultar api simi por consecutivo
    real_state= RealState(real_state_name)
    result= asyncio.run(fetch_api_softin(real_state, code))

    # procesamiento requerido para cargar datos de softin a propiedades
    df= pd.DataFrame(result)
    df["show_villacruz"] = False
    df["show_castillo"] = True
    df["show_estrella"] = False
    df["imagenes"] = df["imagenes"].astype(str)
    df["id"] = 2000000 + df["consecutivo"]
    df.drop_duplicates(subset=["id"], inplace=True)
    df.columns = list(map(format_column_name, df.columns))

    df["activo"] = True

    # propiedades arriendo
    lease = df[df["tipo_servicio"] == "Arriendo"]
    lease.loc[:, "precio"] = lease["precio"]

    # propiedades venta
    sell = df[df["tipo_servicio"] == "Venta"]
    sell.loc[:, "precio"] = sell["precio_venta"]

    # Dividir las propiedades con tipo de servicio "Ambos" en "Arriendo" y "Venta"
    sell_and_lease = df[df["tipo_servicio"] == "Ambos"]

    # Crear DataFrames para "Venta" y "Arriendo"
    lease_ = sell_and_lease.copy()
    lease_.loc[:, "tipo_servicio"] = "Arriendo"
    lease_.loc[:, "precio"] = lease_["precio"]
    lease_.loc[:, "id"] = 10000000 + lease_["id"]

    sell_ = sell_and_lease.copy()
    sell_.loc[:, "tipo_servicio"] = "Venta"
    sell_.loc[:, "precio"] = sell_["precio_venta"]

    df = pd.concat([lease, sell, lease_, sell_])

    df= transform_softin_for_properties(df)

    records_api= df.to_dict("records")

    for record_api_new in records_api:

        record= QuerysProperty.select_by_filter(Property.id==record_api_new.get("id"))

        if not record:
            print(f"Propiedad no disponible en la tablas propiedades id: {record}")
            return False

        record_property_old= record[0].__dict__
        record_property_old.pop('_sa_instance_state', None)

        # Debemos mantener la misma modified_date para que la sincronizacion 30m funcione
        modified_date_property= record_property_old.get("modified_date")

        record_property_old.update(record_api_new)

        record_property_old["modified_date"]= modified_date_property


        QuerysProperty.update_all_by_ids([record_property_old.get("id")], record_property_old)

        start_time = time.time()
        update_records_for_table_attribute_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_attribute_properties: {time.time() - start_time:.2f} segundos")

        start_time = time.time()
        update_records_for_table_gallery_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_gallery_properties: {time.time() - start_time:.2f} segundos")

        # start_time = time.time()
        # update_records_table_property_sectors_for_properties([record_property_old.get("id")])
        # print(f"Tiempo total de ejecución update_records_table_property_sectors_for_properties: {time.time() - start_time:.2f} segundos")

    return True



def run_leech_for_softin_alquiventas(code: int, real_state_name: str):

    print("Actualizanvo propiedad: ", code)

    # consultar api simi por consecutivo
    real_state= RealState(real_state_name)
    result= asyncio.run(fetch_api_softin(real_state, code))

    # procesamiento requerido para cargar datos de softin a propiedades
    df= pd.DataFrame(result)
    df["show_villacruz"] = False
    df["show_castillo"] = False
    df["show_estrella"] = True
    df["imagenes"] = df["imagenes"].astype(str)
    df["id"] = 3000000 + df["consecutivo"]
    df.drop_duplicates(subset=["id"], inplace=True)
    df.columns = list(map(format_column_name, df.columns))

    df["activo"] = True

    # propiedades arriendo
    lease = df[df["tipo_servicio"] == "Arriendo"]
    lease.loc[:, "precio"] = lease["precio"]

    # propiedades venta
    sell = df[df["tipo_servicio"] == "Venta"]
    sell.loc[:, "precio"] = sell["precio_venta"]

    # Dividir las propiedades con tipo de servicio "Ambos" en "Arriendo" y "Venta"
    sell_and_lease = df[df["tipo_servicio"] == "Ambos"]

    # Crear DataFrames para "Venta" y "Arriendo"
    lease_ = sell_and_lease.copy()
    lease_.loc[:, "tipo_servicio"] = "Arriendo"
    lease_.loc[:, "precio"] = lease_["precio"]
    lease_.loc[:, "id"] = 10000000 + lease_["id"]

    sell_ = sell_and_lease.copy()
    sell_.loc[:, "tipo_servicio"] = "Venta"
    sell_.loc[:, "precio"] = sell_["precio_venta"]

    df = pd.concat([lease, sell, lease_, sell_])

    df= transform_softin_for_properties(df)

    records_api= df.to_dict("records")

    for record_api_new in records_api:

        record= QuerysProperty.select_by_filter(Property.id==record_api_new.get("id"))

        if not record:
            print(f"Propiedad no disponible en la tablas propiedades id: {record}")
            return False

        record_property_old= record[0].__dict__
        record_property_old.pop('_sa_instance_state', None)

        # Debemos mantener la misma modified_date para que la sincronizacion 30m funcione
        modified_date_property= record_property_old.get("modified_date")

        record_property_old.update(record_api_new)

        record_property_old["modified_date"]= modified_date_property


        QuerysProperty.update_all_by_ids([record_property_old.get("id")], record_property_old)

        start_time = time.time()
        update_records_for_table_attribute_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_attribute_properties: {time.time() - start_time:.2f} segundos")

        start_time = time.time()
        update_records_for_table_gallery_properties([record_property_old.get("id")])
        print(f"Tiempo total de ejecución update_records_for_table_gallery_properties: {time.time() - start_time:.2f} segundos")

        # start_time = time.time()
        # update_records_table_property_sectors_for_properties([record_property_old.get("id")])
        # print(f"Tiempo total de ejecución update_records_table_property_sectors_for_properties: {time.time() - start_time:.2f} segundos")

    return True
