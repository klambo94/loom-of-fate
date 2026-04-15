from sqlalchemy import Column, String, Enum, MetaData
from core.config import settings
from core.models.enums import RarityEnum
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin

class Rarity(Base, TimestampMixin):
    """Table to determine how rare materials are in the world."""

    __tablename__ = "rarity"
    id = Column(String, primary_key=True, nullable=False, doc="Id of the rarity.")
    name = Column(String, nullable=False, doc="Name of the rarity tier.")
    rarity_type = Column(Enum(RarityEnum), nullable=False, default=RarityEnum.COMMON, doc="Material rarity type.")