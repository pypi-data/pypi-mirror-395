from orion.databases.db_bellatrix.models.model_softin import Softin
from orion.databases.db_bellatrix.repositories.querys_base_bellatix import BaseCRUD


class QuerysSoftin(BaseCRUD[Softin]):
    model = Softin
