from orion.databases.db_empatia.models.model_leech import UpdateCodes
from orion.databases.db_empatia.repositories.querys_base_empatia import BaseCRUD


class QuerysUpdateCodes(BaseCRUD[UpdateCodes]):
    model = UpdateCodes
