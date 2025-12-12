import json

import requests

from orion.journey.journey_villacruz.models import RequestToSendNotifications


def sends_modifica_precio(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "modifica_precio", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.code}]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_45a90_dias_semana1(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"
    payload = json.dumps({"name": "45a90_dias_semana1", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_art_est_arrend(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "art_est_arrend", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_import_contrato(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "import_contrato", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_nuevos_ingresos(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "nuevos_ingresos", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.token}]})
    headers = {"Content-Type": "application/json"}

    response_customer = requests.request("GET", url, headers=headers, data=payload)

    if record.add_data:
        _mobile_adviser = record.add_data.adviser_phone
        _adviser_name = record.add_data.adviser_name
        _name_customer = record.add_data.customer_name
        _mobile_customer = record.add_data.customer_phone
        _token = record.token

        if _mobile_adviser and _adviser_name and _name_customer and _mobile_customer and _token:
            payload = json.dumps(
                {
                    "name": "suscripcion_asesor_ut",
                    "contactId": _mobile_adviser,
                    "clientId": "573116050515",
                    "addMessage": "false",
                    "components": [
                        {"type": "text", "parameter_name": "nombre_asesor", "value": _adviser_name, "index": "0"},
                        {"type": "text", "parameter_name": "nombre_cliente", "value": _name_customer, "index": "1"},
                        {"type": "text", "parameter_name": "cel_cliente", "value": _mobile_customer, "index": "2"},
                        {"type": "button", "index": "0", "parameter_name": "id", "value": _token},
                    ],
                }
            )



            response_adviser = requests.request("GET", url, headers=headers, data=payload)

    print(response_customer.text)

    return True if response_customer.ok else False


def sends_aviso_novedades(record: RequestToSendNotifications):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "aviso_novedades", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.token}]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":
    code = "73498"
    phone = "573103738772"
    # sends_new_revenues(phone=phone, code=code)
    record = RequestToSendNotifications(code=code, phone=phone)
    sends_modifica_precio(record)
