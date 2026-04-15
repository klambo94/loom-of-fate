from enum import Enum


class RarityEnum(Enum):
    COMMON = 1
    UNCOMMON = 2
    EXOTIC = 3
    RARE = 4
    LEGENDARY = 5
    MYTHIC = 6
    EXALTED = 7


class TransactionTypeEnum(str, Enum):
    #Inventory/Resource
    CRAFTING = "CRAFTING_SUCCESS" #Deduct/ Add materials logs input map, output map, recipe used
    RESOURCE_TRANSFER = "RESOURCE_TRANSFER" #Items moved between owned containers
    RESOURCE_GRANT = "RESOURCE_GRANT" #granted items
    ITEM_ACQUISITION = "ITEM_ACQUISITION"

    #Character
    PROFILE_UPDATE = "PROFILE_UPDATE"
    QUEST_STATE_CHANGE = "QUEST_STATE_CHANGE"

    #SYSTEM
    TRANSACTION_ROLLBACK = "TRANSACTION_ROLLBACK" # Used for a failure state
    SYSTEM_INIT= "SYSTEM_INIT"


