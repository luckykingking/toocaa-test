"""Complete the five new-content requests in the original tutorial brief."""


def add_tutorials(page, section, pages):
    formats = section('Choose a format for the job', 'Use vectors for cut outlines and pixels for photographs. The formats below are listed in the current Studio feature reference; support in another application does not automatically mean Studio can import the same file.')
    formats['table'] = {
        'headers': ['Format', 'Typical use', 'TOOCAA Studio reference', 'Check after import'],
        'rows': [
            ['SVG', 'Vector outlines, logos and editable shapes', 'Import; Save as SVG', 'Physical dimensions, text paths and duplicate outlines'],
            ['DXF', 'CAD-style vector geometry', 'Import', 'Drawing units, scale and closed contours'],
            ['PNG / JPG', 'Pixel images and photo engraving', 'Import', 'Finished size, image detail, contrast and background'],
            ['GCode', 'Prepared machine instructions', 'Save as GCode', 'Exact device and job configuration; not a substitute for editable artwork'],
            ['PDF / AI', 'Mixed artwork in supported applications', 'Not listed as Studio imports in this reference', 'Use the supported application or export suitable artwork to SVG or PNG'],
        ],
    }
    download = section('Check imported dimensions with a sample file', 'The size-check SVG below is artwork only. Its square is 20 mm wide and its circle is 10 mm in diameter. Import it and inspect the dimensions on screen before assigning any processing settings. It contains no power, speed or machine-control commands.')
    download['links'] = [('downloads/import-size-check.svg', 'Download the size-check SVG')]
    item = page('tutorials/laser-file-formats/', 'Laser File Formats: SVG, DXF, PNG & GCode',
                'Choose vector or image artwork, check supported TOOCAA Studio imports, and verify size, text and layers before sending a laser job.',
                'Tutorials', [
        formats,
        section('A picture is not a cutting outline', 'A PNG or JPG stores pixels. Importing it does not create a clean vector perimeter, and renaming it to SVG does not convert it. For a photo, prepare image engraving. For an outline cut, use original vector artwork or a deliberate image-tracing workflow, then inspect the resulting paths. Tiny islands and rough traced edges can matter at the finished object size.'),
        section('Prepare vectors before export', 'Keep an editable master file and a separate machine-preparation copy. Convert text to paths when fonts may not be installed on the receiving computer. Check closed shapes, duplicate paths and the actual drawing units. A thick screen stroke can become either one centerline or outlined edges depending on export settings, so inspect the imported geometry rather than assuming it will cut once.', ['Confirm the final width and height in millimeters.', 'Check text and small details at actual output size.', 'Inspect closed contours and remove unintended duplicates.', 'Assign each operation to the correct layer after import.']),
        section('Artwork, projects and machine files are different', 'A saved SVG is useful editable artwork; it is not proof that every machine setting has traveled with it. A GCode file is prepared for a particular controller and configuration. Do not send instructions for a different model or run a downloaded machine file whose motion, power and work area have not been checked. LightBurn has its own project and machine-file formats; its import list is broader than Studio\'s published list.'),
        download,
        section('Run a final preview', 'Confirm the selected device, work area, origin, layer output, operation, power, speed units and passes. Review the processing preview and frame the design using the model\'s normal procedure. A file that looks correct in a drawing program can still contain an unexpected second outline or an image at the wrong size.'),
    ], keywords='laser cutter file formats, SVG laser cutting, DXF laser file, PNG laser engraving, TOOCAA Studio import',
        sources=['studioFeatures', 'lightburnFiles', 'l2Connection', 'novaConnection'],
        related=['tutorials/complex-designs/', 'tutorials/photo-preparation/', 'troubleshooting/file-transfer-failed/'],
        faqs=[('Does changing a PNG filename to .svg make it a vector?', 'No. File renaming does not trace an image. Use genuine vector artwork or a supported tracing tool, then inspect the resulting geometry.'), ('Why is a DXF imported at the wrong size?', 'Check the source drawing units and the imported dimensions. Do not send it to the machine until the physical size is verified.')])
    item['category'] = 'Software'

    item = page('tutorials/color-laser-engraving/', 'Color Laser Engraving: What Your TOOCAA Can Do',
                'Understand colored engraving stock, coating removal and metal-coloring limits before choosing a material or expecting full-color laser output.',
                'Tutorials', [
        section('Color in a design is not printed ink', 'A laser changes the material or its surface; it does not print the RGB colors of a photo as an inkjet would. In Studio, different layer colors identify objects and processing settings. Those on-screen colors do not instruct a standard module to deposit matching red, blue or green ink.'),
        section('Colored stock and coating removal', 'A colored surface can produce contrast when a suitable laser process changes or removes its coating. With documented layered engraving stock, the visible result depends on the layers of the actual blank. Check the complete material identity and its processing instructions rather than assuming every painted sheet has the same construction. Anodized or coated metal is another distinct surface-marking workflow, not evidence of cutting bare sheet metal.'),
        section('Metal color marking uses a different process', 'Specialized laser/material systems can create surface-color effects, but a result advertised for a pulsed fiber or MOPA system is not a preset for a NOVA or L2 diode module. The metal, coating, source type and pulse-control capabilities all matter. Check the exact documented process before promising a multicolor metal result to a customer.'),
        section('Plan a repeatable colored-material test', 'Start with a documented blank from the same batch as the finished job.', ['Identify the substrate, coating and backing, including any adhesive.', 'Match the machine, module and operation to a manufacturer reference.', 'Prepare small text, a filled shape and a fine outline at the intended size.', 'Inspect contrast after cooling and appropriate cleaning.', 'Check handling and the intended use before making a full batch.']),
        section('Do not turn unknown paint into a workaround', 'An attractive surface does not establish laser suitability. Do not process PVC, vinyl or an unidentified coating. A marking compound also needs its own compatibility, ventilation and handling instructions. Adding an unknown spray to obtain a color is not a safe substitute for choosing a documented material.'),
        section('Choose the result you actually need', 'For a colored sign or a high-contrast tag, a suitable layered blank may provide the desired appearance without attempting metal color chemistry. For a photograph, prioritize a readable tonal image on a documented material. If the job requires a specific color palette, confirm an actual sample before committing to a machine, stock purchase or customer order.'),
    ], keywords='color laser engraving, colored laser engraving material, TOOCAA color engraving, diode vs MOPA color marking',
        sources=['laserTypes', 'metalSettings', 'studioFeatures'],
        related=['learn/materials/metal/', 'use-cases/qr-code-signage/', 'tutorials/material-test/'],
        faqs=[('Will red and blue Studio layers engrave in red and blue?', 'No. Layer colors organize processing operations. Output color depends on the material and process, not on screen-layer color.'), ('Can I copy a MOPA color-marking recipe to a diode module?', 'No. Source type, pulse control and the material surface differ. Use a workflow documented for the exact module and blank.')])
    item['category'] = 'Technology'
    item['scope_note'] = 'The older Magic Chroma product URL returned HTTP 404 during review; no current availability or substitute-product claim is made. Layered stock and MOPA limitations are explained separately.'

    by_path = {p['path']: p for p in pages}
    wood = by_path['learn/materials/wood/']
    choices = section('Choose wood for the finished object', 'Pick the stock for the design and its intended use, then check the supplier\'s complete material information. Grain, adhesive, veneer and actual thickness can matter as much as the species name.')
    choices['table'] = dict(headers=['Wood or sheet', 'Useful project direction', 'What to check'], rows=[
        ['Basswood', 'Simple engraving, tags and first cut samples', 'Flatness, actual thickness and contrast on a small sample'],
        ['Birch plywood', 'Assembled panels, boxes and repeated parts', 'Adhesive, voids and whether the reference is for this plywood construction'],
        ['Walnut or cherry', 'Decorative gifts and visible wood grain', 'Engraving contrast against the darker surface'],
        ['MDF or composite board', 'Only when the exact product is documented as suitable', 'Binder, coating and supplier approval; no MDF row in this page\'s lookup'],
    ])
    wood['sections'].insert(1, choices)
    wood['faqs'] = list(wood['faqs']) + [
        ('Why are there burn marks on the front or back?', 'Separate surface smoke deposits from excessive exposure. Check duplicate paths, focus, workholding, air assist and exhaust before changing several settings at once.'),
        ('Why do tabs and slots not fit?', 'Measure the actual sheet and a small cut-fit coupon. Kerf and stock variation affect inside and outside features differently.'),
        ('Can I use the L2 lookup for NOVA?', 'The lookup displays the specified L2 source rows. Use the current NOVA documentation for its own setup and settings rather than treating the lookup as a conversion tool.'),
        ('Are the project pictures tested customer examples?', 'The labeled AI project image is an illustrative concept, not a customer case, supplied design file or proof of tested machine settings.'),
    ]
    wood['illustration'] = 'wood-projects'

    metal = by_path['learn/materials/metal/']
    metal['sources'] = ['metalSettings', 'l2Faq', 'settings']
    surfaces = section('Match the metal surface to the laser module', 'A marking result depends on the source and the surface. TOOCAA publishes separate metal guidance for its machines and discusses its infrared module for metal-focused work. Do not infer a bare-metal cutting capability from a surface-marking example.')
    surfaces['table'] = dict(headers=['Surface or system', 'Check first', 'Do not assume'], rows=[
        ['Anodized aluminum', 'Coating identity, contrast and finish after cleaning', 'That the same result applies to bare aluminum'],
        ['Coated or painted metal', 'All coating ingredients and a documented process', 'That any paint or marking spray is laser-safe'],
        ['Stainless steel', 'Exact module, finish and manufacturer reference', 'That an unknown grade or finish uses one universal setting'],
        ['Infrared / diode / fiber systems', 'The actual laser source and supported operation', 'That equal advertised watts mean identical settings or capability'],
    ])
    metal['sections'].insert(1, surfaces)
    metal['sections'].append(section('Make a useful metal-marking sample', 'Use the same surface finish as the final blank. Include small text, a fine line and a filled shape. Compare the mark under normal viewing angles after the approved cleaning step. If a marking product is involved, follow its own application and safety instructions. A dark fresh mark is not by itself proof of wear resistance or food-contact suitability.'))
    metal['related'] = list(metal['related']) + ['tutorials/color-laser-engraving/']

    acrylic = by_path['learn/materials/acrylic/']
    acrylic['sources'] = ['acrylicSettings', 'settings', 'l2Safety']
    acrylic['sections'].insert(1, section('Cast, extruded and clear acrylic', 'TOOCAA\'s acrylic guide notes that cast stock generally gives stronger engraving contrast than extruded stock. Color and transparency are separate choices: clear acrylic is not a suitable cutting target for the visible-diode workflow described here. Do not copy a CO2 clear-acrylic project to a diode machine or keep increasing exposure to make a transparent sheet absorb the beam.'))
    acrylic['sections'].append(section('Inspect edge quality after a small cut', 'Let the test cool, then examine the edge, corners, holes and underside. A smooth-looking edge does not prove the hole or slot is the right size. Rounded melted corners, sticking pieces or smoke staining call for checking compatibility, duplicate paths, focus, airflow and the matching source settings. A polished appearance is an outcome to test, not a guaranteed finish for every acrylic color.'))
    acrylic['faqs'] = list(acrylic['faqs']) + [('Can I cut clear acrylic with these diode settings?', 'No. The linked TOOCAA acrylic guide distinguishes clear acrylic from suitable opaque stock and directs clear-acrylic work to an appropriate CO2 process.')]

    studio = by_path['tutorials/studio-setup/']
    studio['description'] = 'Open browser-based TOOCAA Studio, connect L2 by USB or NOVA by its documented USB/Wi-Fi workflow, and check the selected machine before a first job.'
    studio['sources'] = ['studioFeatures', 'l2Connection', 'novaConnection']
    studio['sections'] = [
        section('Open the official browser application', 'TOOCAA Studio is an online editing and machine-control tool. Open toocaastudio.com using the browser recommended by the current connection guide, Google Chrome. Do not install an unrelated desktop package claiming to be a required Studio update. Save editable projects before changing the browser session.'),
        section('Connect TOOCAA L2', 'Power on L2 normally and connect its data-capable USB cable. In Studio, choose Connect Device, select L2 and confirm. Select the actual L2 serial port in the browser prompt; the manufacturer\'s guide identifies it as the port that appears when the cable is connected. Close another control session if it is holding the device.'),
        section('Connect TOOCAA NOVA', 'Choose NOVA explicitly, then select USB or Wi-Fi. USB uses its normal data connection and browser serial-port selection. For Wi-Fi, the computer and machine need the same network and IP subnet, a reachable current device address and confirmation on the touchscreen. The current official workflow describes TOOCAA Connect for the Wi-Fi browser connection; use the official guide\'s installation source.'),
        section('Check the workspace before processing', 'Confirm the model shown in Studio, import a simple design and check its physical dimensions. The software\'s work area depends on the selected machine. Review layer mode, output, power, speed units and passes, then use the machine\'s normal focusing and framing procedure on documented test stock. A successful connection is not proof that a file\'s settings suit the material.'),
    ]

    compatibility = section('Start with the machine, not the accessory name', 'L2 and NOVA have different camera, rotary and module arrangements. Match the exact accessory product and its supported machine before ordering. A similar connector or a photograph of a related product is not a compatibility statement.')
    compatibility['table'] = dict(headers=['Accessory or function', 'TOOCAA L2', 'TOOCAA NOVA', 'Check before ordering'], rows=[
        ['Camera positioning', 'Optional L2 Smart Camera workflow', 'Built-in camera and NOVA calibration workflow', 'The actual mounting and software instructions; an L2 camera is not a NOVA upgrade'],
        ['Rotary engraving', 'L2 5-in-1 rotary guide', 'NOVA rotary with 90-degree X-axis setup', 'Accessory identity, workpiece size, grip and clearance'],
        ['Air assist', 'L2-specific kit and controls', 'Smart air-pump control described in Studio', 'Included bundle contents and exact module/air-line compatibility'],
        ['Working panel', 'Use the specified L2 panel or compatible accessory', 'Native blade cutting panel / protective-plate arrangement', 'Dimensions, clearance and whether a proposed panel is explicitly supported'],
        ['Smoke purifier', 'Accessory-specific exhaust setup', 'Optional purifier separate from the rear built-in filter', 'Hose connection, filter part and maintenance requirements'],
        ['Laser module', 'L2 documentation lists diode and infrared options', 'NOVA documentation lists its own interchangeable options', 'Machine mount and module identity, not just the advertised wattage'],
    ])
    links = section('Explore the matching TOOCAA products', 'Use the current product description and the relevant machine manual for compatibility and package contents. Availability and bundles can change; the links below are product-selection starting points, not a promise that every item is included with every machine.')
    links['links'] = [
        ('https://www.toocaa.com/products/toocaa-air-assist-kit-for-l2', 'L2 air assist'),
        ('https://www.toocaa.com/products/toocaa-smart-camera-for-l2', 'L2 Smart Camera'),
        ('https://wiki.toocaa.com/en/TOOCAA-L2/5-in-1RotaryforL2', 'L2 rotary instructions'),
        ('https://wiki.toocaa.com/en/toocaa-nova/NOVARotary', 'NOVA rotary instructions'),
        ('https://www.toocaa.com/collections/working-panel', 'Working panels'),
        ('https://www.toocaa.com/collections/smoke-purifier', 'Smoke purifiers'),
    ]
    page('support/accessories/', 'Choose Accessories for TOOCAA L2 & NOVA',
         'Compare camera, rotary, air assist, working-panel and purifier choices for TOOCAA L2 and NOVA, with model-specific product and manual links.',
         'Support', [
        compatibility,
        section('Choose around the actual project', 'For flat signs and cut panels, prioritize a suitable work surface, documented stock and the prescribed smoke-extraction setup. For a cylindrical object, choose the correct rotary and confirm how the object will be held. A handle, taper or soft wall can change the supported setup even when the nominal diameter looks suitable.'),
        section('Camera and focus are different functions', 'L2\'s optional Smart Camera has its own calibration instructions. NOVA\'s built-in view uses its own Studio calibration and autofocus workflow. A camera can help position artwork but does not make an unknown material safe or guarantee that a warped sheet stays in focus.'),
        section('Plan the airflow system as a whole', 'Air assist at the workpiece is different from enclosure smoke extraction. A purifier is not permission to engrave unknown plastic indoors, and its cartridge is not the same part as NOVA\'s washable rear machine filter. Read the accessory maintenance instructions before selecting replacement filters or deciding where the machine can operate.'),
        links,
        section('Send a clear compatibility question', 'When a listing does not state that your exact configuration is supported, send TOOCAA the model, installed laser module, accessory product name and intended material/object dimensions. Ask which mounting parts, cables or filters are required. Do not purchase on a guessed fit or use an adapter to force an incompatible part to work.'),
    ], keywords='TOOCAA accessories guide, L2 accessories, NOVA rotary, TOOCAA camera air assist purifier',
        sources=['l2Faq', 'novaProduct', 'rotary', 'novaRotary', 'novaPurifierFilter', 'studioFeatures'],
        related=['support/before-you-buy/', 'troubleshooting/rotary-attachment-issues/', 'troubleshooting/nova-smart-air-assist/'],
        faqs=[('Can I use the L2 rotary instructions for NOVA?', 'No. NOVA has a distinct rotary and X-axis installation. Match both the accessory and the machine manual.'), ('Does a purifier make every material safe indoors?', 'No. Identify and approve the material independently, and follow the machine and purifier ventilation instructions.')], label='Accessories for L2 & NOVA')
