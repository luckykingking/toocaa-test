"""Extract the supplied scope table without publishing the private workbook."""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
GROUPS = [
    (2, 8, 'use-cases/', ['use-cases/' + s + '/' for s in ['professional-studio-crafts', 'personalized-gifts', 'qr-code-signage', 'home-decor', 'jewelry', 'gift-box-packaging', 'photo-engraving']]),
    (9, 9, 'tutorials/', []),
    (10, 16, 'learn/materials/', ['learn/materials/' + s + '/' for s in ['wood', 'acrylic', 'stone', 'metal', 'paper', 'other', 'leather']]),
    (17, 18, 'support/', ['support/before-you-buy/', 'support/material-settings/']),
    (19, 19, 'troubleshooting/', []),
    (20, 21, 'software/', ['software/toocaa-studio/', 'software/comparison/']),
    (22, 25, 'who-is-it-for/', ['who-is-it-for/' + s + '/' for s in ['studios', 'diy-gifts', 'classrooms', 'small-businesses']]),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    with zipfile.ZipFile(args.source) as archive:
        strings = [''.join(n.itertext()) for n in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        root = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
        cells = {}
        for cell in root.findall('.//m:c', NS):
            value = cell.find('m:v', NS)
            if value is not None:
                cells[cell.attrib['r']] = strings[int(value.text)] if cell.get('t') == 's' else value.text
    groups, requirements = [], []
    for start, end, hub, targets in GROUPS:
        name, task = cells[f'B{start}'], cells[f'E{start}']
        count = int(cells[f'D{start}'])
        if count != len(targets):
            raise ValueError(f'{name}: requested count and route mapping differ')
        original = cells.get(f'A{start}', '')
        group = dict(name=name, framework=hub, articles=count, task=task, source_range=f'A{start}:F{end}', original_url=original)
        groups.append(group)
        requirements.append(dict(id=f'contract-framework-{start}', brief='contract-framework', section=name, title=name, target=hub, kind='local', description=task, source_cell=f'Sheet1!B{start}:E{start}'))
        for index, target in enumerate(targets):
            row = start + index
            requirements.append(dict(id=f'contract-article-{row}', brief='contract-article', section=name, title=cells[f'C{row}'].strip(), target=target, kind='local', description=task, source_cell=f'Sheet1!C{row}'))
    output = dict(source_name=args.source.name, source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(), sheet='Sheet1', groups=groups, requirements=requirements)
    path = ROOT / 'content/contract-requirements.json'
    path.write_text(json.dumps(output, ensure_ascii=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'Extracted {len(groups)} frameworks and {sum(g["articles"] for g in groups)} specified articles; no workbook binary copied.')


if __name__ == '__main__':
    main()
