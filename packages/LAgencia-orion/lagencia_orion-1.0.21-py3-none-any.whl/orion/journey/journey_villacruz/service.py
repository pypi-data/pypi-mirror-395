from typing import List

from orion.journey.journey_villacruz.models import RequestToSendNotifications
from orion.journey.journey_villacruz.shipments_by_template_for_gmail import send_email_esto_dicen_de_nosotros, send_email_invitacion_seccion_nosotros, send_email_servicion_diferencial
from orion.journey.journey_villacruz.shipments_by_template_for_meta import sends_45a90_dias_semana1, sends_art_est_arrend, sends_aviso_novedades, sends_import_contrato, sends_modifica_precio, sends_nuevos_ingresos


# ===================== Servicio para hacer envios ==============================


class SendMessageByAPIMeta:
    _function_by_template = []

    def __init__(self, templates: List[str], record: RequestToSendNotifications):
        self._function_by_template.clear()
        self.record = record

        for template in templates:
            self._function_by_template.append(self.get_funtions_by_sends(template))

    def send(self):
        for function in self._function_by_template:
            print(f"Haciendo envio con funcion {function} con data {self.record}")
            result = function(self.record)
            return result

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
    record = RequestToSendNotifications(code=code, phone=phone)
    # sends_modifica_precio(record)
