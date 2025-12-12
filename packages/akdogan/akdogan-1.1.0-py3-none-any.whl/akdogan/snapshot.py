import os
from .tree_utils import generate_tree
from .file_utils import read_file_content

IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

def generate_snapshot(root_path, output_file):
    root_path = os.path.abspath(root_path)

    with open(output_file, "w", encoding="utf-8") as out:

        # Header
        out.write("=== PROJECT TREE ===\n\n")
        out.write(generate_tree(root_path))
        out.write("\n\n\n=== FILE CONTENTS ===\n\n")

        # Walk through project
        for current_root, dirs, files in os.walk(root_path):

            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for f in files:
                if f in {".DS_Store"}:
                    continue

                full_path = os.path.join(current_root, f)
                rel_path = os.path.relpath(full_path, root_path)

                out.write(f"\n--- FILE: {rel_path} ---\n")
                content = read_file_content(full_path)
                out.write(content)
                out.write("\n")
