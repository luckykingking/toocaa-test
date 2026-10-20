# TOOCAA customer-site alignment

Reviewed on 2026-10-20. This is an internal implementation record, not customer copy.

## Observed references

- https://www.toocaa.com/
- https://www.toocaa.com/pages/help-center-for-toocaa
- https://www.toocaa.com/pages/help-me-choose
- https://www.toocaa.com/pages/toocaa-studio

REA controlled Chrome captures (1440 x 1000, accessibility and URL):

- Homepage: `ev_286e6729233bb2b2bc756e685ae4152afb78fcadbda505422d08e45e8e710c24`
- Help Center: `ev_9e3180737f3f02e85e01e828f255514a5fc2ee9bd052dbeb306ffd991e8ef62a`

Both final captures completed and their owned browser processes were terminated.
An earlier homepage capture with DOM and screenshot returned a cleanup timeout;
cleanup was not confirmed for that attempt. Its partial observations are not used
as complete evidence. The later accessibility-only captures completed normally.

Playwright DOM/computed-style inspection additionally established the current
menu destinations, asset URLs, #ff6a00 brand color, Inter Tight variable font,
white backgrounds, 600-weight headings and 5px primary-button corners.
Only the current pages were observed; no checkout, account, submission, device
control, customer account, or historical behavior was tested.

## Observed navigation

Products / TOOCAA Space / TOOCAA Studio / Learn / Support / Help Me Choose /
About TOOCAA. The original guide site's five content groups were siblings in
the primary navigation; the new header keeps the live site's top-level order.
The guide routes are integrated under Learn and Support, with a secondary
section navigation. Product, account and cart links open the real TOOCAA store;
there is no local cart, simulated login or fake item count.

The live Learn menu's Tutorials destination was the store homepage during this
review. This project deliberately links Tutorials to its working local library,
rather than reproducing that destination. The live Support menu links to
https://wiki.toocaa.com/en/home; the older Help Center page exposed only its
heading in the captured main region. The wiki is now the manuals/help link.

## Applied decisions

- Keep the existing 60 indexable routes; do not replace product sales pages.
- Make the homepage a searchable Learning Center for existing customers.
- Preserve tutorial filters, site search, material lookup and local support notes.
- Use actual NOVA/L2 images and product links observed in the current store menu.
- Use short, customer-facing explanations instead of implementation/audit copy.
- Keep machine-specific settings and safety limits visible in relevant articles.
- Move article sources into expandable manual/reference lists, rather than
  repeating large audit sections across all customer pages.
- Retain all 17 L2 settings rows unchanged. No transfer to NOVA, calculated
  interpolation, or new unsupported power/speed claims.
- Do not mirror prices, shipping promises, sales promotions, response-time
  promises, newsletter forms or region selectors without their real backend.
- Store original images, the observed font and Lucide icons locally with
  third-party licenses. Asset URLs are in content/images.json and
  scripts/fetch_assets.py.
- Regenerate the TDK export from actual HTML metadata; keyword ownership remains
  a historical research field, not a new claim about current search rankings.

## Verification

- 62 index routes, 60 indexable pages, 60 sitemap entries and 60 metadata rows
  pass the static validator. All 60 are reachable from the homepage.
- All 60 public pages render at 1440px and 390px: 120 checks, no missing images,
  horizontal overflow, blank main content, clipped headings/buttons or JS errors.
- Six main page types also checked at 768px; screenshots inspected on desktop
  and mobile. NOVA and L2 image files were opened and visually identified.
- 20 interaction checks cover hover/keyboard/mobile navigation, Escape, submenu
  links, tutorial filters and empty states, header/home search, result navigation,
  anchor clearance, exact/no-match settings, FAQ, local support notes and CSV.
- 33 unique external content destinations checked. 32 returned HTTP 200 via
  Python. TOOCAA Space encountered a local Python certificate-chain error, then
  loaded normally in Chrome with HTTP 200 (locale redirect to /zh).
- No checkout, account sign-in, hardware control or support submission tested.
