import asyncio
import os
from typing import Dict

import aiohttp
from dotenv import load_dotenv
from sqlalchemy import and_

from orion.databases.db_empatia.repositories.querys_searcher import NewRevenues, QuerysNewRevenues, QuerysSubscriptions, Subscriptions
from orion.tools import list_obj_to_df

load_dotenv()


status_code = {"0": "Exitoso", "2": "numero de whatsapp no valido", "3": "No existe wbot", "4": "WhatsAPP no conectado", "5": "cantidad de parametros no es correctos", "6": "Parametros de seguridad invalidos", "7": "existe un chat abierto para este numero"}


async def shipment_async(url, headers, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, json=data) as response:
            status = response.status
            result = await response.text()
            result = result.replace('"', "")
            return {"status": status, "message": status_code.get(result, "Resultado desconocido")}


async def shimpent_whabonet_alquiventas(message: Dict):
    url = "https://alquiventasback.bonett.chat/gupshup-send-templates"

    headers = {"Content-Type": "application/json"}

    if not message.get("adviser_name"):
        print("Preparando plantilla del cliente")
        data = {
            "app": "laestrellaalquiventas",
            "securekey": "sk_e570ebcf60a548b0bc1de18186d3b78c",
            "template": [{"id": "609dffaa-e57c-482d-aad1-cb3e0e8cc878", "params": [message.get("name_customer"), message.get("token")]}],
            "localid": "suscription",
            "IntegratorUser": "0",
            "message": [],
            "number": message.get("phone_number"),
        }
    else:
        data = {
            "app": "laestrellaalquiventas",
            "securekey": "sk_e570ebcf60a548b0bc1de18186d3b78c",
            "template": [{"id": "cafba504-8d38-495b-8931-2e58c3536143", "params": [message.get("adviser_name"), message.get("customer_name"), message.get("customer_mobile"), message.get("token")]}],
            "localid": "suscription_asesor",
            "IntegratorUser": "0",
            "message": [],
            "number":  message.get("phone_number"),
        }

    print(f"{data=}")
    response = await shipment_async(url, headers, data)
    response.update({"phone": message.get("phone_number")})
    response.update({"suscriber_id": message.get("suscriber_id")})
    return response


async def shipment_match_alquiventas():
    tools_new_revenues = QuerysNewRevenues()
    tools_suscriptions = QuerysSubscriptions()

    records = tools_new_revenues.select_by_filter(NewRevenues.notified == 0)
    df_new_revenues = list_obj_to_df(records)
    df_new_revenues.drop_duplicates(subset=["subscription_id"], inplace=True)

    if df_new_revenues.empty:
        return

    records = tools_suscriptions.select_by_filter(Subscriptions.website == "estrella")
    df_suscriptions = list_obj_to_df(records)

    if df_suscriptions.empty:
        return

    merge = df_new_revenues.merge(df_suscriptions, how="inner", left_on="subscription_id", right_on="id")
    records = merge.to_dict("records")

    # Creacion del mensaje cliente
    content_message_customer = "Hola {name},\n\nEncontramos propiedades que pueden interesarte.\nExplora estas opciones elegidas para ti:\n\n{url_base}{token}"

    # Creacion del mensaje asesor
    content_message_adviser = "Hola {adviser_name},\n\n{name} ha sido notificado porque encontramos propiedades que pueden interesarle.\nPuedes contactarlo al teléfono {mobile}.\n\nLas opciones seleccionadas para el cliente son:\n{url_base}{token}"

    messages_customer = []
    for record in records:
        # print(record.get("name"), record.get("mobile"), record.get("token"))
        message = {
            "suscriber_id": record.get("subscription_id"),
            "phone_number": record.get("mobile"),
            "name_customer": record.get("name"),
            "content": content_message_customer.format(name=record.get("name"), url_base=os.getenv("URL_BASE_SHIPMENT_ALQUIVENTAS"), token=record.get("token")),
            "token": record.get("token"),
        }
        messages_customer += [message]

    messages_adviser = []
    for record in records:
        # print(record.get("name"), record.get("mobile"), record.get("token"))
        if record.get("adviser_mobile") and record.get("adviser_name"):
            message = {
                "suscriber_id": record.get("subscription_id"),
                "phone_number": record.get("adviser_mobile"),
                "customer_name": record.get("name"),
                "content": content_message_adviser.format(name=record.get("name"), adviser_name=record.get("adviser_name"), mobile=record.get("mobile"), url_base=os.getenv("URL_BASE_SHIPMENT_ALQUIVENTAS"), token=record.get("token")),
                "adviser_name": record.get("adviser_name"),
                "customer_mobile": record.get("mobile"),
                "token": record.get("token"),
            }
            messages_adviser += [message]

    # ++ envio masivo clientes
    task = [shimpent_whabonet_alquiventas(message) for message in messages_customer]
    results_customer = await asyncio.gather(*task)

    # ++ envio masivo adviser
    task = [shimpent_whabonet_alquiventas(message) for message in messages_adviser]
    results_adviser = await asyncio.gather(*task)

    for result in results_customer:
        records = tools_new_revenues.select_by_filter(NewRevenues.subscription_id == result.get("suscriber_id"))
        for record in records:
            if result.get("status") == 200:
                record.notified = 1
            else:
                record.notified = 0

            dict_ = {"subscription_id": record.subscription_id, "property_id": record.property_id, "created_at": record.created_at, "notified": record.notified}
            print(dict_)
            tools_new_revenues.update_all_by_filter(and_(NewRevenues.subscription_id == result.get("suscriber_id"), NewRevenues.property_id == record.property_id), dict_)


async def shimpent_whabonet_castillo(message: Dict):
    url = "https://arrcastilloback.bonett.chat/gupshup-send-templates"
    headers = {"Content-Type": "application/json"}

    if not message.get("adviser_name"):
        print("Preparando plantilla para cliente...")
        data = {
            "app": "arrcastillo",
            "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
            "template": [{"id": "425811df-40ea-4167-beb6-f084e10ede49", "params": [message.get("name", ""), message.get("token", "")]}],
            "localid": "suscription",
            "IntegratorUser": "0",
            "message": [],
            "number": message.get("phone_number")
        }
    else:
        print("Preparando plantilla para asesor...")
        data = {
            "app": "arrcastillo",
            "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
            "template": [{"id": "4ee5b7ae-6793-4a0d-ac64-9c38b7038cf6", "params": [message.get("adviser_name"), message.get("name_customer"), message.get("phone_customer"), message.get("token")]}],
            "localid": "suscription_asesor",
            "IntegratorUser": "0",
            "message": [],
            "number": message.get("adviser_mobile"),
        }
        print(f"{data=}")

    response = await shipment_async(url, headers, data)
    response.update({"phone": message.get("phone_number")})
    response.update({"suscriber_id": message.get("suscriber_id")})

    return response


async def shipment_match_castillo():
    tools_new_revenues = QuerysNewRevenues()
    tools_suscriptions = QuerysSubscriptions()

    records = tools_new_revenues.select_by_filter(NewRevenues.notified == 0)
    df_new_revenues = list_obj_to_df(records)
    df_new_revenues.drop_duplicates(subset=["subscription_id"], inplace=True)

    if df_new_revenues.empty:
        print("df_new_revenues vacio")
        return

    records = tools_suscriptions.select_by_filter(Subscriptions.website == "castillo")
    df_suscriptions = list_obj_to_df(records)

    if df_suscriptions.empty:
        return

    merge = df_new_revenues.merge(df_suscriptions, how="inner", left_on="subscription_id", right_on="id")
    records = merge.to_dict("records")
    print(f"{records=}")

    # Creacion del mensaje cliente
    content_message_customer = "Hola {name},\n\nEncontramos propiedades que pueden interesarte.\nExplora estas opciones elegidas para ti:\n\n{url_base}{token}"

    # Creacion del mensaje asesor
    content_message_adviser = "Hola {adviser_name},\n\n{name} ha sido notificado porque encontramos propiedades que pueden interesarle.\nPuedes contactarlo al teléfono {mobile}.\n\nLas opciones seleccionadas para el cliente son:\n{url_base}{token}"

    messages_customer = []
    for record in records:
        # print(record.get("name"), record.get("mobile"), record.get("token"))
        message = {"suscriber_id": record.get("subscription_id"), "phone_number": record.get("mobile"), "content": content_message_customer.format(name=record.get("name"), url_base=os.getenv("URL_BASE_SHIPMENT_CASTILLO"), token=record.get("token")), "name": record.get("name"), "token": record.get("token", "")}
        messages_customer += [message]

    messages_adviser = []
    for record in records:
        # print(record.get("name"), record.get("mobile"), record.get("token"))
        if record.get("adviser_mobile") and record.get("adviser_name"):
            message = {
                "suscriber_id": record.get("subscription_id"),
                "adviser_mobile": record.get("adviser_mobile"),
                "adviser_name": record.get("adviser_name"),
                "content": content_message_adviser.format(name=record.get("name"), adviser_name=record.get("adviser_name"), mobile=record.get("mobile"), url_base=os.getenv("URL_BASE_SHIPMENT_CASTILLO"), token=record.get("token")),
                "name_customer": record.get("name"),
                "phone_customer": record.get("mobile"),
                "token": record.get("token", ""),
            }
            print(f"{message=}")
            messages_adviser += [message]

    # ++ envio masivo customers
    task = [shimpent_whabonet_castillo(message) for message in messages_customer]
    results_customer = await asyncio.gather(*task)

    # ++ envio masivo adviser
    task = [shimpent_whabonet_castillo(message) for message in messages_adviser]
    results_adviser = await asyncio.gather(*task)

    for result in results_customer:
        records = tools_new_revenues.select_by_filter(NewRevenues.subscription_id == result.get("suscriber_id"))
        for record in records:
            if result.get("status") == 200:
                record.notified = 1
            else:
                print("xxx")
                record.notified = 0

            dict_ = {"subscription_id": record.subscription_id, "property_id": record.property_id, "created_at": record.created_at, "notified": record.notified}
            print(dict_)
            tools_new_revenues.update_all_by_filter(and_(NewRevenues.subscription_id == result.get("suscriber_id"), NewRevenues.property_id == record.property_id), dict_)


if __name__ == "__main__":
    # phone_numer= []
    # message= "Mensaje de  prueba desde LAgencia."
    # #result= shimpent_whabonet_castillo(phone_numer, message)
    # result= shimpent_whabonet_alquiventas(phone_numer, message)
    # print(result)

    tools_new_revenues = QuerysNewRevenues()
    tools_suscriptions = QuerysSubscriptions()

    records = tools_new_revenues.select_by_filter(NewRevenues.notified == 0)
    df_new_revenues = list_obj_to_df(records)
    df_new_revenues.drop_duplicates(subset=["subscription_id"], inplace=True)
    print(df_new_revenues)

    records = tools_suscriptions.select_by_filter(Subscriptions.website == "castillo")
    df_suscriptions = list_obj_to_df(records)
    print(df_suscriptions)

    merge = df_new_revenues.merge(df_suscriptions, how="inner", left_on="subscription_id", right_on="id")
    print(merge)

    # Creacion del mensaje
    content = """Hola {name}, encontramos propiedades que pueden interesarte. Explora estas opciones elegidas para ti.
            {url_base}{token}
            """

    messages = []
    records = merge.to_dict("records")
    for record in records:
        print(record.get("name"), record.get("mobile"), record.get("token"))
        message = {"phone_number": record.get("mobile"), "content": content.format(name=record.get("name"), url_base=os.getenv("URL_BASE_SHIPMENT_CASTILLO"), token=record.get("token"))}
        messages += [message]

    print(messages)
    # envio masivo
    # task= [shimpent_whabonet_castillo(message) for message in messages]
