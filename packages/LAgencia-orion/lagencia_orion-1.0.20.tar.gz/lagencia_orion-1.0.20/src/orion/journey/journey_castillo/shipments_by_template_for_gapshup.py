import json

import requests
from loguru import logger

from orion.journey.journey_castillo.models import RequestToSendNotifications


def sends_nuevos_ingresos(record: RequestToSendNotifications):
    url = "https://arrcastilloback.bonett.chat/gupshup-send-templates"

    headers = {"Content-Type": "application/json"}

    if record.add_data:
        print(f"{record=}")
        print([record.add_data.customer_name, record.token])
        print(record.add_data.customer_phone)
        if record.add_data.customer_name and record.add_data.customer_phone and record.token:
            payload_customer = {
                "app": "arrcastillo",
                "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
                "template": [{"id": "425811df-40ea-4167-beb6-f084e10ede49", "params": [record.add_data.customer_name, record.token]}],
                "localid": "suscription",
                "IntegratorUser": "0",
                "message": [],
                "number": record.add_data.customer_phone,
            }


            response_customer = requests.post(url=url, headers=headers, json=payload_customer)
            print(response_customer.text)
            response_customer.raise_for_status()
            logger.info("Notificacion enviada al cliente")


        if record.add_data.adviser_name and record.add_data.adviser_phone and record.token:
            payload_adviser = {
                "app": "arrcastillo",
                "securekey": "sk_e6de090b1f89457698ff81a01b7b9e9e",
                "template": [{"id": "4ee5b7ae-6793-4a0d-ac64-9c38b7038cf6", "params": [record.add_data.adviser_name, record.add_data.customer_name, record.add_data.customer_phone, record.token]}],
                "localid": "suscription_asesor",
                "IntegratorUser": "0",
                "message": [],
                "number": record.add_data.adviser_phone,
            }

            response = requests.post(url=url, headers=headers, json=payload_adviser)
            response.raise_for_status()
            logger.info("Notificacion enviada al asesor")
        return True if response_customer.ok else False

    logger.info("No se enviaron notificaciones nuevos ingresos castillo")

    print(response.text)

