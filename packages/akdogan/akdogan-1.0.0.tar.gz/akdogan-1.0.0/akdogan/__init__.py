import os
from datetime import datetime
from .snapshot import generate_snapshot

def snapshot(path=".", output=None, verbose=True):
    """
    Programmatically generate a snapshot via Python import.
    """
    # Auto-generate output filename if not provided
    if output is None:
        folder_name = os.path.basename(os.path.abspath(path))
        timestamp = datetime.now().strftime("%d.%m.%y-%H:%M")
        output = f"snapshot_{folder_name}_{timestamp}.txt"

    if verbose:
        print("[AKDOGAN] Generating snapshot...")

    generate_snapshot(path, output)

    if verbose:
        print(f"[AKDOGAN] Snapshot created: {output}")

    return output
