#!/usr/bin/env python3
"""
build-index.py — Query and filter skills_index.json via CLI.

Reads skills_index.json and filters by phase, category, or stability.
Outputs filtered results as JSON to stdout.

Usage:
    python tools/build-index.py --phase v1
    python tools/build-index.py --category compression
    python tools/build-index.py --stability stable
    python tools/build-index.py --phase v1 --category encoding
    python tools/build-index.py  # No filters = all skills
"""

import os
import sys
import json
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Query and filter the Marlin skills index"
    )
    parser.add_argument(
        "--phase",
        choices=["v1", "v3"],
        help="Filter by phase (v1 or v3)",
    )
    parser.add_argument(
        "--category",
        choices=[
            "compression", "parsing", "schema", "encoding",
            "formatting", "estimation", "bridge"
        ],
        help="Filter by category",
    )
    parser.add_argument(
        "--stability",
        choices=["stable", "experimental"],
        help="Filter by stability",
    )
    parser.add_argument(
        "--index-file",
        default=None,
        help="Path to skills_index.json (auto-detected if not specified)",
    )

    args = parser.parse_args()

    # Find skills_index.json
    if args.index_file:
        index_path = args.index_file
    else:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        index_path = os.path.join(repo_root, "skills_index.json")

    if not os.path.isfile(index_path):
        print(f"ERROR: skills_index.json not found at {index_path}", file=sys.stderr)
        print("Run 'python tools/generate-catalog.py' first.", file=sys.stderr)
        sys.exit(1)

    with open(index_path, "r", encoding="utf-8") as f:
        index_data = json.load(f)

    skills = index_data.get("skills", [])

    # Apply filters
    if args.phase:
        skills = [s for s in skills if s.get("phase") == args.phase]

    if args.category:
        skills = [s for s in skills if s.get("category") == args.category]

    if args.stability:
        skills = [s for s in skills if s.get("stability") == args.stability]

    # Build output
    output = {
        "generated_at": index_data.get("generated_at", "unknown"),
        "filters": {
            "phase": args.phase,
            "category": args.category,
            "stability": args.stability,
        },
        "total": len(skills),
        "skills": skills,
    }

    # Remove None filters for cleaner output
    output["filters"] = {k: v for k, v in output["filters"].items() if v is not None}

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
