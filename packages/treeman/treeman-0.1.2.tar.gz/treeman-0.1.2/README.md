# treeman

A modern, Python-based `tree` command with:

✓ `.gitignore` support  
✓ JSON output  
✓ Markdown output  
✓ Emoji icons  
✓ Permission-safe traversal  
✓ Skips `.git` and `__pycache__`  

## Install

pip install treeman

## Usage

treeman [-h] [--basenames] [--format {tree,json,markdown}] [path]

Tree output:

treeman [filepath]

JSON output:

treeman [filepath] --format json > structure.json

Markdown output:

treeman [filepath] --format markdown > structure.md
