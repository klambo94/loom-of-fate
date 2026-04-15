
from sqlalchemy import Column, String, Boolean, MetaData
from sqlalchemy.orm import relationship
from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class Material(Base, TimestampMixin):
    """
        Material Model - Holds what type of materials are available.
    """

    __tablename__ = 'material'
    id = Column(String, primary_key=True, index=True, doc="Internal PK: set via generate_id() function that returns a UUID.")
    name = Column(String, index=True, doc="Name of material.")
    description = Column(String, doc="Description of material.")
    is_raw = Column(Boolean, doc="Determines if this material is a raw material")
    rarity_tier = Column(String, doc="Tier to determine how rare this material is in the world.")

    rarity = relationship("Rarity", back_populates="rarity_tier")