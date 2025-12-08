#!/usr/bin/env python3
"""
tui.py

Prototype ncurses TUI for acronym lookup and CRUD operations.
"""

import curses
import yaml
from libidx import build_acronym_index, build_category_index
import crud 

YAML_FILE = "acronyms.yaml"

def input_popup(stdscr, prompt):
    """
    Display a centered popup asking for a single text input.
    Returns the entered text, or None if cancelled.
    Unicode-rounded border version with safe sizing for Windows.
    """

    curses.curs_set(1)  # show cursor for input
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # --- SAFE POPUP DIMENSIONS ---
    padding_x = 10
    padding_y = 6

    text_width = len(prompt) + padding_x
    win_width = min(text_width, w - 4)
    win_width = max(win_width, 30)

    win_height = padding_y
    win_height = min(win_height, h - 4)
    win_height = max(win_height, 8)

    # Center window
    start_y = (h - win_height) // 2
    start_x = (w - win_width) // 2

    # Create popup window
    win = curses.newwin(win_height, win_width, start_y, start_x)

    # --- Unicode Rounded Border (Safe Drawing) ---
    top_border    = "╭" + "─" * (win_width - 2) + "╮"
    bottom_border = "╰" + "─" * (win_width - 2) + "╯"

    win.addstr(0, 0, top_border[:win_width])
    win.addstr(win_height - 1, 0, bottom_border[:win_width])

    for y in range(1, win_height - 1):
        win.addstr(y, 0, "│")
        win.addstr(y, win_width - 1, "│")
    # ------------------------------------------------

    # Prompt label
    win.addstr(2, 2, prompt[:win_width - 4])

    # Input box (inside popup)
    input_width = win_width - 4
    input_win = curses.newwin(1, input_width, start_y + 4, start_x + 2)
    textpad = curses.textpad.Textbox(input_win)

    win.refresh()

    try:
        user_input = textpad.edit().strip()
    except:
        user_input = ""

    curses.curs_set(0)

    if not user_input:
        return None

    return user_input

def main_menu(stdscr):
    """
    Neovim-style centered popup main menu with rounded Unicode borders and vim keybindings.
    SAFE WINDOW VERSION – guaranteed not to cause addwstr() ERR on Windows.
    """
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

        # ===== SAFE SIZING SECTION =====
        MAX_WIDTH = w - 6     # leave 3 cols margin on each side
        MAX_HEIGHT = h - 6    # leave 3 rows margin on top/bottom

        label_width = max(len(label) for label, _ in menu_items)
        padding_x = 10
        padding_y = 8

        desired_width = label_width + padding_x
        desired_height = len(menu_items) + padding_y

        win_width = min(desired_width, MAX_WIDTH)
        win_height = min(desired_height, MAX_HEIGHT)

        win_width = max(win_width, 30)
        win_height = max(win_height, 12)

        start_y = max((h - win_height) // 2, 2)
        start_x = max((w - win_width) // 2, 2)
        # =================================

        win = curses.newwin(win_height, win_width, start_y, start_x)

        # Borders
        top_border = "╭" + "─" * (win_width - 2) + "╮"
        bot_border = "╰" + "─" * (win_width - 2) + "╯"

        win.addstr(0, 0, top_border[:win_width])
        win.addstr(win_height - 1, 0, bot_border[:win_width])

        for y in range(1, win_height - 1):
            win.addstr(y, 0, "│")
            win.addstr(y, win_width - 1, "│")

        # Title
        title = "ACROMAN — Main Menu"
        title_x = max((win_width // 2) - (len(title) // 2), 1)
        win.addstr(2, title_x, title[:win_width - 2], curses.A_BOLD)

        # Menu items
        for idx, (label, _) in enumerate(menu_items):
            y = 4 + idx
            x = 4
            truncated = label[: win_width - 6]

            if idx == selected:
                win.attron(curses.A_REVERSE)
                win.addstr(y, x, truncated)
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(y, x, truncated)

        win.refresh()

        # Input handling
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            selected = max(0, selected - 1)

        elif key in (curses.KEY_DOWN, ord('j')):
            selected = min(len(menu_items) - 1, selected + 1)

        elif key in (curses.KEY_ENTER, 10, 13, ord('l'), ord(' '), curses.KEY_RIGHT):
            return menu_items[selected][1]

        elif key in (ord('q'), ord('Q'), ord('h'), curses.KEY_LEFT):
            return "quit"


def main(stdscr):
    """
    Core TUI loop.
    Displays the main menu, navigates to selected screens,
    and returns when user chooses Quit.
    """
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    while True:
        # Show main menu and get user's choice
        choice = main_menu(stdscr)

        # -------------------------
        # Main Menu → Browse
        # -------------------------
        if choice == "browse":
            browse_screen(stdscr)

        # -------------------------
        # Main Menu → Add (Test Popup Here)
        # -------------------------
        elif choice == "add":
            temp = input_popup(stdscr, "Enter acronym:")

            # After popup closes, show result or cancellation
            stdscr.clear()
            if temp is None:
                stdscr.addstr(2, 2, "Add cancelled.")
            else:
                stdscr.addstr(2, 2, f"You entered: {temp}")
            stdscr.refresh()
            stdscr.getch()

        # -------------------------
        # Main Menu → Edit
        # (placeholder for now)
        # -------------------------
        elif choice == "edit":
            stdscr.clear()
            stdscr.addstr(2, 2, "Edit Acronym (not implemented yet)")
            stdscr.refresh()
            stdscr.getch()

        # -------------------------
        # Main Menu → Delete
        # -------------------------
        elif choice == "delete":
            stdscr.clear()
            stdscr.addstr(2, 2, "Delete Acronym (not implemented yet)")
            stdscr.refresh()
            stdscr.getch()

        # -------------------------
        # Main Menu → Search
        # -------------------------
        elif choice == "search":
            stdscr.clear()
            stdscr.addstr(2, 2, "Search (not implemented yet)")
            stdscr.refresh()
            stdscr.getch()

        # -------------------------
        # Main Menu → Quit
        # -------------------------
        elif choice == "quit":
            break



def run():
    curses.wrapper(main)

if __name__ == "__main__":
    curses.wrapper(main)
