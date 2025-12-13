#!/usr/bin/env python3

from nicegui import ui, native


###########################################################################################
# The main function is called by script `assi-scope`.


def main():
    ui.run(reload=False, port=native.find_open_port())


###########################################################################################
# Run in debug mode using
# > python3 scope.py

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Sound input oscilloscope")
