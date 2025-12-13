"""Utility helpers for recipe math and conversions."""

from __future__ import annotations

import copy
from typing import Dict, List, Any

from ..exceptions import RecipeError

_OZ_TO_ML = 29.5735


def calculate_abv(ingredients: List[Dict[str, float]]) -> float:
    """Estimate final ABV using a volume-weighted average."""
    total_volume = sum(item.get("vol", 0) for item in ingredients)
    if total_volume <= 0:
        return 0.0
    weighted_abv = sum(item.get("vol", 0) * item.get("abv", 0) for item in ingredients)
    return weighted_abv / total_volume


def estimate_cost(ingredients: List[Dict[str, float]]) -> float:
    """Estimate cost of a single cocktail based on bottle prices and usage.
    
    Raises:
        RecipeError: If bottle volume is invalid.
    """
    cost = 0.0
    for item in ingredients:
        bottle_vol = item.get("bottle_vol", 0)
        if bottle_vol <= 0:
            raise RecipeError("Bottle volume must be greater than zero.")
        price_per_bottle = item.get("price_per_bottle", 0)
        used_vol = item.get("used_vol", 0)
        cost += (price_per_bottle / bottle_vol) * used_vol
    return cost


def unit_converter(amount: float, from_unit: str, to_unit: str) -> float:
    """Convert volumes between ml and oz.
    
    Raises:
        RecipeError: If unit is not supported.
    """
    f_unit = from_unit.lower()
    t_unit = to_unit.lower()
    if f_unit == t_unit:
        return amount
    if f_unit == "oz" and t_unit == "ml":
        return amount * _OZ_TO_ML
    if f_unit == "ml" and t_unit == "oz":
        return amount / _OZ_TO_ML
    raise RecipeError(f"Unsupported unit conversion: {from_unit} to {to_unit}")


def scale_recipe(cocktail_dict: Dict[str, Any], servings: int) -> Dict[str, Any]:
    """Return a new recipe with ingredient amounts scaled to the target servings."""
    if servings <= 0:
        raise ValueError("Servings must be positive.")
    new_recipe = copy.deepcopy(cocktail_dict)
    current_servings = cocktail_dict.get("servings", 1) or 1
    factor = servings / current_servings
    scaled_ingredients = []
    for ingredient in new_recipe.get("ingredients", []):
        if isinstance(ingredient, dict) and "amount" in ingredient:
            scaled_item = ingredient.copy()
            amount = scaled_item.get("amount")
            if isinstance(amount, (int, float)):
                scaled_item["amount"] = amount * factor
            scaled_ingredients.append(scaled_item)
        else:
            scaled_ingredients.append(ingredient)
    new_recipe["ingredients"] = scaled_ingredients
    new_recipe["servings"] = servings
    return new_recipe
