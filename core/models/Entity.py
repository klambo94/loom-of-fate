from sqlalchemy import Column, String, Enum

from core.database import Base
from core.models.enums import EntityType
from core.models.mixins.timestamp_mixin import TimestampMixin


class Entity(Base, TimestampMixin):
    __tablename__ = "entity"

    id = Column(String, primary_key=True, index=True, doc="Id of the entity.")

    entity_type = Column(Enum(EntityType), nullable=False, index=True, doc="Type of the entity.")
    name = Column(String, nullable=False, index=True, doc="Name of the entity.")