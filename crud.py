# crud.py

def add_entry(data, entry):
    """
    Add a new acronym entry to the data dictionary.
    entry: dict with keys: acronym, expansion, category, description, aliases, origin, related_acronyms, notes
    """
    category = entry.get("category", "Misc")
    if category not in data:
        data[category] = []
    data[category].append(entry)
    return data

def update_entry(data, acronym, updates):
    """
    Update an existing entry by acronym.
    updates: dict containing any fields to update.
    """
    for entries in data.values():
        for entry in entries:
            if entry["acronym"].lower() == acronym.lower() or acronym.lower() in [a.lower() for a in entry.get("aliases", [])]:
                entry.update(updates)
                return data, True
    return data, False

def delete_entry(data, acronym):
    """
    Delete an acronym entry from the data.
    Returns (updated_data, success_flag)
    """
    for category, entries in data.items():
        for i, entry in enumerate(entries):
            if entry["acronym"].lower() == acronym.lower() or acronym.lower() in [a.lower() for a in entry.get("aliases", [])]:
                del entries[i]
                # remove category if empty
                if not entries:
                    del data[category]
                return data, True
    return data, False

def save_data(data, filepath="acronyms.yaml"):
    """Write the updated data back to the YAML file."""
    import yaml
    with open(filepath, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
