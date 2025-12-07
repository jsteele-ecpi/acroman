# libidx.py

def normalize_data(data):
    """
    Ensure data is always a dict of category -> list of entries.
    - If data is a flat list, wrap in {"All": data}
    - If a category has a single dict instead of a list, wrap it in a list
    """
    if isinstance(data, list):
        return {"All": data}

    normalized = {}
    for k, v in data.items():
        if isinstance(v, dict):
            normalized[k] = [v]
        else:
            normalized[k] = v
    return normalized

def build_acronym_index(data):
    data = normalize_data(data)
    acronym_index = {}
    for category_entries in data.values():
        for entry in category_entries:
            acronym = entry.get("acronym")
            if acronym:
                acronym_index[acronym.lower()] = entry
            for alias in entry.get("aliases", []):
                acronym_index[alias.lower()] = entry
    return acronym_index

def build_category_index(data):
    data = normalize_data(data)
    category_index = {}
    for category_name, entries in data.items():
        category_index[category_name] = entries
    return category_index

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


