"""Preserve supplied HTML briefs and extract their original deliverable lists."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / 'content/briefs'
LOCAL_TUTORIALS = {
    'How to Laser Engrave Wood': 'learn/materials/wood/',
    'How to Laser Engrave on Metal': 'learn/materials/metal/',
    'Acrylic Laser Cutting': 'learn/materials/acrylic/',
    'Laser Cutter File Formats': 'tutorials/laser-file-formats/',
    'Color Laser Engraving': 'tutorials/color-laser-engraving/',
}


class BriefParser(HTMLParser):
    def __init__(self, kind):
        super().__init__()
        self.kind, self.rows = kind, []
        self.heading, self.heading_tag, self.row, self.capture = '', None, None, None
        self.need_description = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h2':
            self.heading, self.heading_tag = '', tag
        classes = a.get('class', '').split()
        if self.kind == 'troubleshooting' and tag == 'a' and 'article-link' in classes:
            self.row = dict(section=self.heading.strip(), title='', target=a['href'].lstrip('/'), kind='local', description='')
            self.need_description = False
        if self.kind == 'tutorials' and tag == 'article' and 'tut-card' in classes:
            self.row = dict(section=self.heading.strip(), title='', target='', kind='local' if 'tut-card--placeholder' in classes else 'external', description='')
        if self.row is not None:
            if tag == ('h4' if self.kind == 'troubleshooting' else 'h3'):
                self.capture = 'title'
            elif tag == 'p' and not self.row['description']:
                self.capture = 'description'
            elif tag == 'span' and self.kind == 'troubleshooting' and self.need_description:
                self.capture, self.need_description = 'description', False
            if tag == 'a' and self.kind == 'tutorials' and a.get('href', '').startswith('https://'):
                self.row['target'] = a['href']

    def handle_data(self, data):
        if self.heading_tag:
            self.heading += data
        if self.row is not None and self.capture:
            self.row[self.capture] += data

    def handle_endtag(self, tag):
        if tag == 'h2':
            self.heading_tag = None
        if tag == 'h4' and self.kind == 'troubleshooting':
            self.need_description = True
        if tag in {'h3', 'h4', 'p'} or (tag == 'span' and self.capture == 'description'):
            self.capture = None
        if self.row is not None and tag == ('a' if self.kind == 'troubleshooting' else 'article'):
            for field in ['title', 'description']:
                self.row[field] = ' '.join(self.row[field].split())
            if self.row['kind'] == 'local' and self.kind == 'tutorials':
                self.row['target'] = next((v for k, v in LOCAL_TUTORIALS.items() if self.row['title'].startswith(k)), '')
                if not self.row['target']:
                    raise ValueError(f"Unmapped tutorial brief: {self.row['title']}")
            self.rows.append(self.row)
            self.row = None


def extract(path, kind):
    parser = BriefParser(kind)
    parser.feed(path.read_text(encoding='utf-8'))
    return parser.rows


def apply_overrides(rows):
    path = ROOT / 'content/requirement-overrides.json'
    overrides = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    for row in rows:
        override = overrides.get(row['target'])
        if override:
            row['original_target'], row['original_kind'] = row['target'], row['kind']
            row.update(override)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--troubleshooting', type=Path)
    parser.add_argument('--tutorials', type=Path)
    args = parser.parse_args()
    BRIEFS.mkdir(parents=True, exist_ok=True)
    for kind in ['troubleshooting', 'tutorials']:
        source = getattr(args, kind)
        if source:
            shutil.copy2(source, BRIEFS / f'{kind}.html')
    sources, requirements = [], []
    for kind, expected in [('troubleshooting', 51), ('tutorials', 22)]:
        path = BRIEFS / f'{kind}.html'
        # Git checkouts may normalize the original HTML's Windows line endings.
        digest = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        sources.append(dict(file=path.relative_to(ROOT).as_posix(), sha256_lf=digest))
        rows = extract(path, kind)
        if len(rows) != expected:
            raise ValueError(f'{kind}: expected {expected} original items, found {len(rows)}')
        requirements.extend(dict(id=f'{kind}-{i+1:02d}', brief=kind, **row) for i, row in enumerate(apply_overrides(rows)))
    for slug, name in [('professional-studio-crafts', 'Studio & Crafts'), ('personalized-gifts', 'Personalized Gifts'), ('qr-code-signage', 'QR Code Signage'), ('home-decor', 'Home Decor'), ('jewelry', 'Jewelry'), ('gift-box-packaging', 'Gift Boxes & Packaging'), ('photo-engraving', 'Photo Engraving')]:
        requirements.append(dict(id='scenario-' + slug, brief='scenario-screenshot', section='Use Cases', title=name, target=f'use-cases/{slug}/', kind='local', description='Seven application areas specified in the supplied page-planning screenshot.'))
    contract = json.loads((ROOT / 'content/contract-requirements.json').read_text(encoding='utf-8'))
    requirements.extend(contract['requirements'])
    output = dict(sources=sources, requirements=requirements)
    (ROOT / 'content/requirements.json').write_text(json.dumps(output, indent=2, ensure_ascii=True) + '\n', encoding='utf-8', newline='\n')
    print(f'Imported {len(requirements)} requirements: original HTML topics plus {len(contract["groups"])} contract frameworks and 22 specified articles.')


if __name__ == '__main__':
    main()
