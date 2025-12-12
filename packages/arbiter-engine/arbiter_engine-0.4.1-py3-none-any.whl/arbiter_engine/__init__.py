"""
Arbiter Engine - Semantic Coherence Infrastructure

The coordinate system for meaning. Not just comparisons - full semantic algebra.

Usage:
    # Ranking (coherence measurement)
    >>> from arbiter_engine import rank
    >>> r = rank("Python memory management", ["garbage collection", "snake habitat"])
    >>> print(r.top.text, r.top.score)
    garbage collection 0.823

    # Vector Algebra (semantic math)
    >>> from arbiter_engine import blend, interpolate, analogy, embed
    >>>
    >>> # Blend concepts
    >>> peace_war = blend(["peace", "war"])
    >>> from arbiter_engine import find_nearest
    >>> matches = find_nearest(peace_war, ["ceasefire", "battle", "truce"])
    >>> print(matches[0].text)
    ceasefire
    >>>
    >>> # Solve analogies: king - man + woman = ?
    >>> result = analogy("king", "man", "woman", ["queen", "princess", "duchess"])
    >>> print(result.text, result.similarity)
    duchess 0.675
    >>>
    >>> # Find semantic paths
    >>> path = interpolate("hate", "love", steps=7)
    >>> # Get raw 72D vectors
    >>> vector = embed("consciousness")

    # CLI
    $ arb "query" candidate1 candidate2 candidate3
    $ arb --json "query" candidate1 candidate2
"""

from .core import iter, rank
from .api import Ranking, Ranked, ArbiterError, ArbiterNetworkError, ArbiterAPIError, ArbiterRateLimitError
from .vectors import (
    # Vector functions
    embed,
    blend,
    interpolate,
    find_nearest,
    analogy,
    distance,
    add,
    subtract,
    # Convenience aliases
    semantic_add,
    semantic_subtract,
    semantic_blend,
    # High-level classes
    SemanticCompressor,
    SemanticMessenger,
    # Data types
    SemanticMatch,
    SemanticPath,
    # Exceptions
    VectorError,
    VectorNetworkError,
    VectorAPIError,
)
from .version import __version__

__all__ = [
    # Ranking functions
    "iter",
    "rank",
    # Vector algebra functions
    "embed",
    "blend",
    "interpolate",
    "find_nearest",
    "analogy",
    "distance",
    "add",
    "subtract",
    # Convenience aliases
    "semantic_add",
    "semantic_subtract",
    "semantic_blend",
    # High-level semantic tools
    "SemanticCompressor",
    "SemanticMessenger",
    # Ranking data types
    "Ranking",
    "Ranked",
    # Vector data types
    "SemanticMatch",
    "SemanticPath",
    # Ranking exceptions
    "ArbiterError",
    "ArbiterNetworkError",
    "ArbiterAPIError",
    "ArbiterRateLimitError",
    # Vector exceptions
    "VectorError",
    "VectorNetworkError",
    "VectorAPIError",
    # Meta
    "__version__",
]
