"""
Local fallback routes through the public Arbiter API.

This module is maintained for backwards compatibility.
For new code, use `from arbiter_engine import rank` instead.
"""

from __future__ import annotations

from .api import rank


def local_iter(query, candidates):
    """
    Legacy function. Use rank() instead.
    
    Routes through the public API endpoint.
    """
    ranking = rank(query, list(candidates), use_freq=True)
    return [(r.text, r.score) for r in ranking.results]
