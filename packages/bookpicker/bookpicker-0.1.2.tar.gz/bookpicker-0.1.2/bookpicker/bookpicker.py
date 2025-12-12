#!/usr/bin/env python3
import curses
import os
import subprocess

START_DIR = os.path.expanduser("~/books")

def open_file(path):
    with open(os.devnull, "w") as devnull:
        subprocess.Popen(
            ["xdg-open", path],
            stdout=devnull,
            stderr=devnull,
            stdin=devnull
        )

def main(stdscr):
    curses.curs_set(0)
    current_dir = START_DIR
    selection = 0

    while True:
        stdscr.clear()
        try:
            entries = os.listdir(current_dir)
        except PermissionError:
            entries = []
        entries = sorted(entries, key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x.lower()))

        if not entries:
            stdscr.addstr(0, 0, "Папка пуста")
        else:
            for i, e in enumerate(entries):
                path = os.path.join(current_dir, e)
                prefix = "[D] " if os.path.isdir(path) else "    "
                mode = curses.A_REVERSE if i == selection else curses.A_NORMAL
                stdscr.addstr(i, 0, f"{prefix}{e}", mode)

        key = stdscr.getch()
        if key in (ord('j'), curses.KEY_DOWN):
            selection = (selection + 1) % len(entries) if entries else 0
        elif key in (ord('k'), curses.KEY_UP):
            selection = (selection - 1) % len(entries) if entries else 0
        elif key == ord('l') or key == curses.KEY_ENTER or key == 10:
            if not entries:
                continue
            chosen_path = os.path.join(current_dir, entries[selection])
            if os.path.isdir(chosen_path):
                current_dir = chosen_path
                selection = 0
            else:
                open_file(chosen_path)
                break
        elif key == ord('h') or key in (curses.KEY_BACKSPACE, 127):
            parent = os.path.dirname(current_dir)
            if parent != current_dir:
                current_dir = parent
                selection = 0
        elif key in (ord('q'), 27):
            break
