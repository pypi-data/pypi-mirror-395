import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional

from loguru import logger
from pydantic import BaseModel

from orion.journey.journey_estrella.models import RequestToSendNotifications


class DataRequestedForGmail(BaseModel):
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_PORT: str | int = os.getenv("SMTP_PORT")
    subject: str
    recipients: List[str]
    html_content: str
    files: Optional[List[Path | str]] = []


def shipment_by_email(data: DataRequestedForGmail):
    print(f"{data.recipients=}")
    recipients = [str(recipient).strip() for recipient in data.recipients]
    cc_recipients = []
    bcc_recipients = []

    # build message
    msg = MIMEMultipart()
    msg["From"] = data.SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = data.subject

    msg["Cc"] = ", ".join(cc_recipients)
    msg["Bcc"] = ", ".join(bcc_recipients)

    # Agregar el HTML como cuerpo del correo
    msg.attach(MIMEText(data.html_content, "html"))

    # Adjuntar archivos PDF
    if data.files:
        for file_path in data.files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)

                    # Obtener el nombre del archivo
                    filename = os.path.basename(file_path)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )

                    msg.attach(part)
                    print(f"✅ Archivo adjuntado: {filename}")
                except Exception as e:
                    print(f"❌ Error al adjuntar {file_path}: {str(e)}")
            else:
                print(f"⚠️  Archivo no encontrado: {file_path}")

    # shipment email
    try:
        server = smtplib.SMTP(data.SMTP_SERVER, data.SMTP_PORT)
        server.starttls()  # Seguridad TLS
        server.login(data.SMTP_USER, data.SMTP_PASSWORD)
        server.sendmail(data.SMTP_USER, recipients + cc_recipients + bcc_recipients, msg.as_string())
        server.quit()
        print("Correo enviado con éxito ✅")
        return True
    except Exception as e:
        print(f"❌ Error al enviar correo: {str(e)}")
        return False


# ===================== Envios por gmail ===============================


def send_email_esto_dicen_de_nosotros(record: RequestToSendNotifications):
    template_name = "esto_dicen_de_nosotros.html"
    subject = "Prueba: Esto dicen de nosotros"
    path_template = Path("orion") / "journey" / "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


def send_email_invitacion_seccion_nosotros(record: RequestToSendNotifications):
    template_name = "invitacion_seccion_nosotros.html"
    subject = "Prueba: Invitación sección nosotros"
    path_template = Path("orion") / "journey" / "journey_castillo"/ "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


def send_email_servicion_diferencial(record: RequestToSendNotifications):
    template_name = "servicio_diferencial.html"
    subject = "Prueba: Servicio diferencial"
    path_template = Path("orion") / "journey" / "templates_gmail" / template_name
    html_template = None
    with open(path_template, "r", encoding="utf-8") as file:
        html_template = file.read()

    if html_template:
        data_requested = DataRequestedForGmail(subject=subject, recipients=record.recipients, html_content=html_template)
        shipment_by_email(data_requested)
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> exitoso")
    else:
        logger.warning(f"Envio de correo <{template_name}> a <{record.recipients}> fallido")


if __name__ == "__main__":
    # Cargar la plantilla HTML
    templates_html = ["templates_gmail/esto_dicen_de_nosotros.html", "templates_gmail/invitacion_seccion_nosotros.html", "templates_gmail/servicio_diferencial.html"]

    for template in templates_html:
        with open(template, "r", encoding="utf-8") as file:
            html_template = file.read()

        data = DataRequestedForGmail
        data.subject = "Prueba"
        data.recipients = ["analista1@lagencia.com.co"]
        data.html_content = html_template

        result_shipment = shipment_by_email(DataRequestedForGmail)
