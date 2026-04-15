from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from core.config import Settings, settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class RecipeMaterials(Base, TimestampMixin):
    """
    Junction model linking Recipes and Materials in the many-to-many relationship.
    This model itself represents a single row: (recipe_id, material_id).
    """
    __tablename__ = "recipe_materials"

    __table_args__ = (
        PrimaryKeyConstraint('recipe_id', 'material_id'),
    )

    recipe_id = Column(String, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    material_id = Column(String, ForeignKey("material.id", ondelete="CASCADE"), primary_key=True)

    recipe = relationship("Recipe", back_populates="recipe_id")
    material = relationship("Material", back_populates="material_id")