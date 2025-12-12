import curses

import bookpicker


def main():
    curses.wrapper(bookpicker.main)
