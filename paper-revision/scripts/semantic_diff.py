#!/usr/bin/env python3
"""Compare two .tex files section by section; report only semantic changes."""
import re, sys
from pathlib import Path

def strip_latex_noise(s: str) -> str:
    """Remove comments, normalize whitespace, strip empty lines."""
    s = re.sub(r'(?<!\\)%.*$', '', s, flags=re.MULTILINE)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n', '\n', s)
    return s.strip()

def split_sections(text: str) -> dict:
    """Split LaTeX text into sections by \\section / \\subsection headers."""
    sections = {}
    pattern = r'\\((?:sub)?section)\*?\{(.+?)\}'
    parts = re.split(pattern, text)
    # parts[0] = preamble, then alternating (section_name, section_body)
    if len(parts) < 3:
        return {'_preamble': text}
    sections['_preamble'] = parts[0].strip()
    for i in range(1, len(parts), 2):
        name = parts[i].strip()
        body = parts[i+1].strip() if i+1 < len(parts) else ''
        sections[name] = body
    return sections

def main():
    if len(sys.argv) != 3:
        print("Usage: python semantic_diff.py old.tex new.tex")
        sys.exit(1)

    old_text = strip_latex_noise(Path(sys.argv[1]).read_text(encoding='utf-8', errors='replace'))
    new_text = strip_latex_noise(Path(sys.argv[2]).read_text(encoding='utf-8', errors='replace'))

    old_secs = split_sections(old_text)
    new_secs = split_sections(new_text)

    all_sections = sorted(set(list(old_secs.keys()) + list(new_secs.keys())))
    changes = 0

    for sec in all_sections:
        old_body = old_secs.get(sec, '')
        new_body = new_secs.get(sec, '')
        if old_body == new_body:
            continue
        if not old_body:
            print(f"[+] {sec}: NEW section ({len(new_body.split())} words)")
        elif not new_body:
            print(f"[-] {sec}: REMOVED ({len(old_body.split())} words)")
        else:
            print(f"[~] {sec}: changed ({len(old_body.split())} → {len(new_body.split())} words)")
        changes += 1

    if not changes:
        print("No semantic changes found between sections.")
    sys.exit(0)

if __name__ == '__main__':
    main()
