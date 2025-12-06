# libidx.py

# def build_acronym_index(data):
#     """
#     Build a fast lookup table from a structured acronym YAML dictionary.

#     Args:
#         data (dict): Dictionary of categories → list of acronym entries.
#             Example:
#             {
#             "Security": [{entry1}, {entry2}, ...],
#             "Networking": [{entry3}, ...],
#             }

#     Returns:
#         dict: Mapping of acronym or alias → entry object.
#     """
#     index = {}
#     for category_entries in data.values():
#         for entry in category_entries:
#             # Primary acronym
#             index[entry["acronym"]] = entry
#             # Aliases
#             for alias in entry.get("aliases", []):
#                 index[alias] = entry
#     return index

# def build_acronym_index(data):
#     acronym_index = {}

#     if isinstance(data, dict):
#         iterable = data.values()
#     elif isinstance(data, list):
#         iterable = data
#     else:
#         raise TypeError(f"Unsupported data type: {type(data)}")

#     for category in iterable:
#         if isinstance(category, list):
#             for entry in category:
#                 acronym_index[entry["acronym"]] = entry["definition"]
#         else:
#             acronym_index[category["acronym"]] = category["definition"]

#     return acronym_index

def build_acronym_index(data):
    acronym_index = {}

    for category_entries in data.values():
        for entry in category_entries:
            acronym = entry.get("acronym")
            if acronym:
                acronym_index[acronym] = entry  # store whole entry

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


