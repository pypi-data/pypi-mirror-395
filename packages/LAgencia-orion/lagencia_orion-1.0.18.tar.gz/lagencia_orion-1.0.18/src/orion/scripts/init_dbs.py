from orion.databases.config_db_bellatrix import BaseBellatrix as BaseBellatrix
from orion.databases.config_db_bellatrix import engine as engine_bellatrix
from orion.databases.config_db_empatia import BaseEmpatia as BaseEmpatia
from orion.databases.config_db_empatia import engine as engine_empatia
from orion.databases.db_empatia.models import models_sectors  # noqa: F401


def create_schemas_bellatrix():
    print("Creando esquemas bellatrix...")
    BaseBellatrix.metadata.create_all(bind=engine_bellatrix)
    print("✅ Esquemas creados correctamente")
    print(f"*** {engine_bellatrix.url}")


def create_schemas_empatia():
    print("Creando esquemas empatia...")
    BaseEmpatia.metadata.create_all(bind=engine_empatia)
    print("✅ Esquemas creados correctamente")
    print(f"*** {engine_empatia.url}")
