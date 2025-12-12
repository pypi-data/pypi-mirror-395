import os
from datetime import datetime
from .snapshot import generate_snapshot
import re

def sanitize_filename(filename: str) -> str:
    """
    Remove invalid characters for Windows filenames
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def snapshot(path=".", output=None, verbose=True):
    """
    Programmatically generate a snapshot via Python import.
    Guarantees that the output file ends with .txt and works on Windows & Mac.
    """
    # Auto-generate output filename if not provided
    if output is None:
        folder_name = os.path.basename(os.path.abspath(path))
        timestamp = datetime.now().strftime("%d-%m-%y_%H-%M")  # : ve . yerine - ve _
        output = f"snapshot_{folder_name}_{timestamp}.txt"
        output = sanitize_filename(output)

    # Ensure .txt extension
    if not output.lower().endswith(".txt"):
        output += ".txt"

    if verbose:
        print("[AKDOGAN] Generating snapshot...")

    # UTF-8 BOM ensures Windows Notepad displays content properly
    generate_snapshot(path, output)

    if verbose:
        print(f"[AKDOGAN] Snapshot created: {output}")

    return output
