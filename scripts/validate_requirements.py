"""Audit rendered delivery against the supplied briefs, not a headline page count."""
import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET

from import_requirements import apply_overrides, extract
from build_site import ALL, BASE, DOCS, HUBS, ILLUSTRATIONS, PAGES, ROOT, SOURCES
from validate_site import Page


def main():
    manifest = json.loads((ROOT / 'content/requirements.json').read_text(encoding='utf-8'))
    errors, verified = [], []
    rows = manifest['requirements']
    expected_rows = []
    for source in manifest['sources']:
        path = ROOT / source['file']
        if hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest() != source['sha256_lf']:
            errors.append(f"Original brief changed: {source['file']}")
        kind = path.stem
        original = apply_overrides(extract(path, kind))
        expected_count = {'troubleshooting': 51, 'tutorials': 22}[kind]
        if len(original) != expected_count:
            errors.append(f'{kind}: original item count is not {expected_count}')
        if any(not row['description'] for row in original):
            errors.append(f'{kind}: original requested detail was not preserved')
        expected_rows.extend(dict(id=f'{kind}-{i+1:02d}', brief=kind, **row) for i, row in enumerate(original))
    if [r for r in rows if r['brief'] in {'tutorials', 'troubleshooting'}] != expected_rows:
        errors.append('Requirement manifest does not match the preserved HTML briefs and explicit source corrections')
    scenario_paths = {f'use-cases/{slug}/' for slug in ['professional-studio-crafts', 'personalized-gifts', 'qr-code-signage', 'home-decor', 'jewelry', 'gift-box-packaging', 'photo-engraving']}
    if {r['target'] for r in rows if r['brief'] == 'scenario-screenshot'} != scenario_paths:
        errors.append('Seven supplied application scenarios are not preserved')
    contract = json.loads((ROOT / 'content/contract-requirements.json').read_text(encoding='utf-8'))
    if [r for r in rows if r['brief'].startswith('contract-')] != contract['requirements']:
        errors.append('Contract frameworks and specified articles are missing from the delivery manifest')
    expected = 80 + len(contract['requirements'])
    if len(rows) != expected or len({r['id'] for r in rows}) != expected:
        errors.append(f'Expected {expected} distinct document requirements')
    if len(contract['groups']) != 7 or sum(g['articles'] for g in contract['groups']) != 22:
        errors.append('The supplied contract must retain seven frameworks and 22 specified articles')
    references = json.loads((ROOT / 'content/reference-checks.json').read_text(encoding='utf-8'))
    reference_by_url = {r['url']: r for r in references['checks']}
    by_path = {p['path']: p for p in ALL}
    tutorial_page = Page(DOCS / 'tutorials/index.html')
    category_map = {'Laser & Cutting Issues':'laser-cutting', 'Engraving Quality Issues':'engraving', 'Hardware & Mechanical Issues':'hardware', 'Software & Connection Issues':'software', 'NOVA Smart Features \u2014 Exclusive':'nova-smart', 'Safety & Ventilation Issues':'safety', 'Maintenance & Care':'maintenance'}
    first_sections = set()
    for required in rows:
        label, target = required['id'], required['target']
        if required['kind'] == 'external':
            proof = reference_by_url.get(target, {})
            if not proof.get('accessible') or proof.get('status') != 200 or not proof.get('h1'):
                errors.append(f'{label}: no verified substantive original reference: {target}')
            if target not in tutorial_page.links:
                errors.append(f'{label}: external tutorial is absent from the rendered library')
            verified.append(dict(id=label, target=target, evidence='HTTP 200, matching article heading, rendered library link'))
            continue
        page = by_path.get(target)
        path = DOCS / target / 'index.html'
        if page is None or not path.is_file():
            errors.append(f'{label}: missing requested content page: {target}')
            continue
        rendered = Page(path)
        if required['brief'] == 'contract-framework':
            if target not in {p['path'] for p in HUBS} or not any(schema.get('@type') == 'CollectionPage' for schema in rendered.schemas):
                errors.append(f'{label}: required framework is not a complete collection page')
            for article in contract['requirements']:
                if article['brief'] == 'contract-article' and article['section'] == required['section']:
                    if not any(article['target'] in href for href in rendered.links):
                        errors.append(f'{label}: missing specified child article {article["target"]}')
            verified.append(dict(id=label, target=BASE + target, evidence='Collection page, original-scope child links and actual metadata'))
            continue
        if len(page['sections']) < 4 or len(page.get('faqs', [])) < 1:
            errors.append(f'{label}: insufficient topic sections or FAQ')
        words = ' '.join(s['text'] + ' ' + ' '.join(s['bullets']) + ' ' + ' '.join(str(v) for row in s.get('table', {}).get('rows', []) for v in row) for s in page['sections']).split()
        if len(words) < 150:
            errors.append(f'{label}: content is only {len(words)} words')
        if rendered.h1 != page['title']:
            errors.append(f'{label}: rendered H1 does not match the content record')
        if any(term in ' '.join(rendered.texts).lower() for term in ['content needed', 'lorem ipsum', 'coming soon', '模块1', '模块4']):
            errors.append(f'{label}: customer page contains a placeholder or internal module label')
        if not page['sources'] or any(key not in SOURCES for key in page['sources']):
            errors.append(f'{label}: missing source references')
        for key in page['sources']:
            if SOURCES[key]['url'] not in rendered.links:
                errors.append(f'{label}: source is not present in rendered references: {key}')
        if required['brief'] == 'troubleshooting':
            if page.get('category') != category_map[required['section']]:
                errors.append(f'{label}: issue is in the wrong original category')
            if not page.get('models'):
                errors.append(f'{label}: machine applicability is missing')
            if page['sections'][0]['text'] in first_sections:
                errors.append(f'{label}: duplicated topic introduction')
            first_sections.add(page['sections'][0]['text'])
        if required['brief'] == 'tutorials':
            if not any(target in href for href in tutorial_page.links):
                errors.append(f'{label}: requested local tutorial is absent from the library')
        verified.append(dict(id=label, target=BASE + target, evidence=f'{len(page["sections"])} topic sections, {len(words)} words, FAQ, sources and rendered links'))

    for page in PAGES:
        if page.get('illustration'):
            info = ILLUSTRATIONS[page['illustration']]
            rendered = (DOCS / page['path'] / 'index.html').read_text(encoding='utf-8')
            if info['file'] not in rendered:
                errors.append(f"{page['path']}: requested illustration is missing")
            if info['file'] in {'wood-project-concepts.png', 'cut-quality-concept.png'} and 'AI-generated' not in rendered:
                errors.append(f"{page['path']}: AI illustration is not disclosed")
    svg = ET.parse(DOCS / 'downloads/import-size-check.svg').getroot()
    square, circle = svg.find('.//{*}rect'), svg.find('.//{*}circle')
    if svg.attrib.get('width') != '40mm' or square is None or circle is None or square.attrib.get('width') != '20' or circle.attrib.get('r') != '5':
        errors.append('SVG import-size exercise has incorrect dimensions')
    with (DOCS / 'keyword-table/delivery-checklist.csv').open(encoding='utf-8-sig', newline='') as f:
        delivery = list(csv.DictReader(f))
    if {r['requirement_id'] for r in delivery} != {r['id'] for r in rows}:
        errors.append('Delivery CSV does not cover all original requirements')
    for row in delivery:
        if row['coverage'] == 'Reference check required':
            errors.append(f"Unverified delivery reference: {row['requirement_id']}")
        required = next(r for r in rows if r['id'] == row['requirement_id'])
        if row.get('requested_detail') != required['description'] or row.get('source_cell', '') != required.get('source_cell', ''):
            errors.append(f"Delivery export lost the original source detail: {row['requirement_id']}")
    report = dict(requirements=len(rows), local=sum(r['kind'] == 'local' for r in rows), external=sum(r['kind'] == 'external' for r in rows), verified=verified, errors=errors)
    with (DOCS / 'keyword-table/contract-delivery.csv').open(encoding='utf-8-sig', newline='') as f:
        contract_export = list(csv.DictReader(f))
    if {r['requirement_id'] for r in contract_export} != {r['id'] for r in contract['requirements']}:
        errors.append('Contract-only delivery CSV must cover seven frameworks and 22 specified articles')
    print(f"Document mapping: {len(rows)} requirement entries; {len({r['target'] for r in rows if r['kind'] == 'local'})} distinct local destinations and {report['external']} existing external TOOCAA articles.")
    print('Contract scope: seven working frameworks and 22 specified articles, checked separately from supplemental tutorial/troubleshooting content.')
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS: every original topic is mapped to substantive rendered content or a verified original article; sources, models, illustrations and delivery export checked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
