# libidx.py

def build_acronym_index(data):
    acronym_index = {}

    for category_entries in data.values():
        for entry in category_entries:
            acronym = entry.get("acronym")
            if acronym:
                acronym_index[acronym.lower()] = entry  # store whole entry

            # Include aliases
            for alias in entry.get("aliases", []):
                acronym_index[alias.lower()] = entry

    return acronym_index

def build_category_index(data):
    """
    Build a reverse index mapping each category to its list of acronym entries.

    Args:
        data (dict): Dictionary of categories → list of acronym entries.

    Returns:
        dict: Mapping of category name → list of entries.
    """
    category_index = {}
    for category_name, entries in data.items():
        category_index[category_name] = entries
    return category_index

def search_acronyms(index, query):
    """
    Perform a case-insensitive partial search on acronyms and aliases.

    Args:
        index (dict): The acronym index from `build_acronym_index`.
        query (str): The search string (partial or full).

    Returns:
        list: Matching entries (full objects) sorted alphabetically by acronym.
    """
    query_lower = query.lower()
    results = []

    for key, entry in index.items():
        if query_lower in key.lower() and entry not in results:
            results.append(entry)

    # Sort results alphabetically by primary acronym
    results.sort(key=lambda e: e["acronym"])
    return results


