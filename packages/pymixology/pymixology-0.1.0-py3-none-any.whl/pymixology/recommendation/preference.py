"""Store and query user preference data."""

from __future__ import annotations

from typing import Dict, List, Any

user_profile: Dict[str, int] = {}


def set_flavor_profile(sweet: int, sour: int, bitter: int, strong: int) -> Dict[str, int]:
    """Save a simple flavor profile.
    
    Raises:
        ValueError: If any value is outside 0-10 range.
    """
    global user_profile
    for val, name in [(sweet, "sweet"), (sour, "sour"), (bitter, "bitter"), (strong, "strong")]:
        if not (0 <= int(val) <= 10):
            raise ValueError(f"{name} value must be between 0 and 10.")
    
    user_profile = {
        "sweet": int(sweet),
        "sour": int(sour),
        "bitter": int(bitter),
        "strong": int(strong),
    }
    return user_profile


def record_review(reviews_db: Any, cocktail_name: str, rating: int):
    """Record a rating in a list or dict store."""
    rating_value = int(rating)
    if isinstance(reviews_db, dict):
        reviews_db[cocktail_name] = rating_value
        return reviews_db
    if isinstance(reviews_db, list):
        reviews_db.append({"cocktail": cocktail_name, "rating": rating_value})
        return reviews_db
    raise TypeError("reviews_db must be a list or dict.")


def get_top_favorites(reviews_db: Any, top_n: int = 3) -> List[str]:
    """Return the top N cocktail names sorted by rating."""
    pairs = []
    if isinstance(reviews_db, dict):
        pairs = list(reviews_db.items())
    elif isinstance(reviews_db, list):
        for entry in reviews_db:
            name = entry.get("cocktail")
            rating = entry.get("rating", 0)
            if name is not None:
                pairs.append((name, rating))
    else:
        raise TypeError("reviews_db must be a list or dict.")

    sorted_pairs = sorted(pairs, key=lambda item: item[1], reverse=True)
    return [name for name, _ in sorted_pairs[:top_n]]
