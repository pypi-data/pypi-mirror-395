import curses

from . import bookpicker


def main():
    curses.wrapper(bookpicker.main)
