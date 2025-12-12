column_mapping_attributes = {
        "id": "id",
        "Cuarto Y Baño De Servicio": "Alcoba del servicio",
        "Balcon": "Balcón",
        "Baño Social": "Baño social",
        "Cocina": "Cocina",
        "Comedor": "Comedor",
        "Cuarto Util": "Cuarto útil",
        "Gas": "Gas",
        "Gimnasio": "Gimnasio",
        "Parqueadero Interno": "Parqueadero cubierto",
        "Piscina": "Piscina",
        "Portería": "Portería",
        "Sala": "Sala",
        "Sala Comedor": "Sala comedor",
        "Unidad Cerrada": "Unidad cerrada",
    }



class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle(self, option: str):
        result = self.process(option)
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
        allowed_options = ["Cuarto Y Baño De Servicio"]
        if option.strip() in allowed_options:
            return "Alcoba del servicio"


class BalconyHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Balcon"]
        if option.strip() in allowed_options:
            return "Balcón"


class SocialBathroomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Baño Social"]
        if option.strip() in allowed_options:
            return "Baño social"


class KitchenHandler(Handler):
    def process(self, option: str):
        allowed_options = [
            "Cocineta", "Cocina Electrica", "Cocina Integral",
            "Cocina Abierta", "Cocina Cerrada", "Cocina Mixta",
            "Cocina Semi-integral", "Cocina Americana"
        ]
        if option.strip() in allowed_options:
            return "Cocina"


class DiningHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Comedor"]
        if option.strip() in allowed_options:
            return "Comedor"


class UsefulRoomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Cuarto Util"]
        if option.strip() in allowed_options:
            return "Cuarto útil"


class GasHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Gas Natural", "Gas Propano"]
        if option.strip() in allowed_options:
            return "Gas"


class GymHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Gimnasio"]
        if option.strip() in allowed_options:
            return "Gimnasio"


class CoveredParkingHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Parqueadero Interno"]
        if option.strip() in allowed_options:
            return "Parqueadero cubierto"


class PoolHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Piscina"]
        if option.strip() in allowed_options:
            return "Piscina"


class HallHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Sala"]
        if option.strip() in allowed_options:
            return "Sala"


class DiningRoomHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Sala Comedor"]
        if option.strip() in allowed_options:
            return "Sala comedor"


class ClosedUnitHandler(Handler):
    def process(self, option: str):
        allowed_options = ["Unidad Cerrada", "Circuito Cerrado", "Conjunto Cerrado"]
        if option.strip() in allowed_options:
            return "Unidad cerrada"


# Crear la cadena de responsabilidad
handler_chain = ServiceBedroomHandler(
    BalconyHandler(
        SocialBathroomHandler(
            KitchenHandler(
                DiningHandler(
                    UsefulRoomHandler(
                        GasHandler(
                            GymHandler(
                                CoveredParkingHandler(
                                    PoolHandler(
                                        HallHandler(
                                            DiningRoomHandler(
                                                ClosedUnitHandler()
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
)


# Uso de la cadena
def map_option(option: str):
    return handler_chain.handle(option)


# # Pruebas
# print(map_option("Balcon"))  # "Balcón"
# print(map_option("Cocina Americana"))  # "Cocina"
# print(map_option("Unidad Cerrada"))  # "Unidad cerrada"
# print(map_option("No existe"))  # None
