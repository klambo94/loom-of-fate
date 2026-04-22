
from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint, Integer, Enum
from sqlalchemy.orm import relationship


from core.database import Base
from core.models.enums import RecipeMaterialType
from core.models.mixins.timestamp_mixin import TimestampMixin


class RecipeMaterials(Base, TimestampMixin):
    """
    Junction model linking Recipes and Materials in the many-to-many relationship.
    This model itself represents a single row: (recipe_id, material_id).
    """
    __tablename__ = "recipe_materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(String, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    material_id = Column(String, ForeignKey("material.id", ondelete="CASCADE"), primary_key=True)
    type = Column(Enum(RecipeMaterialType), default=RecipeMaterialType.INPUT, nullable=False)
    qty = Column(Integer, default=1, nullable=False)

    recipe = relationship("Recipe", back_populates="recipe_id")
    material = relationship("Material", back_populates="material_id")