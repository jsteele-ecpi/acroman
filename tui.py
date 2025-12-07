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

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    menu_items = [
        ("Browse Acronyms", "browse"),
        ("Add Acronym", "add"),
        ("Edit Acronym", "edit"),
        ("Delete Acronym", "delete"),
        ("Search", "search"),
        ("Quit", "quit")
    ]

    selected = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Popup width calculations (PADDED)
        padding_x = 6
        padding_y = 4
        max_label_len = max(len(label) for label, _ in menu_items)
        win_width = max_label_len + padding_x + 4
        win_height = len(menu_items) + padding_y + 4

        # Center window position
        start_y = (h - win_height) // 2
        start_x = (w - win_width) // 2

        # Create popup window
        win = curses.newwin(win_height, win_width, start_y, start_x)

        # Draw rounded border
        win.addstr(0, 0,  "╭" + "─" * (win_width - 2) + "╮")
        win.addstr(win_height - 1, 0, "╰" + "─" * (win_width - 2) + "╯")
        for y in range(1, win_height - 1):
            win.addstr(y, 0, "│")
            win.addstr(y, win_width - 1, "│")

        # Title
        title = "ACROMAN — Main Menu"
        win.addstr(2, (win_width // 2) - (len(title) // 2), title, curses.A_BOLD)

        # Menu items
        for idx, (label, action) in enumerate(menu_items):
            y = 4 + idx
            x = 4

            if idx == selected:
                win.attron(curses.A_REVERSE)
                win.addstr(y, x, f"  {label}")
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(y, x, f"  {label}")

        win.refresh()

        # Read user key
        key = stdscr.getch()

        # Movement (vim + arrows)
        if key in (curses.KEY_UP, ord('k')):
            if selected > 0:
                selected -= 1

        elif key in (curses.KEY_DOWN, ord('j')):
            if selected < len(menu_items) - 1:
                selected += 1

        # Select (Enter, Space, Right, l)
        elif key in (curses.KEY_ENTER, 10, 13, ord('l'), ord(' '), curses.KEY_RIGHT):
            return menu_items[selected][1]

        # Quit with q / h / left
        elif key in (ord('q'), ord('Q'), ord('h'), curses.KEY_LEFT):
            return "quit"


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
