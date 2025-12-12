import os

IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}

def generate_tree(root_path):
    tree_lines = []

    for current_root, dirs, files in os.walk(root_path):
        # Remove ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = current_root.replace(root_path, "").count(os.sep)
        indent = " " * 4 * level
        folder_name = os.path.basename(current_root)
        tree_lines.append(f"{indent}{folder_name}/")

        subindent = " " * 4 * (level + 1)
        for f in files:
            if f not in {".DS_Store"}:
                tree_lines.append(f"{subindent}{f}")

    return "\n".join(tree_lines)
