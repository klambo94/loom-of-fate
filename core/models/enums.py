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
    ACQUIRE_LOCKS = "ACQUIRE_LOCKS"
    RELEASE_LOCKS = "RELEASE_LOCKS"
    TRANSACTION = "TRANSACTION"
    TRANSACTION_START = "TRANSACTION_START"
    TRANSACTION_STOP = "TRANSACTION_STOP"
    TRANSACTION_ROLLBACK = "TRANSACTION_ROLLBACK" # Used for a failure state
    SYSTEM_INIT= "SYSTEM_INIT"


class Scope(str, Enum):
    #Entity based Scopes
    CHARACTER_INVENTORY = "CHARACTER" # Player instance
    CHARACTER_STORAGE = "ACCOUNT_GLOBAL" #Persisted Long term storage
    GROUP_GUILD = "GROUP_GUILD" # Group /Collective

    #World Environment
    WORLD_LOOT = "WORLD_LOOT" #Environment/World


    #Process Scopes
    TRANSACTION_HOLD = "TRANSACTION_HOLD"  #Temp buffer used to hold inputs before they are committed, must clear any items with this scope out of the temp table.
    QUEUE_BUFFER = "QUEUE_BUFFER" #Prevent race conditions, scope for materials reserved for pending action.

class EntityType(str, Enum):
    PLAYER = "PLAYER"
    NPC = "NPC"
    GUILD = "GUILD"
    SYSTEM = "SYSTEM"

class RecipeMaterialType(str, Enum):
    INPUT = "INPUT",
    OUTPUT = "OUTPUT"

class RecipeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"