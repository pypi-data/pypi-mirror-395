"""Custom exceptions for the pymixology package."""

class MixologyError(Exception):
    """Base class for all pymixology exceptions."""
    pass

class IngredientError(MixologyError):
    """Raised when there is an issue with an ingredient."""
    pass

class InventoryError(MixologyError):
    """Raised when there is an issue with inventory management."""
    pass

class RecipeError(MixologyError):
    """Raised when there is an issue with a recipe."""
    pass

class RecommendationError(MixologyError):
    """Raised when there is an issue with recommendations."""
    pass

class DataLoadError(MixologyError):
    """Raised when data loading fails."""
    pass

