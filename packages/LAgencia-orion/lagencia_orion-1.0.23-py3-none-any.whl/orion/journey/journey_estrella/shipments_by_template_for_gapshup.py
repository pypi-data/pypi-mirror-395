import requests
from loguru import logger

from orion.journey.journey_estrella.models import RequestToSendNotifications


def sends_nuevos_ingresos(record: RequestToSendNotifications):
    url = "https://alquiventasback.bonett.chat/gupshup-send-templates"

    headers = {"Content-Type": "application/json"}

    if record.add_data:
        if record.add_data.customer_name and record.add_data.customer_phone and record.token:
            payload_customer = {
                "app": "laestrellaalquiventas",
                "securekey": "sk_e570ebcf60a548b0bc1de18186d3b78c",
                "template": [{"id": "609dffaa-e57c-482d-aad1-cb3e0e8cc878", "params": [record.add_data.customer_name, record.token]}],
                "localid": "suscription",
                "IntegratorUser": "0",
                "message": [],
                "number": record.add_data.customer_phone,
            }

            response_customer = requests.post(url=url, headers=headers, json=payload_customer)
            response_customer.raise_for_status()
            logger.info("Notificacion enviada al cliente")

        if record.add_data.adviser_name and record.add_data.adviser_phone and record.token:
            payload_adviser = {
                "app": "laestrellaalquiventas",
                "securekey": "sk_e570ebcf60a548b0bc1de18186d3b78c",
                "template": [{"id": "cafba504-8d38-495b-8931-2e58c3536143", "params": [record.add_data.adviser_name, record.add_data.customer_name, record.add_data.customer_phone, record.token]}],
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
