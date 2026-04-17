from sqlalchemy import Column, String, Integer, Table, ForeignKey, PrimaryKeyConstraint, Enum
from sqlalchemy.orm import relationship
from core.config import settings
from core.database import Base
from core.models.enums import Scope
from core.models.mixins.timestamp_mixin import TimestampMixin


class  Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"
    __table_args__ = (
        PrimaryKeyConstraint('owner_id', 'scope', 'material_id'),
    )

    owner_id = Column(String, ForeignKey("entity.id", ondelete="CASCADE"), index=True, nullable=False)
    material_id = Column(String, ForeignKey("material.id", ondelete="CASCADE"), index=True, nullable=False, doc="Id of the material in the inventory.")
    matertial_quanty = Column(Integer, nullable=False, doc="Quantity of the material in the inventory.")
    scope = Column(Enum(Scope), nullable=False, index=True, doc="Scope of the material in the inventory.")


    owner = relationship("Entity", back_populates="entity_id")
    material = relationship("Material", back_populates="material_id")
