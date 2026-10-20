# TOOCAA Guides

Static, customer-facing laser project, tutorial, material, support and troubleshooting guides.
GitHub Pages serves `main` from `/docs` at https://luckykingking.github.io/toocaa-test/.

## Content

The 60 indexable pages include the home page, five section hubs, seven use-case guides,
nine material guides, seventeen tutorial articles, five support articles and sixteen
troubleshooting articles. Search and the SEO inventory are `noindex,follow` and are
excluded from the sitemap.

Edit `content/pages.py` for article content and `scripts/build_site.py` for hubs,
navigation and HTML. Shared presentation and behavior live in `docs/assets/site.css`
and `docs/assets/site.js`. The output is static HTML; JavaScript is used only for
menus, filtering, local search, the settings lookup and drafting support notes.

```powershell
python scripts/build_site.py
python scripts/validate_site.py
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

## SEO inventory

The build exports `docs/keyword-table/site-seo-inventory.csv` with each public page's
TDK, H1, canonical, indexing directive and reference URLs. The review page is at
`/keyword-table/`. Original wood keyword CSV/XLSX files are retained as historical
research. Their volume and keyword-ownership fields are not a current crawl.

The validator checks every route, internal link and fragment, image path, unique
title and description, JSON-LD, canonical, homepage reachability, sitemap and CSV
agreement. It does not claim that metadata alone guarantees indexing or rankings.
