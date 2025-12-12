"""
Arbiter API client with explicit data shapes and error handling.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

import requests

PRIVATE_API_URL = "https://api.arbiter.traut.ai/v1/compare"
PUBLIC_API_URL = "https://api.arbiter.traut.ai/public/compare"


class ArbiterError(Exception):
    """Base exception for Arbiter API errors."""
    pass


class ArbiterNetworkError(ArbiterError):
    """Raised when network request fails."""
    pass


class ArbiterAPIError(ArbiterError):
    """Raised when API returns an error response."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API error {status_code}: {message}")


class ArbiterRateLimitError(ArbiterAPIError):
    """Raised when rate limit is exceeded."""
    pass


@dataclass
class Ranked:
    """A single candidate with its coherence score."""
    text: str
    score: float
    
    def __iter__(self):
        """Allow unpacking as (text, score) tuple."""
        return iter((self.text, self.score))


@dataclass
class Ranking:
    """
    Result of a coherence ranking operation.
    
    Can be:
    - Iterated as (text, score) tuples for backwards compatibility
    - Accessed as .top for the highest-scoring candidate
    - Accessed as .results for full Ranked objects
    - Serialized to dict/JSON via .to_dict()
    """
    query: str
    candidates: List[str]
    results: List[Ranked]
    
    @property
    def top(self) -> Ranked:
        """The highest-scoring candidate."""
        return self.results[0] if self.results else None
    
    def __iter__(self):
        """Iterate as (text, score) tuples for backwards compatibility."""
        for r in self.results:
            yield r.text, r.score
    
    def __len__(self):
        return len(self.results)
    
    def to_dict(self) -> dict:
        """Serialize to dictionary for JSON output."""
        return {
            "query": self.query,
            "candidates": self.candidates,
            "top": {"text": self.top.text, "score": self.top.score} if self.top else None,
            "results": [{"text": r.text, "score": r.score} for r in self.results]
        }


# Legacy dataclasses for backwards compatibility
@dataclass
class CompareItem:
    """Legacy: use Ranked instead."""
    text: str
    score: float


@dataclass
class CompareResponse:
    """Legacy: use Ranking instead."""
    query: str
    top: List[CompareItem]
    all: List[CompareItem]


def compare(
    query: str,
    candidates: List[str],
    use_freq: bool = True,
    top_k: Optional[int] = None,
    key: Optional[str] = None,
    timeout: int = 10,
) -> CompareResponse:
    """
    Legacy compare function. Use rank() instead.
    
    Call the Arbiter compare API and structure the response.
    """
    payload = {
        "query": query,
        "candidates": list(candidates),
        "top_k": top_k or len(candidates),
        "use_freq": use_freq,
    }

    api_key = key or os.getenv("ARBITER_API_KEY")
    url = PRIVATE_API_URL if api_key else PUBLIC_API_URL
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ArbiterNetworkError("Request timed out")
    except requests.exceptions.ConnectionError:
        raise ArbiterNetworkError("Could not connect to Arbiter API")
    except requests.exceptions.RequestException as e:
        raise ArbiterNetworkError(f"Network error: {e}")
    
    if response.status_code == 429:
        raise ArbiterRateLimitError(429, "Rate limit exceeded")
    elif response.status_code >= 400:
        try:
            error_msg = response.json().get("detail", response.text)
        except:
            error_msg = response.text
        raise ArbiterAPIError(response.status_code, error_msg)
    
    data = response.json()

    def _map(items):
        return [
            CompareItem(text=item["text"], score=float(item["score"]))
            for item in items
        ]

    all_items = _map(data.get("all", []))
    top_items = _map(data.get("top", [])) or all_items[: payload["top_k"]]

    return CompareResponse(
        query=data.get("query", query),
        top=top_items,
        all=all_items,
    )


def rank(
    query: str,
    candidates: List[str],
    *,
    use_freq: bool = True,
    key: Optional[str] = None,
    timeout: int = 10,
) -> Ranking:
    """
    Rank candidates by semantic coherence with query.
    
    Returns a Ranking object that can be:
    - Iterated as (text, score) tuples
    - Accessed as .top for winner
    - Accessed as .results for full Ranked objects
    - Serialized via .to_dict()
    
    Args:
        query: The constraint/context to measure coherence against
        candidates: List of options to rank
        use_freq: Use frequency mapping (default True)
        key: API key (optional, falls back to ARBITER_API_KEY env var)
        timeout: Request timeout in seconds
    
    Returns:
        Ranking object with results sorted by coherence score
    
    Raises:
        ArbiterNetworkError: Network connectivity issues
        ArbiterRateLimitError: Rate limit exceeded
        ArbiterAPIError: API returned an error
    """
    payload = {
        "query": query,
        "candidates": list(candidates),
        "top_k": len(candidates),
        "use_freq": use_freq,
    }

    api_key = key or os.getenv("ARBITER_API_KEY")
    url = PRIVATE_API_URL if api_key else PUBLIC_API_URL
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout:
        raise ArbiterNetworkError("Request timed out")
    except requests.exceptions.ConnectionError:
        raise ArbiterNetworkError("Could not connect to Arbiter API")
    except requests.exceptions.RequestException as e:
        raise ArbiterNetworkError(f"Network error: {e}")
    
    if response.status_code == 429:
        raise ArbiterRateLimitError(429, "Rate limit exceeded")
    elif response.status_code >= 400:
        try:
            error_msg = response.json().get("detail", response.text)
        except:
            error_msg = response.text
        raise ArbiterAPIError(response.status_code, error_msg)
    
    data = response.json()
    
    results = [
        Ranked(text=item["text"], score=float(item["score"]))
        for item in data.get("all", [])
    ]
    
    return Ranking(
        query=data.get("query", query),
        candidates=list(candidates),
        results=results
    )


def api_iter(query, candidates, key):
    """Legacy helper maintained for backwards compatibility."""
    resp = compare(query, list(candidates), key=key)
    return [(item.text, item.score) for item in resp.all]
