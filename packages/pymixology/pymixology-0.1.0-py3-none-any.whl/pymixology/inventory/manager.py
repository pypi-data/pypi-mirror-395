"""Helpers for managing an inventory list of ingredients."""

from __future__ import annotations

from typing import List

from .items import Ingredient
from ..exceptions import InventoryError


def add_item(inventory_list: List[Ingredient], item_object: Ingredient) -> bool:
    """Append a new Spirit or Mixer to the inventory."""
    if not isinstance(item_object, Ingredient):
        raise TypeError("item_object must be an Ingredient.")
    inventory_list.append(item_object)
    return True


def remove_item(inventory_list: List[Ingredient], item_name: str) -> bool:
    """Remove the first matching item by name.
    
    Raises:
        InventoryError: If the item is not found in the inventory.
    """
    target = item_name.lower().strip()
    for idx, item in enumerate(inventory_list):
        if item.name.lower() == target:
            del inventory_list[idx]
            return True
    raise InventoryError(f"Item '{item_name}' not found in inventory.")


def check_stock(inventory_list: List[Ingredient], item_name: str) -> float:
    """Return current quantity for an item, or 0 when missing."""
    target = item_name.lower().strip()
    for item in inventory_list:
        if item.name.lower() == target:
            return item.quantity
    return 0.0


def get_shopping_list(inventory_list: List[Ingredient], min_threshold: float) -> List[str]:
    """List names that fall below the provided threshold."""
    return [item.name for item in inventory_list if item.quantity < min_threshold]


def total_value(inventory_list: List[Ingredient]) -> float:
    """Return the total estimated value of all inventory items."""
    return sum(item.current_value() for item in inventory_list)

# Day 2 Update: Error handling review
