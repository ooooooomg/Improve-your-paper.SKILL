#!/usr/bin/env python3
"""Verify checkpoint files are real .pt files (>10MB), not stubs (<1KB)."""
import sys, os
from pathlib import Path

MIN_SIZE = 10 * 1024 * 1024  # 10MB

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('checkpoints')
    if not root.exists():
        print(f"Directory not found: {root}")
        sys.exit(1)

    pt_files = list(root.rglob('*.pt'))
    if not pt_files:
        print(f"No .pt files found under {root}")
        sys.exit(0)

    ok = 0; small = []; missing = []
    for f in pt_files:
        size = f.stat().st_size
        if size == 0:
            missing.append(str(f))
        elif size < 100:
            small.append((str(f), size))
        elif size < MIN_SIZE:
            print(f"WARN: {f} ({size/1024**2:.1f} MB) — unusually small")
        else:
            ok += 1

    print(f"OK: {ok} real checkpoints (>{MIN_SIZE/1024**2:.0f} MB)")
    if small:
        print(f"\nSTUB ({len(small)} files, likely fabricated):")
        for f, size in small:
            print(f"  {f} ({size} bytes)")
    if missing:
        print(f"\nEMPTY ({len(missing)} files, 0 bytes):")
        for f in missing:
            print(f"  {f}")

    if small or missing:
        sys.exit(2)

if __name__ == '__main__':
    main()
