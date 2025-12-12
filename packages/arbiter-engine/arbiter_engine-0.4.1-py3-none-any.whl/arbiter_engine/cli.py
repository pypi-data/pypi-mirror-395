"""
Arbiter CLI - Semantic coherence from the command line.

Usage:
    arb "query" candidate1 candidate2 candidate3
    arb --json "query" candidate1 candidate2
"""

import argparse
import json
import sys

from .core import rank
from .api import ArbiterError, ArbiterNetworkError, ArbiterRateLimitError
from .version import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="arb",
        description="Rank candidates by semantic coherence with a query.",
        epilog="Example: arb \"Python memory\" \"garbage collection\" \"snake habitat\" \"malloc\""
    )
    parser.add_argument(
        "query",
        help="Query text to measure coherence against."
    )
    parser.add_argument(
        "candidates",
        nargs="+",
        help="Candidate options to rank."
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        dest="json_output",
        help="Output as JSON for machine consumption."
    )
    parser.add_argument(
        "--no-freq",
        action="store_true",
        help="Disable frequency mapping."
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"arb {__version__}"
    )
    
    args = parser.parse_args()

    try:
        ranking = rank(
            args.query,
            args.candidates,
            use_freq=not args.no_freq
        )
    except ArbiterNetworkError as e:
        if args.json_output:
            print(json.dumps({"error": str(e), "type": "network"}))
        else:
            print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except ArbiterRateLimitError as e:
        if args.json_output:
            print(json.dumps({"error": str(e), "type": "rate_limit"}))
        else:
            print(f"Rate limit exceeded. Try again later.", file=sys.stderr)
        sys.exit(1)
    except ArbiterError as e:
        if args.json_output:
            print(json.dumps({"error": str(e), "type": "api"}))
        else:
            print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json_output:
        print(json.dumps(ranking.to_dict(), indent=2))
    else:
        print(f"\nQuery: {ranking.query}\n")
        for text, score in ranking:
            # Visual indicator for positive/negative coherence
            marker = "✓" if score > 0 else "✗" if score < 0 else " "
            print(f"{score:7.3f}  {text}  {marker}")
        print()


if __name__ == "__main__":
    main()
