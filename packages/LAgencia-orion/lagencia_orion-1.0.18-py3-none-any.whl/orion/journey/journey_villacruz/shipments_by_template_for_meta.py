import json
from pathlib import Path
from typing import List, Optional

import requests
from loguru import logger
from pydantic import BaseModel

from orion.journey.shipments_by_template_for_gmail import DataRequestedForGmail, shipment_by_email


class RequestAPIMeta(BaseModel):
    phone: str
    code: Optional[str] = None
    token: Optional[str] = None
    price: Optional[int] = None
    old_price: Optional[int] = None
    week: Optional[int] = None
    option: Optional[str] = None
    recipients: Optional[List[str]] = None


def sends_modifica_precio(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "modifica_precio", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.code}]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_45a90_dias_semana1(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"
    payload = json.dumps({"name": "45a90_dias_semana1", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_art_est_arrend(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "art_est_arrend", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_import_contrato(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "import_contrato", "contactId": record.phone, "clientId": "573116050515", "addMessage": False})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_nuevos_ingresos(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "nuevos_ingresos", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.token}]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def sends_aviso_novedades(record: RequestAPIMeta):
    url = "https://smart-home.com.co/WhatsAppTemplate.aspx?method=POST"

    payload = json.dumps({"name": "aviso_novedades", "contactId": record.phone, "clientId": "573116050515", "addMessage": False, "components": [{"type": "button", "index": "0", "parameter_name": "id", "value": record.token}]})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


# ===================== Envios por gmail ===============================


def send_email_esto_dicen_de_nosotros(record: RequestAPIMeta):
    template_name = "esto_dicen_de_nosotros.html"
    subject = "Prueba: Esto dicen de nosotros"
    path_template = Path("orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


def send_email_invitacion_seccion_nosotros(record: RequestAPIMeta):
    template_name = "invitacion_seccion_nosotros.html"
    subject = "Prueba: Invitación sección nosotros"
    path_template = Path("orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


def send_email_servicion_diferencial(record: RequestAPIMeta):
    template_name = "servicio_diferencial.html"
    subject = "Prueba: Servicio diferencial"
    path_template = Path("orion") / "journey" / "journey_villacruz" / "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


# ===================== Servicio para hacer envios ==============================


class SendMessageByAPIMeta:
    _function_by_template = []

    def __init__(self, templates: List[str], record: RequestAPIMeta):
        self._function_by_template.clear()
        self.record = record

        for template in templates:
            self._function_by_template.append(self.get_funtions_by_sends(template))

    def send(self):
        for function in self._function_by_template:
            print(f"Haciendo envio con funcion {function} con data {self.record}")
            function(self.record)
            # print()

    def get_funtions_by_sends(self, template_name: str):
        match template_name:
            case "nuevos_ingresos":
                return sends_nuevos_ingresos

            case "modifica_precio":
                return sends_modifica_precio

            case "45a90_dias_semana1":
                return sends_45a90_dias_semana1

            case "art_est_arrend":
                return sends_art_est_arrend

            case "import_contrato":
                return sends_import_contrato

            case "aviso_novedades":
                return sends_aviso_novedades

            case "invitacion_seccion_nosotros":
                return send_email_invitacion_seccion_nosotros

            case "esto_dicen_de_nosotros":
                return send_email_esto_dicen_de_nosotros

            case "servicio_diferencial":
                return send_email_servicion_diferencial

            case _:
                raise


if __name__ == "__main__":
    code = "73498"
    phone = "573103738772"
    # sends_new_revenues(phone=phone, code=code)
    record = RequestAPIMeta(code=code, phone=phone)
    sends_modifica_precio(record)
