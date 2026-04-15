from sqlalchemy import Column, String

from core.database import Base
from core.models.mixins import timestamp_mixin


class ToolCategory(Base, timestamp_mixin):
    __tablename__ = "tool_category"

    id = Column(String, primary_key=True, doc="Id of the tool category.")
    category_name = Column(String, doc="Name of the tool category.")
    description = Column(String, doc="Description of the tool category.")
    tool_type = Column(String, doc="Type of the tool category.")
    tool_type_icon = Column(String, doc="Icon of the tool type.")

