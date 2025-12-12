import argparse
import os
from datetime import datetime
from .snapshot import generate_snapshot

def build_snapshot_name(path: str) -> str:
    # Folder name
    folder = os.path.basename(os.path.abspath(path))

    # Date & time
    now = datetime.now()
    timestamp = now.strftime("%d.%m.%y-%H:%M")

    # Final file name
    return f"{folder}_{timestamp}.txt"

def main():
    parser = argparse.ArgumentParser(description="Akdogan Snapshot Tool")
    parser.add_argument("path", nargs="?", default=".", help="Project root directory")
    parser.add_argument("-o", "--output", help="Snapshot output file (optional)")
    args = parser.parse_args()

    # Build name automatically if user didn't specify one
    output_name = args.output if args.output else build_snapshot_name(args.path)

    print("[AKDOGAN] Generating snapshot...")
    generate_snapshot(args.path, output_name)
    print(f"[AKDOGAN] Snapshot created: {output_name}")
