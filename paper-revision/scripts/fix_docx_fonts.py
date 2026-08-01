#!/usr/bin/env python3
"""Fix docx font consistency: ensure all runs use a single w:sz and w:rFonts value.

Reads an existing .docx, reports font inconsistency, and writes a FIXED
version with all runs normalized to the most common font size and face.
Backup the original before running.
"""
import sys, zipfile
from pathlib import Path
from collections import Counter
from lxml import etree

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def extract_sizes(doc) -> list:
    """Return all w:sz and w:szCs values found."""
    return [int(elem.get(f'{{{NS["w"]}}}val', '0'))
            for elem in doc.iter()
            if '}sz' in elem.tag or '}szCs' in elem.tag]

def normalize_fonts(doc, target_sz: str, target_font: str) -> int:
    """Set all w:rPr/w:sz, w:rPr/w:szCs, and w:rPr/w:rFonts to target values."""
    changed = 0
    for elem in doc.iter():
        if elem.tag.endswith('}sz') or elem.tag.endswith('}szCs'):
            old = elem.get(f'{{{NS["w"]}}}val', '')
            if old != target_sz:
                elem.set(f'{{{NS["w"]}}}val', target_sz)
                changed += 1
        if elem.tag.endswith('}rFonts'):
            for attr in ['ascii', 'hAnsi', 'eastAsia', 'cs']:
                if elem.get(f'{{{NS["w"]}}}{attr}'):
                    old_face = elem.get(f'{{{NS["w"]}}}{attr}')
                    if old_face != target_font:
                        elem.set(f'{{{NS["w"]}}}{attr}', target_font)
                        changed += 1
    return changed

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_docx_fonts.py file.docx [output.docx]")
        print("  If output is omitted, writes to file_FIXED.docx")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_name(f"{input_path.stem}_FIXED.docx")

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    # Extract and parse document.xml
    with zipfile.ZipFile(input_path) as zin:
        xml_data = zin.read('word/document.xml')

    doc = etree.fromstring(xml_data)
    sizes = Counter(extract_sizes(doc))
    if sizes:
        dominant_sz = str(sizes.most_common(1)[0][0])
        dominant_pt = int(dominant_sz) / 2
    else:
        dominant_sz = '22'
        dominant_pt = 11
        print("No explicit font sizes found (style inheritance) — leaving unchanged; "
              f"using w:sz={dominant_sz} ({dominant_pt:.0f}pt) only as the report baseline.")

    print(f"Input font sizes (half-points): {dict(sizes)}")
    print(f"Dominant: w:sz={dominant_sz} ({dominant_pt:.0f}pt)")
    if len(sizes) > 1:
        print(f"FIX: normalizing all runs to w:sz={dominant_sz} ({dominant_pt:.0f}pt)")

    # use 'Calibri' as safe default if we can't determine from XML
    changed = normalize_fonts(doc, dominant_sz, 'Calibri')
    if changed:
        print(f"Changed {changed} font attributes")

    # Rebuild the .docx: copy all original entries, replacing document.xml once.
    # (Appending a duplicate 'word/document.xml' with ZipFile 'a' produces an
    # invalid archive that many unzip tools reject.)
    with zipfile.ZipFile(input_path) as zin, \
         zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                data = etree.tostring(doc, xml_declaration=True,
                                      encoding='UTF-8', standalone=True)
            zout.writestr(item, data)

    # verify
    final_sizes = extract_sizes(etree.fromstring(etree.tostring(doc)))
    if not final_sizes:
        print(f"OK: {output_path} — no explicit font sizes (style inheritance), unchanged")
    elif len(set(final_sizes)) == 1:
        print(f"OK: {output_path} — single font size w:sz={final_sizes[0]}")
    else:
        print(f"WARN: multiple sizes remain: {set(final_sizes)}")

if __name__ == '__main__':
    main()
