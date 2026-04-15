from core.models.rarity import Rarity       # Independent Entity
from core.models.material import Material   # Dependent on Rarity
from core.models.character import Character # Dependent on Material (for relationships)
from core.models.character_inventory import CharacterInventory # Depends on Character and Material
from core.models.user import User           # Dependent on character
from core.models.user_character import UserCharacter # Dependent on User/Character

# The core logic that uses the above models:
from core.models.recipes import Recipe      # Depends on Material
from core.models.recipe_materials import RecipeMaterials
from core.models.audit_log import AuditLog  # Depends on all of the above (the final consumer)

# Enums are always foundational and should be grouped together
from core.models.enums import RarityEnum, TransactionTypeEnum