
from .rarity import Rarity      #  Independent Entity
from .material import Material   # Depends on Rarity
from .character import Character # Dependent on Material (for relationships)
from .character_inventory import CharacterInventory # Depends on Character and Material
from .user import User           # Dependent on character
from .user_character import UserCharacter # Depends on User/Character

# The core logic that uses the above models:
from .recipes import Recipe      # Depends on Material & RecipeRules
from .recipe_materials import RecipeMaterials
from .audit_log import AuditLog  # Depends on all of the above (the final consumer)

# Enums are always foundational and should be grouped together
from .enums import RarityEnum, TransactionTypeEnum

__all__ = [
    "Rarity",
    "Material",
    "Character",
    "CharacterInventory",
    "User",
    "UserCharacter",
    "Recipe",
    "RecipeMaterials",
    "AuditLog",
    "RarityEnum",
    "TransactionTypeEnum"
]
