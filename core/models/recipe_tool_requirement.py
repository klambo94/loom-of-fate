from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class RecipeToolRequirement(Base, TimestampMixin):

    __tablename__ = "recipe_tool_requirement"

    id = Column(String, primary_key=True)

    tool_id = Column(String, ForeignKey("tools.id", ondelete="CASCADE"), doc="Tool id of the tool.")
    recipe_id = Column(String, ForeignKey("recipes.id", ondelete="CASCADE"), doc="Recipe id of the tool.")\

    recipe = relationship("Recipes", back_populates="recipe_id")
    tool = relationship("Tools", back_populates="tool_id")