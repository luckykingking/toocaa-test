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
from pages import PAGES, section  # noqa: E402

DOCS = ROOT / "docs"
BASE = "https://luckykingking.github.io/toocaa-test/"
VERSION = "20261020"
SOURCES = json.loads((ROOT / "content/sources.json").read_text(encoding="utf-8"))
SETTINGS = json.loads((ROOT / "content/settings.json").read_text(encoding="utf-8"))
GROUP_PATHS = {"Use Cases": "use-cases/", "Tutorials": "tutorials/", "Materials": "learn/materials/", "Support": "support/", "Troubleshooting": "troubleshooting/"}
ISSUE_GROUPS = {"laser-cutting": "Laser & Cutting", "engraving": "Engraving Quality", "hardware": "Hardware & Motion", "software": "Software & Connection", "safety": "Safety & Ventilation"}
ASSETS = {
    "workspace": ("workspace.jpg", "TOOCAA laser machine and computer in a studio"),
    "wood": ("wood.jpg", "Wood blanks offered by TOOCAA"),
    "leather": ("leather.jpg", "Leather material offered by TOOCAA"),
    "metal": ("metal.jpg", "Metal blanks offered by TOOCAA"),
    "stone": ("stone.jpg", "Engraved slate example from TOOCAA"),
}

HUBS = [
    dict(path="", title="TOOCAA Laser Cutting & Engraving Guides", description="Find TOOCAA project ideas, practical laser tutorials, material guides, support resources, and troubleshooting for NOVA and L2.", group="Home", keywords="TOOCAA guides, TOOCAA laser cutting, TOOCAA laser engraving", sources=["manual", "settings"], sections=[], label="Home"),
    dict(path="use-cases/", title="Laser Cutting & Engraving Project Ideas", description="Explore seven laser project guides: craft studios, personalized gifts, QR code signs, home decor, jewelry, gift packaging, and photo engraving.", group="Use Cases", keywords="laser cutting project ideas, laser engraving projects, TOOCAA use cases", sources=["manual", "settings"], sections=[], label="Use Cases"),
    dict(path="tutorials/", title="TOOCAA Laser Cutting & Engraving Tutorials", description="Follow practical TOOCAA tutorials for setup, focus, cutting, engraving, material testing, TOOCAA Studio, LightBurn, and rotary preparation.", group="Tutorials", keywords="TOOCAA tutorials, laser cutting tutorials, laser engraving tutorials", sources=["manual", "studio"], sections=[], label="Tutorials"),
    dict(path="learn/materials/", title="Laser Materials Guide: Wood, Acrylic, Leather & More", description="Compare nine laser material guides, check composition and machine compatibility, and find sourced settings for wood, acrylic, leather, and more.", group="Materials", keywords="laser materials guide, laser compatible materials, laser material settings", sources=["settings", "faq"], sections=[], label="Materials"),
    dict(path="support/", title="TOOCAA Support: Setup, Maintenance & Contact", description="Prepare a TOOCAA purchase, set up a delivered machine, review maintenance, and collect the details needed for an official support request.", group="Support", keywords="TOOCAA support, TOOCAA setup, TOOCAA maintenance", sources=["support", "contact"], sections=[], label="Support"),
    dict(path="troubleshooting/", title="TOOCAA Troubleshooting: Cutting, Connection & Safety", description="Find symptom-based checks for TOOCAA laser output, incomplete cuts, engraving quality, movement, connection, smoke, safety alerts, and firmware.", group="Troubleshooting", keywords="TOOCAA troubleshooting, laser not cutting through, laser connection issues", sources=["support", "manual"], sections=[], label="Troubleshooting"),
]
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


def link(page, target, label, cls=""):
    return f'<a href="{esc(relative(page["path"], target))}"' + (f' class="{cls}"' if cls else "") + f'>{esc(label)}</a>'


def title(page):
    return page["title"] if "TOOCAA" in page["title"] else page["title"] + " | TOOCAA"


def header(page):
    path = page["path"]
    groups = []
    for group, hub in GROUP_PATHS.items():
        children = [p for p in PAGES if p["group"] == group]
        # Keep navigation compact; every child is available on the linked hub.
        if group == "Tutorials":
            extra = [("Getting Started", "start"), ("Cutting", "cut"), ("Engraving", "engrave"), ("Materials", "material"), ("Software", "software"), ("Advanced", "advanced")]
            entries = [(hub + "?category=" + key, name) for name, key in extra]
        elif group == "Troubleshooting":
            entries = [(hub + "#" + key, name) for key, name in ISSUE_GROUPS.items()] + [("support/maintenance/", "Maintenance")]
        else:
            entries = [(p["path"], p["label"]) for p in children]
        links = link(page, hub, "All " + group.lower()) + "".join(link(page, dest, name) for dest, name in entries)
        active = ' aria-current="page"' if path == hub else (' aria-current="location"' if page["group"] == group else "")
        menu_id = "nav-" + slug(group)
        groups.append(f'<div class="nav-group"><a href="{esc(relative(path, hub))}"{active}>{group}</a><button class="nav-toggle" type="button" aria-label="Show {group.lower()} menu" aria-expanded="false" aria-controls="{menu_id}"></button><div class="dropdown" id="{menu_id}">{links}</div></div>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="header"><div class="header-inner">
<a class="logo" href="{relative(path, '')}" aria-label="TOOCAA Guides home"><img src="{relative(path, 'assets/images/logo.png')}" alt="TOOCAA" width="116" height="34"/></a>
<button class="menu-button" type="button" aria-label="Open navigation" aria-controls="site-nav" aria-expanded="false"><span></span><span></span><span></span></button>
<nav class="site-nav" id="site-nav" aria-label="Main navigation">{''.join(groups)}</nav>
<form class="header-search" action="{relative(path, 'search/')}" role="search"><input type="search" name="q" aria-label="Search all guides" placeholder="Search guides" required/><button class="icon-button" aria-label="Search guides" type="submit"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg></button></form>
</div></header>'''


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
    cats = {"Getting Started":"start", "Cutting":"cut", "Engraving":"engrave", "Materials":"material", "Software":"software", "Advanced":"advanced"}
    for i, item in enumerate(entries):
        category = item.get("category", item["group"])
        key = cats.get(category, category)
        anchor = f' id="{item["path"].rstrip("/").split("/")[-1]}"' if page["path"] == "use-cases/" else ""
        out.append(f'<li{anchor} data-guide data-category="{esc(key)}"><a href="{esc(relative(page["path"], item["path"]))}"><span class="number">{i+1:02d}</span><span class="category">{esc(category)}</span><h3>{esc(item["label"])}</h3><p>{esc(item["description"])}</p><span class="read">Open guide &rarr;</span></a></li>')
    out.append('</ul>')
    return "\n".join(out)


def products(page):
    return f'''<section class="section" id="product-recommendations"><h2>Explore TOOCAA machines</h2><div class="products"><div><h3>TOOCAA NOVA</h3><p>Check current modules, supported materials, accessories, workspace requirements, and availability on the official product collection.</p>{link(page, 'https://www.toocaa.com/collections/toocaa-nova', 'View TOOCAA NOVA', 'text-link')}</div><div><h3>TOOCAA L2</h3><p>Compare current L2 configurations and check the exact module and accessory requirements for the projects you plan to make.</p>{link(page, 'https://www.toocaa.com/collections/laser-engraving-machine', 'View TOOCAA L2', 'text-link')}</div></div></section>'''


def settings_table(page):
    key = page["path"].split("/")[-2]
    keys = {"wood": {"basswood", "birch", "walnut", "cherry"}, "acrylic": {"acrylic"}, "leather": {"leather"}}.get(key, set())
    rows = [r for r in SETTINGS["rows"] if r["key"] in keys]
    if not rows:
        return ""
    body = ''.join('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in [r["material"], str(r["module"])+"W", str(r["thickness"])+" mm", r["mode"], str(r["power"])+"%", str(r["speed"])+" mm/min", r["passes"]]) + '</tr>' for r in rows)
    return f'''<p>Published TOOCAA L2 reference samples. Do not apply these rows to NOVA or a different material or thickness without model-specific confirmation. Speed values below are in mm/min.</p><div class="table-wrap"><table><caption>TOOCAA L2 reference settings, checked {SOURCES['checked']}</caption><thead><tr><th scope="col">Material</th><th scope="col">Module</th><th scope="col">Thickness</th><th scope="col">Operation</th><th scope="col">Power</th><th scope="col">Speed</th><th scope="col">Passes</th></tr></thead><tbody>{body}</tbody></table></div><p>{link(page, SETTINGS['source'], 'Read the official material settings and conditions')}</p>'''


def wood_lookup(page):
    return '''<section class="article-section" id="settings-calculator"><h2>Find a published wood setting</h2><p>Select the material, L2 module, and operation to see matching published samples. This lookup does not interpolate thicknesses or calculate settings for undocumented materials. Birch means the material named in the source, not every plywood product.</p><form class="lookup-form" aria-label="Published wood settings lookup"><label>Material<select id="woodMaterial"><option value="basswood">Basswood</option><option value="birch">Birch</option><option value="walnut">Walnut Wood</option><option value="cherry">Red Cherry Wood</option><option value="mdf">MDF (no published row here)</option><option value="poplar">Poplar plywood (no published row here)</option></select></label><label>L2 laser module<select id="woodPowerClass"><option value="10">10W</option><option value="20" selected>20W</option><option value="40">40W</option></select></label><label>Operation<select id="woodMode"><option value="Cutting">Cutting</option><option value="Engraving">Engraving</option></select></label></form><div class="lookup-result" id="lookupResult" role="status" aria-live="polite"><p>Use the reference table below; select a combination to filter the published samples.</p></div><p class="review-date">Check the listed sample thickness before using any reference. The source does not guarantee your result.</p></section>''' + '<script type="application/json" id="settingsData">' + json.dumps(SETTINGS) + '</script>'


def ticket_tool():
    return '''<section class="article-section" id="request-builder"><h2>Prepare your support notes</h2><p>Use this checklist to draft a request locally. Copy the result and send it through TOOCAA's official contact page. Nothing is sent from this form.</p><form class="support-tool" id="ticketForm"><label>Machine and module<input name="machine" placeholder="Model, module, and accessory" required/></label><label>Material and settings<input name="settings" placeholder="Material, thickness, power, speed with units, passes" required/></label><label>Problem and checks already completed<textarea name="symptom" placeholder="What happened, exact error, and results of checks" required></textarea></label><button class="button" type="submit">Prepare support notes</button></form><textarea id="ticketOutput" aria-label="Prepared support notes" rows="9" hidden></textarea><button class="button secondary" type="button" id="copyTicket" hidden>Copy notes</button><p class="copy-status" id="copyStatus" role="status"></p></section>'''


def article(page):
    sections = []
    toc = []
    for block in page["sections"]:
        anchor = block.get("anchor") or slug(block["title"])
        toc.append(f'<a href="#{anchor}">{esc(block["title"])}</a>')
        bullets = '<ul>' + ''.join(f'<li>{esc(x)}</li>' for x in block["bullets"]) + '</ul>' if block["bullets"] else ''
        extra = settings_table(page) if anchor == "settings-table" else ""
        sections.append(f'<section class="article-section" id="{anchor}"><h2>{esc(block["title"])}</h2><p>{esc(block["text"])}</p>{bullets}{extra}</section>')
    if page["path"] == "learn/materials/wood/":
        sections.insert(2, wood_lookup(page))
        toc.insert(2, '<a href="#settings-calculator">Find a published setting</a>')
        sections.append('<section class="article-section" id="projects"><h2>Wood project ideas</h2>' + directory(page, [BY_PATH[x] for x in ["use-cases/home-decor/", "use-cases/personalized-gifts/", "use-cases/gift-box-packaging/"]]) + '</section>')
    if page["group"] == "Use Cases":
        sections.append(f'<section class="article-section" id="settings"><h2>Material settings for the project</h2><p>Choose the material guide and the exact model reference before testing. A sample result does not establish settings for a different laser module or sheet.</p><div class="actions">{link(page, "learn/materials/", "Browse material guides", "text-link")}{link(page, "tutorials/material-test/", "Plan a material test", "text-link")}</div></section>')
    if page["path"] == "support/ticket-checklist/":
        sections.append(ticket_tool())
    if page["path"] == "support/contact/":
        sections.append(f'<section class="article-section"><h2>Official TOOCAA channels</h2><div class="actions">{link(page, SOURCES["contact"]["url"], "Contact TOOCAA", "button")}{link(page, SOURCES["support"]["url"], "Open Help Center", "button secondary")}</div></section>')
    return '<div class="article-layout"><div class="article-body">' + ''.join(sections) + '</div><aside class="toc" aria-label="On this page"><strong>On this page</strong>' + ''.join(toc) + '</aside></div>'


def hub_content(page):
    group = page["group"]
    entries = [p for p in PAGES if p["group"] == group]
    if group == "Home":
        return '<section class="section"><div class="section-head"><h2>Choose where to start</h2><p>Plan a project, learn a process, or work through a problem with the machine you already have.</p></div>' + directory(page, HUBS[1:]) + '</section><section class="section"><h2>Start with the basics</h2>' + directory(page, [BY_PATH[x] for x in ["tutorials/first-setup/", "tutorials/material-test/", "learn/materials/wood/", "support/ticket-checklist/"]]) + '</section>' + products(page)
    if group == "Tutorials":
        # Keep material and smoke resources in the library alongside standalone tutorials.
        entries = entries + [BY_PATH["learn/materials/wood/"], BY_PATH["learn/materials/wood/"], BY_PATH["troubleshooting/excessive-smoke-odor/"]]
        entries[-3] = dict(entries[-3], label="Wood & Plywood Cutting Guide", category="Cutting")
        entries[-2] = dict(entries[-2], label="Wood Settings Reference Lookup", category="Materials", path="learn/materials/wood/#settings-calculator")
        entries[-1] = dict(entries[-1], category="Advanced")
        cats = [("all", "All guides"), ("start", "Getting Started"), ("cut", "Cutting"), ("engrave", "Engraving"), ("material", "Materials"), ("software", "Software"), ("advanced", "Advanced")]
        filters = ''.join(f'<button type="button" data-category-filter="{key}" aria-pressed="{str(key == "all").lower()}">{name}</button>' for key, name in cats)
        return '<section class="section" id="tutorial-list"><h2>Browse the tutorials</h2><div class="library-search"><label for="guideQuery">Find a tutorial</label><input type="search" id="guideQuery" placeholder="Search by material or task"/></div><div class="filterbar" role="group" aria-label="Tutorial categories">' + filters + '</div><p class="result-count" id="resultCount" role="status">All guides</p>' + directory(page, entries, True) + '<p class="empty" id="emptyResult" hidden>No matching tutorials. Try another term or choose All guides.</p></section>'
    if group == "Troubleshooting":
        chunks = ['<section class="section"><div class="notice"><p>For a damaged safeguard, persistent flame, unexpected motion, or abnormal smoke condition, stop the job and follow the model-specific safety instructions before further checks.</p></div><h2>Find the symptom</h2>']
        chunks.append('<p>' + ' &middot; '.join(f'<a class="text-link" href="#{key}">{value}</a>' for key, value in ISSUE_GROUPS.items()) + '</p></section>')
        for key, name in ISSUE_GROUPS.items():
            chunks.append(f'<section class="section" id="{key}"><h2>{name}</h2>' + directory(page, [p for p in entries if p["category"] == key]) + '</section>')
        chunks.append(f'<section class="section" id="nova-smart"><h2>NOVA model-specific features</h2><p>Use the current TOOCAA documentation for camera, autofocus, display, or other model-specific warnings. Record the exact message and installed module rather than following an L2 recovery procedure.</p><div class="actions">{link(page, "support/contact/", "Get model-specific support", "button secondary")}</div></section>')
        chunks.append(f'<section class="section" id="maintenance"><h2>Maintenance & Care</h2><p>Keep a baseline sample and follow the documented cleaning and inspection routine.</p><div class="actions">{link(page, "support/maintenance/", "Read the maintenance guide", "text-link")}</div></section>')
        return ''.join(chunks)
    overview = ''
    if group == "Use Cases":
        rows = ''.join('<tr><td>' + link(page, p['path'], p['label']) + '</td><td>' + esc(', '.join(p['sections'][0]['bullets'])) + '</td></tr>' for p in entries)
        overview = '<section class="section" id="project-overview"><h2>Project overview</h2><div class="table-wrap"><table><thead><tr><th scope="col">Use case</th><th scope="col">Project ideas</th></tr></thead><tbody>' + rows + '</tbody></table></div></section>'
    return '<section class="section"><h2>' + {"Materials":"Choose a material", "Use Cases":"Project guides", "Support":"Help for your next step"}[group] + '</h2>' + directory(page, entries) + '</section>' + overview + (products(page) if group in {"Use Cases", "Support"} else '')


def render(page):
    path = page["path"]
    bc, bc_schema = breadcrumb(page)
    hub = page in HUBS
    image_key = page.get("image") or "workspace"
    image_name, image_alt = ASSETS[image_key]
    image_url = BASE + 'assets/images/' + image_name
    schema = {"@context":"https://schema.org", "@type":"CollectionPage" if hub else "Article", "name": page["title"], "description":page["description"], "url": BASE+path, "inLanguage":"en", "isPartOf":{"@type":"WebSite", "name":"TOOCAA Guides", "url":BASE}}
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
        body += f'<section class="home-hero"><div><h1>{esc(page["title"])}</h1><p class="intro">{esc(page["description"])}</p><div class="actions">{link(page, "use-cases/", "Explore projects", "button")}{link(page, "tutorials/first-setup/", "Start with setup", "text-link")}</div></div><img src="{relative(path, "assets/images/workspace.jpg")}" alt="{ASSETS["workspace"][1]}" width="1000" height="800" fetchpriority="high"/></section>'
    else:
        body += f'<section class="hero"><h1>{esc(page["title"])}</h1><p class="intro">{esc(page["description"])}</p>'
        if page.get("image"):
            body += f'<figure class="hero-media"><img src="{relative(path, "assets/images/"+image_name)}" alt="{esc(image_alt)}" width="1200" height="650" fetchpriority="high"/><figcaption>Material and equipment imagery: TOOCAA.</figcaption></figure>'
        body += '</section>'
    body += hub_content(page) if hub else article(page)
    if faqs:
        body += '<section class="section faq" id="faq"><h2>Frequently asked questions</h2>' + ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faqs) + '</section>'
    related = list(dict.fromkeys(page.get("related", [])))
    if related:
        entries = [BY_PATH[p.split('#')[0]] for p in related]
        body += '<section class="section"><h2>Related guides</h2>' + directory(page, entries) + '</section>'
    if page["group"] == "Use Cases" and not hub:
        body += products(page)
    body += '<section class="section"><h2>Official references</h2><ul class="source-list">' + ''.join(f'<li>{link(page, SOURCES[k]["url"], SOURCES[k]["title"])}</li>' for k in page.get("sources", [])) + f'</ul><p class="review-date">References checked {SOURCES["checked"]}. Settings and compatibility must match your exact machine and material.</p></section>'
    body += f'<section class="support-strip"><div><h2>Need help with a specific job?</h2><p>Keep the model, material, file, and settings together when you request support.</p></div>{link(page, "support/ticket-checklist/", "Prepare a support request", "button secondary")}</section></main>'
    body += f'<footer class="footer"><div class="shell footer-inner"><p>TOOCAA Guides &copy; 2026</p><nav class="footer-links" aria-label="Footer">{link(page, "", "Home")}{link(page, "support/contact/", "Contact TOOCAA")}{link(page, "sitemap.xml", "Sitemap")}{link(page, "https://www.toocaa.com/", "Official store")}</nav></div></footer></body></html>'
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
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    # The existing wood keyword files are retained as a dated research snapshot.
    page = dict(path="keyword-table/", group="SEO", title="TOOCAA SEO Inventory", description="Page titles, descriptions, keywords and canonical URLs for the guide site.", label="SEO Inventory")
    table = '<div class="table-wrap"><table><thead><tr><th>Section</th><th>Page / H1</th><th>Title</th><th>Description</th><th>Keywords</th></tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in [esc(r["section"]), link(page, r["url"], r["h1"]), esc(r["title"]), esc(r["description"]), esc(r["keywords"])]) + '</tr>' for r in rows) + '</tbody></table></div>'
    write('keyword-table/index.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>TOOCAA SEO Inventory</title><meta name="description" content="Download and review the site page titles, descriptions, target keywords and canonical URLs."/><meta name="robots" content="noindex,follow"/><link rel="canonical" href="{BASE}keyword-table/"/><link rel="stylesheet" href="../assets/site.css?v={VERSION}"/></head><body><main class="shell"><section class="hero"><h1>Site SEO Inventory</h1><p class="intro">{len(rows)} public pages. Target keywords describe each page topic; this export does not claim rankings or a new audit of keyword ownership on toocaa.com.</p><div class="actions"><a class="button" download href="site-seo-inventory.csv">Download all-page TDK CSV</a><a class="text-link" download href="toocaa-wood-guide-keywords.xlsx">Original wood keyword XLSX</a><a class="text-link" download href="toocaa-wood-guide-keywords.csv">Original wood keyword CSV</a><a class="text-link" href="../">Back to guides</a></div></section><p>Original keyword research files are historical snapshots. Their ownership and volume fields have not been recrawled for this update.</p>{table}</main></body></html>')


def search_page():
    p = dict(path="search/", group="Search", title="Search TOOCAA Guides", description="Search project ideas, materials, tutorials and support guides.", label="Search")
    items = [{"title":x["title"], "description":x["description"], "group":x["group"], "path":x["path"], "keywords":x["keywords"]} for x in ALL]
    data = json.dumps(items).replace('</', '<\\/')
    write('search/index.html', f'<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Search TOOCAA Guides</title><meta name="description" content="Search project ideas, material guides, laser tutorials, support and troubleshooting."/><meta name="robots" content="noindex,follow"/><link rel="canonical" href="{BASE}search/"/><link rel="stylesheet" href="../assets/site.css?v={VERSION}"/><script defer src="../assets/site.js?v={VERSION}"></script></head><body>{header(p)}<main class="shell" id="main"><section class="hero"><h1>Search the guides</h1><p class="intro">Find a material, project, setup task, or symptom.</p></section><section class="section"><form id="siteSearchForm" class="library-search"><label for="siteQuery">Search</label><input id="siteQuery" type="search" name="q" placeholder="For example: plywood, LightBurn, smoke"/></form><p id="searchCount" class="result-count" role="status"></p><ul class="directory" id="searchResults"></ul><noscript>Use the navigation menus to browse all project, tutorial, material, support, and troubleshooting pages.</noscript></section></main><script type="application/json" id="searchData">{data}</script></body></html>')


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
