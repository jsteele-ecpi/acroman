# AcroMan ~ Acronym 'manpage' CLI

> A fast, lightweight command-line tool for searching and exploring computer science acronyms.  
> Built for speed, simplicity, and usability — powered by a structured YAML database and Python indexes.

---

## Features

- 🔍 **Exact lookup**: Quickly retrieve an acronym’s full expansion, category, description, aliases, origin, and related terms.  
- 🎯 **Fuzzy search**: Match partial terms in acronyms, aliases, or descriptions.  
- 🗂️ **Category-aware**: Each entry contains metadata like category and related acronyms.  
- ⚡ **Fast**: Uses an in-memory index for O(1) lookups, even with thousands of entries.  
- 🛠️ **TUI-ready**: Designed to integrate seamlessly with a future terminal UI.

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jsteele-ecpi/acroman.git
cd acroman
```

2. Install Dependencies
```bash
pip install pyyaml
```

## Usage
```bash
python3 acro.py {acronym}
```

## Examples

### Exact lookup
```bash
python3 acro.py API
```

### Fuzzy Search
```bash
python acro.py interface -f
```

Returns all entries where `interface` appears in the acronym, aliases, or description.

## Development Notes

All acronym data is CRUD-ready, enabling future integration with a TUI or database backend.

Indexes (acronym_index and category_index) ensure lightning-fast lookups.

Aliases are automatically included in lookups — no duplicate entries required.

⚡ Tip: Even with ~2,500 YAML lines, lookups are instantaneous due to the hash-table index.

## Contributing

Fork the repository

Make edits to acronyms.yaml or libidx.py

Submit a pull request

All contributions should maintain consistent YAML formatting and index-friendly structure.

## License

MIT License © 2025