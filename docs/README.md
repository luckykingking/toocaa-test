# TOOCAA Content Hub Prototype (English)

This folder is a static HTML prototype that demonstrates the proposed content planning for TOOCAA:
- Support entry (Before/After/Troubleshooting/Contact)
- Use Cases (scenario pages)
- Tutorials (HowTo pages)
- Materials & Settings (table-driven growth)
- SSOT governance (Link Pool)
- Roadmap (1-year plan)

## How to view
Open `index.html` directly, or run a local server for nicer routing:
```bash
python -m http.server 8080
```
Then open:
http://localhost:8080/index.html

## Key example page
- Use Case (full): `/use-cases/studio-pro-crafts/`

## External links
Pages link to the current TOOCAA site:
- Help Center: https://www.toocaa.com/pages/help-center-for-toocaa
- Contact: https://www.toocaa.com/pages/contact
- Product L2: https://www.toocaa.com/products/toocaa-l2-laser-engraver-cutter
- L2 40W module: https://www.toocaa.com/products/toocaa-l2-40w-diode-laser-module
- Air assist (L2): https://www.toocaa.com/products/toocaa-air-assist-kit-for-l2
- Honeycomb panel: https://www.toocaa.com/products/toocaa-laser-cutting-engraving-400mm-400mm-honeycomb-working-panel

## Notes for Shopify implementation
- Each folder here maps to a Shopify Page with a matching handle (or a custom route via theme templates).
- Keep SSOT rules: one canonical URL per topic, and redirect/noindex duplicates.
- For GEO visibility: keep TL;DR + steps + tables + FAQ blocks and add internal links.

Generated: 2026-03-04
