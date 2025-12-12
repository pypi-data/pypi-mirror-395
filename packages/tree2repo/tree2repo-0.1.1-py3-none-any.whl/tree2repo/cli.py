import argparse
import sys

from .core import create_from_tree


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tree2repo",
        description="Create a repo structure from a pasted tree."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Directory where the structure will be created (default: current directory)."
    )
    parser.add_argument(
        "--respect-root",
        action="store_true",
        help="Create the first top-level directory from the tree as well."
    )

    args = parser.parse_args()
    tree_text = sys.stdin.read()

    create_from_tree(
        tree_text=tree_text,
        root=args.root,
        ignore_root_label=not args.respect_root,
    )


if __name__ == "__main__":
    main()
