from dataclasses import dataclass


@dataclass(frozen=True)
class Options:
    mode: str  # 'small' | 'merge' | 'subpkg' | 'dry-run'
    root: str = "."
    backup: bool = True
    format: bool = True
    target_funcs: str = "myutil.py"
    target_consts: str = "constants.py"
    target_classes: str = "classes.py"
    verbose: bool = True
    undo: bool = False
