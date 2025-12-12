from typing import List

from orion.journey.journey_castillo.models import RequestToSendNotifications
from orion.journey.journey_castillo.shipments_by_template_for_gapshup import sends_nuevos_ingresos

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

            case _:
                raise


if __name__ == "__main__":
    code = "73498"
    phone = "573103738772"
    # sends_new_revenues(phone=phone, code=code)
    record = RequestToSendNotifications(code=code, phone=phone)
    # sends_modifica_precio(record)
