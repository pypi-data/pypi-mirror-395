column_mapping_attributes = {
        "id": "id",
        "Alcoba de servicio": "Alcoba del servicio",
        "Balcón": "Balcón",
        "Cocina": "Cocina",
        "Comedor": "Comedor",
        "Cuarto útil": "Cuarto útil",
        "Sala": "Sala",
        "Salón comedor": "Sala comedor",
    }



class Handler:
    def __init__(self, successor=None):
        self.successor= successor

    def handle(self, option: str):
        result= self.process(option)
        if result is not None:
            return result
        if self.successor:
            return self.successor.handle(option)
        return None

    def process(self, option: str):
        """Procesa el valor. Cada manejador específico debe implementar esta lógica."""
        raise NotImplementedError("Subclasses must implement `process`.")


# Manejadores específicos
class ServiceBedroomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Alcoba de servicio"]
        if option.strip() in allowed_options:
            return "Alcoba del servicio"

class BalconyHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Balcón"]
        if option.strip() in allowed_options:
            return "Balcón"

class KitchenHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Cocina"]
        if option.strip() in allowed_options:
            return "Cocina"

class DiningHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Comedor"]
        if option.strip() in allowed_options:
            return "Comedor"

class UsefulRoomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Cuarto útil"]
        if option.strip() in allowed_options:
            return "Cuarto útil"


class HallHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Sala"]
        if option.strip() in allowed_options:
            return "Sala"


class DiningRoomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Salón comedor"]
        if option.strip() in allowed_options:
            return "Sala comedor"


handler_chain= ServiceBedroomHandler(BalconyHandler(KitchenHandler(DiningHandler(UsefulRoomHandler(HallHandler(DiningRoomHandler()))))))


def map_option(option: str):
    return handler_chain.handle(option)


# print(map_option("Alcoba de servicio"))
# print(map_option("Cocina"))
# print(map_option("Salón comedor"))
