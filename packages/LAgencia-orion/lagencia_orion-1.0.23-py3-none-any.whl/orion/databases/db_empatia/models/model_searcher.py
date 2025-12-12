from datetime import datetime, timezone

from geoalchemy2 import Geometry
from sqlalchemy import CHAR, JSON, BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Index, Integer, PrimaryKeyConstraint, SmallInteger, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from orion.databases.config_db_empatia import BaseEmpatia
from orion.databases.db_empatia.models.models_sectors import Sector  # noqa: F401

class Property(BaseEmpatia):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    code = Column(CHAR(15), nullable=True)
    title = Column(String(255), nullable=True)
    tag = Column(String(255))
    description = Column(Text, nullable=True)
    slug = Column(String(255), nullable=True)
    price = Column(BigInteger, default=0)
    old_price = Column(BigInteger, nullable=True)
    property_type = Column(CHAR(20), nullable=True)
    property_type_searcher = Column(CHAR(50), nullable=True)
    management = Column(CHAR(20), nullable=True)
    area = Column(Float(10, 1), default=0.0)
    bedrooms = Column(Integer, default=0)
    bathrooms = Column(Integer, default=0)
    garage = Column(Integer, default=0)
    elevator = Column(Boolean, default=False)
    image = Column(String(500), nullable=True)
    video = Column(String(150), nullable=True)
    price_admon = Column(String(20), default=0)
    show_furnished = Column(Boolean, default=False)

    show_villacruz = Column(Boolean, default=False)
    show_rent_villacruz = Column(Boolean, default=False)
    show_sale_villacruz = Column(Boolean, default=False)
    show_furnished_villacruz = Column(Boolean, default=False)

    show_castillo = Column(Boolean, default=False)
    show_rent_castillo = Column(Boolean, default=False)
    show_sale_castillo = Column(Boolean, default=False)
    show_furnished_castillo = Column(Boolean, default=False)

    show_estrella = Column(Boolean, default=False)
    show_rent_estrella = Column(Boolean, default=False)
    show_sale_estrella = Column(Boolean, default=False)
    show_furnished_estrella = Column(Boolean, default=False)

    show_livin = Column(Boolean, default=False)
    show_rent_livin = Column(Boolean, default=False)
    show_sale_livin = Column(Boolean, default=False)
    show_furnished_livin = Column(Boolean, default=False)

    show_mls_lagencia = Column(Boolean, default=True, server_default=text("true"))
    source = Column(String(50), nullable=True)
    prefix_code = Column(String(15), nullable=True)

    featured = Column(Boolean, default=False)
    age = Column(SmallInteger, default=0)
    urbanization = Column(String(150), nullable=True)
    stratum = Column(SmallInteger, nullable=True)
    address = Column(String(255), nullable=True)
    neighborhood = Column(CHAR(255), nullable=True)
    keys_in = Column(String(255), nullable=True)
    modified_date = Column(DateTime, nullable=True)
    date_to_vacate = Column(DateTime, nullable=True)
    value_predial = Column(SmallInteger, default=0)
    latitude = Column(CHAR(50), nullable=True)
    longitude = Column(CHAR(50), nullable=True)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON", srid=4326), nullable=True)

    alt = Column(String(255), nullable=True)
    tit = Column(String(255), nullable=True)
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(1000), nullable=True)
    meta_keywords = Column(String(1000), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    attributes_property = relationship("AttributeProperties", back_populates="properties", cascade="all, delete")
    gallery_property = relationship("GalleryProperties", back_populates="properties", cascade="all, delete")
    sectors_property = relationship("PropertySector", back_populates="properties", cascade="all, delete")

    descriptions = relationship("DescriptionOfProperty", back_populates="property", cascade="all, delete")

    # Indices
    __table_args__ = (
        Index("ix_properties_code", "code"),
        Index("ix_properties_slug", "slug"),
        Index("ix_properties_price", "price"),
        Index("ix_properties_property_type", "property_type"),
        Index("ix_properties_management", "management"),
        Index("ix_properties_area", "area"),
        Index("ix_properties_bedrooms", "bedrooms"),
        Index("ix_properties_bathrooms", "bathrooms"),
        Index("ix_properties_featured", "featured"),
        Index("ix_properties_garage", "garage"),
        Index(
            "ix_properties_show_properties",
            "show_livin",
            "show_villacruz",
            "show_estrella",
            "show_castillo",
        ),
    )


class Attributes(BaseEmpatia):
    __tablename__ = "attributes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=True)


class AttributeProperties(BaseEmpatia):
    __tablename__ = "attribute_properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    attribute_id = Column(Integer, nullable=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)

    properties = relationship("Property", back_populates="attributes_property")

    # Índices
    __table_args__ = (
        Index("ix_attribute_properties_attribute_id", "attribute_id"),  # Equivalente a KEY attribute_id
        Index("ix_attribute_properties_property_id", "property_id"),  # Equivalente a KEY property_id
    )


class GalleryProperties(BaseEmpatia):
    __tablename__ = "gallery_properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    image = Column(String(255), nullable=True)

    properties = relationship("Property", back_populates="gallery_property")

    # Índices
    __table_args__ = (
        Index("ix_gallery_properties_property_id", "property_id"),  # Equivalente a KEY property_id
    )



class PropertySector(BaseEmpatia):
    __tablename__ = "property_sectors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    sector_id = Column(CHAR(36), ForeignKey("sectors.id", ondelete="CASCADE"), nullable=False)
    meters = Column(Float(6, 2), default=0.00)

    properties = relationship("Property", back_populates="sectors_property")
    sectors = relationship("Sector", back_populates="sectors_property")

    # Índices
    __table_args__ = (
        Index("ix_property_sectors_property_id", "property_id"),  # Equivalente a KEY place_interest_id
        Index("ix_property_sectors_sector_id", "sector_id"),  # Equivalente a KEY sector_id
        Index("ix_property_sectors_searcher_id", "sector_id"),  # Equivalente a KEY searcher_id
    )


class Subscriptions(BaseEmpatia):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    favorite_data_id = Column(Integer)
    name = Column(String(200), nullable=True)
    mobile = Column(String(15), nullable=False)
    email = Column(String(200), nullable=True)
    slug_sectors = Column(String(1000), nullable=False)
    management = Column(String(15))
    property_types = Column(String(300))
    bedrooms = Column(String(20))
    bathrooms = Column(String(20))
    garages = Column(String(20))
    price = Column(String(50))
    option = Column(String(150))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    website = Column(String(30), nullable=True)
    token = Column(String(100))
    adviser_name = Column(String(200), nullable=True)
    adviser_mobile = Column(String(15), nullable=False)
    send_noti= Column(Boolean)
    day_noti= Column(String(20))
    week_noti= Column(Integer)
    send_match = Column(Boolean, default=False)

    new_revenues = relationship("NewRevenues", back_populates="suscribers", cascade="all, delete")


class NewRevenues(BaseEmpatia):
    __tablename__ = "new_revenues"

    subscription_id = Column(Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), primary_key=True)
    price= Column(BigInteger, default=0)
    old_price= Column(BigInteger, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), nullable=False)
    notified = Column(Boolean, default=False)
    type_template= Column(String(20))

    __table_args__ = (PrimaryKeyConstraint(subscription_id, property_id),)

    suscribers = relationship("Subscriptions", back_populates="new_revenues")


class MapPropertyType(BaseEmpatia):
    __tablename__ = "map_property_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    singular = Column(String(50), nullable=False)
    plural = Column(String(50), nullable=False)


class DescriptionOfProperty(BaseEmpatia):
    __tablename__ = "description_of_properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"), nullable=False)
    description_current = Column(Text)
    attributes = Column(JSON, nullable=True, default=None, server_default=None)

    property = relationship("Property", back_populates="descriptions")


class PropertyCatchments(BaseEmpatia):
    __tablename__ = "property_catchments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    images = Column(Text, nullable=True)
    real_estate = Column(String(20), nullable=True)
    attributes = Column(JSON, nullable=True)
    verified = Column(Boolean, default=False, server_default=text("0"))


class Neighborhoods(BaseEmpatia):
    __tablename__ = "neighborhoods"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_match = Column(String(100), nullable=False)
    name_show = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="POLYGON"), nullable=False)


class EmailTemplate(BaseEmpatia):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    html_body = Column(Text, nullable=False)

