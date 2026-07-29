#!/usr/bin/env python3
"""Validate .docx font consistency: report all unique w:sz and w:rFonts values."""
import sys, zipfile
from pathlib import Path
from collections import Counter
from lxml import etree

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_docx_fonts.py file.docx")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    fonts = Counter()
    sizes = Counter()
    paragraph_count = 0

    with zipfile.ZipFile(path) as z:
        xml_data = z.read('word/document.xml')

    doc = etree.fromstring(xml_data)
    for elem in doc.iter():
        if elem.tag.endswith('}sz') or elem.tag.endswith('}szCs'):
            sizes[elem.get(etree.QName(NS['w'], 'val'))] += 1
        if elem.tag.endswith('}rFonts'):
            fonts[elem.get(etree.QName(NS['w'], 'ascii'), '')] += 1
        if elem.tag.endswith('}p'):
            paragraph_count += 1

    print(f"Total paragraphs: {paragraph_count}")
    print(f"\nFont sizes (w:sz, half-points):")
    for sz, count in sizes.most_common():
        pt = int(sz) / 2
        print(f"  w:sz={sz} ({pt:.0f}pt) — {count} occurrences")

    print(f"\nFont faces (w:rFonts ascii):")
    for f, count in fonts.most_common():
        name = f if f else "(inherited)"
        print(f"  {name} — {count} occurrences")

    # Flag issues
    if len(sizes) > 1:
        print(f"\nWARNING: {len(sizes)} different font sizes found. Expected exactly 1.")
    else:
        print(f"\nOK: single font size throughout.")

    para_sizes = set()
    for p in doc.iter():
        if p.tag.endswith('}p'):
            for sz in p.iter():
                if sz.tag.endswith('}sz'):
                    para_sizes.add(sz.get(etree.QName(NS['w'], 'val')))
    if not para_sizes:
        print("WARNING: no direct font size found — likely using style inheritance.")

if __name__ == '__main__':
    main()
