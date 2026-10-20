"""Check public source destinations without submitting forms or controlling devices."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = self.in_h1 = self.in_title = self.in_head = False
        self.h1 = self.title = ''
        self.description = self.keywords = self.canonical = ''

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'head': self.in_head = True
        if tag == 'main': self.in_main = True
        if tag == 'h1' and self.in_main: self.in_h1 = True
        if tag == 'title' and self.in_head: self.in_title = True
        if tag == 'meta' and self.in_head:
            name = attributes.get('name', '').lower()
            if name == 'description': self.description = attributes.get('content', '')
            if name == 'keywords': self.keywords = attributes.get('content', '')
        if tag == 'link' and attributes.get('rel') == 'canonical':
            self.canonical = attributes.get('href', '')

    def handle_endtag(self, tag):
        if tag == 'head': self.in_head = False
        if tag == 'main': self.in_main = False
        if tag == 'h1': self.in_h1 = False
        if tag == 'title': self.in_title = False

    def handle_data(self, data):
        if self.in_h1: self.h1 += data
        if self.in_title: self.title += data


def check(item):
    url, expected = item if isinstance(item, tuple) else (item, '')
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40) as r:
                content = r.read().decode('utf-8', errors='replace')
                headings = Headings()
                headings.feed(content)
                h1 = ' '.join(headings.h1.split())
                similarity = SequenceMatcher(None, expected.lower(), h1.lower()).ratio() if expected else 1
                accessible = r.status == 200 and len(content) > 300 and bool(h1) and similarity >= 0.35
                return dict(url=url, status=r.status, final_url=r.url, title=headings.title.strip(), description=headings.description.strip(), keywords=headings.keywords.strip(), canonical=headings.canonical, h1=h1, expected_title=expected, title_similarity=round(similarity, 3), bytes=len(content), accessible=accessible)
        except Exception as error:
            if attempt == 2:
                return dict(url=url, accessible=False, error=str(error))
            time.sleep(attempt + 1)


def main():
    requirements = json.loads((ROOT / 'content/requirements.json').read_text(encoding='utf-8'))
    urls = sorted({r['target']: r['title'] for r in requirements['requirements'] if r['kind'] == 'external'}.items())
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(check, urls))
    result = dict(checked=datetime.now(timezone.utc).isoformat(), checks=rows)
    (ROOT / 'content/reference-checks.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))
    return int(any(not r['accessible'] for r in rows))


if __name__ == '__main__':
    raise SystemExit(main())
