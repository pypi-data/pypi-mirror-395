import ast
import os
from typing import List, Tuple


# helper: extract code snippet by lineno
def _get_block(source_lines: List[str], node) -> str:
    start = node.lineno - 1
    end = getattr(node, "end_lineno", None)
    if end is None:
        # fallback (older Python) — collect until next blank line (best-effort)
        end = start + 1
        while end < len(source_lines) and source_lines[end].strip() != "":
            end += 1
    return "\n".join(source_lines[start:end]) + "\n"


#########


def parse_top_level_items(path: str):
    """
    Parse a python file and return lists of (name, code) for:
      - functions (top-level)
      - constants (top-level UPPERCASE assignments)
      - classes (top-level)
      - imports (raw code)
    """
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    lines = src.splitlines()
    funcs = []
    consts = []
    classes = []
    imports = []

    for node in tree.body:
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            # keep import line exactly
            imports.append(_get_block(lines, node))

        elif isinstance(node, ast.FunctionDef):
            funcs.append((node.name, _get_block(lines, node)))

        elif isinstance(node, ast.ClassDef):
            classes.append((node.name, _get_block(lines, node)))

        elif isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
                if name.isupper():
                    consts.append((name, _get_block(lines, node)))

    return funcs, consts, classes, imports


def collect_from_files(paths: List[str]):
    """Collect items across many files. Returns aggregated lists and a map by file."""
    all_imports = []
    all_funcs = []
    all_consts = []
    all_classes = []
    file_map = {}
    for p in paths:
        try:
            funcs, consts, classes, imports = parse_top_level_items(p)
        except SyntaxError:
            funcs, consts, classes = [], [], []
        file_map[p] = {
            "funcs": funcs,
            "consts": consts,
            "classes": classes,
            "imports": imports
        }
        all_imports.extend([name for name, _ in imports])
        all_funcs.extend([name for name, _ in funcs])
        all_consts.extend([name for name, _ in consts])
        all_classes.extend([name for name, _ in classes])
    return all_funcs, all_consts, all_classes, all_imports, file_map


def make_all_list(names: List[str]) -> str:
    # return a python list literal with stable ordering
    uniq = sorted(dict.fromkeys(names))
    return "[" + ", ".join(f"'{n}'" for n in uniq) + "]"


def build_top_level_modules(file_map, dry_run=False, targets=None):
    """
    Merge all found codeblocks into top-level modules (for `merge` and `small`).
    `targets` is dict with keys: funcs, consts, classes (file paths).
    """
    targets = targets or {}
    func_blocks = []
    const_blocks = []
    class_blocks = []
    import_blocks = []
    for p, buckets in file_map.items():
        func_blocks.extend(buckets["funcs"])
        const_blocks.extend(buckets["consts"])
        class_blocks.extend(buckets["classes"])
        import_blocks.extend(buckets["imports"])

    # produce content strings
    func_content = "".join(import_blocks) + "\n"
    for _, block in func_blocks:
        func_content += block + "\n\n#***********************************************\n\n"

    const_content = "".join(import_blocks) + "\n"
    for _, block in const_blocks:
        const_content += block + "\n"

    class_content = "".join(import_blocks) + "\n"
    for _, block in class_blocks:
        class_content += block + "\n\n#***********************************************\n\n"

    return (
        func_content,
        const_content,
        class_content,
        func_blocks,
        const_blocks,
        class_blocks,
    )


def build_subpkg_modules(root: str, file_map, dry_run=False, targets=None):
    """
    For `subpkg` mode: create per-subpackage myutil/constants/classes.
    We'll group files by their package path (folder relative to root).
    """
    grouped = {}
    for path, buckets in file_map.items():
        # determine immediate package folder relative to root
        rel = os.path.relpath(os.path.dirname(path), root)
        key = rel if rel != "." else ""
        grouped.setdefault(key, {"funcs": [], "consts": [], "classes": []})
        grouped[key]["funcs"].extend(buckets["funcs"])
        grouped[key]["consts"].extend(buckets["consts"])
        grouped[key]["classes"].extend(buckets["classes"])

    # produce map: package -> (func_content, const_content, class_content)
    out = {}
    for pkg, buckets in grouped.items():
        func_content = "# auto-generated for package: %s\n\n" % (pkg or "top")
        for _, block in buckets["funcs"]:
            func_content += block + "\n"
        const_content = "# auto-generated constants for %s\n\n" % (pkg or "top")
        for _, block in buckets["consts"]:
            const_content += block + "\n"
        class_content = "# auto-generated classes for %s\n\n" % (pkg or "top")
        for _, block in buckets["classes"]:
            class_content += block + "\n"
        out[pkg] = (func_content, const_content, class_content, buckets)
    return out
