"""Recommendation helpers using recipes and inventory data."""

from __future__ import annotations

import random
from typing import Iterable, List, Dict, Any

from pymixology.inventory.items import Ingredient
from ..exceptions import RecommendationError


def _normalize_ingredient(item: Any) -> Dict[str, Any]:
    """Normalize ingredient representation to a consistent dict."""
    if isinstance(item, dict):
        return {
            "name": str(item.get("name", "")),
            "amount": item.get("amount"),
            "unit": item.get("unit"),
        }
    return {"name": str(item), "amount": None, "unit": None}


def _ingredient_name(item: Any) -> str:
    """Normalize ingredient representation to a name string."""
    return _normalize_ingredient(item).get("name", "")


def _has_required_amount(required: Dict[str, Any], inventory_item: Ingredient) -> bool:
    """Check whether inventory quantity satisfies recipe requirement (when provided)."""
    required_amount = required.get("amount")
    if isinstance(required_amount, (int, float)) and required_amount > 0:
        return inventory_item.quantity >= required_amount
    return True


def get_makeable_cocktails(inventory_list: List[Ingredient], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Return cocktail names that can be made with current inventory."""
    inventory_lookup = {item.name.lower(): item for item in inventory_list}
    ready: List[str] = []
    for recipe in recipe_db:
        normalized_ingredients = [_normalize_ingredient(item) for item in recipe.get("ingredients", [])]
        if not normalized_ingredients:
            continue
        can_make = True
        for ingredient in normalized_ingredients:
            name = ingredient.get("name", "").lower()
            inventory_item = inventory_lookup.get(name)
            if not inventory_item or not _has_required_amount(ingredient, inventory_item):
                can_make = False
                break
        if can_make:
            ready.append(recipe.get("name", ""))
    return ready


def find_cocktails_with_ingredients(target_ingredients: List[str], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Recommend cocktails that include any of the target ingredients."""
    targets = {item.lower() for item in target_ingredients}
    matches = []
    for recipe in recipe_db:
        ingredients = {_normalize_ingredient(item).get("name", "").lower() for item in recipe.get("ingredients", [])}
        if ingredients & targets:
            matches.append(recipe.get("name", ""))
    return matches


def recommend_by_flavor(user_profile: Dict[str, int], recipe_db: Iterable[Dict[str, Any]]) -> List[str]:
    """Match recipes against user flavor preferences.
    
    Raises:
        RecommendationError: If profile contains invalid values.
    """
    scored = []
    for key, val in user_profile.items():
        if val < 0:
            raise RecommendationError(f"Invalid profile value for {key}: {val}")

    for recipe in recipe_db:
        flavor_key = str(recipe.get("flavor", "")).lower()
        score = user_profile.get(flavor_key, 0)
        if score > 0:
            scored.append((score, recipe.get("name", "")))
    scored.sort(reverse=True, key=lambda item: item[0])
    return [name for _, name in scored]


def surprise_me(recipe_db: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Return a random cocktail dict.
    
    Raises:
        RecommendationError: If no recipes are available.
    """
    recipes = list(recipe_db)
    if not recipes:
        raise RecommendationError("No recipes available.")
    return random.choice(recipes)

# Day 2 Update: Error handling review
