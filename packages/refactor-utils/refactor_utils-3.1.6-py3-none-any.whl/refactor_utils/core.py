import os
from typing import Dict, List, Tuple
from .options import Options
from . import movers, utils


# Helper to write top-level __init__.py
def write_top_init(
    all_funcs: List[str],
    all_consts: List[str],
    all_classes: List[str],
    opts: Options,
    dry_run: bool,
):
    imports = []
    items = []
    if all_funcs:
        imports.append(
            f"from .{os.path.splitext(opts.target_funcs)[0]} import " +
            ", ".join(sorted(set(all_funcs))))
        items.extend(all_funcs)
    if all_consts:
        imports.append(
            f"from .{os.path.splitext(opts.target_consts)[0]} import " +
            ", ".join(sorted(set(all_consts))))
        items.extend(all_consts)
    if all_classes:
        imports.append(
            f"from .{os.path.splitext(opts.target_classes)[0]} import " +
            ", ".join(sorted(set(all_classes))))
        items.extend(all_classes)
    content = "\n".join(imports) + "\n\n__all__ = " + movers.make_all_list(
        items) + "\n"
    if opts.verbose:
        print("Writing top-level __init__.py with these imports:")
        for li in imports:
            print("  ", li)
        print("And __all__ with", len(items), "items")
    utils.overwrite_file(opts.root + "/" + "__init__.py", content, dry_run)


def run_small(opts: Options):
    # top-level only (non-recursive)
    py_files = utils.list_py_files(opts.root, recursive=False)
    # only consider files in root, skip __init__.py (we'll rewrite)
    paths = [
        p for p in py_files if os.path.abspath(p) != os.path.abspath(
            os.path.join(opts.root, "__init__.py"))
    ]
    all_funcs, all_consts, all_classes, file_map = movers.collect_from_files(
        paths)
    if opts.verbose:
        print("Found (top-level) functions:", all_funcs)
        print("Found (top-level) constants:", all_consts)
        print("Found (top-level) classes:", all_classes)

    func_content, const_content, class_content, _, _, _ = (
        movers.build_top_level_modules(file_map))
    targets = {
        "funcs": os.path.join(opts.root, opts.target_funcs),
        "consts": os.path.join(opts.root, opts.target_consts),
        "classes": os.path.join(opts.root, opts.target_classes),
    }

    if opts.backup:
        utils.ensure_backups(
            list(targets.values()) + [os.path.join(opts.root, "__init__.py")])

    utils.write_file(targets["funcs"],
                     func_content,
                     dry_run=(opts.mode == "dry-run"))
    utils.write_file(targets["consts"],
                     const_content,
                     dry_run=(opts.mode == "dry-run"))
    utils.write_file(targets["classes"],
                     class_content,
                     dry_run=(opts.mode == "dry-run"))

    write_top_init(all_funcs,
                   all_consts,
                   all_classes,
                   opts,
                   dry_run=(opts.mode == "dry-run"))

    if opts.format and not (opts.mode == "dry-run"):
        for t in targets.values():
            utils.try_format(t)
        utils.try_format(os.path.join(opts.root, "__init__.py"))


def run_merge(opts: Options):
    # recursive scan; move everything into top-level modules
    py_files = utils.list_py_files(opts.root, recursive=True)
    # skip the generated top-level targets and their backups
    skip = {
        os.path.join(opts.root, "__init__.py"),
        os.path.join(opts.root, opts.target_funcs),
        os.path.join(opts.root, opts.target_consts),
        os.path.join(opts.root, opts.target_classes),
    }
    paths = [
        p for p in py_files
        if os.path.abspath(p) not in {os.path.abspath(s) for s in skip}
    ]
    all_funcs, all_consts, all_classes, all_imports, file_map = movers.collect_from_files(
        paths)

    if opts.verbose:
        print("Found imports:", all_imports)
        print("Found functions:", all_funcs)
        print("Found constants:", all_consts)
        print("Found classes:", all_classes)

    func_content, const_content, class_content, _, _, _ = (
        movers.build_top_level_modules(file_map))
    targets = {
        "funcs": os.path.join(opts.root, opts.target_funcs),
        "consts": os.path.join(opts.root, opts.target_consts),
        "classes": os.path.join(opts.root, opts.target_classes),
    }

    if opts.backup:
        utils.ensure_backups(
            list(targets.values()) + [os.path.join(opts.root, "__init__.py")])

    # overwrite mode for merge (we want a single merged file)
    utils.overwrite_file(targets["funcs"],
                         func_content,
                         dry_run=(opts.mode == "dry-run"))
    utils.overwrite_file(targets["consts"],
                         const_content,
                         dry_run=(opts.mode == "dry-run"))
    utils.overwrite_file(targets["classes"],
                         class_content,
                         dry_run=(opts.mode == "dry-run"))

    write_top_init(all_funcs,
                   all_consts,
                   all_classes,
                   opts,
                   dry_run=(opts.mode == "dry-run"))

    if opts.format and not (opts.mode == "dry-run"):
        for t in targets.values():
            utils.try_format(t)
        utils.try_format(os.path.join(opts.root, "__init__.py"))

    # remove old files
    for p in paths:
        if p.endswith("__init__.py"):
            continue
        if p in skips:
            continue
        utils.safe_remove(p)


def run_subpkg(opts: Options):
    # recursively create per-subpackage modules
    py_files = utils.list_py_files(opts.root, recursive=True)
    skip = {os.path.join(opts.root, "__init__.py")}
    paths = [
        p for p in py_files
        if os.path.abspath(p) not in {os.path.abspath(s) for s in skip}
    ]
    all_funcs, all_consts, all_classes, file_map = movers.collect_from_files(
        paths)

    pkg_map = movers.build_subpkg_modules(opts.root, file_map)
    # For each package (key=relpath), write files into that package folder
    written_items = {"funcs": [], "consts": [], "classes": []}
    for pkg, (func_content, const_content, class_content,
              buckets) in pkg_map.items():
        # pkg == "" means top-level root
        folder = os.path.join(opts.root, pkg) if pkg else opts.root
        func_target = os.path.join(folder, opts.target_funcs)
        const_target = os.path.join(folder, opts.target_consts)
        class_target = os.path.join(folder, opts.target_classes)
        if opts.backup:
            utils.ensure_backups([
                func_target,
                const_target,
                class_target,
                os.path.join(folder, "__init__.py"),
            ])
        utils.write_file(func_target,
                         func_content,
                         dry_run=(opts.mode == "dry-run"))
        utils.write_file(const_target,
                         const_content,
                         dry_run=(opts.mode == "dry-run"))
        utils.write_file(class_target,
                         class_content,
                         dry_run=(opts.mode == "dry-run"))
        # try to update that package's __init__.py to re-export
        items = []
        if buckets["funcs"]:
            items.extend([n for n, _ in buckets["funcs"]])
        if buckets["consts"]:
            items.extend([n for n, _ in buckets["consts"]])
        if buckets["classes"]:
            items.extend([n for n, _ in buckets["classes"]])
        if items:
            imports = []
            if buckets["funcs"]:
                imports.append(
                    f"from .{os.path.splitext(opts.target_funcs)[0]} import " +
                    ", ".join([n for n, _ in buckets["funcs"]]))
            if buckets["consts"]:
                imports.append(
                    f"from .{os.path.splitext(opts.target_consts)[0]} import " +
                    ", ".join([n for n, _ in buckets["consts"]]))
            if buckets["classes"]:
                imports.append(
                    f"from .{os.path.splitext(opts.target_classes)[0]} import "
                    + ", ".join([n for n, _ in buckets["classes"]]))
            content = ("\n".join(imports) + "\n\n__all__ = " +
                       movers.make_all_list(items) + "\n")
            utils.overwrite_file(
                os.path.join(folder, "__init__.py"),
                content,
                dry_run=(opts.mode == "dry-run"),
            )
        written_items["funcs"].extend([n for n, _ in buckets["funcs"]])
        written_items["consts"].extend([n for n, _ in buckets["consts"]])
        written_items["classes"].extend([n for n, _ in buckets["classes"]])

    # do NOT modify top-level __init__.py here (unless top-level items were present)
    # If top-level items found (pkg == ""), ensure exported in top-level __init__
    top_buckets = pkg_map.get("", None)
    if top_buckets:
        _, _, _, buckets = top_buckets
        if buckets and (buckets["funcs"] or buckets["consts"] or
                        buckets["classes"]):
            write_top_init(
                [n for n, _ in buckets["funcs"]],
                [n for n, _ in buckets["consts"]],
                [n for n, _ in buckets["classes"]],
                opts,
                dry_run=(opts.mode == "dry-run"),
            )

    if opts.format and not (opts.mode == "dry-run"):
        # format all generated files by scanning pkg_map locations
        for pkg in pkg_map:
            folder = os.path.join(opts.root, pkg) if pkg else opts.root
            utils.try_format(os.path.join(folder, opts.target_funcs))
            utils.try_format(os.path.join(folder, opts.target_consts))
            utils.try_format(os.path.join(folder, opts.target_classes))


def run(opts: Options):
    # central dispatcher
    if opts.undo:
        # restore backups for common files
        targets = [
            os.path.join(opts.root, opts.target_funcs),
            os.path.join(opts.root, opts.target_consts),
            os.path.join(opts.root, opts.target_classes),
            os.path.join(opts.root, "__init__.py"),
        ]
        restored = utils.restore_backups(targets)
        if opts.verbose:
            print("Restored:", restored)
        return

    if opts.mode == "small":
        run_small(opts)
    elif opts.mode == "merge":
        run_merge(opts)
    elif opts.mode == "subpkg":
        run_subpkg(opts)
    elif opts.mode == "dry-run":
        # shrink to dry-run variants of merge (simulate)
        opts = opts.__class__(**{**opts.__dict__, "mode": "dry-run"})
        run_merge(opts)
    else:
        raise ValueError("Unknown mode: " + str(opts.mode))
