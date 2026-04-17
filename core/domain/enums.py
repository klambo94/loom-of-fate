from enum import Enum

class OperationType(str, Enum):
    ADD = "ADD",
    DEDUCT = "DEDUCT",
    TRANSFER = "TRANSFER",
