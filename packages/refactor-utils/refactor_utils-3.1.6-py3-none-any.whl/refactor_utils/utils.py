import os
import shutil
import subprocess
from typing import List, Tuple

BACKUP_SUFFIX = ".bak"


def safe_remove(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exceptions:
        pass
    return False


def list_py_files(root: str, recursive: bool = True):
    py_files = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            # skip backup files and package installer artifacts
            if fname.endswith(BACKUP_SUFFIX + ".py"):
                continue
            full = os.path.join(dirpath, fname)
            # skip typical virtual env folders if present
            if "/.venv/" in full or "/venv/" in full:
                continue
            py_files.append(full)
        if not recursive:
            break
    return py_files


def ensure_backups(paths: List[str]):
    for p in paths:
        if os.path.exists(p):
            shutil.copy2(p, p + BACKUP_SUFFIX)


def restore_backups(paths: List[str]):
    restored = []
    for p in paths:
        bak = p + BACKUP_SUFFIX
        if os.path.exists(bak):
            shutil.copy2(bak, p)
            restored.append(p)
    return restored


def try_format(path: str):
    if not os.path.exists(path):
        return False
    # try ruff first
    try:
        subprocess.run(["ruff", "format", path], check=False)
    except Exception:
        pass
    # fall back to yapf
    try:
        subprocess.run(["yapf", "-i", path], check=False)
    except Exception:
        pass
    return True


def write_file(path: str, content: str, dry_run: bool):
    if dry_run:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)


def overwrite_file(path: str, content: str, dry_run: bool):
    if dry_run:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
