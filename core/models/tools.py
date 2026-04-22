from sqlalchemy import String, Column, Boolean, Integer, BLOB, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class Tools(Base, TimestampMixin):

    __tablename__ = 'tools'

    id = Column(String, primary_key=True, doc="Id of the tool")
    name = Column(String, doc="Name of the tool")
    description = Column(String, doc="Description of the tool")
    is_consumable = Column(Boolean, doc="Whether the tool is consumable")
    required_skill_lvl = Column(Integer, doc="Skill level required to use the tool")
    tool_icon = Column(String, doc="Icon of the tool")
    durability = Column(Integer, nullable=False, doc="How durable the tool is.")
    efficiency = Column(Integer, nullable=False, doc="How efficient the tool is.")

    tool_category_id = Column(String, ForeignKey("tool_category.id", ondelete="CASCADE"), doc="Categorie of the tool")
    tool_category = relationship("ToolCategory", back_populates="tools")

