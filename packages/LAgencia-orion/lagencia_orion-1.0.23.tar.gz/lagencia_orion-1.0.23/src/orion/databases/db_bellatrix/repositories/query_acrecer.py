from orion.databases.db_bellatrix.models.model_acrecer import MLSAcrecer
from orion.databases.db_bellatrix.repositories.querys_base_bellatix import BaseCRUD


class QuerysMLSAcrecer(BaseCRUD[MLSAcrecer]):
    model = MLSAcrecer
