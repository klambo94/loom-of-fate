import logging
import threading
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from core import Recipe, RecipeMaterials, Tools
from core.models.enums import RecipeStatus
from core.models.recipe_tool_requirement import RecipeToolRequirement

logger = logging.getLogger(__name__)

class RecipeService:
    """
        Loads crafting recipes from the database, aggregates full transformation rules,
        and caches them in-memory. Thread-safe singleton for concurrent access.
    """
    _instance = None
    _global_lock = threading.RLock()
    _cache: Dict[str, dict]
    _cache_lock: threading.RLock
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._global_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._cache: Dict[str, dict] = {}
            self._cache_lock = threading.RLock()
            self._initialized = True


    def load_recipes(self, db_session: Session) -> Dict[str, Recipe]:
        logger.debug("Loading recipes...")

        db_recipes = {}
        logger.debug("Grabbing lock.")

        try:
            with self._global_lock:
                stmt = (
                    select(Recipe)
                    .options(
                        joinedload(Recipe.recipe_materials)
                        .joinedload(RecipeMaterials.material),
                        joinedload(Recipe.tool_requirements)
                        .joinedload(RecipeToolRequirement.tool)
                        .joinedload(Tools.tool_category)
                    )
                    .where(Recipe.status == RecipeStatus.ACTIVE)
                )

                logger.debug(f"Executing query {stmt}.")
                db_recipes = db_session.execute(stmt).unique().scalars().all()
                logger.debug(f"Loaded {len(db_recipes)} recipes.")


            recipe_map = {}
            for recipe, recipe_mat, material in db_recipes:
                if recipe.id not in recipe_map:
                    recipe_map[recipe.id] = {
                        "id": recipe.id,
                        "name": recipe.name,
                        "description": recipe.description,
                        "type": recipe.recipe_type,
                        "crafting_time_min": recipe.crafting_time_min,
                        "inputs": [],
                        "outputs": [],
                        "tools": [],
                    }

                    # Aggregate materials based on type
                    if recipe.recipe_materials:
                        for rm in recipe.recipe_materials:
                            mat_entry = {
                                "material_id": rm.material.id,
                                "material_name": rm.material.name,
                                "quantity": rm.qty,
                                "rarity_tier": rm.material.rarity_tier
                            }

                            mat_type = getattr(recipe_mat, 'type', 'input')
                            if mat_type == 'input':
                                recipe_map[recipe.id]["inputs"].append(mat_entry)
                            elif mat_type == 'output':
                                recipe_map[recipe.id]["outputs"].append(mat_entry)

                    # Aggregate Tools
                    if recipe.recipe_tool_requirement:
                        for rtr in recipe.recipe_tool_requirement:
                            if rtr.tool:
                                recipe_map[recipe.id]["tools"].append({
                                    "tool_id": rtr.tool.id,
                                    "tool_name": rtr.tool.name,
                                    "category": rtr.tool.tool_category.category_name if rtr.tool.tool_category else None
                                })

            # Atomic cache update
            with self._cache_lock:
                self._cache = recipe_map

            logger.info(f"RecipeService: Successfully loaded {len(recipe_map)} recipes into cache.")
            return len(recipe_map)
        except Exception as e:
            logger.error(f"RecipeService: Failed to load recipes from DB. {e}")
            raise RuntimeError("Failed to initialize RecipeService cache") from e


    def get_recipe(self, recipe_name: str) -> Optional[dict]:
        """Retrieve a recipe by name from the in-memory cache."""
        with self._cache_lock:
            for recipe in self._cache.values():
                if recipe["name"].lower() == recipe_name.lower():
                    return recipe
        return None

    def get_recipe_by_id(self, recipe_id: str) -> Optional[dict]:
        with self._cache_lock:
            return self._cache.get(recipe_id)

    def validate_recipe_exists(self, recipe_name: str) -> bool:
        return self.get_recipe(recipe_name) is not None

    def get_recipe_materials(self, recipe_name: str) -> Optional[dict]:
        """Returns structured inputs/outputs for CraftingEngine validation."""
        recipe = self.get_recipe(recipe_name)
        if not recipe:
            return None
        return {
            "inputs": recipe["inputs"],
            "outputs": recipe["outputs"]
        }

    def refresh_cache(self, db_session: Session) -> dict[str, Recipe]:
        """Reloads recipes from DB (useful for runtime config updates)."""
        logger.info("RecipeService: Triggering cache refresh.")
        return self.load_recipes(db_session)