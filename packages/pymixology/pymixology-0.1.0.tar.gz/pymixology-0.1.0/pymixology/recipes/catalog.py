"""Recipe catalog utilities for loading and querying cocktails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Dict, Any

from ..exceptions import DataLoadError


def load_recipes(filepath: str) -> List[Dict[str, Any]]:
    """Load recipe data from a JSON file into a list of dicts.
    
    Raises:
        DataLoadError: If the file cannot be read or parsed.
    """
    path = Path(filepath)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise DataLoadError(f"Recipe file not found: {filepath}") from e
    except json.JSONDecodeError as e:
        raise DataLoadError(f"Failed to parse recipe file: {e}") from e

    if not isinstance(data, list):
        raise ValueError("Recipe data must be a list of dicts.")
    return [_normalize_recipe(recipe) for recipe in data]


def search_cocktail(recipe_db: Iterable[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """Find cocktails whose names contain the given query (case-insensitive)."""
    query = name.lower().strip()
    results: List[Dict[str, Any]] = []
    for recipe in recipe_db:
        cocktail_name = str(recipe.get("name", "")).lower()
        if query in cocktail_name:
            results.append(recipe)
    return results


def filter_by_base(recipe_db: Iterable[Dict[str, Any]], base_spirit: str) -> List[Dict[str, Any]]:
    """Filter cocktails by base spirit (case-insensitive exact match)."""
    target = base_spirit.lower().strip()
    return [recipe for recipe in recipe_db if str(recipe.get("base", "")).lower() == target]


def display_recipe(cocktail_dict: Dict[str, Any]) -> None:
    """Print a formatted recipe summary."""
    name = cocktail_dict.get("name", "Unknown Cocktail")
    ingredients = [_normalize_ingredient(item) for item in cocktail_dict.get("ingredients", [])]
    steps = cocktail_dict.get("steps", [])

    print(f"Recipe: {name}")
    print("Ingredients:")
    for item in ingredients:
        print(f"- {_format_ingredient(item)}")
    print("Steps:")
    for i, step in enumerate(steps, start=1):
        print(f"{i}. {step}")


def _normalize_ingredient(ingredient: Any) -> Dict[str, Any]:
    """Ensure an ingredient entry is a consistently shaped dict."""
    if isinstance(ingredient, dict):
        return {
            "name": str(ingredient.get("name", "")),
            "amount": ingredient.get("amount"),
            "unit": ingredient.get("unit"),
        }
    return {"name": str(ingredient), "amount": None, "unit": None}


def _normalize_recipe(recipe: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize ingredient entries inside a recipe dict."""
    normalized = dict(recipe)
    normalized["ingredients"] = [_normalize_ingredient(item) for item in recipe.get("ingredients", [])]
    return normalized


def _format_ingredient(ingredient: Dict[str, Any]) -> str:
    """Render an ingredient dict into a human-friendly string."""
    name = ingredient.get("name", "Unknown ingredient")
    amount = ingredient.get("amount")
    unit = ingredient.get("unit")
    if amount is None:
        return name
    if isinstance(amount, (int, float)):
        amount_str = f"{amount:.2f}".rstrip("0").rstrip(".")
    else:
        amount_str = str(amount)
    if unit:
        return f"{amount_str} {unit} {name}"
    return f"{amount_str} {name}"

# Day 2 Update: Error handling review
