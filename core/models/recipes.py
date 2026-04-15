from sqlalchemy import Column, String, Table, ForeignKey, MetaData, Integer
from sqlalchemy.orm import relationship, DeclarativeBase
from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin



# Many-to-Many between recipe and materials


class Recipe(Base, TimestampMixin):

    __tablename__ = "recipes"

    id = Column(String, primary_key=True, doc="Id of the recipe.")
    name = Column(String, doc="Name of the recipe.")
    description = Column(String, doc="Description of the recipe.")
    recipe_type = Column(String, doc="Type of the recipe.")
    crafting_time_min = Column(Integer, nullable=False, doc="Minutes of the recipe.")
    tool_reqs = Column(String, nullable=False, doc="Tool requirements.")
    materials = Column(String, nullable=False, doc="Materials.")
    tool_requirements = relationship("RecipieToolRequirement", back_populates="tool_reqs",  doc="Tool Requirements of the recipe.")
    recipe_materials = relationship("RecipeMaterials", back_populates="materials", doc="Materials of the recipe.")



