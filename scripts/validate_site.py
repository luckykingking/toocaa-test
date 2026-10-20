"""Check every generated route, SEO field, structured-data block and internal link."""
from collections import Counter, deque
import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = "https://luckykingking.github.io/toocaa-test/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack, self.errors, self.links, self.ids, self.images = [], [], [], [], []
        self.meta, self.schemas, self.texts = {}, [], []
        self.title = self.h1 = self.canonical = ""
        self.script_type = None
        self.script_text = ""
        self.noindex = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in a:
            self.ids.append(a["id"])
        if tag in {"a", "link"} and "href" in a:
            self.links.append(a["href"])
        if tag in {"script", "img"} and "src" in a:
            self.links.append(a["src"])
        if tag == "form" and a.get("action"):
            self.links.append(a["action"])
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        if tag == "meta":
            self.meta[a.get("name", a.get("property", ""))] = a.get("content", "")
            if a.get("http-equiv", "").lower() == "refresh":
                self.errors.append("unexpected redirect")
        if tag == "img":
            self.images.append(a)
        if tag == "script":
            self.script_type = a.get("type")
            self.script_text = ""

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "script" and self.script_type == "application/ld+json":
            try:
                self.schemas.append(json.loads(self.script_text))
            except json.JSONDecodeError as error:
                self.errors.append(f"invalid JSON-LD: {error}")
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced tag {tag}")
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack and self.stack[-1] == "script":
            self.script_text += data
            return
        if "title" in self.stack:
            self.title += data
        if "h1" in self.stack:
            self.h1 += data
        if not any(tag in self.stack for tag in ["script", "style", "nav", "header", "footer"]):
            self.texts.append(data)


def main():
    pages = {path.resolve(): Page(path) for path in DOCS.rglob("index.html")}
    errors, titles, descriptions = [], [], []
    graph = {p: set() for p in pages}
    indexed = {}
    for path, p in pages.items():
        label = path.relative_to(DOCS)
        p.noindex = "noindex" in p.meta.get("robots", "")
        if p.stack:
            p.errors.append(f"unclosed tags {p.stack}")
        if not p.title.strip() or not p.h1.strip():
            p.errors.append("missing title or H1")
        if not p.meta.get("description"):
            p.errors.append("missing description")
        if len(p.ids) != len(set(p.ids)):
            p.errors.append("duplicate element IDs")
        if not p.noindex:
            expected = BASE + path.parent.relative_to(DOCS).as_posix().replace(".", "").strip("/")
            if not expected.endswith("/"):
                expected += "/"
            if p.canonical != expected:
                p.errors.append(f"canonical mismatch: {p.canonical} != {expected}")
            indexed[p.canonical] = path
            titles.append(p.title.strip())
            descriptions.append(p.meta["description"])
            for field in ["og:title", "og:description", "og:url", "og:image", "twitter:card"]:
                if not p.meta.get(field):
                    p.errors.append(f"missing {field}")
            types = [s.get("@type") for s in p.schemas]
            if "BreadcrumbList" not in types or not any(t in types for t in ["Article", "CollectionPage"]):
                p.errors.append("missing page/breadcrumb structured data")
            if p.meta.get("og:url") != p.canonical:
                p.errors.append("OG URL does not match canonical")
        for img in p.images:
            if not img.get("alt"):
                p.errors.append("missing image alt")
            if not img.get("width") or not img.get("height"):
                p.errors.append("missing explicit image dimensions")
        for href in p.links:
            u = urlparse(href)
            if u.scheme in {"mailto", "tel", "data"}:
                continue
            if u.scheme or u.netloc:
                if not href.startswith(BASE):
                    continue
                local = unquote(u.path[len(urlparse(BASE).path):])
                target = (DOCS / local).resolve()
            else:
                if u.path.startswith("/"):
                    p.errors.append(f"root-relative URL loses project prefix: {href}")
                    continue
                target = (path.parent / unquote(u.path)).resolve() if u.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                p.errors.append(f"missing internal target: {href}")
                continue
            if target in pages:
                graph[path].add(target)
                if u.fragment and unquote(u.fragment) not in pages[target].ids:
                    p.errors.append(f"missing fragment: {href}")
        errors.extend(f"{label}: {e}" for e in p.errors)
    for name, values in [("title", titles), ("description", descriptions)]:
        errors.extend(f"duplicate {name}: {value}" for value, count in Counter(values).items() if count > 1)
    sitemap = ET.parse(DOCS / "sitemap.xml")
    locations = [node.text for node in sitemap.findall(".//{*}loc")]
    if set(locations) != set(indexed):
        errors.append(f"sitemap mismatch: {set(locations)^set(indexed)}")
    if len(locations) != len(set(locations)):
        errors.append("duplicate sitemap locations")
    seen, queue = set(), deque([(DOCS / "index.html").resolve()])
    while queue:
        node = queue.popleft()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(graph.get(node, set()) - seen)
    for path in set(indexed.values()) - seen:
        errors.append(f"orphan page: {path.relative_to(DOCS)}")
    with (DOCS / 'keyword-table/site-seo-inventory.csv').open(encoding="utf-8-sig", newline="") as f:
        inventory = list(csv.DictReader(f))
    if {row["canonical"] for row in inventory} != set(indexed):
        errors.append("SEO CSV does not cover the complete indexable site")
    for row in inventory:
        p = pages[indexed[row["canonical"]]]
        if row["title"] != p.title or row["description"] != p.meta["description"] or row["h1"] != p.h1:
            errors.append(f"SEO CSV differs from actual metadata: {row['url']}")
    if BASE + "sitemap.xml" not in (DOCS / 'robots.txt').read_text(encoding="utf-8"):
        errors.append("robots.txt has no correct sitemap declaration")
    print(f"Checked {len(pages)} HTML routes, {len(indexed)} indexable pages, {len(locations)} sitemap URLs, {len(inventory)} SEO inventory rows.")
    print(f"Homepage-reachable indexable pages: {len(set(indexed.values()) & seen)} / {len(indexed)}")
    if errors:
        print('\n'.join(errors))
        return 1
    print("PASS: metadata, JSON-LD, internal links, anchors, assets, crawl reachability, sitemap and SEO inventory.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
