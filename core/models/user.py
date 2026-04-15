from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, PrimaryKeyConstraint, MetaData
from sqlalchemy.orm import relationship

from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, doc="Internal PK: set via generate_id() function that returns a UUID")
    email = Column(String, unique=True, index=True, nullable=False, doc="Email address of user")

    character_id = Column(String, ForeignKey("character.id", ondelete="SET NULL"), index=True, nullable=False)

    character = relationship("UserCharacter", back_populates="character_id")

