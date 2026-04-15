from sqlalchemy import PrimaryKeyConstraint, Column, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship

from core.config import settings
from core.database import Base
from core.models.mixins.timestamp_mixin import TimestampMixin


class UserCharacter(Base, TimestampMixin):

    __tablename__ = "user_character"

    __table_args__ = (
        PrimaryKeyConstraint('character_id', 'user_id'),
    )

    character_id = Column(String, ForeignKey("character.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)

    character = relationship("Character", back_populates="character_id")
    user = relationship("User", back_populates="user_id")
