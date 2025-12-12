#from sqlalchemy.future import select

#from orion.databases.config_db_empatia import get_session_empatia
from orion.databases.db_empatia.models.model_searcher import (
    AttributeProperties,
    Attributes,
    DescriptionOfProperty,
    GalleryProperties,
    MapPropertyType,
    Neighborhoods,
    NewRevenues,
    Property,
    PropertyCatchments,
    PropertySector,
    #Sector,
    Subscriptions,
)
from orion.databases.db_empatia.repositories.querys_base_empatia import BaseCRUD


class QuerysProperty(BaseCRUD[Property]):
    model = Property


class QuerysAttributes(BaseCRUD[Attributes]):
    model = Attributes


class QuerysAttributeProperties(BaseCRUD[AttributeProperties]):
    model = AttributeProperties


class QuerysGalleryProperties(BaseCRUD[GalleryProperties]):
    model = GalleryProperties


# class QuerysSector(BaseCRUD[Sector]):
#     model = Sector

#     def update_reference_id(name_lugar: str, reference_sector):
#         with get_session_empatia() as session:
#             stmt = select(Sector).where(Sector.name == name_lugar)
#             records = session.scalars(stmt).all()
#             for record in records:
#                 record.reference_sector = reference_sector
#             session.commit()


class QuerysPropertySector(BaseCRUD[PropertySector]):
    model = PropertySector


class QuerysSubscriptions(BaseCRUD[Subscriptions]):
    model = Subscriptions


class QuerysNewRevenues(BaseCRUD[NewRevenues]):
    model = NewRevenues


class QuerysMapPropertyType(BaseCRUD[MapPropertyType]):
    model = MapPropertyType


class QuerysDescriptionOfProperty(BaseCRUD[DescriptionOfProperty]):
    model = DescriptionOfProperty


class QuerysPropertyCatchments(BaseCRUD[PropertyCatchments]):
    model = PropertyCatchments


class QuerysNeighborhoods(BaseCRUD[Neighborhoods]):
    model = Neighborhoods
