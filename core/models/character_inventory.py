from sqlalchemy import Column, String, Integer, Table, ForeignKey, PrimaryKeyConstraint, MetaData
from sqlalchemy.orm import relationship
from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class CharacterInventory(Base, TimestampMixin):
    __tablename__ = "character_inventory"
    __table_args__ = (

        PrimaryKeyConstraint('character_id', 'material_id'),
    )
    character_id = Column(String, ForeignKey("character.id", ondelete="CASCADE"), index=True, nullable=False)
    material_id = Column(String, ForeignKey("material.id", ondelete="CASCADE"), index=True, nullable=False, doc="Id of the material in the inventory.")
    matertial_quanty = Column(Integer, nullable=False, doc="Quantity of the material in the inventory.")

    character = relationship("Character", back_populates="character_id")
    material = relationship("Material", back_populates="material_id")
