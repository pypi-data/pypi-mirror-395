import asyncio
import copy
import warnings
from datetime import datetime
from typing import Dict, List

import aiohttp
import pandas as pd

from orion.databases.db_empatia.repositories.querys_searcher import (
    NewRevenues,
    QuerysNewRevenues,
    QuerysProperty,
    QuerysSubscriptions,
)
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
    "livin": {
        "name": "mensaje_suscripcion",
        "contactId": "_mobile",
        "clientId": "573184444845",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "name", "value": "_name", "index": "0"},
            {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"},
        ],
    },
    "villacruz": {
        "name": "mensaje_suscripcion",
        "contactId": "_mobile",
        "clientId": "573116050515",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "name", "value": "_name", "index": "0"},
            {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"},
        ],
    },
    "livin_customer": {
        "name": "suscripcion_cliente_ut",
        "contactId": "_mobile",
        "clientId": "573184444845",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "name", "value": "_name", "index": "0"},
            {"type": "button", "index": "0", "parameter_name": "id", "value": "_token"},
        ],
    },
    "villacruz_customer": {
        "name": "susc_de_utilidad",
        "contactId": "_mobile",
        "clientId": "573116050515",
        "addMessage": "false",
        "components": [
            {"type": "text", "parameter_name": "name", "value": "_name", "index": "0"},
            {"type": "button", "index": "1", "parameter_name": "id", "value": "_token"},
        ],
    },
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


def is_valid_value(value) -> bool:
    """
    Valida que un valor no sea None, NaN, vacío o string 'None'.
    """
    if value is None:
        return False
    if pd.isna(value):
        return False
    if isinstance(value, str) and value.strip() in ["", "None", "none", "NULL", "null"]:
        return False
    return True


async def requests_async(url: str, payload: Dict, headers: Dict) -> Dict:
    """
    Envía una solicitud HTTP POST de forma asíncrona.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            status = response.status
            text = await response.text()

            if "Resultado: Enviado" in text:
                print("status: ", status, "Resultado: Enviado")
            else:
                print("status: ", status, text)

            # Si quieres que el DAG falle cuando el servicio responda distinto de 200,
            # descomenta esto:
            # if status != 200:
            #     raise Exception(f"Error enviando mensaje: HTTP {status} - {text}")

            return {"subscription_id": payload.get("subscription_id"), "status": status}


async def _send_messages(payloads: List[Dict]) -> List[Dict]:
    """
    Envía múltiples mensajes de forma asíncrona usando `requests_async`.
    """
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"
    headers = {"content-type": "application/json"}

    tasks = [requests_async(url, payload, headers) for payload in payloads]
    return await asyncio.gather(*tasks)


def send_messages(messages: List[Dict]) -> List[Dict]:
    """
    Ejecuta el envío de mensajes asíncronos desde una función sincrónica.
    """
    if not messages:
        return []
    return asyncio.run(_send_messages(messages))


def update_notified_status_from_table_new_revenues(shipment_results: List[Dict]):
    """
    Marca como notificados los registros de nuevos ingresos que hayan sido enviados exitosamente.
    """
    for result in shipment_results:
        if result.get("status") == 200:
            records = QuerysNewRevenues.select_by_filter(
                NewRevenues.subscription_id == result.get("subscription_id")
            )
            if not records:
                continue

            for record in records:
                record.notified = True

            QuerysNewRevenues.upsert_all(records)


def build_messages_livin_customer() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'livin' (cliente).
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar (livin)")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[
        ["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    ]

    merged = new_revenues.merge(
        subscriptions, how="inner", left_on="subscription_id", right_on="id"
    ).drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")

    bool_cols = ["show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    merged[bool_cols] = merged[bool_cols].fillna(False).astype("bool")
    merged = merged[merged["show_livin"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    merged = merged[merged["website"] == "livin"]

    records = merged.to_dict("records")

    messages = []
    for record in records:
        mobile = record.get("mobile")

        if not is_valid_value(mobile):
            print(
                f"⚠️ Registro sin móvil válido de cliente (livin_customer), se omite. "
                f"subscription_id={record.get('subscription_id')}, mobile={mobile}"
            )
            continue

        template = copy.deepcopy(templates.get("livin_customer"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = str(mobile).strip()
        template["components"][0]["value"] = record.get("name")
        template["components"][1]["value"] = record.get("token")

        messages.append(template)

    print(f"✅ Se construyeron {len(messages)} mensajes para clientes de livin")
    return messages


def build_messages_villacruz_customer() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'villacruz' (cliente).
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[:, ["id", "name", "mobile", "email", "website", "token"]]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar (villacruz)")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[
        ["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    ]

    merged = new_revenues.merge(
        subscriptions, how="inner", left_on="subscription_id", right_on="id"
    ).drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")
    merged["show_villacruz"].fillna(False, inplace=True)
    merged = merged[merged["show_villacruz"]]

    merged.drop_duplicates(subset=["token"], inplace=True)
    merged = merged[merged["website"] == "villacruz"]

    records = merged.to_dict("records")

    messages = []
    for record in records:
        mobile = record.get("mobile")

        if not is_valid_value(mobile):
            print(
                f"⚠️ Registro sin móvil válido de cliente (villacruz_customer), se omite. "
                f"subscription_id={record.get('subscription_id')}, mobile={mobile}"
            )
            continue

        template = copy.deepcopy(templates.get("villacruz_customer"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = str(mobile).strip()
        template["components"][0]["value"] = record.get("name")
        template["components"][1]["value"] = record.get("token")

        messages.append(template)

    print(f"✅ Se construyeron {len(messages)} mensajes para clientes de villacruz")
    return messages


def build_messages_livin_adviser() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'livin' (asesor).
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[
            :,
            [
                "id",
                "name",
                "mobile",
                "email",
                "website",
                "token",
                "adviser_name",
                "adviser_mobile",
            ],
        ]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar (livin_adviser)")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[
        ["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    ]

    merged = new_revenues.merge(
        subscriptions, how="inner", left_on="subscription_id", right_on="id"
    ).drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")

    bool_cols = ["show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    merged[bool_cols] = merged[bool_cols].fillna(False).astype("bool")
    merged = merged[merged["show_livin"]]
    merged = merged[merged["website"] == "livin"]

    merged.drop_duplicates(subset=["token"], inplace=True)
    records = merged.to_dict("records")

    messages = []
    skipped = 0

    for record in records:
        adviser_mobile = record.get("adviser_mobile")
        adviser_name = record.get("adviser_name")
        client_mobile = record.get("mobile")

        # ✅ Validación estricta usando la función is_valid_value
        if not is_valid_value(adviser_mobile):
            print(
                f"⚠️ Registro sin adviser_mobile válido (livin_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, adviser_mobile={adviser_mobile}"
            )
            skipped += 1
            continue

        if not is_valid_value(adviser_name):
            print(
                f"⚠️ Registro sin adviser_name válido (livin_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, adviser_name={adviser_name}"
            )
            skipped += 1
            continue

        if not is_valid_value(client_mobile):
            print(
                f"⚠️ Registro sin client_mobile válido (livin_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, client_mobile={client_mobile}"
            )
            skipped += 1
            continue

        template = copy.deepcopy(templates.get("livin_adviser"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = str(adviser_mobile).strip()
        template["components"][0]["value"] = str(adviser_name).strip()
        template["components"][1]["value"] = record.get("name")
        template["components"][2]["value"] = str(client_mobile).strip()
        template["components"][3]["value"] = record.get("token")

        messages.append(template)

    print(f"✅ Se construyeron {len(messages)} mensajes para asesores de livin (omitidos: {skipped})")
    return messages


def build_messages_villacruz_adviser() -> List[Dict]:
    """
    Construye mensajes de notificación para la página 'villacruz' (asesor).
    """
    records = QuerysSubscriptions.select_all()
    subscriptions = list_obj_to_df(records)

    if not subscriptions.empty:
        subscriptions = subscriptions.loc[
            :,
            [
                "id",
                "name",
                "mobile",
                "email",
                "website",
                "token",
                "adviser_name",
                "adviser_mobile",
            ],
        ]

    records = QuerysNewRevenues.select_by_filter(NewRevenues.notified == 0)
    new_revenues = list_obj_to_df(records)

    if new_revenues.empty:
        print("No hay nuevos clientes para notificar (villacruz_adviser)")
        return []

    records = QuerysProperty.select_all()
    properties = list_obj_to_df(records)[
        ["id", "show_livin", "show_villacruz", "show_estrella", "show_castillo"]
    ]

    merged = new_revenues.merge(
        subscriptions, how="inner", left_on="subscription_id", right_on="id"
    ).drop(columns=["id", "created_at"])
    merged = merged.merge(properties, how="inner", left_on="property_id", right_on="id")
    merged["show_villacruz"].fillna(False, inplace=True)
    merged = merged[merged["show_villacruz"]]
    merged = merged[merged["website"] == "villacruz"]

    merged.drop_duplicates(subset=["token"], inplace=True)
    records = merged.to_dict("records")

    messages = []
    skipped = 0

    for record in records:
        adviser_mobile = record.get("adviser_mobile")
        adviser_name = record.get("adviser_name")
        client_mobile = record.get("mobile")

        # ✅ Validación estricta usando la función is_valid_value
        if not is_valid_value(adviser_mobile):
            print(
                f"⚠️ Registro sin adviser_mobile válido (villacruz_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, adviser_mobile={adviser_mobile}"
            )
            skipped += 1
            continue

        if not is_valid_value(adviser_name):
            print(
                f"⚠️ Registro sin adviser_name válido (villacruz_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, adviser_name={adviser_name}"
            )
            skipped += 1
            continue

        if not is_valid_value(client_mobile):
            print(
                f"⚠️ Registro sin client_mobile válido (villacruz_adviser), se omite. "
                f"subscription_id={record.get('subscription_id')}, client_mobile={client_mobile}"
            )
            skipped += 1
            continue

        template = copy.deepcopy(templates.get("villacruz_adviser"))
        template["subscription_id"] = record.get("subscription_id")
        template["contactId"] = str(adviser_mobile).strip()
        template["components"][0]["value"] = str(adviser_name).strip()
        template["components"][1]["value"] = record.get("name")
        template["components"][2]["value"] = str(client_mobile).strip()
        template["components"][3]["value"] = record.get("token")

        messages.append(template)

    print(f"✅ Se construyeron {len(messages)} mensajes para asesores de villacruz (omitidos: {skipped})")
    return messages


def shipment_match_livin():
    messages = build_messages_livin_customer()
    all_results: List[Dict] = []

    if messages:
        print(f"*** cliente livin messages={messages}")
        all_results.extend(send_messages(messages))

    messages = build_messages_livin_adviser()
    if messages:
        print(f"*** asesor livin messages={messages}")
        all_results.extend(send_messages(messages))

    if all_results:
        update_notified_status_from_table_new_revenues(all_results)
        ...


def shipment_match_villacruz():
    all_results: List[Dict] = []

    messages = build_messages_villacruz_customer()
    if messages:
        print(f"*** cliente villacruz messages={messages}")
        all_results.extend(send_messages(messages))

    messages = build_messages_villacruz_adviser()
    if messages:
        print(f"*** asesor villacruz messages={messages}")
        all_results.extend(send_messages(messages))

    if all_results:
        update_notified_status_from_table_new_revenues(all_results)
        ...


def shimpmets_suscribers(**kwargs):
    try:
        if asyncio.get_event_loop_policy().__class__.__name__ != "SelectorEventLoop":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

    execution_date: datetime = kwargs.get("execution_date").time()
    start_time = datetime.strptime("01-01-2024 14:00:00", "%d-%m-%Y %H:%M:%S").time()
    end_time = datetime.strptime("01-01-2024 15:00:00", "%d-%m-%Y %H:%M:%S").time()

    if start_time <= execution_date < end_time:
        shipment_match_livin()
        shipment_match_villacruz()

        # Si estas funciones son corutinas, se llaman así:
        # asyncio.run(shipment_match_castillo())
        # asyncio.run(shipment_match_alquiventas())


if __name__ == "__main__":
    shipment_match_villacruz()