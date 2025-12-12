import asyncio
import copy
import warnings
from typing import Dict, List

import aiohttp

from orion.databases.db_empatia.repositories.querys_searcher import NewRevenues, QuerysNewRevenues, QuerysProperty, QuerysSubscriptions
from orion.tools import list_obj_to_df

warnings.simplefilter("ignore", FutureWarning)

# + Cambiar a SelectorEventLoop si estamos en Windows
try:
    if asyncio.get_event_loop_policy().__class__.__name__ != "SelectorEventLoop":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except Exception:
    pass


# Diccionario de plantillas predefinidas para cada sitio web (livin y villacruz)
templates = {
    "livin": {"name": "mensaje_suscripcion", "contactId": "_mobile", "clientId": "573184444845", "addMessage": "false", "components": [{"type": "text", "parameter_name": "name", "value": "_name", "index": "0"}, {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"}]},
    "villacruz": {"name": "mensaje_suscripcion", "contactId": "_mobile", "clientId": "573116050515", "addMessage": "false", "components": [{"type": "text", "parameter_name": "name", "value": "_name", "index": "0"}, {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"}]},
    "livin_customer": {"name": "suscripcion_cliente_ut", "contactId": "_mobile", "clientId": "573184444845", "addMessage": "false", "components": [{"type": "text", "parameter_name": "name", "value": "_name", "index": "0"}, {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"}]},
    "villacruz_customer": {"name": "susc_de_utilidad", "contactId": "_mobile", "clientId": "573116050515", "addMessage": "false", "components": [{"type": "text", "parameter_name": "name", "value": "_name", "index": "0"}, {"type": "button", "index": "1", "parameter_name": "id", "value": "_token"}]},
    "livin_adviser": {
        "name": "sucripcion_asesor_ut",
        "contactId": "_mobile_adviser",
        "clientId": "573184444845",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "nombre_asesor", "value": "_name_adviser", "index": "0"},
            {"type": "text", "parameter_name": "nombre_cliente", "value": "_name_customer", "index": "1"},
            {"type": "text", "parameter_name": "cel_cliente", "value": "_mobile_customer", "index": "2"},
            {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"},
        ],
    },
    "villacruz_adviser": {
        "name": "suscripcion_asesor_ut",
        "contactId": "_mobile",
        "clientId": "573116050515",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "nombre_asesor", "value": "_name_adviser", "index": "0"},
            {"type": "text", "parameter_name": "nombre_cliente", "value": "_name_customer", "index": "1"},
            {"type": "text", "parameter_name": "cel_cliente", "value": "_mobile", "index": "2"},
            {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"},
        ],
    },
}


async def requests_async(url: str, payload: Dict, headers: Dict) -> Dict:
    """
    Envía una solicitud HTTP POST de forma asíncrona.

    Parámetros:
        url (str): URL destino de la solicitud.
        payload (Dict): Datos a enviar en formato JSON.
        headers (Dict): Encabezados HTTP necesarios.

    Retorna:
        Dict: Contiene el ID de suscripción y el estado HTTP de la solicitud.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            status = response.status
            data = await response.text()
            if "Resultado: Enviado" in data:
                print("status: ", status, "Resultado: Enviado")
            else:
                print("status: ", status, data)

            content_type = response.content
            # print("content_type: ", content_type)

            text = await response.text()
            # print(text)
            return {"subscription_id": payload.get("subscription_id"), "status": status}


async def _send_messages(payloads: List[Dict]) -> List[Dict]:
    """
    Envía múltiples mensajes de forma asíncrona usando `requests_async`.

    Parámetros:
        payloads (List[Dict]): Lista de mensajes a enviar.

    Retorna:
        List[Dict]: Lista de resultados por cada mensaje enviado.
    """

    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"
    headers = {"content-type": "application/json"}

    task = [requests_async(url, payload, headers) for payload in payloads]
    return await asyncio.gather(*task)


def send_messages(messages: List[Dict]) -> List[Dict]:
    """
    Ejecuta el envío de mensajes asíncronos desde una función sincrónica.

    Parámetros:
        messages (List[Dict]): Mensajes a enviar.

    Retorna:
        List[Dict]: Lista de resultados por mensaje.
    """
    return asyncio.run(_send_messages(messages))


def update_notified_status_from_table_new_revenues(shipment_results: List[Dict]):
    """
    Marca como notificados los registros de nuevos ingresos que hayan sido enviados exitosamente.

    Parámetros:
        shipment_results (List[Dict]): Resultado de envío por suscripción [{'subscription_id': 9, 'status': 200}].
    """

    for result in shipment_results:
        if result.get("status") == 200:
            records = QuerysNewRevenues.select_by_filter(NewRevenues.subscription_id == result.get("subscription_id"))
            if not records:
                continue

            for record in records:
                record.notified = True

            QuerysNewRevenues.upsert_all(records)


def build_messages_livin_customer() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'livin'.

    Filtra suscripciones y nuevos ingresos aún no notificados, une la información y
    genera los mensajes con base en la plantilla definida.

    Retorna:
        List[Dict]: Lista de mensajes generados listos para enviar.
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]]

    merged = new_revenues.merge(subscriptions, how="inner", left_on="subscription_id", right_on="id").drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")

    bool_cols = ["show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    merged[bool_cols] = merged[bool_cols].fillna(False).astype("bool")
    merged[bool_cols] = merged[bool_cols].infer_objects(copy=False)
    merged = merged[merged["show_livin"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    merged = merged[merged["website"] == "livin"]
    records = merged.to_dict("records")

    messages = []
    for record in records:
        template = copy.deepcopy(templates.get("livin_customer"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = "573103555742"#record.get("mobile")
        template["components"][0]["value"] = record.get("name")
        template["components"][1]["value"] = record.get("token")

        messages += [template.copy()]

    return messages


def build_messages_villacruz_customer() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'villacruz'.

    Filtra suscripciones y nuevos ingresos aún no notificados, une la información y
    genera los mensajes con base en la plantilla definida.

    Retorna:
        List[Dict]: Lista de mensajes generados listos para enviar.
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]]

    merged = new_revenues.merge(subscriptions, how="inner", left_on="subscription_id", right_on="id").drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")
    merged["show_villacruz"].fillna(False, inplace=True)
    merged = merged[merged["show_villacruz"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    print(merged)
    merged = merged[merged["website"] == "villacruz"]
    records = merged.to_dict("records")

    messages = []
    for record in records:
        template = copy.deepcopy(templates.get("villacruz_customer"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = record.get("mobile")
        template["components"][0]["value"] = record.get("name")
        template["components"][1]["value"] = record.get("token")
        # template["components"][2]["value"]= record.get("token")

        messages += [template.copy()]

    return messages


def build_messages_livin_adviser() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'livin'.

    Filtra suscripciones y nuevos ingresos aún no notificados, une la información y
    genera los mensajes con base en la plantilla definida.

    Retorna:
        List[Dict]: Lista de mensajes generados listos para enviar.
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token", "adviser_name", "adviser_mobile"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]]

    merged = new_revenues.merge(subscriptions, how="inner", left_on="subscription_id", right_on="id").drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")
    # merged["show_livin"] = merged["show_livin"].fillna(False)
    # merged["show_villacruz"] = merged["show_villacruz"].fillna(False)
    # merged["show_estrella"] = merged["show_estrella"].fillna(False)
    # merged["show_castillo"] = merged["show_castillo"].fillna(False)
    bool_cols = ["show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    merged[bool_cols] = merged[bool_cols].fillna(False).astype("bool")
    merged[bool_cols] = merged[bool_cols].infer_objects(copy=False)
    merged = merged[merged["show_livin"]]

    merged = merged[merged["show_livin"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    merged = merged[merged["website"] == "livin"]
    records = merged.to_dict("records")

    messages = []
    for record in records:
        template = copy.deepcopy(templates.get("livin_adviser"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = record.get("adviser_mobile")
        template["components"][0]["value"] = record.get("adviser_name")
        template["components"][1]["value"] = record.get("name")
        template["components"][2]["value"] = record.get("mobile")
        template["components"][3]["value"] = record.get("token")
        # template["components"][4]["value"]= record.get("token")

        messages += [template.copy()]

    return messages


def build_messages_villacruz_adviser() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'villacruz'.

    Filtra suscripciones y nuevos ingresos aún no notificados, une la información y
    genera los mensajes con base en la plantilla definida.

    Retorna:
        List[Dict]: Lista de mensajes generados listos para enviar.
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token", "adviser_name", "adviser_mobile"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]]

    merged = new_revenues.merge(subscriptions, how="inner", left_on="subscription_id", right_on="id").drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")
    merged["show_villacruz"].fillna(False, inplace=True)
    merged = merged[merged["show_villacruz"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    merged = merged[merged["website"] == "villacruz"]
    records = merged.to_dict("records")

    messages = []
    for record in records:
        template = copy.deepcopy(templates.get("villacruz_adviser"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = record.get("adviser_mobile")
        template["components"][0]["value"] = record.get("adviser_name")
        template["components"][1]["value"] = record.get("name")
        template["components"][2]["value"] = record.get("mobile")
        template["components"][3]["value"] = record.get("token")
        # template["components"][4]["value"]= record.get("token")

        messages += [template.copy()]

    return messages


def shipment_match_livin():
    messages = build_messages_livin_customer()
    if messages:
        print(messages)
        results = send_messages(messages)

    # messages = build_messages_livin_adviser()
    # if messages:
    #     print(messages)
    # results = send_messages(messages)

    # update_notified_status_from_table_new_revenues(results)


def shipment_match_villacruz():
    messages = build_messages_villacruz_customer()
    print(f"*** cliente {messages=}")
    if messages:
        results = send_messages(messages)

    messages = build_messages_villacruz_adviser()
    print(f"*** asesor {messages=}")
    if messages:
        results = send_messages(messages)

    if results:
        update_notified_status_from_table_new_revenues(results)


if __name__ == "__main__":
    # shipment_match_livin()
    shipment_match_villacruz()
