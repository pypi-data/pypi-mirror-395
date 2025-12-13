import argparse
import os
from .options import Options
from .core import run

def parse_args():
    p = argparse.ArgumentParser(prog="pyrefactor", description="Refactor small python packages")
    p.add_argument("run", nargs="?", default="run", help="command: run")
    p.add_argument("--mode", choices=["small", "merge", "subpkg", "dry-run"], default="small", help="operation mode")
    p.add_argument("--root", default=".", help="root package folder (default: current directory)")
    p.add_argument("--no-backup", action="store_true", help="do not create .bak backups")
    p.add_argument("--no-format", action="store_true", help="do not attempt to auto-format files")
    p.add_argument("--func-file", default="myutil.py", help="target functions filename")
    p.add_argument("--const-file", default="constants.py", help="target constants filename")
    p.add_argument("--class-file", default="classes.py", help="target classes filename")
    p.add_argument("--quiet", action="store_true", help="suppress verbose output")
    p.add_argument("--undo", action="store_true", help="restore backups (.bak) for top-level files")
    return p.parse_args()

def main():
    args = parse_args()
    opts = Options(
        mode=args.mode,
        root=args.root,
        backup=not args.no_backup,
        format=not args.no_format,
        target_funcs=args.func_file,
        target_consts=args.const_file,
        target_classes=args.class_file,
        verbose=not args.quiet,
        undo=args.undo,
    )
    if opts.verbose:
        print(f"Running pyrefactor mode={opts.mode} root={opts.root}")
    run(opts)

if __name__ == "__main__":
    main()