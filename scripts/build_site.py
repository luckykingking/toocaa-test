"""Build the static guide site. Run from any directory with Python 3.10+."""
from __future__ import annotations

import csv
import html
import json
import posixpath
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "content"))
from pages import PAGES, FRAMEWORK_HUBS, section  # noqa: E402

DOCS = ROOT / "docs"
BASE = "https://luckykingking.github.io/toocaa-test/"
VERSION = "20261020-complete"
SOURCES = json.loads((ROOT / "content/sources.json").read_text(encoding="utf-8"))
SETTINGS = json.loads((ROOT / "content/settings.json").read_text(encoding="utf-8"))
GROUP_PATHS = {"Use Cases": "use-cases/", "Tutorials": "tutorials/", "Materials": "learn/materials/", "Support": "support/", "Troubleshooting": "troubleshooting/", "Software": "software/", "Who It's For": "who-is-it-for/"}
ISSUE_GROUPS = {"laser-cutting": "Laser & Cutting", "engraving": "Engraving Quality", "hardware": "Hardware & Motion", "software": "Software & Connection", "nova-smart": "NOVA Smart Features", "safety": "Safety & Ventilation", "maintenance": "Maintenance & Care"}
REQUIREMENTS = json.loads((ROOT / 'content/requirements.json').read_text(encoding='utf-8'))
ILLUSTRATIONS = {
    'cut-quality': dict(file='cut-quality-concept.png', alt='Illustrated comparison of scorched, incomplete and cleanly separated plywood cuts', caption='AI-generated cut-quality illustration, not a measured machine test. Left: scorched edges. Center: incomplete separation. Right: a separated cut.', width=1536, height=1024),
    'wood-projects': dict(file='wood-project-concepts.png', alt='Concepts for a plywood box, engraved coasters and a hanging sign', caption='AI-generated project concepts. These are not customer cases, downloadable designs or proof of tested settings.', width=1536, height=1024),
    'nova-window': dict(file='nova-window-screws.png', alt='TOOCAA NOVA module securing screws identified in the official maintenance photograph', caption='TOOCAA NOVA 10W/20W maintenance reference: securing screws. Disconnect power and let the module cool before maintenance.', width=1310, height=985, source='novaLens'),
    'nova-filter': dict(file='nova-filter-housing.png', alt='NOVA rear built-in filter housing in the TOOCAA maintenance guide', caption='The NOVA built-in machine-filter housing, shown in the TOOCAA maintenance guide. This is not the optional purifier cartridge.', width=1300, height=969, source='novaInternalFilter'),
}
ASSETS = {
    "workspace": ("workspace.jpg", "TOOCAA laser machine and computer in a studio"),
    "wood": ("wood.jpg", "Wood blanks offered by TOOCAA"),
    "leather": ("leather.jpg", "Leather material offered by TOOCAA"),
    "metal": ("metal.jpg", "Metal blanks offered by TOOCAA"),
    "stone": ("stone.jpg", "Engraved slate example from TOOCAA"),
}

HUBS = [
    dict(path="", title="TOOCAA Learning Center", description="Get started with your TOOCAA laser. Find setup tutorials, material settings, project ideas, and help for cutting and engraving with NOVA and L2.", group="Home", keywords="TOOCAA guides, TOOCAA tutorials, TOOCAA material settings, TOOCAA support", sources=["manual", "settings"], sections=[], label="Learning Center"),
    dict(path="use-cases/", title="Laser Cutting & Engraving Project Ideas", description="Explore seven laser project guides: craft studios, personalized gifts, QR code signs, home decor, jewelry, gift packaging, and photo engraving.", group="Use Cases", keywords="laser cutting project ideas, laser engraving projects, TOOCAA use cases", sources=["manual", "settings"], sections=[], label="Use Cases"),
    dict(path="tutorials/", title="TOOCAA Laser Cutting & Engraving Tutorials", description="Follow practical TOOCAA tutorials for setup, focus, cutting, engraving, material testing, TOOCAA Studio, LightBurn, and rotary preparation.", group="Tutorials", keywords="TOOCAA tutorials, laser cutting tutorials, laser engraving tutorials", sources=["manual", "studio"], sections=[], label="Tutorials"),
    dict(path="learn/materials/", title="Laser Materials Guide: Wood, Acrylic, Leather & More", description="Choose wood, acrylic, leather, and other laser materials. Find L2 setting references, preparation steps, and tips for checking your finished work.", group="Materials", keywords="laser materials guide, laser compatible materials, laser material settings", sources=["settings", "faq"], sections=[], label="Materials"),
    dict(path="support/", title="TOOCAA Support: Setup, Maintenance & Contact", description="Get help with your TOOCAA laser: first setup, maintenance, troubleshooting, manuals, and contact details for the support team.", group="Support", keywords="TOOCAA support, TOOCAA setup, TOOCAA maintenance", sources=["wiki", "contact"], sections=[], label="Support"),
    dict(path="troubleshooting/", title="TOOCAA Troubleshooting: Cutting, Connection & Safety", description="Find symptom-based checks for TOOCAA laser output, incomplete cuts, engraving quality, movement, connection, smoke, safety alerts, and firmware.", group="Troubleshooting", keywords="TOOCAA troubleshooting, laser not cutting through, laser connection issues", sources=["support", "manual"], sections=[], label="Troubleshooting"),
]
HUBS += FRAMEWORK_HUBS
ALL = HUBS + PAGES
BY_PATH = {p["path"]: p for p in ALL}
HUBS[1]["faqs"] = [("Which project should I try first?", "Choose a small design on documented stock, such as a simple wood name tag or coaster. Test the material and inspect focus, placement, and edge quality before making a batch.")]


def esc(value):
    return html.escape(str(value), quote=True)


def slug(value):
    import re
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def relative(path, target):
    if target.startswith(("https://", "http://", "mailto:", "#")):
        return target
    root = posixpath.relpath(".", path.rstrip("/") or ".")
    return ("" if root == "." else root + "/") + (target or "index.html")


def link(page, target, label, cls="", download=False):
    return f'<a href="{esc(relative(page["path"], target))}"' + (f' class="{cls}"' if cls else "") + (' download' if download else '') + f'>{esc(label)}</a>'


def title(page):
    return page["title"] if "TOOCAA" in page["title"] else page["title"] + " | TOOCAA"


def header(page):
    path = page["path"]
    store = "https://www.toocaa.com/"
    def menu(name, target, columns, active=False):
        menu_id = "nav-" + slug(name)
        content = []
        for heading, entries in columns:
            links = ''.join(link(page, dest, label) for dest, label in entries)
            content.append(f'<div class="menu-column"><p>{esc(heading)}</p>{links}</div>')
        current = ' aria-current="location"' if active else ''
        return f'<div class="nav-group"><a href="{esc(relative(path, target))}"{current}>{name}</a><button class="nav-toggle" type="button" aria-label="Show {name.lower()} menu" aria-expanded="false" aria-controls="{menu_id}"></button><div class="dropdown" id="{menu_id}">{"".join(content)}</div></div>'
    products_menu = menu("Products", store + "collections/all-product", [
        ("Machines", [(store + "collections/toocaa-nova", "TOOCAA NOVA"), (store + "collections/laser-engraving-machine", "TOOCAA L2"), (store + "pages/help-me-choose", "Compare machines")]),
        ("Materials", [(store + "collections/plywood", "Plywood"), (store + "collections/leather", "PU Leather"), (store + "collections/metal", "Metal Blanks"), (store + "collections/slate-plant-labels", "Slate Plant Labels"), (store + "collections/materials", "All materials")]),
        ("Accessories", [(store + "collections/air-assist", "Air Assist"), (store + "collections/smoke-purifier", "Smoke Purifier"), (store + "collections/smart-camera", "Smart Camera"), (store + "collections/rotary-roller", "Rotary Roller"), (store + "collections/accessories", "All accessories")]),
    ])
    learn_menu = menu("Learn", "", [
        ("Learn with TOOCAA", [("", "Learning Center"), ("tutorials/", "Tutorials"), ("learn/materials/", "Material Guides"), ("use-cases/", "Use Cases"), ("who-is-it-for/", "Who It's For")]),
        ("Tools & inspiration", [("software/", "Software Guides"), ("support/material-settings/", "Material Settings"), ("support/accessories/", "Accessories Guide"), (store + "blogs/toocaa-knowledge-share", "Blog"), (SOURCES["space"]["url"], "Project Files on TOOCAA Space")]),
    ], page["group"] in {"Home", "Tutorials", "Materials", "Use Cases", "Software", "Who It's For"})
    support_menu = menu("Support", "support/", [
        ("Machine help", [("support/", "Support"), ("support/before-you-buy/", "Before You Buy"), ("support/material-settings/", "Material Settings"), ("troubleshooting/", "Troubleshooting"), ("tutorials/first-setup/", "First Setup"), ("support/maintenance/", "Maintenance & Care"), (SOURCES["wiki"]["url"], "Support Center & Manuals"), ("support/contact/", "Contact Us")]),
        ("Orders & policies", [(store + "pages/shipping-policy", "Shipping Policy"), (store + "pages/aftersales-policies", "Aftersales Policy"), (store + "pages/warranty-policy", "Warranty"), (store + "pages/refund-policy", "Return & Refund Policy")]),
    ], page["group"] in {"Support", "Troubleshooting"})
    groups = [products_menu, link(page, SOURCES["space"]["url"], "TOOCAA Space", "nav-direct"), link(page, SOURCES["studio"]["url"], "TOOCAA Studio", "nav-direct"), learn_menu, support_menu, link(page, SOURCES["choose"]["url"], "Help Me Choose", "nav-direct"), link(page, store + "pages/about-us", "About TOOCAA", "nav-direct")]
    family = "Support" if page["group"] in {"Support", "Troubleshooting"} else "Learn"
    secondary = [("support/", "Support"), ("troubleshooting/", "Troubleshooting"), ("support/material-settings/", "Material Settings"), ("support/maintenance/", "Maintenance"), ("support/contact/", "Contact Us")] if family == "Support" else [("", "Learning Center"), ("use-cases/", "Use Cases"), ("tutorials/", "Tutorials"), ("learn/materials/", "Materials"), ("software/", "Software"), ("who-is-it-for/", "Who It's For")]
    sublinks = ''.join(f'<a href="{esc(relative(path, dest))}"' + (' aria-current="page"' if path == dest else ' aria-current="location"' if dest and path.startswith(dest) and not any(path.startswith(d) for d, _ in secondary if d != dest and d.startswith(dest)) else '') + f'>{label}</a>' for dest, label in secondary)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="utility"><div class="wide-shell"><span>TOOCAA Learning Center</span>{link(page, store, 'Shop TOOCAA &rarr;').replace('&amp;rarr;', '&rarr;')}</div></div>
<header class="header"><div class="header-inner">
<a class="logo" href="{relative(path, '')}" aria-label="TOOCAA Learning Center home"><img src="{relative(path, 'assets/images/logo.png')}" alt="TOOCAA" width="150" height="15"/></a>
<button class="menu-button" type="button" aria-label="Open navigation" aria-controls="site-nav" aria-expanded="false"><span></span><span></span><span></span></button>
<form class="header-search" action="{relative(path, 'search/')}" role="search"><input type="search" name="q" aria-label="Search all guides" placeholder="Search tutorials, materials, and support" required/><button class="icon-button" aria-label="Search guides" title="Search guides" type="submit"><img src="{relative(path, 'assets/icons/search.svg')}" alt="Search" width="22" height="22"/></button></form>
<div class="store-actions"><a class="icon-button" href="{store}customer_authentication/redirect?locale=en&amp;region_country=US" aria-label="TOOCAA store account" title="TOOCAA store account"><img src="{relative(path, 'assets/icons/user-round.svg')}" alt="Account" width="23" height="23"/></a><a class="icon-button" href="{store}cart" aria-label="TOOCAA store cart" title="TOOCAA store cart"><img src="{relative(path, 'assets/icons/shopping-bag.svg')}" alt="Cart" width="23" height="23"/></a></div>
<nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(groups)}</nav>
</div></header><nav class="section-nav" aria-label="{family} navigation"><div class="shell"><span>{family}</span>{sublinks}</div></nav>'''


def breadcrumb(page):
    items = [("Home", "")]
    if page["group"] in GROUP_PATHS and page["path"] != GROUP_PATHS[page["group"]]:
        items.append((page["group"], GROUP_PATHS[page["group"]]))
    if page["path"]:
        items.append((page["label"], page["path"]))
    html_items = []
    for index, (name, path) in enumerate(items):
        html_items.append((link(page, path, name) if index < len(items)-1 else f'<span aria-current="page">{esc(name)}</span>'))
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [dict({"@type": "ListItem"}, position=i+1, name=name, item=BASE+path) for i, (name, path) in enumerate(items)]}
    return '<nav class="breadcrumb" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(html_items) + '</nav>', schema


def directory(page, entries, searchable=False):
    out = ['<ul class="directory"' + (' id="guide-list"' if searchable else '') + '>']
    cats = {"Getting Started":"start", "Cutting":"cut", "Engraving":"engrave", "Materials":"material", "Software":"software", "Advanced":"advanced", "Technology":"technology", "Buying Guides":"buying", "Safety":"safety"}
    for i, item in enumerate(entries):
        category = item.get("category", item["group"])
        key = cats.get(category, category)
        anchor = ''
        models = ','.join(item.get('models', ['L2', 'NOVA']))
        read = 'Read on toocaa.com &nearr;' if item['path'].startswith('https://') else 'Read guide &rarr;'
        model_tag = '<span class="model-tag">TOOCAA NOVA</span>' if item.get('models') == ['NOVA'] else ''
        out.append(f'<li{anchor} data-guide data-category="{esc(key)}" data-models="{esc(models)}"><a href="{esc(relative(page["path"], item["path"]))}"><span class="category">{esc(ISSUE_GROUPS.get(category, category))}</span>{model_tag}<h3>{esc(item["label"])}</h3><p>{esc(item["description"])}</p><span class="read">{read}</span></a></li>')
    out.append('</ul>')
    return "\n".join(out)


def products(page):
    return f'''<section class="section" id="product-recommendations"><div class="section-head"><h2>Find your TOOCAA</h2>{link(page, SOURCES['choose']['url'], 'Compare NOVA and L2', 'text-link')}</div><div class="products"><div><a class="product-image" href="https://www.toocaa.com/collections/toocaa-nova"><img src="{relative(page['path'], 'assets/images/nova.jpg')}" alt="TOOCAA NOVA enclosed desktop laser engraver" width="900" height="600" loading="lazy"/></a><h3>TOOCAA NOVA</h3><p>For home projects and everyday making. An enclosed laser with a built-in camera and autofocus to help you position and prepare your designs.</p>{link(page, 'https://www.toocaa.com/collections/toocaa-nova', 'Explore NOVA', 'button')}</div><div><a class="product-image" href="https://www.toocaa.com/collections/laser-engraving-machine"><img src="{relative(page['path'], 'assets/images/l2.webp')}" alt="TOOCAA L2 enclosed desktop laser engraver and cutter" width="900" height="600" loading="lazy"/></a><h3>TOOCAA L2</h3><p>For a dedicated craft workspace and repeat orders. A larger working area and a choice of laser modules for cutting and engraving projects.</p>{link(page, 'https://www.toocaa.com/collections/laser-engraving-machine', 'Explore L2', 'button')}</div></div></section>'''


def settings_table(page):
    key = page["path"].split("/")[-2]
    all_settings = page['path'] == 'support/material-settings/'
    keys = {r['key'] for r in SETTINGS['rows']} if all_settings else {"wood": {"basswood", "birch", "walnut", "cherry"}, "acrylic": {"acrylic"}, "leather": {"leather"}}.get(key, set())
    rows = [r for r in SETTINGS["rows"] if r["key"] in keys]
    if not rows:
        return '<p>No matching numerical row is included for this material in the retained L2 data. Do not calculate a substitute for another machine or stock. ' + link(page, SOURCES['settings']['url'], 'Check the current TOOCAA material reference') + '.</p>'
    body = ''.join(f'<tr data-material="{esc(r["key"])}" data-module="{r["module"]}" data-operation="{esc(r["mode"])}">' + ''.join(f'<td>{esc(v)}</td>' for v in [r["material"], str(r["module"])+"W", str(r["thickness"])+" mm", r["mode"], str(r["power"])+"%", str(r["speed"])+" mm/min", r["passes"]]) + '</tr>' for r in rows)
    filters = ''
    if all_settings:
        materials = {r['key']: r['material'] for r in rows}
        options = ''.join(f'<option value="{esc(k)}">{esc(v)}</option>' for k, v in materials.items())
        filters = '<div class="lookup-form" id="materialSettingsFilters"><label>Material<select data-setting-filter="material"><option value="all">All materials</option>' + options + '</select></label><label>L2 module<select data-setting-filter="module"><option value="all">All modules</option><option value="10">10W</option><option value="20">20W</option><option value="40">40W</option></select></label><label>Operation<select data-setting-filter="operation"><option value="all">All operations</option><option value="Cutting">Cutting</option><option value="Engraving">Engraving</option></select></label></div><p id="materialSettingsCount" class="result-count" role="status">17 reference rows</p>'
    table_id = ' id="materialSettingsTable"' if all_settings else ''
    return filters + f'''<p>These settings are for the TOOCAA L2 configurations listed below. Match the material, thickness, module, and operation, then test an offcut before starting your project. For NOVA, use the settings in the NOVA documentation. All speeds below are in mm/min.</p><div class="table-wrap"><table{table_id}><caption>TOOCAA L2 material settings</caption><thead><tr><th scope="col">Material</th><th scope="col">Module</th><th scope="col">Thickness</th><th scope="col">Operation</th><th scope="col">Power</th><th scope="col">Speed</th><th scope="col">Passes</th></tr></thead><tbody>{body}</tbody></table></div><p>{link(page, SETTINGS['source'], 'View the full TOOCAA material settings table')}</p>'''


def wood_lookup(page):
    return '''<section class="article-section" id="settings-calculator"><h2>Find wood settings for your L2</h2><p>Choose your wood, laser module, and operation. Results show the matching entries from the TOOCAA L2 material table, including the tested thickness.</p><form class="lookup-form" aria-label="TOOCAA L2 wood settings"><label>Material<select id="woodMaterial"><option value="basswood">Basswood</option><option value="birch">Birch</option><option value="walnut">Walnut Wood</option><option value="cherry">Red Cherry Wood</option><option value="mdf">MDF</option><option value="poplar">Poplar plywood</option></select></label><label>L2 laser module<select id="woodPowerClass"><option value="10">10W</option><option value="20" selected>20W</option><option value="40">40W</option></select></label><label>Operation<select id="woodMode"><option value="Cutting">Cutting</option><option value="Engraving">Engraving</option></select></label></form><div class="lookup-result" id="lookupResult" role="status" aria-live="polite"><p>Select a combination to find a matching L2 setting, or use the table below.</p></div><p class="review-date">Use a small test piece from your material batch. Settings for birch do not cover every type of birch plywood. Unlisted combinations have no calculated substitute.</p></section>''' + '<script type="application/json" id="settingsData">' + json.dumps(SETTINGS) + '</script>'


def ticket_tool():
    return '''<section class="article-section" id="request-builder"><h2>Prepare your support notes</h2><p>Use this checklist to draft a request locally. Copy the result and send it through TOOCAA's official contact page. Nothing is sent from this form.</p><form class="support-tool" id="ticketForm"><label>Machine and module<input name="machine" placeholder="Model, module, and accessory" required/></label><label>Material and settings<input name="settings" placeholder="Material, thickness, power, speed with units, passes" required/></label><label>Problem and checks already completed<textarea name="symptom" placeholder="What happened, exact error, and results of checks" required></textarea></label><button class="button" type="submit">Prepare support notes</button></form><textarea id="ticketOutput" aria-label="Prepared support notes" rows="9" hidden></textarea><button class="button secondary" type="button" id="copyTicket" hidden>Copy notes</button><p class="copy-status" id="copyStatus" role="status"></p></section>'''


def illustration(page, key):
    item = ILLUSTRATIONS[key]
    source = ' ' + link(page, SOURCES[item['source']]['url'], 'View the illustrated TOOCAA procedure') if item.get('source') else ''
    return f'<figure class="article-media"><img src="{relative(page["path"], "assets/images/" + item["file"])}" alt="{esc(item["alt"])}" width="{item["width"]}" height="{item["height"]}" loading="lazy"/><figcaption>{esc(item["caption"])}{source}</figcaption></figure>'


def article(page):
    sections = []
    toc = []
    for index, block in enumerate(page["sections"]):
        anchor = block.get("anchor") or slug(block["title"])
        toc.append(f'<a href="#{anchor}">{esc(block["title"])}</a>')
        tag = 'ol' if block.get('ordered') else 'ul'
        bullets = f'<{tag}>' + ''.join(f'<li>{esc(x)}</li>' for x in block["bullets"]) + f'</{tag}>' if block["bullets"] else ''
        extra = settings_table(page) if anchor == "settings-table" else ""
        if block.get('table'):
            table = block['table']
            extra += '<div class="table-wrap"><table><thead><tr>' + ''.join(f'<th scope="col">{esc(v)}</th>' for v in table['headers']) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in row) + '</tr>' for row in table['rows']) + '</tbody></table></div>'
        if block.get('links'):
            extra += '<div class="actions">' + ''.join(link(page, dest, label, 'text-link', download=dest.startswith('downloads/')) for dest, label in block['links']) + '</div>'
        sections.append(f'<section class="article-section" id="{anchor}"><h2>{esc(block["title"])}</h2><p>{esc(block["text"])}</p>{bullets}{extra}</section>')
        if index == 0 and page.get('illustration') and page['path'] != 'learn/materials/wood/':
            sections.append(illustration(page, page['illustration']))
    if page["path"] == "learn/materials/wood/":
        sections.insert(2, wood_lookup(page))
        toc.insert(2, '<a href="#settings-calculator">L2 wood settings</a>')
        sections.append('<section class="article-section" id="projects"><h2>Wood project ideas</h2>' + illustration(page, 'wood-projects') + directory(page, [BY_PATH[x] for x in ["use-cases/home-decor/", "use-cases/personalized-gifts/", "use-cases/gift-box-packaging/"]]) + '</section>')
    if page["group"] == "Use Cases":
        sections.append(f'<section class="article-section" id="settings"><h2>Set up your material</h2><p>Find preparation tips for your material, then run a small test with settings for your machine and laser module.</p><div class="actions">{link(page, "learn/materials/", "Browse material guides", "text-link")}{link(page, "tutorials/material-test/", "Run a material test", "text-link")}</div></section>')
    if page['group'] == 'Materials' and page['path'] != 'learn/materials/wood/':
        projects = [BY_PATH[p] for p in page.get('related', []) if p.startswith('use-cases/')]
        if projects:
            sections.append('<section class="article-section" id="project-ideas"><h2>Projects for this material</h2>' + directory(page, projects) + '</section>')
    if page["path"] == "support/ticket-checklist/":
        sections.append(ticket_tool())
    if page["path"] == "support/contact/":
        sections.append(f'<section class="article-section"><h2>Contact & manuals</h2><div class="actions">{link(page, "mailto:service@toocaa.com", "Email support", "button")}{link(page, SOURCES["contact"]["url"], "Contact page", "text-link")}{link(page, SOURCES["wiki"]["url"], "Open Support Center", "text-link")}</div></section>')
    return '<div class="article-layout"><div class="article-body">' + ''.join(sections) + '</div><aside class="toc" aria-label="On this page"><strong>On this page</strong>' + ''.join(toc) + '</aside></div>'


def project_showcase(page, entries):
    images = {'professional-studio-crafts':'workspace', 'personalized-gifts':'leather', 'qr-code-signage':'metal', 'home-decor':'wood', 'jewelry':'metal', 'gift-box-packaging':'wood', 'photo-engraving':'stone'}
    sections = []
    for item in entries:
        key = item['path'].rstrip('/').split('/')[-1]
        name, alt = ASSETS[images.get(key, item.get('image') or 'workspace')]
        media = f'<figure><img src="{relative(page["path"], "assets/images/" + name)}" alt="{esc(alt)}" width="900" height="600" loading="lazy"/><figcaption>{esc(alt)}.</figcaption></figure>'
        if key in {'home-decor', 'gift-box-packaging', 'diy-gifts'}:
            media = illustration(page, 'wood-projects')
        is_case = item['group'] == 'Use Cases'
        projects = item['sections'][0]['bullets'] if is_case else [row[0] for row in item['sections'][1]['table']['rows']]
        ideas = ''.join('<li>' + esc(x) + '</li>' for x in projects)
        preparation = item['sections'][1 if is_case else 0]['text']
        quality = item['sections'][3 if is_case else 4]['text']
        sections.append(f'<section class="scenario-band" id="{key}"><div class="scenario-layout"><div><h2>{esc(item["label"])}</h2><p>{esc(item["description"])}</p><ul>{ideas}</ul><h3>Prepare your project</h3><p>{esc(preparation)}</p><h3>Check the finished piece</h3><p>{esc(quality)}</p>{link(page, item["path"], "Open the " + item["label"].lower() + " guide", "text-link")}</div>{media}</div></section>')
    return ''.join(sections)


def hub_content(page):
    group = page["group"]
    entries = [p for p in PAGES if p["group"] == group]
    if page.get('collections'):
        sections = []
        for heading, paths in page['collections']:
            sections.append('<section class="section"><h2>' + esc(heading) + '</h2>' + directory(page, [BY_PATH[p] for p in paths]) + '</section>')
        if group == 'Software':
            sections.insert(0, '<section class="section"><div class="actions">' + link(page, SOURCES['studio']['url'], 'Open TOOCAA Studio', 'button') + link(page, SOURCES['lightburn']['url'], 'L2 LightBurn setup reference', 'text-link') + '</div></section>')
            sections.insert(1, f'<figure class="workspace-band"><img src="{relative(page["path"], "assets/images/workspace.jpg")}" alt="TOOCAA L2 and a computer used to prepare a laser project" width="1400" height="729" loading="lazy"/></figure>')
        if group == "Who It's For":
            sections.insert(1, project_showcase(page, entries))
        return ''.join(sections) + (products(page) if group == "Who It's For" else '')
    if group == "Home":
        tasks = [("tutorials/first-setup/", "Set up your laser", "Unboxing, workspace, and your first job"), ("learn/materials/wood/#settings-calculator", "Find material settings", "Wood references for your L2 module"), ("troubleshooting/", "Solve a problem", "Cut quality, connections, and machine checks"), ("https://wiki.toocaa.com/en/home", "Find your machine manual", "NOVA and L2 documentation in the Support Center")]
        shortcuts = '<div class="task-links">' + ''.join(f'<a href="{esc(relative(page["path"], dest))}"><strong>{label}</strong><span>{desc}</span><span class="task-arrow" aria-hidden="true">&rarr;</span></a>' for dest, label, desc in tasks) + '</div>'
        resources = [(SOURCES["studio"]["url"], "TOOCAA Studio", "Open the design and machine-control software."), (SOURCES["space"]["url"], "TOOCAA Space", "Browse designs and project files for your next make."), (SOURCES["settings"]["url"], "Material settings", "Find the full TOOCAA machine settings reference.")]
        resource_links = '<div class="resource-links">' + ''.join(f'<a href="{dest}"><h3>{label}</h3><p>{desc}</p><span aria-hidden="true">&rarr;</span></a>' for dest, label, desc in resources) + '</div>'
        return shortcuts + f'<figure class="workspace-band"><img src="{relative(page["path"], "assets/images/workspace.jpg")}" alt="TOOCAA L2 and a computer on a craft studio workbench" width="1400" height="729" fetchpriority="high"/></figure>' + '<section class="section"><div class="section-head"><h2>Explore the guides</h2><p>Find a project, choose your material, and get help with your setup.</p></div>' + directory(page, HUBS[1:]) + '</section><section class="section"><div class="section-head"><h2>Your first projects</h2>' + link(page, "tutorials/", "All tutorials", "text-link") + '</div>' + directory(page, [BY_PATH[x] for x in ["tutorials/first-engraving/", "tutorials/material-test/", "learn/materials/wood/", "tutorials/photo-preparation/"]]) + '</section><section class="section"><h2>Designs, software & settings</h2>' + resource_links + '</section>' + products(page)
    if group == "Tutorials":
        # Keep material and smoke resources in the library alongside standalone tutorials.
        entries = entries + [BY_PATH["learn/materials/wood/"], BY_PATH["learn/materials/wood/"], BY_PATH["troubleshooting/excessive-smoke-odor/"]]
        entries[-3] = dict(entries[-3], label="Wood & Plywood Cutting Guide", category="Cutting")
        entries[-2] = dict(entries[-2], label="Wood Settings Reference Lookup", category="Materials", path="learn/materials/wood/#settings-calculator")
        entries[-1] = dict(entries[-1], category="Advanced")
        entries += [BY_PATH['learn/materials/metal/'], BY_PATH['learn/materials/acrylic/']]
        categories = {'Getting Started':'Getting Started', 'Material Guides':'Materials', 'Software Guides':'Software', 'Laser Technology':'Technology', "Buyer's Guide":'Buying Guides', 'Safety':'Safety'}
        for required in REQUIREMENTS['requirements']:
            if required['brief'] == 'tutorials' and required['kind'] == 'external':
                entries.append(dict(path=required['target'], label=required['title'], description=required['description'], group='Tutorials', category=categories[required['section']]))
            elif required['brief'] == 'tutorials' and required.get('original_kind') == 'external':
                entries.append(dict(BY_PATH[required['target']], category=categories[required['section']]))
        cats = [("all", "All guides"), ("start", "Getting Started"), ("cut", "Cutting"), ("engrave", "Engraving"), ("material", "Materials"), ("software", "Software"), ("advanced", "Advanced"), ("technology", "Technology"), ("buying", "Buying Guides"), ("safety", "Safety")]
        filters = ''.join(f'<button type="button" data-category-filter="{key}" aria-pressed="{str(key == "all").lower()}">{name}</button>' for key, name in cats)
        return '<section class="section" id="tutorial-list"><h2>Browse the tutorials</h2><div class="library-search"><label for="guideQuery">Find a tutorial</label><input type="search" id="guideQuery" placeholder="Search by material or task"/></div><div class="filterbar" role="group" aria-label="Tutorial categories">' + filters + '</div><p class="result-count" id="resultCount" role="status">All guides</p>' + directory(page, entries, True) + '<p class="empty" id="emptyResult" hidden>No matching tutorials. Try another term or choose All guides.</p></section>'
    if group == "Troubleshooting":
        chunks = ['<section class="section"><div class="notice"><p>For a damaged safeguard, persistent flame, unexpected motion, or abnormal smoke condition, stop the job and follow the model-specific safety instructions before further checks.</p></div><h2>Find the symptom</h2>']
        chunks.append('<div class="library-search"><label for="issueQuery">Search issues</label><input id="issueQuery" type="search" placeholder="For example: camera, USB, smoke"/></div><div class="machine-filter" role="group" aria-label="Machine model"><button type="button" data-machine="all" aria-pressed="true">All machines</button><button type="button" data-machine="L2" aria-pressed="false">L2</button><button type="button" data-machine="NOVA" aria-pressed="false">NOVA</button></div><p class="result-count" id="issueCount" role="status"></p><p id="issueEmpty" class="empty" hidden>No matching issues. Try another symptom or choose All machines.</p>')
        chunks.append('<nav class="issue-jumps" aria-label="Issue categories">' + ''.join(f'<a class="text-link" href="#{key}">{value}</a>' for key, value in ISSUE_GROUPS.items()) + '</nav></section>')
        for key, name in ISSUE_GROUPS.items():
            chunks.append(f'<section class="section" data-issue-section id="{key}"><h2>{name}</h2>' + directory(page, [p for p in entries if p["category"] == key]) + '</section>')
        return ''.join(chunks)
    overview = ''
    if group == "Use Cases":
        rows = ''.join('<tr><td>' + link(page, p['path'], p['label']) + '</td><td>' + esc(', '.join(p['sections'][0]['bullets'])) + '</td></tr>' for p in entries)
        overview = '<section class="section" id="project-overview"><h2>Project overview</h2><div class="table-wrap"><table><thead><tr><th scope="col">Use case</th><th scope="col">Project ideas</th></tr></thead><tbody>' + rows + '</tbody></table></div></section>'
        overview = project_showcase(page, entries) + overview
    manuals = f'<section class="section"><div class="section-head"><div><h2>Manuals for your machine</h2><p>Find NOVA and L2 documentation, installation instructions, and machine-specific help in the TOOCAA Support Center.</p></div>{link(page, SOURCES["wiki"]["url"], "Open Support Center", "button")}</div></section>' if group == "Support" else ''
    if group == 'Materials':
        overview = '<section class="section"><h2>From a material to a tested setup</h2>' + directory(page, [BY_PATH[p] for p in ['support/material-settings/', 'tutorials/material-test/', 'tutorials/laser-safety/']]) + '</section>'
    return manuals + '<section class="section"><h2>' + {"Materials":"Choose a material", "Use Cases":"Project guides", "Support":"How can we help?"}[group] + '</h2>' + directory(page, entries) + '</section>' + overview + (products(page) if group == "Use Cases" else '')


def footer(page):
    groups = [
        ("Shop", [("https://www.toocaa.com/collections/toocaa-nova", "TOOCAA NOVA"), ("https://www.toocaa.com/collections/laser-engraving-machine", "TOOCAA L2"), ("https://www.toocaa.com/collections/materials", "Materials"), ("https://www.toocaa.com/collections/accessories", "Accessories")]),
        ("Learn", [("use-cases/", "Use Cases"), ("tutorials/", "Tutorials"), ("learn/materials/", "Material Guides"), ("software/", "Software Guides"), ("who-is-it-for/", "Who It's For"), (SOURCES["studio"]["url"], "TOOCAA Studio"), (SOURCES["space"]["url"], "TOOCAA Space")]),
        ("Support", [("support/", "Support"), ("support/material-settings/", "Material Settings"), ("troubleshooting/", "Troubleshooting"), (SOURCES["wiki"]["url"], "Manuals & Documentation"), ("support/contact/", "Contact Us")]),
        ("Orders & policies", [("https://www.toocaa.com/pages/shipping-policy", "Shipping Policy"), ("https://www.toocaa.com/pages/warranty-policy", "Warranty"), ("https://www.toocaa.com/pages/refund-policy", "Returns & Refunds"), ("https://www.toocaa.com/pages/privacy-policy", "Privacy Policy")]),
    ]
    columns = ''.join(f'<div><h3>{name}</h3>' + ''.join(link(page, dest, label) for dest, label in entries) + '</div>' for name, entries in groups)
    return f'<footer class="footer"><div class="shell"><div class="footer-brand"><img src="{relative(page["path"], "assets/images/logo.png")}" alt="TOOCAA" width="150" height="15"/>{link(page, "mailto:service@toocaa.com", "service@toocaa.com")}</div><nav class="footer-columns" aria-label="Footer">{columns}</nav><div class="footer-bottom"><span>&copy; 2026 TOOCAA Learning Center</span>{link(page, "sitemap.xml", "Sitemap")}{link(page, "https://www.toocaa.com/", "TOOCAA Store")}</div></div></footer>'


def render(page):
    path = page["path"]
    bc, bc_schema = breadcrumb(page)
    hub = page in HUBS
    image_key = page.get("image") or "workspace"
    image_name, image_alt = ASSETS[image_key]
    image_url = BASE + 'assets/images/' + image_name
    schema = {"@context":"https://schema.org", "@type":"CollectionPage" if hub else "Article", "name": page["title"], "description":page["description"], "url": BASE+path, "inLanguage":"en", "isPartOf":{"@type":"WebSite", "name":"TOOCAA Learning Center", "url":BASE}}
    if not hub:
        schema.update(headline=page["title"], mainEntityOfPage=BASE+path)
        if page.get("image"):
            schema["image"] = image_url
    schemas = [schema, bc_schema]
    faqs = page.get("faqs", [])
    if faqs:
        schemas.append({"@context":"https://schema.org", "@type":"FAQPage", "mainEntity":[{"@type":"Question", "name":q, "acceptedAnswer":{"@type":"Answer", "text":a}} for q, a in faqs]})
    head = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(title(page))}</title><meta name="description" content="{esc(page['description'])}"/><meta name="keywords" content="{esc(page['keywords'])}"/>
<meta name="robots" content="index,follow"/><link rel="canonical" href="{BASE+path}"/>
<meta property="og:type" content="{'website' if hub else 'article'}"/><meta property="og:title" content="{esc(title(page))}"/><meta property="og:description" content="{esc(page['description'])}"/><meta property="og:url" content="{BASE+path}"/><meta property="og:image" content="{image_url}"/><meta name="twitter:card" content="summary_large_image"/>
<link rel="icon" href="{relative(path, 'assets/images/logo.png')}"/><link rel="stylesheet" href="{relative(path, 'assets/site.css')}?v={VERSION}"/>
{''.join('<script type="application/ld+json">'+json.dumps(s, ensure_ascii=True).replace('</', '<\\/')+'</script>' for s in schemas)}
<script defer src="{relative(path, 'assets/site.js')}?v={VERSION}"></script></head><body>'''
    body = header(page) + '<main id="main" class="shell">' + (bc if path else '')
    if page["group"] == "Home":
        body += f'<section class="learning-intro"><h1>{esc(page["title"])}</h1><p class="intro">From your first engraving to your next collection.<br/>Find tutorials, material advice, and help for your TOOCAA laser.</p><form class="learning-search" action="search/" role="search" aria-label="Learning Center search"><label class="sr-only" for="homeQuery">What would you like to make or solve?</label><input id="homeQuery" type="search" name="q" placeholder="Search a project, material, or problem" required/><button class="icon-button" type="submit" aria-label="Search Learning Center" title="Search Learning Center"><img src="assets/icons/search.svg" alt="Search" width="24" height="24"/></button></form><p class="popular">Popular: {link(page, "tutorials/first-engraving/", "First engraving")} {link(page, "learn/materials/wood/", "Wood settings")} {link(page, "tutorials/lightburn-setup/", "LightBurn")}</p></section>'
    else:
        body += f'<section class="hero"><h1>{esc(page["title"])}</h1><p class="intro">{esc(page["description"])}</p>'
        if page.get('models'):
            body += '<p class="applies-to">Applies to: ' + esc(' / '.join('TOOCAA ' + m for m in page['models'])) + '</p>'
        if page.get("image") and image_key != "workspace":
            body += f'<figure class="hero-media"><img src="{relative(path, "assets/images/"+image_name)}" alt="{esc(image_alt)}" width="1200" height="650" fetchpriority="high"/></figure>'
        body += '</section>'
    body += hub_content(page) if hub else article(page)
    if faqs:
        body += '<section class="section faq" id="faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs) + '</section>'
    related = list(dict.fromkeys(page.get("related", [])))
    if related:
        entries = [BY_PATH[p.split('#')[0]] for p in related]
        body += '<section class="section"><h2>Related guides</h2>' + directory(page, entries) + '</section>'
    if page["group"] in {"Use Cases", "Who It's For"} and not hub:
        body += products(page)
    if not hub:
        body += '<details class="references"><summary>Manuals &amp; material references</summary><ul class="source-list">' + ''.join(f'<li>{link(page, SOURCES[k]["url"], SOURCES[k]["title"])}</li>' for k in page.get("sources", [])) + '</ul></details>'
    body += f'<section class="support-strip"><div><h2>Need a hand?</h2><p>Get help with your machine, material, or project.</p></div><div class="actions">{link(page, "troubleshooting/", "Troubleshooting", "text-link")}{link(page, "support/contact/", "Contact TOOCAA", "button secondary")}</div></section></main>'
    body += footer(page) + '</body></html>'
    return head + body


def write(path, text):
    destination = DOCS / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    if path.endswith('.html') and '<link rel="icon"' not in text:
        parent = Path(path).parent.as_posix()
        image = BASE + 'assets/images/logo.png' if path == '404.html' else relative('' if parent == '.' else parent + '/', 'assets/images/logo.png')
        text = text.replace('</head>', f'<link rel="icon" href="{image}"/></head>')
    destination.write_text(text, encoding="utf-8", newline="\n")


def exports():
    rows = [dict(url=BASE+p["path"], section=p["group"], title=title(p), description=p["description"], keywords=p["keywords"], h1=p["title"], canonical=BASE+p["path"], robots="index,follow", official_references=" | ".join(SOURCES[k]["url"] for k in p.get("sources", [])), checked=SOURCES["checked"]) for p in ALL]
    target = DOCS / 'keyword-table/site-seo-inventory.csv'
    with target.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    checks_path = ROOT / 'content/reference-checks.json'
    checks = json.loads(checks_path.read_text(encoding='utf-8')) if checks_path.exists() else {'checks': []}
    references = {r['url']: r for r in checks['checks']}
    delivery = []
    for required in REQUIREMENTS['requirements']:
        local = required['kind'] == 'local'
        p = BY_PATH.get(required['target']) if local else None
        reference = references.get(required['target'], {})
        delivery.append(dict(
            requirement_id=required['id'], brief=required['brief'], section=required['section'],
            source_cell=required.get('source_cell', ''),
            original_request=required['title'], requested_detail=required['description'], original_target=required.get('original_target', required['target']),
            delivery_url=BASE + required['target'] if local else required['target'],
            coverage='Local content page' if local else 'Verified TOOCAA article' if reference.get('accessible') else 'Reference check required',
            title=title(p) if p else reference.get('title', ''), description=p['description'] if p else reference.get('description', ''),
            keywords=p['keywords'] if p else reference.get('keywords', ''), h1=p['title'] if p else reference.get('h1', ''),
            canonical=BASE + p['path'] if p else reference.get('canonical', ''),
            models=' / '.join(p.get('models', [])) if p else '',
            references=' | '.join(SOURCES[k]['url'] for k in p.get('sources', [])) if p else required['target'],
            scope_notes=' '.join(filter(None, [required.get('resolution_note', ''), p.get('scope_note', '')])) if local else 'Existing official article, not newly authored here. Metadata is copied from the linked page; a blank description or keywords field means that meta tag was not found.',
            checked=SOURCES['checked'] if local else checks.get('checked', ''),
        ))
    with (DOCS / 'keyword-table/delivery-checklist.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=delivery[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(delivery)
    with (DOCS / 'keyword-table/contract-delivery.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=delivery[0].keys(), lineterminator='\n')
        w.writeheader()
        w.writerows(row for row in delivery if row['brief'].startswith('contract-'))
    # The existing wood keyword files are retained as a dated research snapshot.
    page = dict(path="keyword-table/", group="SEO", title="TOOCAA SEO Inventory", description="Page titles, descriptions, keywords and canonical URLs for the guide site.", label="SEO Inventory")
    table = '<div class="table-wrap"><table><thead><tr><th>Section</th><th>Page / H1</th><th>Title</th><th>Description</th><th>Keywords</th></tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in [esc(r["section"]), link(page, r["url"], r["h1"]), esc(r["title"]), esc(r["description"]), esc(r["keywords"])]) + '</tr>' for r in rows) + '</tbody></table></div>'
    contract_link = link(page, 'keyword-table/contract-delivery.csv', 'Download contract scope: 7 hubs + 22 articles', 'button', download=True)
    contract_section = '<section class="section"><h2>Original scope table</h2><p>The contract-only export separates the seven section frameworks from the 22 specified articles and retains the original sheet references.</p>' + contract_link + '</section>'
    write('keyword-table/index.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>TOOCAA SEO Inventory</title><meta name="description" content="Download and review the site page titles, descriptions, target keywords and canonical URLs."/><meta name="robots" content="noindex,follow"/><link rel="canonical" href="{BASE}keyword-table/"/><link rel="stylesheet" href="../assets/site.css?v={VERSION}"/></head><body><main class="shell"><section class="hero"><h1>Site SEO Inventory</h1><p class="intro">{len(rows)} public pages and {len(delivery)} document requirements. Target keywords describe page topics; this export does not claim rankings or a new audit of keyword ownership on toocaa.com.</p><div class="actions"><a class="button" download href="site-seo-inventory.csv">Download all-page TDK CSV</a><a class="button secondary" download href="delivery-checklist.csv">Download full delivery checklist</a><a class="text-link" download href="toocaa-wood-guide-keywords.xlsx">Original wood keyword XLSX</a><a class="text-link" download href="toocaa-wood-guide-keywords.csv">Original wood keyword CSV</a><a class="text-link" href="../">Back to guides</a></div></section><p>Original keyword research files are historical snapshots. Their ownership and volume fields have not been recrawled for this update.</p>{contract_section}{table}</main></body></html>')


def search_page():
    p = dict(path="search/", group="Search", title="Search TOOCAA Guides", description="Search project ideas, materials, tutorials and support guides.", label="Search")
    items = [{"title":x["title"], "description":x["description"], "group":x["group"], "path":x["path"], "keywords":x["keywords"]} for x in ALL]
    data = json.dumps(items).replace('</', '<\\/')
    write('search/index.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Search TOOCAA Guides</title><meta name="description" content="Search project ideas, material guides, laser tutorials, support and troubleshooting."/><meta name="robots" content="noindex,follow"/><link rel="canonical" href="{BASE}search/"/><link rel="stylesheet" href="../assets/site.css?v={VERSION}"/><script defer src="../assets/site.js?v={VERSION}"></script></head><body>{header(p)}<main class="shell" id="main"><section class="hero"><h1>Search the guides</h1><p class="intro">Find a material, project, setup task, or symptom.</p></section><section class="section"><form id="siteSearchForm" class="library-search"><label for="siteQuery">Search</label><input id="siteQuery" type="search" name="q" placeholder="For example: plywood, LightBurn, smoke"/></form><p id="searchCount" class="result-count" role="status"></p><ul class="directory" id="searchResults"></ul><noscript>Use the navigation menus to browse all project, tutorial, material, support, and troubleshooting pages.</noscript></section></main>{footer(p)}<script type="application/json" id="searchData">{data}</script></body></html>')


def main():
    for p in ALL:
        write(p['path'] + 'index.html', render(p))
    write('assets/settings-data.json', json.dumps(SETTINGS, indent=2) + '\n')
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p["path"]}</loc></url>\n' for p in ALL) + '</urlset>\n'
    write('sitemap.xml', sitemap)
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n')
    write('404.html', '<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="robots" content="noindex,follow"/><title>Page Not Found | TOOCAA Guides</title><link rel="stylesheet" href="'+BASE+'assets/site.css"/></head><body><main class="shell"><section class="hero"><h1>Page not found</h1><p class="intro">The guide may have moved. Browse the current guide library to find the material, project, or support topic.</p><div class="actions"><a class="button" href="'+BASE+'">Open TOOCAA Guides</a><a class="text-link" href="'+BASE+'search/">Search guides</a></div></section></main></body></html>')
    write('llms.txt', '# TOOCAA Guides\n\nPractical guides for laser projects, materials, setup and troubleshooting.\n\n' + '\n'.join(f'- [{p["title"]}]({BASE+p["path"]}): {p["description"]}' for p in HUBS) + '\n')
    search_page()
    exports()
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (ROOT / 'robots.txt').write_text((DOCS/'robots.txt').read_text(encoding='utf-8'), encoding='utf-8')
    (ROOT / 'llms.txt').write_text((DOCS/'llms.txt').read_text(encoding='utf-8'), encoding='utf-8')
    print(f'Built {len(ALL)} public pages, search, SEO inventory, sitemap and robots.txt.')


if __name__ == '__main__':
    main()
