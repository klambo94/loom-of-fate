import logging
import json
from json import JSONEncoder

from fastapi_pagination.ext import sqlalchemy
from sqlalchemy.orm import Session

from core import TransactionTypeEnum
from core.exceptions import MalformedRequestParmsException, ResourceLockException
from core.exceptions.error_enums import ErrorCodeEnum
from core.models import audit_log
from core.models.enums import Scope
from services.AuditService import AuditService

logger = logging.getLogger(__name__)

class MaterialService:
    """Manages all inventory handling"""
    ___db: Session
    audit_service: AuditService

    def __init__(self, db_session: Session):
        self.___db = db_session
        audit_service = AuditService(self.___db)

    def acquire_and_validate(self,
                             owner_id: str,
                             inv_scope: str,
                             operations: list[dict],
                             required_inputs: dict[str, int]) -> tuple[dict | None, bool]:
        """ Acquires the necessary locks on resources, validates said resources.
            :param owner_id: is the owner of the resource
            :param inv_scope: is the scope of the inventory
            :param operations: a list of operations to validate against
            :param required_inputs: the required inputs to validate against
            :return Lock context: is_valid based on validations."""

        logger.info("Acquiring lock and validating material requirements")

        if not owner_id or not inv_scope or not operations or not required_inputs:
            err: str = (f"Unable to acquire locks for empty or null inputs. "
                        f"Owner: {owner_id}, inv_scope: {inv_scope}, "
                        f"operations: {operations}, required inputs: {required_inputs}.")
            logger.error(err)
            self.audit_service.log(transaction_type=TransactionTypeEnum.ACQUIRE_LOCKS,
                                   transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                           "required_inputs": required_inputs,
                                                                           "inv_scope": inv_scope,
                                                                           "err_msg": err,
                                                                           "exception": ErrorCodeEnum.MALFORMED_REQUEST_ERROR
                                                                           }),
                                   owner_id=owner_id)
            raise MalformedRequestParmsException(f"{err} Error Code: ({ErrorCodeEnum.MALFORMED_REQUEST_ERROR})")

        try:
            # start db connection
            self.___db.begin()
            self.audit_service.log(transaction_type=TransactionTypeEnum.ACQUIRE_LOCKS,
                                   transaction_payload=JSONEncoder.encode({"stage": "start",
                                                                           "required_inputs": required_inputs,
                                                                           "inv_scope": inv_scope
                                                                           }),
                                   owner_id=owner_id)

            material_ids = required_inputs["material_ids"]
            lock_query, = """
                          SELECT material_id, material_quantity
                          FROM inventory
                          WHERE owner_id = :owner_id,
                               AND material_id IN :material_ids
                               AND scope = :inv_scope
                        FOR UPDATE;
                          """

            locked_data = self.___db.execute(lock_query, owner_id=owner_id, material_ids=material_ids, inv_scope=inv_scope)


            # check for deduct, as we can't remove what we don't have but we can add what we don't have
            # so we must validate that 1) the material exists and 2) there is enough material
            contains_deduct_op: bool = False
            for op in operations:
                if op[type] == 'deduct':
                    contains_deduct_op =  True

            validation_map = {item['material_id']: item['material_quantity'] for item in locked_data}
            for r_material_id, r_required_qty in required_inputs.items():
                material_id_inv = validation_map[r_material_id]
                material_inv_qty = validation_map[r_required_qty]
                if (material_id_inv  is None
                        or (contains_deduct_op and material_inv_qty < r_required_qty)):
                    return None, False


            return {'locked_data': validation_map}, True

        except sqlalchemy.exe.OperationalError as e:

            if "deadlock" in str(e).lower() or "timeout" in str(e).lower():
                err = f"Database contention detected. Locks may be in use. Please retry. Error: {e}"
                logging.warning(err)
                self.audit_service.log(transaction_type=TransactionTypeEnum.ACQUIRE_LOCKS,
                                       transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                               "required_inputs": required_inputs,
                                                                               "inv_scope": inv_scope,
                                                                               "err_msg": err,
                                                                               "exception": e
                                                                               }))
                raise ResourceLockException(err)
            else:
                self.audit_service.log(transaction_type=TransactionTypeEnum.ACQUIRE_LOCKS,
                                       transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                               "required_inputs": required_inputs,
                                                                               "inv_scope": inv_scope,
                                                                               "err_msg": e.message,
                                                                               "exception": e
                                                                               }))
            raise e

        except Exception as e:
            err: str = f"Unable to acquire locks or validate due to Exception. Exception: {e}."
            logger.error(err)
            self.audit_service.log(transaction_type=TransactionTypeEnum.ACQUIRE_LOCKS,
                                   transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                           "required_inputs": required_inputs,
                                                                           "inv_scope": inv_scope,
                                                                           "err_msg": err,
                                                                           "exception": "e"
                                                                           }),
                                   owner_id=owner_id)
            raise RuntimeError(err) from e


    def execute_atomic_transaction(self,
                                   locked_context: dict,
                                   inv_scope: Scope,
                                   operations: list[dict]) -> bool:
        """
            Executes a batch of updates (deduction and/or addition) using the resources
            that have already been locked by the calling service.

            This function executes ALL database writes atomically within one scope.
            :param locked_context: A dictionary containing key parameters needed for WHERE clauses (owner_id, etc.).
            :param operations: List of dictionaries defining {type: 'deduct'/'add', material_id: str, qty: int}
            :param inv_scope: id of material
            :returns a boolean if transaction was successful or not.
        """

        if not locked_context or not operations:
            err:str = "Locked context or operations are not available in request."
            self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION,
                                   transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                           "locked_context": locked_context,
                                                                           "operations": operations,
                                                                           "inv_scope": inv_scope,
                                                                           "err_msg": err,
                                                                           "exception": ErrorCodeEnum.MALFORMED_REQUEST_ERROR
                                                                           }),
                                   owner_id=locked_context['owner_id'])
            raise MalformedRequestParmsException(err)
        owner_id = locked_context['owner_id']
        self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION_START,
                               transaction_payload=JSONEncoder.encode({"stage": "start",
                                                                       "locked_context": locked_context,
                                                                       "operations":operations,
                                                                       "inv_scope": inv_scope,
                                                                       }),
                               owner_id=owner_id)
        try:
            with self.___db.begin():

                for op in operations:
                    material_id = locked_context["material_id"]
                    qty = locked_context["qty"]
                    op_type = op

                    if op_type == "deduct":
                        self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION,
                                               transaction_payload=JSONEncoder.encode({"stage": "update",
                                                                                       "inv_scope": inv_scope,
                                                                                       "material_id": material_id,
                                                                                       "qty": qty,
                                                                                       "op_type": op_type}),
                                               owner_id = owner_id)
                        self.___db.execute(""" UPDATE inventory 
                                SET material_quantity = material_quantity - :qty 
                                WHERE owner_id = :owner_id 
                                  AND scope = :inv_scope
                                  AND material_id = :material_id""",
                            {
                                "qty": qty,
                                "owner_id": owner_id,
                                "material_id": material_id
                            })
                    elif op_type == "add":
                        self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION,
                                               transaction_payload=JSONEncoder.encode({"stage": "update",
                                                                                       "inv_scope": inv_scope,
                                                                                       "material_id": material_id,
                                                                                       "qty": qty,
                                                                                       "op_type": op_type}),
                                               owner_id=owner_id)
                        self.___db.execute(""" UPDATE inventory
                                               SET material_quantity = material_quantity + :qty
                                               WHERE owner_id = :owner_id
                                                 AND scope = :inv_scope
                                                 AND material_id = :material_id""",
                                           {
                                               "qty": qty,
                                               "owner_id": owner_id,
                                               "material_id": material_id
                                           })

                    self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION_STOP,
                                           transaction_payload=JSONEncoder.encode({"stage": "success",
                                                                                   "inv_scope": inv_scope,
                                                                                   "material_id": material_id,
                                                                                   "qty": qty,
                                                                                   "op_type": op_type}),
                                           owner_id=owner_id)
                    logger.info("Successfully executed the atomic transaction.")
                    return True
        except Exception as e:
            err = f"Failed to execute the atomic transaction: {e}"
            self.audit_service.log(transaction_type=TransactionTypeEnum.TRANSACTION,
                                   transaction_payload=JSONEncoder.encode({"stage": "error",
                                                                           "locked_context": locked_context,
                                                                           "operations": operations
                                                                           }),
                                   owner_id=owner_id)
            return False

    def deduct(self, owner_id: str, material_id: str, inv_scope: Scope, qty: int) -> tuple[bool, list[dict]]:
        """
        Checks if a deduction is feasible based on current inventory
        and prepares the operation structure for the central transaction executor.
        :param owner_id: Owner ID
        :param material_id: Material ID
        :param inv_scope: Inventory Scope
        :param qty: Quantity to deduct
        :returns and Operation object to encapsulate the deduction
        """
        if not owner_id or not material_id or not inv_scope or not qty:
            logger.error("Deduction failed: Missing one or more required parameters.")
            return False, []

        if qty <= 0:
            logger.error("Deduction failed: Required quantity must be positive.")
            return False, []

        # If feasible, we return the necessary operation list.
        operations = [
            {'type': 'deduct',
             'material_id': material_id,
             'qty': qty}
        ]
        return True, operations

    def add(self, owner_id: str,
            material_id: str,
            inv_scope: Scope,
            qty: int) -> tuple[bool, list[dict]]:
        """
        Logic Caller: Validates input and prepares the operation structure
        for adding materials to the inventory.
        Returns (is_valid: bool, operations: list[dict])
        """
        if not owner_id or not material_id or not inv_scope or not qty:
            logger.error("Addition failed: Missing one or more required parameters.")
            return False, []

        if qty <= 0:
            logger.error("Addition failed: Required quantity must be positive.")
            return False, []

        operations = [
            {'type': 'add',
             'material_id': material_id,
             'qty': qty}
        ]
        return True, operations

    def transfer_ownership(self,
                           curr_owner_id: str,
                           next_owner_id: str,
                           material_id: str,
                           curr_scope: Scope,
                           new_scope: Scope,
                           qty: int) -> tuple[bool, dict]:
        """
        Calculates the parameters for a full transfer transaction.
        Returns (is_transfer_feasible: bool, operation_payload: dict)
        """
        if not curr_owner_id or not next_owner_id or not material_id or not qty:
            logger.error("Transfer failed: Missing one or more required parameters.")
            return False, {}

        if qty <= 0:
            logger.error("Transfer failed: Quantity must be positive.")
            return False, {}

        # If feasible, package both operations and all necessary context for the orchestrator.
        payload = {'deductions': [
            {'type': 'deduct',
             'material_id': material_id,
             'qty': qty}  # Deduct from current owner/scope
        ], 'increments': [
            {'type': 'add',
             'material_id': material_id,
             'qty': qty}  # Add to new owner/scope
        ], 'contexts': {
            'source_owner': curr_owner_id, 'source_scope': curr_scope,
            'target_owner': next_owner_id, 'target_scope': new_scope
        }}
        # Context is vital because the source and target owners/scopes are different.

        return True, payload