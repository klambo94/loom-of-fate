from logging import getLogger

from psycopg import Transaction
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session

from core import TransactionTypeEnum

logger = getLogger(__name__)
class AuditService:
    ___db:Session

    def __init__(self, database_session):
        self.___db = database_session

    def log(self, transaction_type:TransactionTypeEnum, transaction_payload: str, owner_id: str):
        """
           Inserts a single audit record into the audit_log table.
           This is purely a logging operation and does not check for existence or conflict.
           """
        try:

            self.___db.execute("""
                               INSERT INTO audit_log (transaction_type, transaction_payload, owner_id)
                               VALUES (:transaction_type, :transaction_payload, :owner_id);
                               """, {
                                   "transaction_type": transaction_type.value,  # Use the actual enum string value
                                   "transaction_payload": transaction_payload,
                                   "owner_id": owner_id
                               })
            self.___db.commit()

        except Exception as e:
            logger.error(f"Failed to write audit log entry: {e}")