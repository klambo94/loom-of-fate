from sqlalchemy import Column, String

from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class ToolCategory(Base, TimestampMixin):
    __tablename__ = "tool_category"

    id = Column(String, primary_key=True, doc="Id of the tool category.")
    category_name = Column(String, nullable=False, doc="Name of the tool category.")
    description = Column(String, nullable=False, doc="Description of the tool category.")
    tool_type = Column(String, nullable=False, doc="Type of the tool category.")
    tool_type_icon = Column(String,  doc="Icon of the tool type.")

