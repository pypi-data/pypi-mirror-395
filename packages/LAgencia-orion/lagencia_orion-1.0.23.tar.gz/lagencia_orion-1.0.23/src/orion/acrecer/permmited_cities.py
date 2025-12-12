"""Listado de ciudades permitidas para consultar en el servicio MLS Acrecer.

Esta lista define las ciudades sobre las cuales se realizarán las consultas
a la API de Acrecer. Es la configuración por defecto para la extracción de datos.
"""

CIUDADES = [
    "EL RETIRO",
    "ENVIGADO",
    "ITAGUI",
    "Itaguí",
    "LA CEJA",
    "LA ESTRELLA",
    "MEDELLÍN",
    "RETIRO",
    "RIONEGRO",
    "SABANETA",
    "San Antonio De Pereira",
    "San Antonio De Prado",
]


FILTERS_MLS_ACRECER = [
    {"city": "ENVIGADO", "zone": "BOSQUES DE ZUÑIGA"},
    {"city": "ENVIGADO", "zone": "ENVIGADO"},
    {"city": "ENVIGADO", "zone": "Guanteros"},
    {"city": "ENVIGADO", "zone": "LAS PALMAS"},
    {"city": "ENVIGADO", "zone": "SUR"},
    {"city": "ITAGUI", "zone": "ITAGUI"},
    {"city": "ITAGUI", "zone": "LIMONAR"},
    {"city": "Itaguí", "zone": "ITAGUI"},
    {"city": "MEDELLÍN", "zone": "El Poblado"},
    {"city": "MEDELLÍN", "zone": "LAURELES"},
    {"city": "MEDELLÍN", "zone": "MEDELLIN"},
    {"city": "MEDELLÍN", "zone": "POBLADO"},
    {"city": "Medellín", "zone": "CENTRORIENTAL"},
    {"city": "Medellín", "zone": "Centroccidental"},
    {"city": "Medellín", "zone": "SUR ORIENTAL"},
    {"city": "Medellín", "zone": "Suroccidental"},
    {"city": "SABANETA", "zone": "AVES MARIA"},
    {"city": "SABANETA", "zone": "LAS VEGAS"},
    {"city": "SABANETA", "zone": "SABANETA"},
]
