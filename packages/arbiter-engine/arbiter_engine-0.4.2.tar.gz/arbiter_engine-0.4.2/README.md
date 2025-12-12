# ARBITER

Semantic disambiguation in 72 dimensions. 26MB. Deterministic. No ML inference.

```bash
pip install arbiter-engine
```

## The Problem

Your vector search returns snake care guides for "Python memory management."

```python
from arbiter_engine import rank

r = rank(
    "Python memory management for large data pipelines",
    [
        "Python garbage collection uses reference counting",
        "Ball pythons require humid enclosures",
        "Reticulated pythons are the longest snakes",
        "Monty Python Flying Circus aired on BBC in 1969"
    ]
)

for text, score in r:
    print(f"{score:6.3f}  {text}")
```

```
 0.574  Python garbage collection uses reference counting
 0.248  Ball pythons require humid enclosures
 0.164  Reticulated pythons are the longest snakes
-0.085  Monty Python Flying Circus aired on BBC in 1969
```

Monty Python went **negative**. ARBITER doesn't just rank—it rejects.

## Quick Start

### Ranking

```python
from arbiter_engine import rank

r = rank("jaguar speed", ["animal running", "car performance"])
print(r.top.text, r.top.score)  # animal running 0.539
```

### CLI

```bash
arb "Python memory" "garbage collection" "snake habitat"
```

## Why ARBITER

| | |
|---|---|
| **26MB** | Runs anywhere. Air-gapped. Edge. Embedded. |
| **Deterministic** | Same input → same output. Always. |
| **No inference** | Not an LLM. Geometric measurement. |
| **72 dimensions** | 10.7× compression from 768D embeddings. |
| **Negative scores** | Wrong answers get rejected, not just ranked low. |

## Real Results

### Drug Discovery

```python
r = rank(
    "Optimize lead compound for selective COX-2 inhibition with minimal GI toxicity",
    [
        "Replace carboxylic acid with sulfonamide",
        "Convert to prodrug ester", 
        "Add polar morpholine ring"
    ]
)
print(r.top.text)  # Replace carboxylic acid with sulfonamide
```

That sulfonamide modification became Celebrex—a $3B/year drug. ARBITER scored it highest in under a second.

### Security Alert Triage

```
Query: "SECURITY ALERT: Agent persistence mechanism detected in registry run keys"

0.558  Malware establishing persistence via registry autorun
0.401  Insurance agent CRM software startup entry
0.198  Travel agent booking system launcher
```

20/20 validated on SOC triage scenarios.

## Vector Algebra

ARBITER isn't just ranking—it's a full coordinate system for meaning.

```python
from arbiter_engine import embed, blend, find_nearest, analogy

# Get 72D vectors
vector = embed("consciousness")  # shape: (72,)

# Blend concepts
peace_war = blend(["peace", "war"])
matches = find_nearest(peace_war, ["ceasefire", "battle", "truce"])
print(matches[0].text)  # ceasefire (0.899 similarity)

# Solve analogies: king - man + woman = ?
result = analogy("king", "man", "woman", ["queen", "princess", "duchess"])
print(result.text)  # duchess (0.675 similarity)
```

## Semantic Fingerprinting

Create 72D semantic fingerprints for ranking and retrieval.

```python
from arbiter_engine import SemanticCompressor

# Create semantic fingerprint (72 floats)
compressed = SemanticCompressor.compress("Your long document...")

# Query against the compressed vector directly
relevance = SemanticCompressor.similarity(compressed, "your query")
```

Results:
- 1.000 top-rank accuracy when original is in candidate set
- 0.648 cross-lingual similarity (English→Spanish)
- 0.730 relevance discrimination in compressed documents

## API Reference

### rank(query, candidates)

Rank candidates by semantic coherence.

```python
r = rank("query", ["option a", "option b", "option c"])
r.top           # Highest-scoring candidate
r.top.text      # "option a"
r.top.score     # 0.723
list(r)         # [(text, score), ...] for iteration
```

### embed(text)

Get 72D semantic vector.

```python
vector = embed("machine learning")  # numpy array, shape (72,)
```

### blend(concepts, weights=None)

Combine concepts.

```python
midpoint = blend(["hot", "cold"])  # Average
weighted = blend(["war", "peace"], weights=[0.3, 0.7])  # 70% peace
```

### find_nearest(vector, candidates)

Find closest matches to a vector.

```python
matches = find_nearest(vector, ["option a", "option b"])
matches[0].text       # Best match
matches[0].similarity # Similarity score
```

### analogy(a, b, c, candidates)

Solve a:b::c:?

```python
result = analogy("hot", "cold", "love", ["hate", "indifference"])
# hot is to cold as love is to... hate
```

### distance(concept1, concept2)

Measure semantic similarity.

```python
sim = distance("love", "affection")  # 0.847
```

## Installation

```bash
pip install arbiter-engine
```

Requirements: Python ≥ 3.8, requests, numpy, scipy

## Pricing

| Tier | Price | Use Case |
|------|-------|----------|
| **Research** | $250/month | Non-commercial. Academic & startup exploration. |
| **Startup** | $2,500/month | Commercial use up to $1M ARR. |
| **Enterprise** | $500,000/year | Self-hosted. Air-gapped. Full support. |

API key:
```bash
export ARBITER_API_KEY=arb_xxxxxxxxxxxxx
```

Get access at [getarbiter.dev](https://getarbiter.dev)

## Links

- Website: [getarbiter.dev](https://getarbiter.dev)
- API Docs: [api.arbiter.traut.ai/docs](https://api.arbiter.traut.ai/docs)
- PyPI: [pypi.org/project/arbiter-engine](https://pypi.org/project/arbiter-engine/)
- Enterprise: founder@traut.ai

## License

MIT - Copyright (c) 2025 Joel Trout II
