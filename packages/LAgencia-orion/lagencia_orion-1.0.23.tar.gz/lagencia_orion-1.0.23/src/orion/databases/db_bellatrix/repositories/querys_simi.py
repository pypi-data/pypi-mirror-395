from orion.databases.db_bellatrix.models.model_simi import Simi
from orion.databases.db_bellatrix.repositories.querys_base_bellatix import BaseCRUD


class QuerysSimi(BaseCRUD[Simi]):
    model = Simi

