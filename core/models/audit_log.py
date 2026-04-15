from sqlalchemy import Column, String, Enum, MetaData
from sqlalchemy.dialects.postgresql import JSONB

from core.config import settings
from core.database import Base
from core.models.enums import TransactionTypeEnum
from core.models.mixins.timestamp_mixin import TimestampMixin


class AuditLog(Base, TimestampMixin):

    __tablename__ = "audit_log"

    id = Column(String, primary_key=True, index=True, doc="Id for user events for audits")
    user_id= Column(String, nullable=False, index=True, doc="User ID")
    transaction_type = Column(Enum(TransactionTypeEnum), index=True, nullable=False, doc="Transaction type")
    transaction_payload = Column(JSONB, nullable=False, doc="Result of the Event")
