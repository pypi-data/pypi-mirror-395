import argparse
import os
from datetime import datetime
from .snapshot import generate_snapshot
import re

def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters for Windows filenames
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def build_snapshot_name(path: str) -> str:
    """
    Build snapshot filename with folder name + timestamp + .txt
    Safe for Windows and Mac.
    """
    folder = os.path.basename(os.path.abspath(path))
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")  # : yerine -
    filename = f"{folder}_{timestamp}.txt"
    return sanitize_filename(filename)

def main():
    parser = argparse.ArgumentParser(description="Akdogan Snapshot Tool")
    parser.add_argument("path", nargs="?", default=".", help="Project root directory")
    parser.add_argument("-o", "--output", help="Snapshot output file (optional)")
    args = parser.parse_args()

    # Build name automatically if user didn't specify one
    output_name = args.output if args.output else build_snapshot_name(args.path)

    # Ensure .txt extension
    if not output_name.lower().endswith(".txt"):
        output_name += ".txt"

    print("[AKDOGAN] Generating snapshot...")
    generate_snapshot(args.path, output_name)
    print(f"[AKDOGAN] Snapshot created: {output_name}")
