#!/usr/bin/env python3
"""Verify LaTeX cross-references: find undefined labels, duplicate labels, and unmatched cites."""
import re, sys, os
from pathlib import Path
from collections import defaultdict

def scan_file(path: str) -> dict:
    """Scan a .tex file and return all labels, refs, and cites."""
    text = Path(path).read_text(encoding='utf-8', errors='replace')
    labels = set(re.findall(r'\\label\{([^}]+)\}', text))
    refs   = set(re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}', text))
    cites  = set(re.findall(r'\\cite\{([^}]+)\}', text))
    bibitems = set()
    for m in re.finditer(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', text):
        bibitems.add(m.group(1))
    return {'labels': labels, 'refs': refs, 'cites': cites, 'bibitems': bibitems}

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    tex_files = list(root.glob('**/*.tex'))
    if not tex_files:
        print(f"No .tex files found under {root}")
        sys.exit(1)

    all_labels = set(); all_refs = set(); all_cites = set(); all_bibitems = set()
    for f in tex_files:
        r = scan_file(str(f))
        all_labels  |= r['labels']
        all_refs    |= r['refs']
        all_cites   |= r['cites']
        all_bibitems |= r['bibitems']

    undefined  = sorted(all_refs - all_labels)
    duplicates = sorted(find_duplicates(root))
    uncited    = sorted(all_cites - all_bibitems) if all_bibitems else []

    issues = bool(undefined) + bool(duplicates) + bool(uncited)
    if not issues:
        print("OK: all cross-references resolved.")
        sys.exit(0)

    for u in undefined:
        print(f"UNDEFINED: \\ref{{{u}}} has no matching \\label")
    for d in duplicates:
        print(f"DUPLICATE: \\label{{{d}}} defined in multiple files")
    for u in uncited:
        print(f"UNCITED: \\cite{{{u}}} has no matching \\bibitem")
    sys.exit(1)

def find_duplicates(root: Path) -> list:
    label_files = defaultdict(list)
    for f in root.glob('**/*.tex'):
        for m in re.findall(r'\\label\{([^}]+)\}', f.read_text(encoding='utf-8', errors='replace')):
            label_files[m].append(str(f))
    return [k for k, v in label_files.items() if len(v) > 1]

if __name__ == '__main__':
    main()
