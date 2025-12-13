"""
refactor_utils package

Provides a CLI `pyrefactor` to reorganize small packages:
- move top-level functions -> myutil.py
- move UPPERCASE constants -> constants.py
- move top-level classes -> classes.py

Modes:
- small: top-level only
- merge: recursively merge everything into top-level modules
- subpkg: keep subpackages separate (each gets own myutil/constants/classes)
- dry-run: show proposed changes without writing
"""

__version__ = "0.1.0"
