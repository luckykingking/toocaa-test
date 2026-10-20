# TOOCAA Guides

Static, customer-facing laser project, tutorial, material, support and troubleshooting guides.
GitHub Pages serves `main` from `/docs` at https://luckykingking.github.io/toocaa-test/.

## Content

The 109 indexable pages include the home page, seven section hubs, seven use-case guides,
ten material guides, nineteen tutorial articles, seven support articles, two software
guides, four audience guides and fifty-two
troubleshooting articles. Search and the SEO inventory are `noindex,follow` and are
excluded from the sitemap.

Edit `content/pages.py`, `content/troubleshooting_additions.py` and
`content/tutorial_additions.py` and `content/framework_additions.py` for article content and `scripts/build_site.py` for hubs,
navigation and HTML. Shared presentation and behavior live in `docs/assets/site.css`
and `docs/assets/site.js`. The output is static HTML; JavaScript is used only for
menus, filtering, local search, the settings lookup and drafting support notes.

```powershell
python scripts/build_site.py
python scripts/validate_site.py
python scripts/validate_requirements.py
node --check docs/assets/site.js
python -m http.server 9040 --directory docs
```

Open http://localhost:9040/ for local navigation. Building needs Python 3.12 or newer
and no third-party dependencies. GitHub Actions checks the full site and verifies
that generated output has been committed.

## Sources and assets

`content/sources.json` records official references and their review date.
`content/settings.json` contains published TOOCAA L2 sample rows with explicit module,
thickness, operation and speed units. The lookup matches those rows; it never
interpolates unsupported combinations or transfers L2 settings to NOVA.

`content/images.json` records original TOOCAA image URLs. Images are stored locally
for reliable loading. Run `python scripts/fetch_assets.py` only when refreshing the
approved assets. Check the images visually after a source refresh.

The shared header follows the current TOOCAA store navigation. Tutorials, material
guides and use cases live under Learn; troubleshooting and maintenance live under
Support. Store, account, cart, Studio, Space, manuals and policy links go to the
real TOOCAA services. They are not simulated locally. The observed Inter Tight
font and Lucide icons are local assets with their licenses. The comparison and
REA evidence references are recorded in `content/official-site-review.md`.

## SEO inventory

The build exports `docs/keyword-table/site-seo-inventory.csv` with each public page's
TDK, H1, canonical, indexing directive and reference URLs. The review page is at
`/keyword-table/`. Original wood keyword CSV/XLSX files are retained as historical
research. Their volume and keyword-ownership fields are not a current crawl.

The validator checks every route, internal link and fragment, image path, unique
title and description, JSON-LD, canonical, homepage reachability, sitemap and CSV
agreement. It does not claim that metadata alone guarantees indexing or rankings.

## Supplied briefs and delivery

`content/briefs/` preserves the supplied troubleshooting and tutorial HTML.
`content/requirements.json` maps the original 80 HTML/screenshot items plus the 29
contract framework/article entries. The original group contains 51 troubleshooting
topics, 22 tutorial resources and seven application scenarios. Source hashes normalize CRLF
to LF so Git's line-ending conversion does not change the audit result. Rebuild
the manifest with `python scripts/import_requirements.py`.

Sixteen tutorial resources remain links to existing official TOOCAA articles.
`python scripts/check_references.py` refreshes their HTTP and article-heading
evidence in `content/reference-checks.json`. The original accessories-selection
article contained placeholder copy, so `content/requirement-overrides.json`
explicitly maps that item to the completed local accessories guide instead.

`docs/keyword-table/delivery-checklist.csv` covers every original requirement and
includes its delivery URL, metadata, applicability, source references and scope
notes. The SEO inventory covers all 109 public pages. Passing validation proves
content and navigation coverage, not manufacturer approval or physical machine
testing. This repository publishes the GitHub Pages review site, not the official
TOOCAA storefront; production import requires updating the base URL and reviewing
device-specific instructions with TOOCAA.

`content/generated-images.json` records the two AI illustration prompts and
provenance. Both illustrations are labeled as concepts, not real customer work or
machine-test results. Maintenance photographs are sourced from the matching
official NOVA guides and recorded in `content/images.json`.

The supplied scope workbook is authoritative for the seven content families:
Use Cases (7 articles), Tutorials (framework; client-authored articles), Materials
(7 articles), Support (2 articles), Troubleshooting (framework; client-authored
articles), Software (2 articles), Who It's For (4 articles). These are 7 frameworks
and 22 specified articles, not a promise to substitute a large article count for
complete section pages. The extra tutorial and troubleshooting content remains
separately identified in the delivery export.

`content/contract-requirements.json` preserves this table's cells, tasks and route
mapping without publishing the private workbook. Refresh it only from the supplied
workbook with `python scripts/import_contract.py --source <workbook-path>`.
`docs/keyword-table/contract-delivery.csv` is the contract-only handoff (29 rows),
including TDK and the original sheet/cell references. Framework work follows the
approved wood-guide structure (`aabc2ba`) and seven-scenario use-case structure
(`7c426e9`) while keeping the current official-site-aligned header and colors.
