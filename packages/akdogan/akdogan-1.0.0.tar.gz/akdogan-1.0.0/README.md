# akdogan — Universal LLM-Optimized Project Snapshot Tool

[![PyPI version](https://img.shields.io/pypi/v/akdogan.svg)](https://pypi.org/project/akdogan/)
[![Python versions](https://img.shields.io/pypi/pyversions/akdogan.svg)](https://pypi.org/project/akdogan/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**akdogan** is a lightweight, cross-platform tool designed to bridge the gap between complex software projects and Large Language Models (LLMs).

It instantly converts your entire project—directory structure, source code, and data previews—into a single, structured `.txt` file optimized for the context windows of ChatGPT, Claude, Gemini, and Llama.

---

## 🧠 Why Use akdogan?

Developers often struggle to share code context with AI because:
- **ZIP files** are often rejected or hard to parse.
- **Copy-pasting** dozens of files manually is tedious.
- **Binary files** (images, pyc) create noise and waste tokens.
- **Large CSV/Excel** files consume context limits without providing structure.

**akdogan solves this** by intelligently curating your project into a single, token-efficient text file.

---

## ✨ Key Features

- **📂 Visual Directory Tree:** Generates a clean map of your project structure.
- **📄 Smart Content Extraction:** Reads `.py`, `.js`, `.html`, `.rs`, `.go` and more.
- **📊 Data Previews:** Automatically extracts only the **first 5 rows** of `.csv` and `.xlsx` files (skips bulk data).
- **🚫 Noise Filtering:** Ignores system files like `.git`, `__pycache__`, `node_modules`, `venv`, and binary executables.
- **🧪 Dual Mode:** Run it from the terminal (CLI) or import it in your Python scripts.
- **🖥️ Cross-Platform:** 100% compatible with Windows, macOS, and Linux.

---

## 🚀 Installation

Requires Python **3.8+**.

```bash
pip install akdogan
```

## 📦 CLI Usage

Navigate to your project folder and run:

```bash
# Snapshot the current directory
akdogan .
```

Options

Target a specific directory:

```bash
akdogan /Users/berke/dev/my-cool-project
```

Save to a specific output file:

```bash
akdogan . -o context_for_gpt.txt
```

## 🐍 Python Library Usage

You can also use akdogan programmatically within your automation scripts:

```python
import akdogan

# Generate snapshot for the current directory
akdogan.snapshot('.')

# Or target a specific path
akdogan.snapshot('/path/to/target')
```

This will generate a file named `snapshot_<folder>_<timestamp>.txt` automatically.

## 📁 Output Format Example

The generated text file is structured specifically for LLM comprehension:

```
=== PROJECT TREE ===

my_project/
    ├── app.py
    ├── utils/
    │   └── helper.py
    └── data/
        └── dataset.csv

=== FILE CONTENTS ===

--- FILE: app.py ---
import os
def main():
    print("Hello World")

--- FILE: utils/helper.py ---
def help_me():
    return True

--- FILE: data/dataset.csv ---
id,name,role
1,Alice,Admin
2,Bob,User
<<FIRST 5 ROWS ONLY>>
```

---

## 🛠 Development

To contribute or modify the tool locally:

Clone the repository:

```bash
git clone https://github.com/yourusername/akdogan.git
cd akdogan
```

Run locally:

```bash
python -m akdogan .
```

Run tests:

```bash
pytest
```

Build package:

```bash
python -m build
```

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright © 2025 Berke Akdoğan
