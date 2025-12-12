from shapely import MultiPolygon, Polygon


def create_geometry_from_coordinates(latitude: float, longitude: float):
    """Crea un MULTIPOLYGON a partir de las coordenadas (lat, lon)"""

    # Para hacer un MULTIPOLYGON, creamos un polígono pequeño alrededor del punto
    coordinates = [(longitude - 0.00001, latitude - 0.00001), (longitude + 0.00001, latitude - 0.00001), (longitude + 0.00001, latitude + 0.00001), (longitude - 0.00001, latitude + 0.00001), (longitude - 0.00001, latitude - 0.00001)]

    # Creamos el polígono alrededor del punto
    polygon = Polygon(coordinates)

    # Convertimos el polígono en un MULTIPOLYGON
    multipolygon = MultiPolygon([polygon])

    return multipolygon



