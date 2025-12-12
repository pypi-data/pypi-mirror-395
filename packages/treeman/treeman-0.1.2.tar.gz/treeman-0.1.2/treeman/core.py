# pytree/core.py

import os
from pathspec import PathSpec

def load_gitignore(base_path):
    gitignore_path = os.path.join(base_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        return None

    with open(gitignore_path, "r") as f:
        patterns = f.read().splitlines()

    return PathSpec.from_lines("gitwildmatch", patterns)


def is_ignored(path, base_path, spec):
    if spec is None:
        return False
    rel = os.path.relpath(path, base_path)
    return spec.match_file(rel)


def print_children(entity, level=0, entity_array=None, counter_array=None,
                   want_basenames=1, base_path=None, gitignore_spec=None):

    if base_path is None:
        base_path = os.path.abspath(entity)
        gitignore_spec = load_gitignore(base_path)

    # Skip ignored
    if is_ignored(entity, base_path, gitignore_spec):
        return

    # Skip internal dirs
    skip_dirs = {".git", "__pycache__"}
    if os.path.isdir(entity) and os.path.basename(entity) in skip_dirs:
        return

    # Init arrays
    if entity_array is None:
        entity_array = {}
    if counter_array is None:
        counter_array = {}

    if level not in entity_array:
        entity_array[level] = []
    entity_array[level].append(entity)

    if level not in counter_array:
        counter_array[level] = [0, 0]

    if os.path.isdir(entity):
        counter_array[level][0] += 1

        try:
            entries = os.listdir(entity)
        except PermissionError:
            print(f"⚠️  Permission denied: {entity}")
            return
        except OSError:
            print(f"⚠️  Could not access: {entity}")
            return

        for local_entity in entries:
            local_entity_path = os.path.join(entity, local_entity)
            try:
                print_children(local_entity_path, level + 1,
                               entity_array, counter_array,
                               want_basenames, base_path, gitignore_spec)
            except PermissionError:
                print(f"⚠️  Permission denied: {local_entity_path}")
                continue
            except OSError:
                print(f"⚠️  Error reading: {local_entity_path}")
                continue

    else:
        counter_array[level][1] += 1

    # Pretty-print only at root
    if level == 0:
        for key in sorted(entity_array.keys()):
            print(f"{key}:")
            for ent in entity_array[key]:
                indent = "\t" * key
                symbol = "📁" if os.path.isdir(ent) else "📄"
                name = os.path.basename(ent) if want_basenames else ent
                print(f"{indent}├── {symbol} {name}")
            print()

        print("📊 Summary:")
        for key in sorted(counter_array.keys()):
            folders, files = counter_array[key]
            print(f"Level {key}: Folders={folders}, Files={files}")


def build_tree_dict(path):
    node = {
        "path": path,
        "name": os.path.basename(path),
        "type": "folder" if os.path.isdir(path) else "file"
    }

    if os.path.isdir(path):
        try:
            entries = os.listdir(path)
        except Exception:
            entries = []

        node["children"] = [
            build_tree_dict(os.path.join(path, entry))
            for entry in entries
        ]

    return node


def tree_to_markdown(node, level=0):
    lines = []
    indent = "  " * level
    prefix = "- " if level else "# "

    lines.append(f"{indent}{prefix}{node['name']}")

    for child in node.get("children", []):
        lines.extend(tree_to_markdown(child, level + 1))

    return lines
