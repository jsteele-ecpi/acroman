#!/usr/bin/env python3
"""
acro.py

Command-line tool to display acronyms like man pages.
"""

import argparse
import yaml
from difflib import get_close_matches
from colorama import Fore, Style, init

from libidx import build_acronym_index, build_category_index

init(autoreset=True)

DEFAULT_YAML = "acronyms.yaml"


# ------------------------------------------------------------
# Pretty Printer
# ------------------------------------------------------------
def display_entry(entry):
    title = Fore.CYAN + Style.BRIGHT
    label = Fore.YELLOW + Style.BRIGHT
    value = Fore.WHITE
    sep = Fore.MAGENTA + ("-" * 60)

    def fmt(field):
        return entry.get(field) or "None"

    print(sep)
    print(f"{title}Acronym: {value}{fmt('acronym')}")
    print(f"{label}Definition: {value}{fmt('definition')}")
    print(f"{label}Category: {value}{fmt('category')}")
    print(f"{label}Description:\n{value}{fmt('description')}")
    print(f"{label}Aliases: {value}{fmt('aliases')}")
    print(f"{label}Origin: {value}{fmt('origin')}")
    print(f"{label}Related Acronyms: {value}{fmt('related_acronyms')}")
    print(f"{label}Notes: {value}{fmt('notes')}")
    print(sep)


# ------------------------------------------------------------
# YAML Loader (guarantees dict at root)
# ------------------------------------------------------------
def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if isinstance(data, list):
        data = {"default": data}

    return data


# ------------------------------------------------------------
# Fuzzy Search (only returns acronym strings)
# ------------------------------------------------------------
# def fuzzy_search(index, query, limit=5):
#     choices = list(index.keys())
#     return get_close_matches(query.upper(), choices, n=limit, cutoff=0.6)

def fuzzy_search(index, query, limit=3):
    """
    Fuzzy search across:
    - acronym
    - aliases
    - description
    - definition
    - category
    - related_acronyms
    """

    query = query.upper()

    # Collect searchable strings mapped back to acronyms
    search_pool = {}

    for ac, entry in index.items():
        # Always allow direct acronym
        search_pool[ac] = ac

        # Aliases
        for alias in entry.get("aliases") or []:
            search_pool[alias.upper()] = ac

        # Related acronyms
        for rel in entry.get("related_acronyms") or []:
            search_pool[rel.upper()] = ac

        # Text fields (definition + description + category)
        # We store them but map BACK to the acronym
        for field in ("definition", "description", "category"):
            text = entry.get(field)
            if text:
                for word in text.upper().split():
                    search_pool[word] = ac

    # Fuzzy match the query against all searchable terms
    candidates = list(search_pool.keys())
    matches = get_close_matches(query, candidates, n=limit * 2, cutoff=0.55)

    # Convert matched search terms → acronyms
    final = []
    for m in matches:
        ac = search_pool[m]
        if ac not in final:
            final.append(ac)
        if len(final) >= limit:
            break

    return final

# ------------------------------------------------------------
# Main Program Logic
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Look up acronyms from a structured YAML reference."
    )

    parser.add_argument(
        "query",
        help="Acronym or term to search for"
    )

    parser.add_argument(
        "-f", "--fuzzy",
        action="store_true",
        help="Use fuzzy search (when exact/alias match is not known)"
    )

    parser.add_argument(
    "-l", "--limit",
    type=int,
    default=3,
    help="Maximum number of fuzzy acronym matches to return (default: 3)"
    )

    args = parser.parse_args()
    query = args.query.strip().upper()

    # Load data
    data = load_yaml(DEFAULT_YAML)
    acronym_index = build_acronym_index(data)
    category_index = build_category_index(data)

    # --------------------------------------------------------
    # 1️⃣ Exact acronym match (case-insensitive)
    # --------------------------------------------------------
    entry = acronym_index.get(query)
    if entry:
        display_entry(entry)
        return

    # --------------------------------------------------------
    # 2️⃣ Alias match (if user didn’t request fuzzy)
    # --------------------------------------------------------
    if not args.fuzzy:
        for ac, ent in acronym_index.items():
            aliases = ent.get("aliases") or []
            # Normalize alias strings to uppercase for comparison
            if any(a.upper() == query for a in aliases):
                display_entry(ent)
                return

        # No exact + no alias match → show error & exit
        print(f"\n❌ Acronym '{query}' not found.\n")
        print("Tip: Try using -f for fuzzy matching:")
        print(f"    python acro.py {args.query} -f")
        print("------------------------------------------------------------")
        return

    # --------------------------------------------------------
    # 3️⃣ Fuzzy search (only when -f is used)
    # --------------------------------------------------------
    results = fuzzy_search(acronym_index, query, limit=args.limit)

    print(f"\n❌ No exact match for '{query}'.")
    if results:
        print("\nClosest matches:\n")
        for ac in results:
            print(f"  • {ac}")

        print("\nShowing similar entries:\n")
        for ac in results:
            display_entry(acronym_index[ac])
    else:
        print("\nNo similar acronyms found.")
        print("------------------------------------------------------------")

    return


# ------------------------------------------------------------
if __name__ == "__main__":
    main()
