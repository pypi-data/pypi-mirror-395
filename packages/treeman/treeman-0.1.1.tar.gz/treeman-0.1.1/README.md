# pytree

A modern, Python-based `tree` command with:

✓ `.gitignore` support  
✓ JSON output  
✓ Markdown output  
✓ Emoji icons  
✓ Permission-safe traversal  
✓ Skips `.git` and `__pycache__`  

## Install

pip install pytree

## Usage

pytree.py [-h] [--basenames]
               [--format {tree,json,markdown}][path]

Tree output:

pytree [filepath]

JSON output:

pytree [filepath] --format json > structure.json

Markdown output:

pytree [filepath] --format markdown > structure.md
