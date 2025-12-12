"""
Core arbiter functions.

Provides both:
- rank(): Semantically correct name, returns Ranking object
- iter(): Alias for arb.iter pun, returns list of tuples for compatibility
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

from .api import rank as _rank, Ranking, Ranked


def rank(
    query: str,
    candidates: Sequence[str],
    *,
    use_freq: bool = True,
    key: str | None = None,
) -> Ranking:
    """
    Rank candidates by semantic coherence with query.
    
    Returns a Ranking object that can be:
    - Iterated as (text, score) tuples
    - Accessed as .top for the highest-scoring candidate
    - Accessed as .results for full Ranked objects
    - Serialized via .to_dict() for JSON
    
    Example:
        >>> from arbiter_engine import rank
        >>> r = rank("Python memory management", ["garbage collection", "snake habitat"])
        >>> print(r.top.text)
        garbage collection
        >>> for text, score in r:
        ...     print(f"{score:.3f} {text}")
    """
    return _rank(query, list(candidates), use_freq=use_freq, key=key)


def iter(
    query: str,
    candidates: Sequence[str],
    use_freq: bool = True,
    top_k: int | None = None,
) -> List[Tuple[str, float]]:
    """
    Syntactic sugar for the standard ARBITER compare operation.
    
    Returns sorted (candidate, score) tuples for backwards compatibility.
    
    Note: This is an alias that allows the arb.iter pun:
        >>> import arbiter_engine as arb
        >>> arb.iter("query", ["a", "b"])  # spells "arbiter"
    
    For new code, prefer rank() which returns a proper Ranking object.
    """
    ranking = _rank(query, list(candidates), use_freq=use_freq)
    results = ranking.results[:top_k] if top_k else ranking.results
    return [(r.text, r.score) for r in results]
