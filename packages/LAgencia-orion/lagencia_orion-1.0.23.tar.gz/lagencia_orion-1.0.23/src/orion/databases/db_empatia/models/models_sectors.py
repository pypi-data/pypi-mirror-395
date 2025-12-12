import uuid

from geoalchemy2 import Geometry
from sqlalchemy import CHAR, Boolean, Column, DateTime, Index, Integer, String, UniqueConstraint, func, text
from sqlalchemy.orm import relationship

from orion.databases.config_db_empatia import BaseEmpatia



class Sector(BaseEmpatia):
    __tablename__ = "sectors"
    id = Column(CHAR(36), primary_key=True)
    name = Column(String(500), nullable=False)
    # formatted_name = Column(String(100), nullable=False)
    searcher = Column(String(500), nullable=True)
    slug = Column(String(255), nullable=True)
    sector = Column(String(199), nullable=True)
    type = Column(String(50), nullable=True)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=True)
    order = Column(Integer, nullable=True)
    category_point_interest = Column(String(150), nullable=True)
    reference_sector = Column(CHAR(36), nullable=True)

    show_villacruz = Column(Boolean, nullable=False, default=False, server_default="0")
    show_rent_villacruz = Column(Boolean, nullable=False, default=False, server_default="0")
    show_sale_villacruz = Column(Boolean, nullable=False, default=False, server_default="0")
    show_furnished_villacruz = Column(Boolean, nullable=False, default=False, server_default="0")

    show_castillo = Column(Boolean, nullable=False, default=False, server_default="0")
    show_rent_castillo = Column(Boolean, nullable=False, default=False, server_default="0")
    show_sale_castillo = Column(Boolean, nullable=False, default=False, server_default="0")
    show_furnished_castillo = Column(Boolean, nullable=False, default=False, server_default="0")

    show_estrella = Column(Boolean, nullable=False, default=False, server_default="0")
    show_rent_estrella = Column(Boolean, nullable=False, default=False, server_default="0")
    show_sale_estrella = Column(Boolean, nullable=False, default=False, server_default="0")
    show_furnished_estrella = Column(Boolean, nullable=False, default=False, server_default="0")

    show_livin = Column(Boolean, nullable=False, default=False, server_default="0")
    show_rent_livin = Column(Boolean, nullable=False, default=False, server_default="0")
    show_sale_livin = Column(Boolean, nullable=False, default=False, server_default="0")
    show_furnished_livin = Column(Boolean, nullable=False, default=False, server_default="0")

    # Índices
    __table_args__ = (
        Index("ix_sectors_name", "name"),
        Index("ix_sectors_slug", "slug"),
        Index("ix_sectors_type", "type"),
        Index("ix_sectors_show_sectors", "show_villacruz", "show_castillo", "show_estrella", "show_livin"),
        Index("ix_sectors_order", "order"),
        Index("ix_sectors_show_rent_villacruz", "show_rent_villacruz"),
        Index("ix_sectors_show_sale_villacruz", "show_sale_villacruz"),
        Index("ix_sectors_show_furnished_villacruz", "show_furnished_villacruz"),
        Index("ix_sectors_show_rent_castillo", "show_rent_castillo"),
        Index("ix_sectors_show_sale_castillo", "show_sale_castillo"),
        Index("ix_sectors_show_furnished_castillo", "show_furnished_castillo"),
        Index("ix_sectors_show_rent_estrella", "show_rent_estrella"),
        Index("ix_sectors_show_sale_estrella", "show_sale_estrella"),
        Index("ix_sectors_show_furnished_estrella", "show_furnished_estrella"),
        Index("ix_sectors_show_rent_livin", "show_rent_livin"),
        Index("ix_sectors_show_sale_livin", "show_sale_livin"),
        Index("ix_sectors_show_furnished_livin", "show_furnished_livin"),
        Index("ix_sectors_searcher", "searcher"),
    )
    sectors_property = relationship("PropertySector", back_populates="sectors", cascade="all, delete")


class Municipio(BaseEmpatia):
    __tablename__ = "municipios"
    __table_args__ = (Index("idx_municipios_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_municipios_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Vereda(BaseEmpatia):
    __tablename__ = "veredas"
    __table_args__ = (Index("idx_vereda_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_veredas_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Corregimiento(BaseEmpatia):
    __tablename__ = "corregimientos"
    __table_args__ = (Index("idx_corregimientos_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_corregimientos_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Comuna(BaseEmpatia):
    __tablename__ = "comunas"
    __table_args__ = (Index("idx_comunas_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_comunas_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Barrio(BaseEmpatia):
    __tablename__ = "barrios"
    __table_args__ = (Index("idx_barrio_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_barrios_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Lugar(BaseEmpatia):
    __tablename__ = "lugares"
    __table_args__ = (Index("idx_lugares_geometry", "geometry", mysql_prefix="SPATIAL"), UniqueConstraint("name", name="uq_lugares_name"))

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    name = Column(String(100), nullable=False, unique=True)
    formatted_name = Column(String(100), nullable=False)
    geometry = Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=False)
    category_point_interest = Column(String(100), nullable=True)
    active = Column(Boolean, server_default="1")
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Alias(BaseEmpatia):
    __tablename__ = "alias"

    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"))
    origin_id = Column(CHAR(36))
    name = Column(CHAR(36))
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class RelatedNeighborhoods(BaseEmpatia):
    __tablename__ = "barrios_relacionados"
    id = Column(CHAR(36), primary_key=True, server_default=text("UUID()"), default=lambda: str(uuid.uuid4()))
    origin_id = Column(CHAR(36), nullable=False)
    origin_name = Column(String(500), nullable=False)
    related_id = Column(CHAR(36), nullable=False)
    related_name = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

