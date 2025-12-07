#!/usr/bin/env python3
"""
tui.py

Prototype ncurses TUI for acronym lookup and CRUD operations.
"""

import curses
import yaml
from libidx import build_acronym_index, build_category_index
import crud  # our CRUD functions

YAML_FILE = "acronyms.yaml"

def main(stdscr):
    curses.curs_set(0)  # hide cursor
    stdscr.clear()
    stdscr.refresh()

    # Load data
    with open(YAML_FILE, "r") as f:
        data = yaml.safe_load(f)

    acronym_index = build_acronym_index(data)
    category_index = build_category_index(data)

    # Flatten entries for display
    entries = [entry for entries_list in category_index.values() for entry in entries_list]

    selected = 0
    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Display 10 entries at a time
        start = max(0, selected - 5)
        end = min(len(entries), start + 10)

        for idx, entry in enumerate(entries[start:end], start):
            if idx == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx - start, 0, f"> {entry['acronym']}: {entry['definition']}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx - start, 0, f"  {entry['acronym']}: {entry['definition']}")

        stdscr.addstr(h-2, 0, "UP/DOWN (k/j): Navigate  A: Add  D: Delete  Q: Quit")
        stdscr.refresh()

        key = stdscr.getch()
        if (key == curses.KEY_UP or key == ord('k')) and selected > 0:
            selected -= 1
        elif (key == curses.KEY_DOWN or key == ord('j')) and selected < len(entries) - 1:
            selected += 1
        elif key in (ord('q'), ord('Q')):
            break
        elif key in (ord('a'), ord('A')):
            # Minimal add example (real TUI input would be a form)
            new_entry = {
                "acronym": "MCP",
                "definition": "Model Context Protocol",
                "category": "Software / Networking",
                "description": "New acronym example",
                "aliases": [],
                "origin": "",
                "related_acronyms": [],
                "notes": ""
            }
            data = crud.add_entry(data, new_entry)
            crud.save_data(data)
            entries.append(new_entry)
        elif key in (ord('d'), ord('D')):
            entry_to_delete = entries[selected]
            data, success = crud.delete_entry(data, entry_to_delete["acronym"])
            if success:
                crud.save_data(data)
                entries.pop(selected)
                if selected >= len(entries):
                    selected = len(entries) - 1

if __name__ == "__main__":
    curses.wrapper(main)
