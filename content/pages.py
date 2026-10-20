"""Customer-facing guide copy. Numeric settings live separately from editorial content."""

PAGES = []


def page(path, title, description, group, sections, *, keywords="", faqs=(), related=(), sources=("settings", "manual"), image=None, label=None):
    item = dict(path=path, title=title, description=description, group=group, sections=sections,
                keywords=keywords, faqs=faqs, related=related, sources=sources, image=image, label=label or title)
    PAGES.append(item)
    return item


def section(title, text, bullets=(), anchor=None):
    return dict(title=title, text=text, bullets=bullets, anchor=anchor)


MATERIALS = [
    ("wood", "Wood", "wood laser cutting, laser engrave wood, plywood laser settings",
     "Choose wood for boxes, signs, and gifts. Find L2 cutting and engraving settings, plus tips for preparing and testing your sheet.",
     "Basswood gives pale engraving backgrounds; birch plywood suits assembled parts; walnut and cherry provide a darker decorative finish. Grain, glue, moisture, and surface treatments change the outcome even when two boards have the same nominal thickness.",
     "Check the sheet is flat, identify the wood and adhesive, and measure the actual thickness. Select laser-compatible stock with information from its supplier. A decorative veneer or treated board needs separate checking from solid unfinished wood.",
     "A dark face usually calls for checking smoke extraction, flatness, focus, and excessive dwell. If one area stays attached, inspect the board for voids or glue pockets instead of repeatedly burning the same spot.",
     ["Cut a small square and an internal circle before a detailed design.", "Engrave a small text sample across the grain and compare its contrast.", "Measure a slot and tab pair after cutting to account for kerf.", "Save the sheet supplier, thickness, module, speed units, and result."],
     "wood", ["use-cases/home-decor/", "tutorials/material-test/", "troubleshooting/not-cutting-through/"]),
    ("acrylic", "Acrylic", "acrylic laser cutting, diode laser acrylic, acrylic engraving settings",
     "Choose acrylic for your laser, find L2 black acrylic settings, and prepare a small test for jewelry, signs, and decorative pieces.",
     "Acrylic response depends on color, transparency, thickness, and laser wavelength. A dark acrylic example in a diode laser table does not establish that clear, blue, white, or mirrored acrylic will behave the same way. Confirm the exact sheet is suitable for your module before buying a large batch.",
     "Ask for the material identity and laser suitability rather than relying on the name 'plastic.' Check masking and backing as well as the sheet itself. Never substitute PVC, vinyl, or an unidentified plastic for acrylic.",
     "Melting, a cloudy edge, or a shallow mark can have different causes. Verify compatibility and focus first; then test a small piece using a row that matches the machine and material. Record each change and avoid repeated passes on a visibly overheating sample.",
     ["Confirm the sheet is acrylic and suitable for the laser wavelength.", "Test an offcut of the actual color and thickness.", "Check both the front and underside after the sample cools.", "Measure holes and slots before nesting jewelry or sign components."],
     "workspace", ["use-cases/jewelry/", "tutorials/acrylic-cutting/", "use-cases/qr-code-signage/"]),
    ("leather", "Leather", "laser cutting leather, laser engraving leather, leather tags",
     "Prepare leather tags and engraved accessories with material checks, test pieces, and a repeatable finishing workflow.",
     "Leather can be used for tags, labels, patches, and accessories, but tanning methods, dyes, finishes, and synthetic layers matter. A natural appearance does not prove that a sheet is suitable for laser processing. Identify its composition and obtain the supplier's laser guidance first.",
     "Check the hide or sheet for coatings, synthetic backing, adhesive, and treatment. Do not laser-process PVC-based imitation leather or unknown composites. Choose a small offcut from the same batch and arrange extraction before the test.",
     "Fine text can lose definition when the surface scorches, while cut edges can deposit residue. Start with simple lettering, inspect the mark after cleaning, and check that the finished piece does not transfer residue onto fabric or skin.",
     ["Confirm composition and laser suitability with the supplier.", "Hold the offcut flat without putting fixtures in the beam path.", "Test text, a hole, and a short outline separately.", "Check cleaning and finish compatibility before making the full batch."],
     "leather", ["use-cases/personalized-gifts/", "tutorials/leather-cutting/", "use-cases/professional-studio-crafts/"]),
    ("metal", "Metal", "laser marking metal, anodized aluminum engraving, diode metal engraving",
     "Understand metal marking limits, distinguish surface marking from cutting, and prepare a model-specific test.",
     "Surface marking, removing a coating, and cutting metal are different jobs. A desktop diode laser marking example is not evidence that it can cut sheet metal. Match the metal, coating, laser module, and intended process to the manufacturer's documentation.",
     "Identify whether the workpiece is bare metal, painted, coated, or anodized. Check any marking product separately and follow its supplier's instructions. Reflective surfaces and unknown coatings need a material-specific assessment before exposure to the beam.",
     "A mark that looks dark under one light may have weak contrast or poor wear resistance under another. Inspect the result after cleaning and under normal use conditions. Do not increase exposure indefinitely when a material is outside the machine's supported process.",
     ["Verify that the documented operation is marking or engraving, not cutting.", "Use a matching surface and coating for the sample.", "Compare small text and filled areas after cleaning.", "Keep the protective enclosure and other safeguards in place."],
     "metal", ["tutorials/metal-marking/", "use-cases/personalized-gifts/", "support/before-you-buy/"]),
    ("glass", "Glass", "laser engraving glass, diode laser glass, glass engraving preparation",
     "Review glass engraving constraints, surface preparation, artwork choices, and inspection before attempting a glass project.",
     "Glass is an engraving topic, not a general cutting material for the desktop diode workflows in this guide. Its response depends on the glass, surface preparation, laser system, and workholding. A coating or preparation method must be specifically approved for the process rather than improvised from an unrelated tutorial.",
     "Identify the glass type and ask the manufacturer about suitability. Exclude cracked, chipped, unknown, or valuable pieces from first tests. If a rotary is required, confirm the accessory is compatible with the machine and supports the object's shape and weight.",
     "Surface chips, uneven marks, and fine cracks are reasons to stop and reassess the process. Inspect an inexpensive sample under good light. Laser processing can change the surface; do not assume that a decorated food-contact area remains suitable for its original purpose.",
     ["Confirm the manufacturer documents the glass engraving workflow.", "Use a simple test image on an inexpensive blank.", "Check fixture clearance and rotation before enabling the job.", "Inspect the cooled result for chips and cracks before handling."],
     "workspace", ["tutorials/rotary-engraving/", "tutorials/irregular-shapes/", "support/contact/"]),
    ("paper", "Paper", "laser cut paper, paper laser cutting, cardstock laser projects",
     "Set up laser-cut cards and paper details with careful material selection, secure workholding, and small test designs.",
     "Plain paper and cardstock are useful for folded cards, invitations, stencils, and packaging prototypes. Foils, glitter, laminates, coatings, and adhesive layers can change both the result and suitability. Verify the complete construction rather than treating every decorative paper as plain cardstock.",
     "Keep sheets flat and prevent movement from airflow. Choose a design with enough bridges to hold delicate details together. Remove scraps from the bed and confirm extraction before testing; paper is combustible and needs continuous attendance during processing.",
     "Overlapping vectors can cut the same line more than once. Check the artwork for duplicate paths and tiny loose islands before changing settings. Brown edges, lifting corners, and disappearing details need attention to dwell, support, and design size.",
     ["Check coatings and adhesive with the supplier.", "Test a short straight cut and a small curve.", "Review the underside and fragile details after cutting.", "Make a full-scale fold test before committing to printed stock."],
     "workspace", ["tutorials/paper-cutting/", "use-cases/gift-box-packaging/", "learn/materials/cardboard/"]),
    ("stone", "Stone", "laser engraving slate, stone laser engraving, engraved stone coasters",
     "Prepare slate and stone engraving tests, choose legible artwork, and compare surface contrast before engraving a finished piece.",
     "Slate and other stone surfaces can produce useful engraved marks, but mineral composition, texture, sealant, and natural variation affect contrast. Choose engraving blanks with a known surface and test the same material as the final piece.",
     "Check the blank for unstable layers, cracks, and coatings. Support it so that the top surface stays level. A rough or curved surface can move out of focus across the image even when its center is positioned correctly.",
     "Small gray details in a photograph may disappear on textured stone. Begin with text or a simple high-contrast graphic and compare it with a small image sample. Inspect after cleaning before deciding whether any finish is appropriate for the item.",
     ["Use an inexpensive blank from the same batch.", "Level the engraving area and set focus to that surface.", "Compare simple line art with a filled sample.", "Keep a reference photo and the file used for each test."],
     "stone", ["tutorials/stone-engraving/", "tutorials/photo-preparation/", "use-cases/home-decor/"]),
    ("fabric", "Fabric", "laser cutting fabric, laser cut felt, fabric laser cutting preparation",
     "Check textile composition and finishing treatments before testing felt, fabric labels, appliques, or patterns with a desktop laser.",
     "Fabric is not one material. Fiber composition, dyes, flame-retardant treatments, adhesive backing, and surface coatings all matter. A felt example in a settings table should not be applied automatically to an unidentified textile or synthetic blend.",
     "Get composition and processing information from the supplier. Start with a flat scrap from the same roll and keep layers from shifting. Avoid unknown synthetic materials, vinyl layers, and products whose coating or adhesive cannot be identified.",
     "A cut that looks acceptable while hot may leave a stiff edge or weak fibers. Inspect after cooling, flex the sample, and check the intended sewing or bonding step. Continuous attendance and effective extraction are essential for combustible textiles.",
     ["Identify every fiber, coating, and backing layer.", "Test a single layer before a stacked layout.", "Check flexibility, residue, and dimensional change after cooling.", "Include a sewing or bonding test for the finished use."],
     "workspace", ["use-cases/professional-studio-crafts/", "tutorials/material-test/", "tutorials/laser-safety/"]),
    ("cardboard", "Cardboard", "laser cut cardboard, cardboard packaging prototype, corrugated laser cutting",
     "Prototype cardboard packaging and inserts with clear folds, measured slots, and fire-conscious cutting preparation.",
     "Cardboard is useful for testing box size, insert fit, and assembly before moving to more expensive stock. Solid board and corrugated board behave differently, and printed surfaces, adhesives, and laminates must be checked individually.",
     "Measure the board's actual thickness and note the direction of corrugation. Build an early version without a valuable item inside it. Keep loose scraps clear and watch the job continuously because cardboard can ignite.",
     "A folded prototype can fail even when the outline cuts correctly. Check fold direction, compressed edges, slot allowance, and the order of assembly. Distinguish a visual packaging mockup from packaging that has been tested to protect a shipped product.",
     ["Identify the board and any surface treatment.", "Cut a small tab, slot, and fold sample.", "Assemble an unprinted prototype at full size.", "Test the fit separately from load-bearing or shipping claims."],
     "workspace", ["use-cases/gift-box-packaging/", "tutorials/paper-cutting/", "learn/materials/paper/"])
]

for slug, name, kw, intro, choice, preparation, quality, steps, image, related in MATERIALS:
    material_title = {"glass": "Glass Laser Engraving: Compatibility & Preparation", "metal": "Metal Laser Marking: Surfaces & Preparation", "stone": "Stone & Slate Laser Engraving Guide"}.get(slug, f"{name} Laser Cutting & Engraving Guide")
    page(f"learn/materials/{slug}/", material_title, intro, "Materials", [
        section(f"Working with {name.lower()}", choice, anchor="material-selection"),
        section("Check the material before processing", preparation, anchor="safety"),
        section("Prepare a useful test", "A material test is useful only when it represents the final job. Use the same sheet or batch, record the laser module and software units, and change one setting at a time. Keep the sample after the job so you can compare a later delivery against it.", steps, "clean-workflow"),
        section("Inspect the result", quality),
        section("Choose settings for the exact machine", "Use the manufacturer's material table for the exact laser module and processing mode. Speed in mm/min is not the same as mm/s, and an engraving row is not a cutting instruction. If the material, thickness, or surface does not match a published entry, treat it as an undocumented combination and seek model-specific guidance before continuing.", anchor="settings-table")
    ], keywords=kw, image=image, related=related, sources=("stone", "settings") if slug == "stone" else ("settings", "manual"),
    faqs=[(f"Can every {name.lower()} product use the same laser settings?", "No. Composition, thickness, surface treatments, and the laser module change the result. Test the actual stock and use a matching manufacturer reference."),
          ("Should I increase power if the first test fails?", "Check compatibility, focus, workholding, and speed units first. Stop if the material overheats, produces unexpected fumes, or is not documented for the process.")])


USE_CASES = [
    ("professional-studio-crafts", "Studio & Crafts", "Laser Cutting for Craft Studios", "laser cutting crafts, small batch laser products, laser engraving studio",
     "Build repeatable craft collections, client samples, and small batches with material tests, reusable fixtures, and clear quality checks.",
     ["Branded leather labels", "Wood inlay samples", "Acrylic charms", "Paper product tags"],
     "Begin with one approved sample that records the artwork revision, material batch, dimensions, finish, and hardware. Ask the client to approve spelling and placement at the actual finished size. A repeat order should start from that record, rather than a photo of an earlier piece.",
     "Use a layout with room for workholding and a small batch identifier outside the finished parts. Keep a reference blank and a finished sample. When stock or artwork changes, check a small batch before filling the bed.",
     "Review the first, middle, and last pieces in a batch. Check edges, small text, dimensions, and assembly against the approved sample. Account for finishing and rework when deciding how many pieces to make.",
     ["wood", "acrylic", "leather", "paper"], "workspace"),
    ("personalized-gifts", "Personalized Gifts", "Personalized Laser Engraved Gifts", "personalized laser gifts, laser engraved names, custom engraved gifts",
     "Make engraved name tags, keepsakes, and small gift sets with legible artwork, confirmed personalization, and a consistent finish.",
     ["Named wooden keepsakes", "Leather luggage tags", "Engraved coasters", "Anniversary photo plaques"],
     "Confirm the exact name, date, punctuation, and message before preparing the file. View the design at the size it will appear on the object. Keep essential text away from holes, edges, handles, and heavily textured areas.",
     "Test on an inexpensive blank from the same batch. Use a fixture to hold the gift in a repeatable position. Run the framing check with the workpiece secured and compare the outline with the intended engraving area.",
     "Check every personalized item against the order, not against memory. Inspect readability after cleaning. Include any material-specific care information and check that packaging does not rub the engraved face.",
     ["wood", "leather", "stone", "metal"], "wood"),
    ("qr-code-signage", "QR Code Signs", "Laser Engraved QR Code Signs", "laser engraved QR code, QR code signs, laser cut business signs",
     "Create QR code signs for menus, product pages, and events with a working destination, readable contrast, and real scan tests.",
     ["Countertop menu signs", "Event information plaques", "Product care cards", "Small business display signs"],
     "Decide where the code will lead and verify that page before engraving. Keep the URL short where possible. Retain the quiet zone around the code and avoid stretching it, rounding its modules, or placing decoration inside it.",
     "Choose a flat surface that can produce a clear light-dark distinction. Test at the final physical size with the same finish and mounting angle. An attractive vector preview is not proof that the engraved code can be scanned.",
     "Scan the finished sign on several phones at the intended distance and under realistic lighting. Test again after cleaning, sealing, and mounting. Keep a text URL or another route to the destination when that helps visitors.",
     ["wood", "acrylic", "metal"], "workspace"),
    ("home-decor", "Home Decor", "Laser Cut Home Decor Projects", "laser cut home decor, laser cut wall art, wood laser ornaments",
     "Plan layered wall art, coasters, decorative panels, and ornaments with material selection, joinery tests, and practical finishing checks.",
     ["Layered wall art", "Engraved coaster sets", "Seasonal ornaments", "Decorative box panels"],
     "Choose the scale, mounting method, and viewing distance before drawing details. Fine bridges that look good on screen can be fragile at the finished size. Prototype one section before committing to a large sheet.",
     "Cut a slot and tab sample for assembled pieces. Number layers outside visible faces and verify the orientation before gluing. Keep mounting hardware, wiring, and heat sources separate from the decorative cutting plan.",
     "Inspect edges and check that small parts are secure. Match the finish to the intended environment. Decorative laser-cut panels are not automatically suitable as structural, electrical, food-contact, or heat-resistant components.",
     ["wood", "stone", "acrylic"], "wood"),
    ("jewelry", "Jewelry", "Laser Cut Jewelry: Earrings, Pendants & Charms", "laser cut jewelry, laser cut earrings, acrylic pendants, wood charms",
     "Design earrings, pendants, charms, and display cards with useful test pieces for weight, hole placement, edge finish, and hardware fit.",
     ["Wood earrings", "Compatible acrylic pendants", "Engraved wooden charms", "Jewelry display cards"],
     "Start with a shape that has enough material around the hardware hole. Compare the size and weight with an existing comfortable piece. Thin bridges and engraved details should be checked at full scale before nesting a batch.",
     "Cut a pair of samples, fit the actual findings, and inspect both faces after cleaning. Check acrylic compatibility by color and wavelength; clear acrylic is not interchangeable with the dark acrylic used in a diode settings table.",
     "Flex the sample gently at vulnerable areas and inspect for cracks around holes. Use suitable jewelry findings and finishes, and check the supplier's information for skin-contact components. Verify a matched pair after assembly, not just after cutting.",
     ["wood", "acrylic", "paper"], "wood"),
    ("gift-box-packaging", "Gift Packaging", "Laser Cut Gift Boxes & Packaging", "laser cut gift box, laser cut packaging, custom box inserts",
     "Prototype gift boxes, presentation inserts, sleeves, and tags with measured fits, simple assembly, and repeatable layouts.",
     ["Wood presentation boxes", "Cardboard inserts", "Branded hang tags", "Invitation sleeves"],
     "Measure the item and leave space for wrapping, hardware, and removal. Choose whether the package is a visual presentation piece or must protect an item during delivery. Those are different acceptance tests.",
     "Test tabs, slots, folds, and closures before cutting the complete box. Check the actual board thickness rather than a catalog value. For printed stock, verify registration on an inexpensive prototype before cutting a finished print.",
     "Assemble the full package and check access to the item, closing force, sharp edges, and any residue. Validate transport protection separately. Do not describe a decorative prototype as shipping protection without suitable testing.",
     ["wood", "cardboard", "paper"], "wood"),
    ("photo-engraving", "Photo Engraving", "Laser Photo Engraving on Wood & Acrylic", "laser photo engraving, photo engraving wood, dither laser photo",
     "Prepare portraits, pet photos, and keepsake plaques with careful cropping, small test engravings, and material-specific contrast checks.",
     ["Family photo plaques", "Pet portrait keepsakes", "Engraved wood portraits", "Small commemorative panels"],
     "Use a sharp original photo with useful detail around the eyes, hair, and subject outline. Crop for the final object before resizing. Simplify a distracting background and keep important features away from hardware or edges.",
     "Compare a small dithered image test on the actual material. A lighter photo on a screen does not guarantee a lighter engraved result, and wood grain can hide midtones. Keep a record of image edits separately from machine settings.",
     "Inspect from the normal viewing distance after cleaning. Avoid increasing resolution beyond what the material can resolve. Get approval for the final crop and contrast before engraving a valuable or irreplaceable item.",
     ["wood", "acrylic", "stone"], "workspace")
]

for slug, label, title, kw, intro, projects, planning, workflow, inspection, mats, image in USE_CASES:
    page(f"use-cases/{slug}/", title, intro, "Use Cases", [
        section("Project ideas", "Choose a small project that matches the available material and finishing process. These are design directions to prototype; the final quality comes from the artwork, stock, setup, and inspection together.", projects, "projects"),
        section("Prepare the design", planning, anchor="design"),
        section("Make and check a sample", workflow, ["Confirm the composition and laser compatibility of every layer.", "Use the machine's current documentation to check setup and speed units.", "Frame the job, run one sample, and inspect it before repeating.", "Record artwork revisions and material details with the approved result."], "workflow"),
        section("Quality checks before delivery", inspection, anchor="quality"),
        section("Choose a machine and material", "Match the work area, supported materials, accessories, ventilation arrangement, and software to the project. Cutting and engraving have different requirements. Current module options and accessory compatibility should be confirmed on TOOCAA's product pages before ordering.", anchor="products")
    ], keywords=kw, image=image, label=label,
    related=[f"learn/materials/{m}/" for m in mats] + ["tutorials/material-test/", "support/before-you-buy/"],
    faqs=[("Can I use one setting for every piece?", "Only after testing the exact material and setup. A different supplier, coating, thickness, or laser module can change the result; keep a reference sample and recheck new stock."),
          ("Where should I get power and speed settings?", "Use a documented row for the exact machine, laser module, material, and operation. Run a small test and record the result before using a full layout.")])


TUTORIALS = [
    ("first-setup", "Getting Started", "TOOCAA First Setup Checklist", "TOOCAA setup, laser engraver first setup", "Prepare a stable workspace, check the machine manual, arrange extraction, and run a small first job before starting a project.",
     "Workspace before assembly", "Set the machine on a stable, level surface with the clearances specified in its manual. Plan where smoke will be extracted and keep cables and the exhaust route clear of moving parts. The machine, laser module, and accessories should be identified before following assembly instructions.",
     ["Read the manual for the exact model and module.", "Check the delivered parts against the packing list and inspect for damage.", "Complete the documented assembly and ventilation setup with power disconnected.", "Install the supported software, then verify the connection and work area.", "Load a simple test file, frame it, and run it on a documented material."],
     "Before the first full project", "Check focus, workholding, framing, and the job's speed units. Stay at the machine while it runs. If motion, smoke extraction, or any safeguard does not work as documented, stop and resolve that issue before continuing.", ["manual", "support"], ["tutorials/laser-safety/", "tutorials/studio-setup/", "support/after-you-buy/"]),
    ("laser-safety", "Getting Started", "Laser Cutter Safety Before Every Job", "laser cutter safety, laser ventilation, laser material safety", "Check materials, ventilation, workholding, and protective safeguards before cutting or engraving with a desktop laser.",
     "Know what is going under the beam", "Identify the complete material, including coatings, adhesive, backing, and treatments. Do not process PVC, vinyl, unidentified plastics, or stock whose composition cannot be confirmed. A settings entry for one material does not approve a different material with a similar appearance.",
     ["Confirm the material is documented for the machine and process.", "Clear scraps and flammable clutter from the working area.", "Check extraction, the exhaust path, and any filters according to the manual.", "Use the supplied protective system and keep interlocks functional.", "Frame the job and stay present throughout processing."],
     "Know when to stop", "Stop the job for persistent flame, unusual odor, unexpected smoke leakage, loss of motion, or a safety warning. Use the machine's documented stop procedure. Do not bypass sensors or keep retrying a job with an unresolved safety fault.", ["manual", "support"], ["troubleshooting/excessive-smoke-odor/", "learn/materials/", "support/contact/"]),
    ("studio-setup", "Getting Started", "TOOCAA Studio Setup & Machine Connection", "TOOCAA Studio setup, TOOCAA software download", "Find the official TOOCAA Studio download, match the supported machine and operating system, and check the first connection.",
     "Use the current official download", "Open TOOCAA's software page and confirm the release supports your operating system and model. Keep a note of the version you install. Follow the connection method described for the machine; USB, network features, and accessory support are not interchangeable across models.",
     ["Download from the official TOOCAA software page.", "Follow the model-specific installation and connection instructions.", "Connect a known data cable when using a wired connection.", "Select the correct machine profile and confirm work-area orientation.", "Import a simple file and check its dimensions before framing."],
     "Check the result before running", "Make sure the artwork size, origin, enabled layers, and speed units match the intended job. If the machine is missing from the device list, close other control software and work through the connection guide before sending another command.", ["studio", "support"], ["tutorials/lightburn-setup/", "troubleshooting/usb-not-connecting/", "tutorials/first-engraving/"]),
    ("first-engraving", "Getting Started", "Your First Laser Engraving Project", "first laser engraving project, beginner laser engraving", "Start with a simple design and a documented material, then check focus, layout, and a small engraving before the final job.",
     "Keep the first file simple", "A short line of text and a simple shape are enough to check size, position, and contrast. Use an inexpensive blank with a known composition. Avoid a complex photo, valuable object, or a crowded batch until the basic workflow is repeatable.",
     ["Choose a manufacturer-documented engraving material.", "Import a small design and confirm its physical size.", "Set focus and secure the blank without blocking machine travel.", "Choose a matching reference row and verify speed units.", "Frame, run a small test, and inspect after the job has stopped."],
     "Make the second test informative", "Change one variable and keep the original sample beside the next result. Record power, speed, passes, material, and module. A clean second test is more useful than a full sheet of guesses because you can tell which change affected the mark.", ["manual", "settings"], ["tutorials/material-test/", "tutorials/focus-positioning/", "use-cases/personalized-gifts/"]),
    ("focus-positioning", "Getting Started", "Laser Focus & Workpiece Positioning", "laser focus, laser engraving positioning, frame laser job", "Check surface height, workholding, origin, and framing before a laser job to reduce placement errors and uneven marks.",
     "Focus follows the actual surface", "Use the focus method specified for the installed module. A bowed sheet, raised corner, curved object, or uneven support can change the distance across the artwork. Setting focus once at the center will not correct a workpiece that moves or slopes during the job.",
     ["Make the workpiece flat and stable within the travel area.", "Set focus with the method documented for the module.", "Confirm the artwork dimensions and software origin.", "Run the documented framing or positioning check.", "Recheck clearance around clamps and the full outline."],
     "Repeatable positioning", "A simple fixture can make repeated placement easier, but the fixture itself must be safe and outside the processing area. Keep a marked reference edge and reframe after changing the object or file. Use model-specific instructions for any camera or autofocus calibration.", ["manual", "support"], ["tutorials/irregular-shapes/", "troubleshooting/engraving-misalignment/", "tutorials/first-engraving/"]),
    ("acrylic-cutting", "Cutting", "Acrylic Cutting With a Diode Laser", "diode acrylic cutting, acrylic cutting settings", "Check acrylic compatibility, select a matching published setting, and inspect a small cut before making signs or jewelry.",
     "Color and wavelength matter", "Transparent or pale acrylic can behave very differently from dark acrylic under a diode laser. Start by checking the machine's documented material compatibility. Do not rely on a tutorial for a different laser technology or assume a color change is only cosmetic.",
     ["Confirm that the sheet is acrylic and suitable for the laser wavelength.", "Identify thickness, surface masking, and any backing.", "Choose a documented row for the installed module and material.", "Frame a small sample with extraction operating.", "Inspect the cooled edge, underside, and dimensions."],
     "A useful quality check", "Compare a straight edge, a small hole, and a corner. If the sample melts or fails to separate, stop and check compatibility, focus, and support before increasing exposure. Save the settings alongside the exact color and supplier of the acrylic.", ["settings", "faq"], ["learn/materials/acrylic/", "use-cases/jewelry/", "troubleshooting/not-cutting-through/"]),
    ("leather-cutting", "Cutting", "Leather Cutting & Engraving Preparation", "laser cut leather tags, leather engraving workflow", "Identify leather composition, test a small piece, and check the finished edge before making labels, tags, or accessories.",
     "Identify the complete sheet", "Tanning, surface finish, dye, adhesive, and synthetic backing affect laser suitability. Confirm them with the supplier. Do not laser-process PVC-based imitation leather or unknown composites, even if a previous material with a similar color worked.",
     ["Confirm composition and laser suitability before the job.", "Hold a scrap from the same batch flat in the work area.", "Test a short line of text and a small outline separately.", "Inspect the cooled surface and clean it with a suitable method.", "Check residue, flexibility, and hardware fit before production."],
     "Build a repeatable tag", "Keep text legible at the final size, leave enough material around holes, and test the actual fastener. Finishing changes can affect color and feel, so inspect after the full finishing process rather than approving an uncleaned test piece.", ["settings", "manual"], ["learn/materials/leather/", "use-cases/personalized-gifts/", "tutorials/material-test/"]),
    ("paper-cutting", "Cutting", "Laser Cutting Paper & Cardboard", "paper laser cutting tutorial, cardboard laser cutting", "Prepare flat stock, clean vectors, and a small fold or slot test for cards, stencils, and packaging prototypes.",
     "Prepare the file and the sheet together", "Paper details need enough bridges to hold together at the chosen size. Check duplicate vectors, tiny islands, and the order of operations before changing machine settings. Plain cardstock is not interchangeable with laminated, foil-backed, or adhesive stock.",
     ["Verify the complete paper or board composition.", "Clear scraps and secure the sheet against movement.", "Check duplicate lines and small loose details in the file.", "Test a curve, straight cut, and any fold or slot.", "Stay present and inspect the top and underside after cutting."],
     "Check the assembled result", "A packaging outline is only useful when it folds and fits correctly. Measure the actual board thickness, assemble an inexpensive full-scale prototype, and check closure and removal of the item. Fire risk and airflow need attention even on a short paper job.", ["manual", "settings"], ["learn/materials/paper/", "learn/materials/cardboard/", "use-cases/gift-box-packaging/"]),
    ("stone-engraving", "Engraving", "Stone & Slate Engraving Preparation", "slate engraving tutorial, stone laser engraving preparation", "Level a stone blank, prepare high-contrast artwork, and compare a small engraving before making coasters or keepsakes.",
     "Start with a known blank", "Stone varies in mineral composition, flatness, texture, and sealant. Use an inexpensive blank from the same batch as the final piece. A rough or curved surface may be out of focus across part of the image, even if the central area is correct.",
     ["Identify the stone and check for coatings, cracks, and loose layers.", "Support the blank level and set focus to the engraving surface.", "Prepare simple text or high-contrast artwork.", "Run a small test using model-specific guidance.", "Clean and inspect the result before considering a finish."],
     "Choose detail the surface can show", "Start with bold text or line art before testing a photograph. Compare the result at the intended viewing distance. Texture can hide subtle gray detail; increasing image resolution alone will not create contrast that the material cannot produce.", ["stone", "settings"], ["learn/materials/stone/", "tutorials/photo-preparation/", "use-cases/home-decor/"]),
    ("irregular-shapes", "Engraving", "Positioning Irregular Shapes for Engraving", "engrave irregular shapes, laser engraving jig", "Use stable support, verified clearance, and small placement tests when engraving an object with an uneven or curved shape.",
     "Separate support from image distortion", "A fixture can hold an object still, but it does not flatten a curved engraving surface. Check how much the surface height varies across the artwork. Keep the first design small enough to sit within a suitable focus area and check the machine's documented clearance.",
     ["Identify a stable face and a repeatable reference edge.", "Support the object without placing clamps in the travel path.", "Confirm focus across the intended engraving area.", "Frame the job and inspect the complete motion clearance.", "Test on an inexpensive matching object before the final piece."],
     "When a rotary is needed", "Use an accessory only if it is documented for the exact machine and object. Check weight, dimensions, clearance, and cable routing. Follow its setup procedure and restore the normal device configuration after the rotary job.", ["manual", "rotary"], ["tutorials/rotary-engraving/", "tutorials/focus-positioning/", "troubleshooting/engraving-misalignment/"]),
    ("photo-preparation", "Engraving", "Prepare a Photo for Laser Engraving", "laser photo preparation, photo engraving dithering", "Crop and resize a photo for the finished object, compare a small dither test, and preserve the settings used for the approved image.",
     "Choose a useful original", "Start with a sharp photo that retains detail around the subject's eyes and outline. Crop it to the final object's proportions before resizing. Keep the untouched source file so you can return to it when a contrast or sharpening change removes detail.",
     ["Crop for the final physical dimensions.", "Reduce distracting background detail when appropriate.", "Compare grayscale and a suitable dither preview.", "Engrave a small section on the actual material.", "Evaluate after cleaning at the intended viewing distance."],
     "Keep image edits separate from machine settings", "If a test is too dark, first identify whether lost detail came from the file or the exposure. Change one factor at a time. Save the original photo, edited file, software processing mode, material, and machine settings with the approved sample.", ["manual", "settings"], ["use-cases/photo-engraving/", "learn/materials/wood/", "learn/materials/stone/"]),
    ("complex-designs", "Engraving", "Prepare Detailed Cutting & Engraving Files", "laser detailed designs, laser cut engrave layer order", "Check duplicate paths, small features, layer order, and registration before running a detailed cut-and-engrave project.",
     "Inspect the artwork at finished size", "A large screen preview can hide details that will be too fragile or too small to engrave. Check text, bridges, closed paths, and duplicated vectors at the intended size. Keep a separate editable source and an exported machine file.",
     ["Confirm dimensions and remove duplicate paths.", "Separate engraving, scoring, and cutting operations.", "Preview the operation order and inspect travel.", "Test the smallest important feature on matching stock.", "Keep the workpiece supported until critical operations finish."],
     "Check registration and assembly", "Parts that align on screen can fit differently after material is removed. Test slots, tabs, and layered registration marks before cutting the whole layout. Label hidden faces and keep the artwork version with the approved assembly.", ["manual", "lightburn"], ["use-cases/professional-studio-crafts/", "use-cases/gift-box-packaging/", "tutorials/material-test/"]),
    ("metal-marking", "Engraving", "Prepare a Metal Marking Test", "laser metal marking test, anodized aluminum laser", "Distinguish marking from cutting, confirm surface compatibility, and evaluate a small metal marking sample after cleaning.",
     "Identify the surface operation", "Removing a coating and marking bare metal are different processes. Check the exact metal, coating, laser module, and any approved marking product. A desktop diode marking example does not establish metal cutting capability.",
     ["Confirm a documented process for the metal and module.", "Identify coatings and follow any approved preparation instructions.", "Keep protective safeguards in place around reflective objects.", "Test small text and a filled patch on a matching sample.", "Inspect the cleaned result under ordinary lighting."],
     "Decide what a successful mark means", "A dark sample may not have the wear resistance or contrast a finished product needs. Compare readability after cleaning and normal handling. If the manufacturer does not document the material-process combination, seek guidance rather than escalating exposure.", ["settings", "support"], ["learn/materials/metal/", "use-cases/personalized-gifts/", "support/contact/"]),
    ("material-test", "Materials", "Run a Laser Material Test & Keep a Settings Log", "laser material test, laser speed power test grid", "Use a small, controlled test to compare power and speed, then keep a clear record for the exact machine and material.",
     "Start from a matching reference", "Record the machine, module, material identity, actual thickness, operation, focus method, and speed units. Begin with manufacturer guidance that matches those details. A cutting table for a different laser module is not a formula for converting settings.",
     ["Choose a small sample from the actual batch.", "Check focus, extraction, and workholding.", "Create a limited test with clearly labeled variations.", "Change one factor at a time and watch the process.", "Inspect after cooling and save the sample with the result."],
     "Record why the sample passed", "For cutting, check separation, edge quality, and dimensions. For engraving, compare readability and contrast after cleaning. Record failures as well as successes so a later operator knows which combinations were rejected. Recheck after changing stock or servicing the machine.", ["settings", "manual"], ["learn/materials/wood/#settings-calculator", "learn/materials/", "support/maintenance/"]),
    ("studio-design", "Software", "Prepare a Project in TOOCAA Studio", "TOOCAA Studio design, prepare laser file", "Prepare artwork at its finished size, choose the correct machine, and check the planned job before sending it from TOOCAA Studio.",
     "Match the workspace to the machine", "Use a current supported software release and the correct device profile. Confirm the model and laser module before applying material guidance. Product features and connection methods can change; the official software page is the reference for current support.",
     ["Open or import the artwork and check its dimensions.", "Separate engraving and cutting operations.", "Select the connected machine and appropriate processing mode.", "Verify speed units, enabled layers, and placement.", "Frame and test before running the final design."],
     "Keep a production copy", "Save a working source and an exported version associated with the sample. Keep personalization fields easy to review and name files clearly. When a project is reopened on a different computer or software release, verify its settings before sending it to the machine.", ["studio", "support"], ["tutorials/studio-setup/", "tutorials/material-test/", "use-cases/professional-studio-crafts/"]),
    ("lightburn-setup", "Software", "TOOCAA L2 LightBurn Setup & First Job", "TOOCAA L2 LightBurn setup, LightBurn laser connection", "Follow the official L2 setup guide, verify the device profile and units, and frame a small test before cutting or engraving.",
     "Use the model-specific device instructions", "Install the supported LightBurn release and follow TOOCAA's L2 setup guide. Verify the controller profile, work area, and origin against the current documentation. Do not copy an L2 configuration onto another machine because its name or work area looks similar.",
     ["Connect the machine with a known data cable.", "Close other software that may hold the device connection.", "Create or import the documented L2 device profile.", "Confirm work-area size, origin, speed units, and layer settings.", "Frame a small test file before starting the laser job."],
     "When connection or placement is wrong", "Check the selected device and port, cable, and any driver required by the official instructions. If the file is placed incorrectly, inspect origin and coordinate mode before altering the mechanics. Record software and firmware versions when requesting support.", ["lightburn", "manual"], ["troubleshooting/usb-not-connecting/", "troubleshooting/engraving-misalignment/", "tutorials/material-test/"]),
    ("rotary-engraving", "Advanced", "TOOCAA L2 5-in-1 Rotary Setup", "TOOCAA L2 rotary setup, tumbler laser engraving", "Check rotary compatibility, object support, clearance, and the official setup procedure before engraving a cylindrical workpiece.",
     "Confirm the accessory matches the job", "The referenced 5-in-1 rotary guide is for L2. Check compatibility with your installed machine and module before connecting hardware. An object's diameter, taper, handle, weight, and surface coating affect whether it can be supported and processed correctly.",
     ["Power down before connecting accessories as directed in the manual.", "Assemble the documented rotary configuration for the object.", "Secure and level a suitable test blank.", "Follow the guide's device and rotation setup checks.", "Run a small placement test and inspect before engraving the full wrap."],
     "Finish the accessory workflow", "Stop if the object slips, the drive stalls, or the surface moves out of focus. Keep settings for the accessory and normal flat-bed work separate, and restore the normal device configuration before the next non-rotary job.", ["rotary", "support"], ["tutorials/irregular-shapes/", "learn/materials/metal/", "troubleshooting/rotary-attachment-issues/"])
]

for slug, category, title, kw, intro, heading, context, steps, final_heading, conclusion, sources, related in TUTORIALS:
    page(f"tutorials/{slug}/", title, intro, "Tutorials", [
        section(heading, context, anchor="prepare"),
        section("Work through the job", "Use the following sequence with the current instructions for the exact machine. Keep the first job small enough to inspect clearly and leave time to check the result before repeating it.", steps, "workflow"),
        section(final_heading, conclusion, anchor="check-result"),
        section("Save the setup for the next job", "Keep the artwork version, stock details, software version, laser module, focus method, speed units, power, passes, and a photo of the finished test together. If any of those change, run a fresh check rather than assuming the old result still applies.", anchor="record")
    ], keywords=kw, sources=sources, related=related, label=title,
    faqs=[("Can I transfer these steps to a different machine?", "Use the workflow as preparation, but verify all device, accessory, connection, and processing details in the documentation for the actual model. Settings do not transfer automatically."),
          ("What should I keep with a successful test?", "Save the file, material identity and thickness, module, software units, settings, and a photo or physical sample. This makes later changes easier to compare.")])
    PAGES[-1]["category"] = category


# Keep each FAQ about the actual page rather than repeating generic SEO questions.
CASE_FAQS = {
    "professional-studio-crafts": ("How do I keep a craft batch consistent?", "Keep an approved sample, artwork revision, material batch, and fixture reference. Inspect pieces from the beginning, middle, and end, and recheck when stock changes."),
    "personalized-gifts": ("What should be approved before engraving a personalized gift?", "Confirm spelling, dates, punctuation, artwork size, and placement. Compare the final design with the order and test on a matching inexpensive blank."),
    "qr-code-signage": ("How do I check an engraved QR code works?", "Scan the finished sign on several phones at the intended distance and under realistic lighting. Test after cleaning, finishing, and mounting, while preserving the code's quiet zone."),
    "home-decor": ("How do I check that layered decor will assemble?", "Test the actual material thickness with a tab and slot sample, verify layer orientation, and assemble a small section before cutting a complete layout."),
    "jewelry": ("What should I test before making laser-cut earrings?", "Check finished weight, the strength around hardware holes, edge finish, cracks, and the fit of actual findings. Inspect after cleaning and assembly."),
    "gift-box-packaging": ("How do I test a laser-cut gift box?", "Assemble a full-size prototype and check slots, folds, closures, item access, and residue. Validate shipping protection separately from appearance and fit."),
    "photo-engraving": ("Why does an engraved photo look different from the screen?", "Material texture and contrast change the visible tones. Test a small crop on the actual stock, evaluate after cleaning, and keep image edits separate from machine-setting changes.")
}
for item in PAGES:
    if item["group"] == "Use Cases":
        item["faqs"] = [CASE_FAQS[item["path"].split('/')[-2]]]
    elif item["group"] == "Tutorials":
        item["faqs"] = []


SUPPORT = [
    ("before-you-buy", "Before You Buy", "Choose a TOOCAA Laser for Your Projects", "TOOCAA buying guide, NOVA L2 comparison, choose laser engraver",
     "Compare the work area, material compatibility, software, ventilation, and accessory requirements that matter for your projects.",
     [("Start with the finished item", "List the materials, physical dimensions, and operations you need: cutting an outline, engraving an image, or marking a surface. Confirm the relevant capability on the current product page. Maximum advertised thickness does not describe the finish, time, or reliability of every material."),
      ("Plan the whole workspace", "Allow for the enclosure, lid travel, exhaust route, power, computer, accessories, and space to load a sheet. Check how smoke will be managed in the intended room. A machine that fits on a desk still needs the clearances and ventilation specified in its manual."),
      ("Check the software and accessories", "Confirm operating-system support, connection options, supported file formats, and any required software license. Check rotary, air assist, bed, camera, or extraction compatibility by exact model. An accessory shown with a related model is not proof it fits the one you plan to order."),
      ("Check the current purchase details", "Use TOOCAA's live store for current module choices, availability, shipping, warranty, and return terms. Save your questions with the planned material and project size so support can respond to a concrete use case.")],
     ["use-cases/", "learn/materials/", "support/contact/"]),
    ("after-you-buy", "After You Buy", "TOOCAA Setup After Delivery", "TOOCAA getting started, laser engraver after delivery",
     "Check the delivery, identify your exact model and module, complete the official setup, and keep a record of the first test.",
     [("Check the delivery before assembly", "Compare delivered components with the packing list and inspect for visible transport damage. Record the order and serial details. Contact support about damaged or missing components before using a setup that may be incomplete."),
      ("Follow the correct manual", "Identify the exact machine and laser module, then follow its assembly and protective-system instructions. Plan extraction and clearances before powering up. Avoid instructions for another model that happen to show similar components."),
      ("Connect and verify", "Install the supported software from the official source. Confirm the device, workspace, origin, and speed units. Test movement and framing as directed by the manual before sending the first processing job."),
      ("Keep the first sample", "Use a simple file and documented stock. Note the settings, focus method, and software version, and retain the sample. It provides a baseline if a later material batch or maintenance change affects the result.")],
     ["tutorials/first-setup/", "tutorials/studio-setup/", "tutorials/first-engraving/"]),
    ("maintenance", "Maintenance", "Laser Cutter Maintenance & Inspection", "laser cutter maintenance, laser lens inspection, laser bed cleaning",
     "Inspect the bed, optics, extraction route, and moving parts using the maintenance instructions for the installed machine.",
     [("Power down before access", "Stop the job, let the work area cool, and disconnect power before accessing components as directed in the manual. Do not reach into moving parts or perform electrical repair from a general cleaning guide."),
      ("Inspect optics and the bed", "Check for deposits or damage on accessible optics and remove loose scraps from the working bed. Use only the cleaning materials and access method specified for the component. An unsuitable solvent or wipe can damage an optical coating."),
      ("Check extraction and movement", "Inspect accessible hoses, ducts, and filters for blockage, poor seating, or damage. Check the work area for obstructions and follow model-specific mechanical inspection steps. Do not tighten belts or lubricate rails by guesswork."),
      ("Verify after maintenance", "Reassemble protective parts, restore the documented focus and configuration, and run a small baseline sample. Record the work and any replaced components. If a fault remains or a component appears damaged, stop and request support.")],
     ["troubleshooting/weak-laser-output/", "troubleshooting/excessive-smoke-odor/", "support/contact/"]),
    ("ticket-checklist", "Support Checklist", "Prepare a Useful TOOCAA Support Request", "TOOCAA support request, laser troubleshooting information",
     "Collect the machine, software, material, settings, symptoms, and photos that help TOOCAA support understand a fault.",
     [("Identify the machine and problem", "Include the exact model, laser module, relevant accessory, and order or serial information through the official support channel. Describe what you expected, what happened, and whether the fault is repeatable or intermittent."),
      ("Record the job configuration", "List material identity and actual thickness, the file type and size, power, speed with units, passes, processing mode, focus method, and software version. Note the firmware only if you can read it through the normal supported interface."),
      ("Show the fault safely", "Take a clear photo of the sample and any displayed error. A short video can show unexpected motion when it is safe to record. Do not recreate a dangerous event, bypass an interlock, or expose the beam to make a better recording."),
      ("Summarize the checks already completed", "List each check and its result rather than saying everything was tried. Include whether the same file works on another blank and whether the fault began after a stock, software, accessory, or maintenance change.")],
     ["support/contact/", "troubleshooting/", "tutorials/material-test/"]),
    ("contact", "Contact TOOCAA", "Contact TOOCAA Customer Support", "TOOCAA contact, TOOCAA customer support",
     "Need help with your machine, an order, or a project? Contact TOOCAA at service@toocaa.com or use the contact page to reach the team.",
     [("Contact the support team", "Email service@toocaa.com or use the TOOCAA contact page for product, order, and technical questions. For setup instructions and machine manuals, open the TOOCAA Support Center."),
      ("For a machine issue", "Have the exact model, module, material, software version, speed units, job settings, and a clear description ready. Include a photo of the sample or error when safe and relevant. Send order and serial information only through the official private support channel."),
      ("For a buying question", "Describe the material, object size, intended cutting or engraving operation, workspace, and required accessory. That lets the product team discuss a concrete application without relying on a broad claim about all materials."),
      ("While a fault is unresolved", "Leave the machine stopped if a safeguard, damaged component, unexpected motion, persistent flame, or abnormal smoke condition is involved. Follow the manufacturer's instructions before returning it to use.")],
     ["support/ticket-checklist/", "support/before-you-buy/", "troubleshooting/"])
]

for slug, label, title, kw, intro, blocks, related in SUPPORT:
    page(f"support/{slug}/", title, intro, "Support", [section(t, x) for t, x in blocks], keywords=kw, label=label,
         related=related, sources=("support", "contact"), faqs=[
         ("Where can I confirm current support or purchase terms?", "Use the official TOOCAA contact and policy pages. Current availability, warranty, shipping, and return terms are determined there.")])


ISSUES = [
    ("laser-not-firing", "laser-cutting", "Laser Not Firing", "laser not firing, TOOCAA laser not firing",
     "Separate a disabled processing layer, a normal safety stop, and a hardware fault before trying another job.",
     "A visible positioning light, software connection, or moving head does not prove that the processing laser is enabled. Check the job configuration and any displayed status first. Safety systems must remain functional during every check.",
     ["Record the exact message or status shown by the machine and software.", "Confirm the intended processing layer is enabled and has appropriate settings.", "Check normal readiness, cover closure, and other documented safeguards.", "Review the same small file on a known compatible sample.", "If the warning remains or output is absent, stop and send support the status and configuration."],
     "Do not bridge a sensor, bypass a lock, or test an exposed beam. Repeated start attempts do not establish which safety or hardware condition is stopping the job.", ["tutorials/laser-safety/", "support/ticket-checklist/"]),
    ("weak-laser-output", "laser-cutting", "Weak Laser Output", "weak laser output, laser engraving too faint",
     "Check stock, focus, accessible optics, and file settings before assuming the laser module has lost power.",
     "A faint result may come from a material change, an unfocused surface, deposits, different speed units, or a different processing mode. Compare a small retained baseline sample and the file that originally produced it.",
     ["Identify changes in stock, software, module, or recent maintenance.", "Verify power, speed units, passes, and enabled layers.", "Check workpiece flatness and set focus using the manual.", "Power down and inspect accessible optics using the documented method.", "Run one small baseline check if the machine is safe and correctly assembled."],
     "Do not remove protective optics or compensate indefinitely with slower motion. Stop for damaged components, unusual heating, or an unresolved output change and contact support.", ["support/maintenance/", "tutorials/material-test/"]),
    ("not-cutting-through", "laser-cutting", "Laser Not Cutting Through", "laser not cutting through, plywood not cutting through",
     "Check material identity, thickness, focus, speed units, and support when a laser cut leaves attached fibers or an incomplete outline.",
     "A failed cut is not always a power problem. A different adhesive, a bowed sheet, duplicate paths, or an unsupported material can change the result. Inspect where the cut failed before choosing another setting.",
     ["Confirm the material and operation are documented for the installed module.", "Measure actual thickness and inspect flatness, coatings, and glue layers.", "Compare the selected reference row and software speed units.", "Check focus, extraction, and workpiece support.", "Run a small controlled sample and inspect the underside after the machine stops."],
     "Stop if the sample overheats, flames persist, or the material produces unexpected fumes. Do not keep burning a stuck area or leave additional passes unattended.", ["learn/materials/wood/", "learn/materials/acrylic/", "tutorials/material-test/"]),
    ("burnt-charred-edges", "laser-cutting", "Burnt Edges & Smoke Stains", "laser burnt edges, charred wood laser cutting",
     "Identify excess dwell, duplicate lines, flatness problems, and smoke deposits before changing the cutting workflow.",
     "A dark edge and a smoke-stained face are different observations. Check whether the line is being cut more than once, whether the sheet is level, and whether smoke is being removed from the work area.",
     ["Inspect the file for duplicate vectors and repeated passes.", "Compare power, speed units, and operation with the material reference.", "Check focus, support, and any documented air-assist setup.", "Inspect extraction and remove scraps with power off.", "Compare one small sample after changing a single factor."],
     "A surface mask must itself be compatible with the laser process. Do not add an unknown adhesive or coating to hide a setup problem, and stop for persistent flame.", ["learn/materials/wood/#clean-workflow", "troubleshooting/excessive-smoke-odor/"]),
    ("engraving-too-light-or-dark", "engraving", "Engraving Too Light or Too Dark", "engraving too light, laser engraving too dark",
     "Separate image contrast, exposure, and material variation when an engraving loses detail or appears too faint.",
     "Inspect the file preview and the material separately. A dark photograph can lose midtones before it reaches the laser, while a material surface may produce weak contrast even with a sound file. Keep image edits and machine adjustments in separate tests.",
     ["Compare the original image with the processed preview.", "Check the operation mode, power, speed units, and focus.", "Use a small matching blank with a simple text or filled sample.", "Change one setting or image-processing factor at a time.", "Inspect after cleaning at the intended viewing distance."],
     "Higher resolution or repeated exposure does not guarantee more detail. Stop when the surface overheats or the process is outside documented material compatibility.", ["tutorials/photo-preparation/", "use-cases/photo-engraving/"]),
    ("engraving-misalignment", "engraving", "Engraving Misalignment", "laser engraving misalignment, laser placement wrong",
     "Check origin, file dimensions, workholding, and accessory configuration when engraving lands in the wrong place.",
     "First identify whether the entire design is displaced or whether separate operations drift relative to each other. A consistent offset often points to placement or configuration; a changing offset also calls for checking movement and workholding.",
     ["Verify the artwork dimensions, origin, and coordinate mode.", "Confirm the blank and fixture have not moved.", "Frame a small test with clear reference edges.", "Check that rotary or other accessory configuration matches the current job.", "Record a photo of the reference marks and the resulting offset."],
     "Do not compensate for a growing mechanical error by moving artwork repeatedly. Stop for unexpected motion, skipped travel, or a possible collision and follow model-specific support guidance.", ["tutorials/focus-positioning/", "tutorials/lightburn-setup/"]),
    ("wavy-blurry-engraving", "engraving", "Blurry or Wavy Engraving", "blurry laser engraving, wavy engraving lines",
     "Check focus, surface stability, artwork quality, and machine motion when engraved lines look soft or uneven.",
     "Look at both a straight vector and a small filled area. If the source image is already soft, machine adjustments cannot recover the missing detail. If sharp vectors become wavy on the material, inspect the setup and motion.",
     ["Confirm the file is sharp and correctly scaled.", "Level the surface and set focus according to the module guide.", "Secure the workpiece and check the fixture for movement.", "Inspect accessible moving parts with power disconnected.", "Compare a small baseline file before making any documented mechanical adjustment."],
     "Belt tension, rail lubrication, and calibration procedures differ by model. Avoid arbitrary adjustments; document abnormal noise or play for support.", ["tutorials/focus-positioning/", "support/maintenance/"]),
    ("machine-wont-turn-on", "hardware", "Machine Will Not Turn On", "TOOCAA not turning on, laser cutter power problem",
     "Check the normal external power path and record indicator behavior without opening the machine or power supply.",
     "Note whether the machine has no indicators, briefly starts, or powers up but will not begin a job. These are different fault descriptions. Use the power accessories supplied or approved for the exact machine.",
     ["Stop and disconnect power if there is visible damage, odor, or abnormal heat.", "Check the normal external connection and documented power controls.", "Confirm the outlet and supplied power accessories are being used as instructed.", "Record any indicator, screen, or startup behavior.", "If normal startup still fails, contact support with model and power-supply details."],
     "Do not open the power supply, probe powered connectors, or substitute an unapproved adapter. Electrical diagnosis belongs with the manufacturer or qualified service.", ["support/contact/", "support/ticket-checklist/"]),
    ("homing-failure", "hardware", "Homing Failure or Unexpected Motion", "laser homing failure, laser motor grinding",
     "Stop unexpected movement, check visible obstructions and configuration, and gather useful evidence for support.",
     "Homing failure may present as a blocked axis, repeated travel into a limit, a grinding sound, or an incorrect origin. Record what the head was attempting to do and whether a fixture, cable, or accessory was recently changed.",
     ["Stop the machine using the documented procedure.", "Disconnect power before inspecting the work area.", "Check for a visible obstruction, loose item, cable snag, or misplaced fixture.", "Review the selected machine profile and accessory configuration.", "Follow the model's documented recovery instructions or request support."],
     "Do not force an axis while powered or repeatedly drive into a stop. Avoid changing firmware travel limits or sensor configuration to conceal an unresolved fault.", ["tutorials/focus-positioning/", "support/ticket-checklist/"]),
    ("usb-not-connecting", "software", "USB Connection Not Detected", "laser USB not connecting, TOOCAA connection issue",
     "Check the data cable, selected device, software access, and documented drivers when the computer cannot find the laser.",
     "A charging cable can provide power without a usable data connection. Several control programs may also compete for the same port. Identify the operating system, software release, and device profile before changing the installation.",
     ["Verify the machine is normally powered and ready.", "Use a known data cable and check the connection at both ends.", "Close other machine-control applications.", "Select the correct device and port using the official setup guide.", "Install only the driver specified for the model and operating system."],
     "Record any device or port error before reinstalling software. Do not flash firmware merely because the computer has not detected a device.", ["tutorials/studio-setup/", "tutorials/lightburn-setup/", "support/contact/"]),
    ("wifi-connection-troubleshooting", "software", "Network Connection Checks", "TOOCAA Wi-Fi connection, laser network connection",
     "Confirm that the exact machine and software support the connection method, then follow their documented network setup.",
     "Network support depends on the model, firmware, and software. First verify the connection is a supported one. Keep a record of the visible error and whether the machine was previously connected on the same network.",
     ["Check the model's current supported connection methods.", "Follow the documented network setup and band requirements.", "Confirm the computer and machine are on the intended network.", "Record the displayed network status without sharing passwords.", "Use an approved wired connection for comparison if the manual supports it."],
     "Do not disable network security broadly, expose machine controls to the internet, or use an undocumented reset procedure. Share network error details through the official private support channel.", ["studio", "support"], ["tutorials/studio-setup/", "support/ticket-checklist/"]),
    ("lightburn-not-detecting", "software", "LightBurn Does Not Detect the L2", "LightBurn not detecting TOOCAA L2, LightBurn device setup",
     "Review the L2 device setup, data connection, selected port, and other software using the machine.",
     "Treat the device profile and the connection as separate checks. A profile can exist even if the machine is disconnected, while a detected port does not prove the selected profile or origin is correct.",
     ["Follow TOOCAA's current L2 LightBurn setup instructions.", "Check normal machine readiness and a known USB data cable.", "Close competing machine-control software.", "Verify the documented device type and selected port.", "Record the software error and operating-system device behavior for support."],
     "Do not copy a different model's firmware or controller configuration to force detection. Confirm work area and origin before a test after the connection is restored.", ["lightburn", "manual"], ["tutorials/lightburn-setup/", "troubleshooting/usb-not-connecting/"]),
    ("rotary-attachment-issues", "hardware", "Rotary Attachment Slipping or Misalignment", "laser rotary slipping, L2 rotary troubleshooting",
     "Check accessory compatibility, support, grip, clearance, and the documented rotary configuration before another test.",
     "Tapered objects, handles, uneven grip, and unsupported weight can make a cylindrical object slip or move out of focus. Check the physical support before correcting a distorted design with repeated software scaling.",
     ["Stop and power down before changing accessory connections.", "Verify the exact rotary and machine are compatible.", "Check support, level, grip, and clearance for the object.", "Review the official device and rotation configuration.", "Use an inexpensive sample for a small alignment check."],
     "Stop for a stalled drive, slipping object, collision, or cable snag. Restore the documented normal configuration before returning to a flat-bed job.", ["rotary", "support"], ["tutorials/rotary-engraving/", "tutorials/irregular-shapes/"]),
    ("excessive-smoke-odor", "safety", "Excessive Smoke or Odor", "laser smoke ventilation, laser cutter smoke leakage",
     "Stop processing and check material suitability, extraction, ducting, and filters when smoke is not being managed normally.",
     "Different materials produce different residues, but visible leakage or an unusual odor should not be treated as an expected result to tolerate. Identify what changed and keep the machine stopped while the cause is unresolved.",
     ["Stop the job and follow the manufacturer's safe stopping procedure.", "Confirm the complete material is suitable for laser processing.", "With power off, inspect accessible ducting and hoses for damage or blockage.", "Check seating and maintenance of filters using the model instructions.", "Resume only when the documented extraction arrangement is restored."],
     "A filter is not a universal approval to process unknown materials. Stop immediately for persistent flame or an unsafe air condition, and request manufacturer guidance when the fault remains.", ["tutorials/laser-safety/", "support/maintenance/", "support/contact/"]),
    ("safety-alarm", "safety", "Safety Alarm or Protective Cover Warning", "TOOCAA safety alarm, laser cover warning, emergency stop",
     "Record the alarm and follow the documented stop and recovery procedure while keeping every protective system active.",
     "A safety warning may indicate a cover, motion, heat, extraction, or other model-specific condition. Read the exact message rather than assuming that an alarm with a similar appearance has the same cause.",
     ["Stop the job and make the work area safe.", "Record the exact message and what happened immediately before it.", "Check normal cover closure and visible obstructions without bypassing sensors.", "Use the model-specific recovery procedure only after the cause is addressed.", "Contact support if the warning returns or a safeguard appears damaged."],
     "Do not defeat an interlock, bridge a sensor, or suppress a warning to complete a job. A recurring safety fault should remain out of service until resolved.", ["manual", "support"], ["tutorials/laser-safety/", "support/contact/"]),
    ("firmware-update-stuck", "software", "Firmware Update or Software Error", "TOOCAA firmware update problem, laser software error",
     "Confirm the correct model and official release instructions, save the error details, and use manufacturer guidance for update recovery.",
     "An interrupted update, a software crash, and a disconnected device need different recovery steps. Record the exact stage and message. Firmware and recovery files must match the exact machine; a related model is not a substitute.",
     ["Read the official update or recovery instructions before interrupting a process.", "Record the model, software release, visible firmware version, and error.", "Keep the documented connection and power conditions stable.", "Use only the exact official file and procedure when instructed.", "Contact TOOCAA support when the documented recovery is unclear or unsuccessful."],
     "Do not repeatedly flash guessed files, change controller parameters, or follow an undocumented factory reset. Preserve the error evidence so support can recommend the appropriate recovery.", ["support", "studio"], ["support/ticket-checklist/", "support/contact/"])
]

for issue in ISSUES:
    if len(issue) == 9:
        slug, category, title, kw, intro, context, checks, stop, related = issue
        sources = ["manual", "support"]
    else:
        slug, category, title, kw, intro, context, checks, stop, sources, related = issue
    page(f"troubleshooting/{slug}/", title, intro, "Troubleshooting", [
        section("Identify the symptom", context, anchor="symptom"),
        section("Checks in order", "Begin with the visible status, configuration, and material. Keep a note of each check and its result. Inspect hardware only with the machine stopped and power disconnected as directed by the manual.", checks, "checks"),
        section("Stop and seek support when needed", stop, anchor="stop"),
        section("What to include in a support request", "Send the exact model and module, software version, material identity, file details, job settings with units, and the full error message. Describe the last successful job and any recent change. Include clear photos when safe; do not reproduce a hazardous event to record it.", anchor="support")
    ], keywords=kw, related=related + ["support/ticket-checklist/"], sources=sources,
    faqs=[("What should I check for: " + title.lower() + "?", context)])
    PAGES[-1]["category"] = category
