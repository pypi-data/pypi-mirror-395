"""Inventory item classes with simple inheritance."""

from __future__ import annotations

from typing import Union

from ..exceptions import IngredientError


class Ingredient:
    """Generic ingredient with quantity and value tracking."""

    def __init__(self, name: str, quantity: float, expiry_date: str, value: float = 0.0) -> None:
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.unit_value = (float(value) / quantity) if quantity else 0.0

    def info(self) -> str:
        """Return a short description string."""
        value = self.current_value()
        value_part = f", Value: {value:.2f}" if value else ""
        return f"Name: {self.name}, Qty: {self.quantity}{value_part}"

    def use(self, amount: Union[int, float]) -> bool:
        """Reduce quantity when stock is available.
        
        Raises:
            IngredientError: If amount is invalid or insufficient stock.
        """
        if amount <= 0:
            raise IngredientError("Amount to use must be positive.")
        if amount > self.quantity:
            raise IngredientError(f"Insufficient stock. Have {self.quantity}, need {amount}.")
        self.quantity -= amount
        return True

    def current_value(self) -> float:
        """Return the current estimated value based on remaining quantity."""
        return self.unit_value * self.quantity


class Spirit(Ingredient):
    """Alcoholic ingredient with ABV."""

    def __init__(self, name: str, quantity: float, expiry_date: str, abv: float, value: float = 0.0) -> None:
        super().__init__(name, quantity, expiry_date, value=value)
        self.abv = abv

    def get_abv(self) -> float:
        return self.abv


class Mixer(Ingredient):
    """Non-spirit ingredient that may be carbonated."""

    def __init__(self, name: str, quantity: float, expiry_date: str, is_carbonated: bool, value: float = 0.0) -> None:
        super().__init__(name, quantity, expiry_date, value=value)
        self.is_carbonated = is_carbonated

    def is_fizzy(self) -> bool:
        return bool(self.is_carbonated)
