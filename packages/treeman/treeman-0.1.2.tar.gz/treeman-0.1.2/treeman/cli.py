# pytree/cli.py

import argparse
import json
import os
from .core import print_children, build_tree_dict, tree_to_markdown

def main():
    parser = argparse.ArgumentParser(description="Visualize directory structure like `tree`.")
    parser.add_argument("path", nargs="?", default=".", help="Directory path (default: current directory)")
    parser.add_argument("--basenames", action="store_true", help="Show basenames instead of absolute paths")
    parser.add_argument("--format", choices=["tree", "json", "markdown"], default="tree",
                        help="Output format: tree (default), json, or markdown.")

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    basenames = bool(args.basenames)

    if not os.path.exists(root_path):
        print("❌ Error: Path does not exist.", root_path)
        return

    if args.format == "tree":
        print_children(root_path, want_basenames=basenames)

    elif args.format == "json":
        tree = build_tree_dict(root_path)
        print(json.dumps(tree, indent=2))

    elif args.format == "markdown":
        tree = build_tree_dict(root_path)
        md = tree_to_markdown(tree)
        print("\n".join(md))
