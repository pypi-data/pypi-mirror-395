from orion.databases.db_bellatrix.models.model_mls import MLS
from orion.databases.db_bellatrix.repositories.querys_base_bellatix import BaseCRUD


class QuerysMLS(BaseCRUD[MLS]):
    model = MLS
