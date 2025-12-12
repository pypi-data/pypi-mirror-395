"""
PyEventBT
Documentation: https://pyeventbt.com
GitHub: https://github.com/marticastany/pyeventbt

Author: Marti Castany
Copyright (c) 2025 Marti Castany
Licensed under the Apache License, Version 2.0
"""

"""
PyEventBT - Main Application Module

This is a placeholder module for the PyEventBT package.
The full implementation is under development.
"""


def hello():
    return "Welcome to PyEventBT - Event-Driven Backtesting Framework (Under Development)"


def get_version():
    """
    Get the current version of PyEventBT.
    
    Returns:
        str: The version number
    """
    from . import __version__
    return __version__


if __name__ == "__main__":
    print(hello())
    print(f"Version: {get_version()}")

