"""Slug generation utilities."""

import re
import unicodedata


def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from text.

    Args:
        text: Text to convert to slug

    Returns:
        URL-friendly slug
    """
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    text = text.strip("-")
    return text


def generate_unique_slug(base_slug: str, existing_slugs: list[str]) -> str:
    """Generate a unique slug by appending a number if needed.

    Args:
        base_slug: Base slug to make unique
        existing_slugs: List of existing slugs

    Returns:
        Unique slug
    """
    if base_slug not in existing_slugs:
        return base_slug

    counter = 1
    while f"{base_slug}-{counter}" in existing_slugs:
        counter += 1

    return f"{base_slug}-{counter}"

