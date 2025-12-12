from .resolver import CountryResolver

__all__ = ["CountryResolver"]


# Optional module-level singleton for convenience
_resolver: CountryResolver | None = None


def get_resolver(allow_fuzzy: bool = False, fuzzy_min_score: float = 0.86) -> CountryResolver:
    """
    Get a singleton CountryResolver instance for the current process.

    In Lambda, this means you can call get_resolver() inside the handler and
    the data will be re-used across warm invocations.
    """
    global _resolver
    if _resolver is None:
        _resolver = CountryResolver(allow_fuzzy=allow_fuzzy, fuzzy_min_score=fuzzy_min_score)
    return _resolver
