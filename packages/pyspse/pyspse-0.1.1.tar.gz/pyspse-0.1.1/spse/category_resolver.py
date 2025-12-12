"""Category resolver for SPSE base segments."""

import json
from functools import lru_cache
from importlib import resources


@lru_cache(maxsize=1)
def load_categories():
    """Load category list from bundled JSON."""
    with resources.files(__package__).joinpath("categories.json").open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def list_categories():
    """Return all categories as list of dicts."""
    return load_categories()


def search_categories(term):
    """Case-insensitive search by name or slug."""
    term_lower = term.lower()
    return [c for c in load_categories() if term_lower in c.get("name", "").lower() or term_lower in c.get("newUrlPath", "").lower()]


def find_by_slug(slug):
    """Find exact slug match by newUrlPath."""
    slug_lower = slug.lower()
    for c in load_categories():
        if c.get("newUrlPath", "").lower() == slug_lower:
            return c
    return None