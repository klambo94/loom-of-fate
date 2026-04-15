from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class Character(Base, TimestampMixin):


    __tablename__ = "character"

    id = Column(String, primary_key=True, nullable=False, doc="Id of the character.")
    name = Column(String, nullable=False, doc="Name of the character.")

