"""
Arbiter Vectors - Semantic Algebra in 72 Dimensions

The coordinate system for meaning. Blend concepts, find semantic paths,
solve analogies, and navigate meaning space.

Examples:
    >>> from arbiter_engine import blend, interpolate, analogy
    >>>
    >>> # Blend concepts
    >>> peace_treaty = blend(["war", "peace"])  # Returns semantic coordinates
    >>>
    >>> # Find semantic path
    >>> path = interpolate("hate", "love", steps=5)
    >>>
    >>> # Solve analogies
    >>> result = analogy("king", "man", "woman", ["queen", "princess", "duchess"])
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple, Union

import numpy as np
import requests
from scipy.spatial.distance import cosine

EMBED_API_URL = "https://api.arbiter.traut.ai/public/embed"


class VectorError(Exception):
    """Base exception for vector operations."""
    pass


class VectorNetworkError(VectorError):
    """Raised when network request fails."""
    pass


class VectorAPIError(VectorError):
    """Raised when API returns an error."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Vector API error {status_code}: {message}")


@dataclass
class SemanticMatch:
    """A concept and its similarity to a target vector."""
    text: str
    similarity: float

    def __iter__(self):
        """Allow unpacking as (text, similarity) tuple."""
        return iter((self.text, self.similarity))


@dataclass
class SemanticPath:
    """A path through semantic space from one concept to another."""
    start: str
    end: str
    steps: int
    path_vectors: List[np.ndarray]
    nearest_concepts: Optional[List[str]] = None

    def __len__(self):
        return self.steps

    def __iter__(self):
        """Iterate over path vectors."""
        return iter(self.path_vectors)


def _get_vectors(
    texts: Sequence[str],
    use_freq: bool = True,
    key: Optional[str] = None,
    timeout: int = 10
) -> Tuple[np.ndarray, int]:
    """
    Get 72D semantic vectors from ARBITER embed API.

    Returns:
        (vectors, dimensionality) tuple where vectors is shape (n_texts, dim)
    """
    payload = {
        "texts": list(texts),
        "use_freq": use_freq
    }

    api_key = key or os.getenv("ARBITER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    try:
        response = requests.post(EMBED_API_URL, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        raise VectorNetworkError("Request timed out")
    except requests.exceptions.ConnectionError:
        raise VectorNetworkError("Could not connect to ARBITER API")
    except requests.exceptions.RequestException as e:
        raise VectorNetworkError(f"Network error: {e}")

    if response.status_code >= 400:
        try:
            error_msg = response.json().get("detail", response.text)
        except:
            error_msg = response.text
        raise VectorAPIError(response.status_code, error_msg)

    data = response.json()
    vectors = np.array(data["vectors"])
    dim = data.get("dim", vectors.shape[1] if len(vectors) > 0 else 72)

    return vectors, dim


def embed(
    text: Union[str, Sequence[str]],
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> Union[np.ndarray, List[np.ndarray]]:
    """
    Get 72D semantic vector(s) for text.

    Args:
        text: Single string or sequence of strings to embed
        use_freq: Use frequency mapping (default True)
        key: Optional API key

    Returns:
        Single vector (if text is string) or list of vectors (if text is sequence)

    Example:
        >>> vector = embed("consciousness")
        >>> vector.shape
        (72,)
        >>> vectors = embed(["love", "hate", "indifference"])
        >>> len(vectors)
        3
    """
    if isinstance(text, str):
        vectors, _ = _get_vectors([text], use_freq=use_freq, key=key)
        return vectors[0]
    else:
        vectors, _ = _get_vectors(text, use_freq=use_freq, key=key)
        return list(vectors)


def blend(
    concepts: Sequence[str],
    weights: Optional[Sequence[float]] = None,
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> np.ndarray:
    """
    Blend multiple concepts with optional weights.

    Args:
        concepts: List of concepts to blend
        weights: Optional weights for each concept (default: equal weights)
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        72D blended semantic vector

    Example:
        >>> # Equal blend
        >>> peace_treaty = blend(["war", "peace"])
        >>>
        >>> # Weighted blend (more peace than war)
        >>> compromise = blend(["war", "peace"], weights=[0.3, 0.7])
        >>>
        >>> # Three-way blend
        >>> fusion = blend(["technology", "art", "science"], weights=[0.4, 0.3, 0.3])
    """
    vectors, _ = _get_vectors(concepts, use_freq=use_freq, key=key)

    if weights is None:
        weights = np.ones(len(concepts)) / len(concepts)
    else:
        weights = np.array(weights)
        if len(weights) != len(concepts):
            raise ValueError(f"Number of weights ({len(weights)}) must match number of concepts ({len(concepts)})")
        # Normalize weights to sum to 1
        weights = weights / weights.sum()

    blended = np.average(vectors, weights=weights, axis=0)
    return blended


def interpolate(
    start: str,
    end: str,
    steps: int = 5,
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> SemanticPath:
    """
    Find semantic path between two concepts.

    Args:
        start: Starting concept
        end: Ending concept
        steps: Number of points along the path (including start and end)
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        SemanticPath object with path_vectors

    Example:
        >>> path = interpolate("hate", "love", steps=7)
        >>> len(path)
        7
        >>> # Get vectors along the path
        >>> for i, vector in enumerate(path):
        ...     print(f"Step {i}: {vector.shape}")
    """
    if steps < 2:
        raise ValueError("steps must be at least 2")

    vectors, _ = _get_vectors([start, end], use_freq=use_freq, key=key)
    v_start, v_end = vectors[0], vectors[1]

    path_vectors = []
    for i in range(steps):
        t = i / (steps - 1)
        point = (1 - t) * v_start + t * v_end
        path_vectors.append(point)

    return SemanticPath(
        start=start,
        end=end,
        steps=steps,
        path_vectors=path_vectors
    )


def find_nearest(
    vector: np.ndarray,
    candidates: Sequence[str],
    top_k: Optional[int] = None,
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> List[SemanticMatch]:
    """
    Find which candidates are nearest to a vector.

    Args:
        vector: Target semantic vector (72D)
        candidates: List of concepts to compare
        top_k: Return only top K matches (default: all)
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        List of SemanticMatch objects sorted by similarity (high to low)

    Example:
        >>> # Find what a blend means
        >>> peace_war = blend(["peace", "war"])
        >>> matches = find_nearest(peace_war, ["truce", "battle", "ceasefire"])
        >>> print(matches[0].text, matches[0].similarity)
        ceasefire 0.899
    """
    candidate_vectors, _ = _get_vectors(candidates, use_freq=use_freq, key=key)

    matches = []
    for text, candidate_vec in zip(candidates, candidate_vectors):
        similarity = 1 - cosine(vector, candidate_vec)
        matches.append(SemanticMatch(text=text, similarity=similarity))

    # Sort by similarity (high to low)
    matches.sort(key=lambda x: x.similarity, reverse=True)

    if top_k is not None:
        matches = matches[:top_k]

    return matches


def analogy(
    a: str,
    b: str,
    c: str,
    candidates: Sequence[str],
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> SemanticMatch:
    """
    Solve semantic analogies: a is to b as c is to ?

    Computes the vector: c + (b - a), then finds the nearest candidate.

    Args:
        a: First term of source relationship
        b: Second term of source relationship
        c: First term of target relationship
        candidates: Possible answers for second term of target
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        Best matching candidate with similarity score

    Example:
        >>> # king is to man as woman is to ?
        >>> result = analogy("king", "man", "woman",
        ...                  ["queen", "princess", "duchess"])
        >>> print(result.text, result.similarity)
        duchess 0.675
        >>>
        >>> # hot is to cold as love is to ?
        >>> result = analogy("hot", "cold", "love",
        ...                  ["hate", "indifference", "apathy"])
        >>> print(result.text)
        hate
    """
    vectors, _ = _get_vectors([a, b, c], use_freq=use_freq, key=key)
    va, vb, vc = vectors[0], vectors[1], vectors[2]

    # Compute analogical vector: c + (b - a)
    result_vector = vc + (vb - va)

    # Find nearest candidate
    matches = find_nearest(result_vector, candidates, top_k=1,
                          use_freq=use_freq, key=key)

    return matches[0] if matches else None


def distance(
    concept1: Union[str, np.ndarray],
    concept2: Union[str, np.ndarray],
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> float:
    """
    Measure semantic distance between two concepts.

    Args:
        concept1: First concept (string or vector)
        concept2: Second concept (string or vector)
        use_freq: Use frequency mapping (if concepts are strings)
        key: Optional API key

    Returns:
        Cosine similarity (1 = identical, 0 = unrelated, -1 = opposite)

    Example:
        >>> similarity = distance("love", "affection")
        >>> print(f"{similarity:.3f}")
        0.847
        >>>
        >>> # Can also use pre-computed vectors
        >>> v1 = embed("machine learning")
        >>> v2 = embed("artificial intelligence")
        >>> similarity = distance(v1, v2)
    """
    if isinstance(concept1, str):
        v1 = embed(concept1, use_freq=use_freq, key=key)
    else:
        v1 = concept1

    if isinstance(concept2, str):
        v2 = embed(concept2, use_freq=use_freq, key=key)
    else:
        v2 = concept2

    return 1 - cosine(v1, v2)


def add(
    *concepts: str,
    use_freq: bool = True,
    key: Optional[str] = None
) -> np.ndarray:
    """
    Add semantic vectors (equal to blend with equal weights).

    Args:
        *concepts: Concepts to add
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        Sum of semantic vectors

    Example:
        >>> # war + peace
        >>> result = add("war", "peace")
        >>> matches = find_nearest(result, ["ceasefire", "battle", "truce"])
        >>> print(matches[0].text)
        ceasefire
    """
    vectors, _ = _get_vectors(concepts, use_freq=use_freq, key=key)
    return np.sum(vectors, axis=0)


def subtract(
    concept1: str,
    concept2: str,
    *,
    use_freq: bool = True,
    key: Optional[str] = None
) -> np.ndarray:
    """
    Subtract semantic vectors.

    Args:
        concept1: Concept to subtract from
        concept2: Concept to subtract
        use_freq: Use frequency mapping
        key: Optional API key

    Returns:
        Difference vector

    Example:
        >>> # What's the "royal" component? (king - man)
        >>> royal = subtract("king", "man")
        >>> # Add it to woman
        >>> woman_vec = embed("woman")
        >>> result = royal + woman_vec
        >>> matches = find_nearest(result, ["queen", "princess", "peasant"])
        >>> print(matches[0].text)
        duchess
    """
    vectors, _ = _get_vectors([concept1, concept2], use_freq=use_freq, key=key)
    return vectors[0] - vectors[1]


# Convenience aliases for mathematical feel
def semantic_add(*concepts, **kwargs):
    """Alias for add()."""
    return add(*concepts, **kwargs)


def semantic_subtract(a, b, **kwargs):
    """Alias for subtract()."""
    return subtract(a, b, **kwargs)


def semantic_blend(concepts, weights=None, **kwargs):
    """Alias for blend()."""
    return blend(concepts, weights=weights, **kwargs)


class SemanticCompressor:
    """
    Compress and query documents using semantic vectors.

    Compress any text to 72 numbers with preserved meaning.
    Query compressed documents without decompression.

    Examples:
        >>> # Compress a document
        >>> doc = "Quantum biology breakthroughs in photosynthesis efficiency"
        >>> compressed = SemanticCompressor.compress(doc)
        >>> print(compressed.shape)
        (72,)
        >>>
        >>> # Query the compressed document
        >>> relevance = SemanticCompressor.similarity(compressed, "quantum effects")
        >>> print(f"Relevance: {relevance:.3f}")
        0.730
        >>>
        >>> # Batch compress multiple documents
        >>> docs = ["Document 1", "Document 2", "Document 3"]
        >>> compressed_docs = SemanticCompressor.batch_compress(docs)
        >>> print(len(compressed_docs))
        3
    """

    @staticmethod
    def compress(text: str, *, use_freq: bool = True, key: Optional[str] = None) -> np.ndarray:
        """
        Compress any text to 72 semantic coordinates.

        Args:
            text: Text to compress
            use_freq: Use frequency mapping
            key: Optional API key

        Returns:
            72D semantic vector representing the text
        """
        return embed(text, use_freq=use_freq, key=key)

    @staticmethod
    def similarity(compressed_doc: np.ndarray, query: str, *, use_freq: bool = True, key: Optional[str] = None) -> float:
        """
        Measure relevance between compressed document and query.

        Args:
            compressed_doc: Compressed document (72D vector)
            query: Query string
            use_freq: Use frequency mapping for query
            key: Optional API key

        Returns:
            Similarity score (1 = identical, 0 = unrelated)
        """
        query_vec = embed(query, use_freq=use_freq, key=key)
        return 1 - cosine(compressed_doc, query_vec)

    @staticmethod
    def batch_compress(texts: List[str], *, use_freq: bool = True, key: Optional[str] = None) -> List[np.ndarray]:
        """
        Compress multiple documents efficiently.

        Args:
            texts: List of texts to compress
            use_freq: Use frequency mapping
            key: Optional API key

        Returns:
            List of 72D vectors
        """
        return embed(texts, use_freq=use_freq, key=key)


class SemanticMessenger:
    """
    Language-agnostic semantic communication protocol.

    Encode messages to semantic coordinates, decode to any language.
    The "semantic telegraph" - transmit meaning as 72 numbers.

    Examples:
        >>> # Encode a message
        >>> message = "Deploy emergency response team to grid sector 7B"
        >>> vector = SemanticMessenger.encode(message)
        >>> print(vector.shape)
        (72,)
        >>>
        >>> # Decode to nearest candidate
        >>> candidates = [
        ...     "Deploy emergency response team to grid sector 7B",
        ...     "Stand down all teams",
        ...     "Begin routine maintenance"
        ... ]
        >>> decoded = SemanticMessenger.decode(vector, candidates)
        >>> print(decoded)
        Deploy emergency response team to grid sector 7B
        >>>
        >>> # Cross-lingual communication
        >>> english_msg = "We need urgent medical supplies"
        >>> vector = SemanticMessenger.encode(english_msg)
        >>> spanish_options = [
        ...     "Necesitamos suministros médicos urgentes",
        ...     "Todo está bien",
        ...     "Esperando instrucciones"
        ... ]
        >>> decoded_spanish = SemanticMessenger.decode(vector, spanish_options)
        >>> print(decoded_spanish)
        Necesitamos suministros médicos urgentes
    """

    @staticmethod
    def encode(message: str, *, use_freq: bool = True, key: Optional[str] = None) -> np.ndarray:
        """
        Encode message to semantic coordinates.

        Args:
            message: Message to encode
            use_freq: Use frequency mapping
            key: Optional API key

        Returns:
            72D semantic vector
        """
        return embed(message, use_freq=use_freq, key=key)

    @staticmethod
    def decode(vector: np.ndarray, language_candidates: List[str], *, use_freq: bool = True, key: Optional[str] = None) -> str:
        """
        Decode vector to nearest meaning in target language.

        Args:
            vector: Semantic vector to decode
            language_candidates: Possible messages in target language
            use_freq: Use frequency mapping for candidates
            key: Optional API key

        Returns:
            Best matching message from candidates
        """
        matches = find_nearest(vector, language_candidates, top_k=1, use_freq=use_freq, key=key)
        return matches[0].text if matches else ""

    @staticmethod
    def similarity(vector: np.ndarray, candidate: str, *, use_freq: bool = True, key: Optional[str] = None) -> float:
        """
        Measure how well a candidate matches the encoded vector.

        Args:
            vector: Encoded message vector
            candidate: Candidate message
            use_freq: Use frequency mapping
            key: Optional API key

        Returns:
            Similarity score (1 = perfect match, 0 = unrelated)
        """
        candidate_vec = embed(candidate, use_freq=use_freq, key=key)
        return 1 - cosine(vector, candidate_vec)
