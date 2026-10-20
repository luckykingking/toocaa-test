"""Complete the seven content families and 22 articles in the supplied scope table."""


def add_frameworks(page, section, pages):
    def s(title, text, steps=(), table=None):
        block = section(title, text, steps)
        block['ordered'] = bool(steps)
        if table:
            block['table'] = dict(headers=table[0], rows=table[1])
        return block

    def guide(path, title, description, group, keywords, blocks, sources, related, faqs, **extra):
        item = page(path, title, description, group, blocks, keywords=keywords, sources=sources, related=related, faqs=faqs)
        item.update(extra)
        return item

    guide('learn/materials/other/', 'Other Laser Materials: Glass, Fabric & Composites',
          'Check glass, textiles, cork and mixed-material blanks before processing. Identify coatings, adhesives and unknown layers before choosing laser settings.',
          'Materials', 'other laser materials, laser compatible materials, laser engraving glass, laser cutting fabric', [
        s('Identify the complete blank', 'A shop label such as craft sheet, faux leather or foam does not identify every component. Ask for the substrate, coating, adhesive and backing. A material data sheet may describe handling hazards without approving laser processing; obtain explicit suitability information for the intended process too.'),
        s('Choose a documented material route', 'Use a specific guide when the composition is known. A visually similar blank may need a different process.', table=(['Material family', 'Guide or next check', 'Important limit'], [
            ['Glass and stone', 'Use the glass or stone engraving guide', 'Engraving is not a claim of glass or stone cutting capability'],
            ['Fabric and felt', 'Identify fiber, dye, finish and backing', 'Unknown synthetic blends and vinyl layers are not accepted substitutes'],
            ['Cork and laminated boards', 'Identify binders, adhesive and all layers', 'A natural-looking face does not establish the safety of the core'],
            ['Unknown plastic, foam or composite', 'Keep out of the machine until positively identified', 'Do not perform a burn test to identify an unknown material'],
        ])),
        s('Check settings without inventing a substitute', 'There is no universal other-material setting. Match the actual machine, module, stock and operation to a published reference. If a matching entry is absent, ask TOOCAA before processing it. Do not borrow a wood or acrylic recipe simply because the sheet has the same thickness.'),
        s('Prepare a controlled sample', 'Only test stock already established as suitable. Use the same construction and batch as the final blank.', ['Record the supplier and all layers.', 'Check the workpiece support and model-specific focus method.', 'Keep the initial design small and inspect both faces after cooling.', 'Retain the sample, file and settings with their units.']),
        s('Keep unsuitable materials out', 'Do not process PVC, vinyl, unidentified plastic, or material whose coating or adhesive cannot be verified. A purifier, low power, enclosure or small sample does not make an unknown composition acceptable. Stop for cracking, unstable movement, abnormal fumes or an unresolved safety warning.'),
    ], ['l2Safety', 'settings', 'manual'], ['learn/materials/glass/', 'learn/materials/fabric/', 'learn/materials/cardboard/', 'learn/materials/stone/', 'support/material-settings/'], [('Can I test an unknown plastic with a quick laser pulse?', 'No. Establish its complete composition and suitability before exposure. A small burn can still release hazardous products.')], label='Other Materials')

    guide('support/material-settings/', 'TOOCAA Material Settings: L2 Reference & Test Records',
          'Find published L2 settings by material, module and operation. Check thickness and speed units, and keep NOVA settings separate from L2 references.',
          'Support', 'TOOCAA material settings, L2 laser settings, laser power speed table, material test record', [
        s('Match all parts of a setting', 'Start with the exact model and installed module, then the material, actual thickness and operation. A cutting value is not an engraving value. The reference rows on this page are published L2 examples, not a conversion between modules and not a guarantee for every supplier or finish.'),
        dict(s('Filter the published L2 rows', 'The table keeps the original power, speed and passes together. All listed speeds are in millimeters per minute. An empty filter result means this reference has no matching row; it does not calculate a substitute.'), anchor='settings-table'),
        s('Read the settings fields', 'Check the application units before entering numbers.', table=(['Field', 'Meaning', 'Check before processing'], [
            ['Module', 'The installed optical laser module', 'Do not copy a row to another power class or machine'],
            ['Thickness and operation', 'Stock dimension and cutting or engraving task', 'Measure the sample and select the intended layer mode'],
            ['Power', 'The percentage used in the published example', 'A percentage is not a portable optical-watt specification'],
            ['Speed', 'Travel speed, listed here in mm/min', '1 mm/s equals 60 mm/min; verify the software display'],
            ['Passes', 'Number of repetitions in the reference', 'Inspect the sample rather than adding passes to unknown stock'],
        ])),
        s('Keep a useful test record', 'Use a suitable offcut from the same batch. Retain a photo and physical sample so later changes can be compared.', ['Record model, module, material supplier and actual thickness.', 'Save the artwork revision, processing mode and focus method.', 'Record power, speed with units, passes and documented air-assist setup.', 'Inspect separation, edge condition, small text and final dimensions.', 'Retest after a material, module, artwork or maintenance change.']),
        s('For NOVA and unlisted stock', 'Use the current NOVA documentation and its supported material workflow. A recognition tag or suggested preset does not prove that an unidentified material is suitable. When a matching reference is missing, send support the complete material and module details rather than interpolating the L2 table.'),
    ], ['settings', 'novaFaq', 'l2Safety'], ['tutorials/material-test/', 'learn/materials/wood/', 'learn/materials/', 'support/contact/'], [('Why does a filter show no result?', 'No row in the retained L2 source data matches that combination. Use the full current TOOCAA reference or ask support; do not infer a missing recipe.'), ('Can these settings be used unchanged on NOVA?', 'No. They are L2 reference rows. Use NOVA-specific setup and material guidance.')], label='Material Settings')

    guide('software/toocaa-studio/', 'TOOCAA Studio: Design, Connect & Prepare a Laser Job',
          'Use browser-based TOOCAA Studio to prepare artwork, connect L2 or NOVA, check layers and preview a job before processing.',
          'Software', 'TOOCAA Studio, TOOCAA laser software, TOOCAA Studio file formats, NOVA camera software', [
        s('Start in the browser', 'Open TOOCAA Studio through the official TOOCAA software page. The current connection guides use Chrome. Keep the machine manual beside the software instructions: signing into an account, selecting a device and setting up a physical workspace are separate tasks.'),
        s('Bring in the right artwork', 'The published Studio feature overview lists JPG, PNG, DXF and SVG imports, with SVG and GCode save options. Choose vectors for outline work and images for photographs. Check physical dimensions and text after import; the on-screen appearance alone does not prove that the final toolpath has the intended scale.'),
        s('Connect the actual machine', 'Use the guide for the exact model, not a copied profile.', table=(['Machine', 'Documented connection route', 'Check'], [
            ['L2', 'USB serial connection in the supported browser', 'Data cable, actual serial port and driver requirement where applicable'],
            ['NOVA', 'Documented USB or Wi-Fi connection', 'For Wi-Fi: shared network/subnet, TOOCAA Connect and device confirmation'],
            ['NOVA camera workflow', 'Refresh, focus and calibrate using the NOVA guide', 'A stale overlay or L2 camera procedure is not a substitute'],
        ])),
        s('Prepare the job', 'Keep the first task small enough to inspect clearly.', ['Confirm the selected device and work area.', 'Verify dimensions, closed contours and duplicate outlines.', 'Assign the correct operation and output state to each layer.', 'Check power, speed units and passes against a matching reference.', 'Refresh placement and frame the design using the model instructions.', 'Process only with the documented safeguards, extraction and attendance.']),
        s('Keep artwork and machine files distinct', 'Save an editable design separately from prepared machine instructions. A downloaded GCode file may contain settings for another controller or work area. Do not treat it as portable artwork. Retain the successful design, material identity, module and job settings so a later change can be diagnosed.'),
    ], ['studio', 'studioFeatures', 'l2Connection', 'novaConnection', 'novaCamera'], ['tutorials/studio-setup/', 'tutorials/studio-design/', 'tutorials/laser-file-formats/', 'software/comparison/'], [('Is Studio the same as a desktop application I must reinstall?', 'The workflow documented here is browser-based. Follow the current official connection instructions rather than an unrelated desktop or phone-app reinstall procedure.'), ('Do layer colors print the same colors on the material?', 'No. Layer colors organize operations; the material and process determine the resulting appearance.')], label='TOOCAA Studio Guide')

    guide('software/comparison/', 'TOOCAA Studio vs LightBurn: Choose Your Laser Workflow',
          'Compare Studio and LightBurn for artwork, connection, camera setup, image engraving and saved files without assuming every model uses the same profile.',
          'Software', 'TOOCAA Studio vs LightBurn, best software for TOOCAA L2, laser software comparison', [
        s('Choose by the device and the task', 'A familiar interface is useful only if the selected device profile and workflow match the actual machine. TOOCAA publishes browser-based Studio connection guides for L2 and NOVA, and a separate L2 LightBurn operation guide. Check the applicable documentation before transferring a setup between machines.'),
        s('Compare the working differences', 'Use the current software documentation for a feature or license decision; the table does not promise identical behavior across models.', table=(['Task', 'TOOCAA Studio', 'LightBurn'], [
            ['Working environment', 'Browser-based workflow in the current TOOCAA guides', 'Installed application; check current operating-system and license requirements'],
            ['Machine setup', 'Separate L2 USB and NOVA USB/Wi-Fi guides', 'Use the TOOCAA L2 setup guide for L2; verify other models independently'],
            ['Artwork import', 'Published list: JPG, PNG, DXF, SVG', 'Broader supported import list in the LightBurn file reference'],
            ['Camera placement', 'NOVA-specific refresh and calibration workflow', 'Do not assume Studio camera calibration transfers to another application'],
            ['Photo controls', 'Use the available Studio image controls', 'Image modes, line interval and Interval Test are documented separately'],
            ['Saved files', 'SVG artwork and prepared GCode options', 'Application project and machine-file formats are distinct'],
        ])),
        s('When Studio is a useful starting point', 'Use the documented Studio route when preparing a first supported job, connecting NOVA with its camera workflow, or keeping the design and setup instructions within TOOCAA\'s ecosystem. Learn the layers, dimensions and preview before adding a complex file. Keep recognition presets separate from independent material identification.'),
        s('When to explore LightBurn', 'For a documented compatible setup, its image modes, interval tests and project controls can help when refining photo work or a repeatable design. Learn the device selection and units first. A paid license or more controls do not establish material safety, and an L2 example is not automatic proof of a NOVA configuration.'),
        s('Move a project without losing its meaning', 'Keep an editable artwork master and verify the imported copy rather than assuming all processing settings travel with it.', ['Compare width, height and units.', 'Check text paths, duplicate contours and images.', 'Reassign operations and confirm output layers.', 'Verify machine profile, origin, settings and preview.', 'Frame and inspect a small suitable sample before a full batch.']),
    ], ['studioFeatures', 'lightburn', 'lightburnFiles', 'lightburnImageMode', 'novaConnection'], ['software/toocaa-studio/', 'tutorials/lightburn-setup/', 'tutorials/laser-file-formats/', 'tutorials/photo-preparation/'], [('Which software is automatically best for every TOOCAA owner?', 'Neither is a universal answer. Start with a workflow documented for the exact machine, then choose the controls and file handling needed for the job.'), ('Can I copy a device profile between Studio and LightBurn?', 'Recheck the actual model, controller, work area, origin and speed units. Do not assume profile or camera settings transfer unchanged.')], label='Studio vs LightBurn')

    audiences = [
        ('studios', 'Laser Cutting for Creative Studios', 'Plan client samples and repeat craft work with an artwork master, material records, fixtures and a clear approval process.', 'laser engraver for studios, craft studio laser cutter, small batch laser workflow',
         'A studio job often begins with an approved sample rather than a large run. Define the object size, material, engraved detail, finishing and hardware before nesting a sheet. Keep the client\'s approved spelling, logo revision and placement together with that sample.',
         [('Custom labels', 'Leather or documented coated blanks', 'Legibility and residue after finishing'), ('Cut collections', 'Known wood or suitable opaque acrylic', 'Fit, kerf and repeated dimensions'), ('Client samples', 'The actual planned production stock', 'Approval of text, layout and finish at final size')],
         ['Agree the object, artwork revision and acceptance points.', 'Make one representative sample on the production stock.', 'Record its fixture, focus method and settings with units.', 'Inspect pieces from the start, middle and end of a batch.'],
         'Compare usable work area, supported module, file handling, accessory clearance and extraction for the actual jobs. L2 and NOVA have distinct focus, camera and rotary workflows. Check the current product and accessory documentation rather than choosing only by an advertised wattage.',
         ['use-cases/professional-studio-crafts/', 'tutorials/complex-designs/', 'support/accessories/'], 'workspace'),
        ('diy-gifts', 'Make Personalized Gifts with a TOOCAA Laser', 'Prepare names, dates, photos and small gift sets with a clear design check and a test on matching stock before engraving the final blank.', 'laser engraver for DIY gifts, personalized laser gifts, custom photo engraving gifts',
         'Choose a blank whose complete composition is documented. A wooden tag, leather label, coated-metal keepsake and stone photo panel need different preparation. Confirm whether the design needs an outline cut, text engraving or a photograph before preparing the file.',
         [('Names and dates', 'Wood tags or suitable identified blanks', 'Spelling, punctuation and actual text size'), ('Photo keepsakes', 'Documented wood or stone engraving blanks', 'Crop, contrast and readable tones'), ('Gift packaging', 'Known paper, cardboard or wood', 'Fit, fold direction and assembly')],
         ['Confirm every name, date and image permission.', 'Preview the design at the final physical size.', 'Test on matching inexpensive stock.', 'Inspect placement and finish after cooling and cleaning.'],
         'A built-in camera can help place a design, but it cannot restore an old overlay after the blank moves. Refresh the view and check focus using the model guide. Round gifts may need a compatible rotary, not a flat-bed setup with guessed height or diameter.',
         ['use-cases/personalized-gifts/', 'use-cases/photo-engraving/', 'tutorials/rotary-engraving/'], 'wood'),
        ('classrooms', 'Plan Laser Projects for a Supervised Classroom', 'Organize suitable classroom laser projects around trained supervision, identified materials, controlled access and an approved workspace.', 'classroom laser cutter, laser engraving education, supervised STEM laser projects',
         'A classroom workflow begins with the institution\'s risk assessment, trained operator and machine-specific safety instructions. An enclosure does not authorize unattended or unsupervised student operation. Plan access control, extraction, emergency procedures and who is responsible for each processing job.',
         [('Design and measurement', 'Simple flat parts on approved stock', 'Final dimensions and how kerf affects fit'), ('Assembly exercises', 'Small documented wood or card parts', 'Stable joints, fragile details and safe handling'), ('Artwork preparation', 'Original vector shapes and simple images', 'Size, duplicate paths and image/vector differences')],
         ['Approve the room, machine and material workflow with the responsible institution.', 'Limit operation to trained, authorized supervision.', 'Have students prepare and review artwork away from the machine.', 'Use a small known-stock sample and inspect cooled parts.', 'Clear scraps and restore controlled access after the session.'],
         'Choose equipment only after checking its complete safeguarding and ventilation instructions against the intended institution and age group. Do not claim that a machine is certified for a particular school, child age or classroom merely because it is enclosed. Confirm purchasing and access questions directly with TOOCAA.',
         ['tutorials/laser-safety/', 'tutorials/laser-file-formats/', 'troubleshooting/protective-cover-sensor/'], 'workspace'),
        ('small-businesses', 'Plan Repeat Laser Orders for a Small Business', 'Build repeatable laser orders with approved samples, material checks, realistic job records and a maintenance plan tied to the actual equipment.', 'laser engraver for small business, repeat laser orders, laser engraving production workflow',
         'Start with a finished item and a repeatable acceptance standard. A successful demonstration does not establish production throughput, profit or demand. Record the whole job, including preparation, material handling, processing, cleanup, finishing, inspection and packing.',
         [('Repeat personalization', 'Reusable fixtures and approved artwork', 'Correct customer data on every item'), ('Branded packaging', 'Actual sheet thickness and construction', 'Assembly, logo placement and finish'), ('Product collections', 'Controlled material batches', 'Variation between the first and last pieces')],
         ['Approve a finished sample and preserve its artwork revision.', 'Separate material batches and record setup changes.', 'Inspect a small first batch before loading more stock.', 'Track rejects, finishing and maintenance as actual job costs.', 'Recheck a baseline after a module or material change.'],
         'Match the usable work area, supported material, accessories and extraction to the order rather than assuming that more advertised power guarantees better economics. Compare NOVA and L2 in the current official guide. Never promise a fixed daily output, payback period or profit without measured evidence from the real workflow.',
         ['use-cases/gift-box-packaging/', 'use-cases/qr-code-signage/', 'support/maintenance/'], 'workspace'),
    ]
    for slug, title, intro, keywords, planning, projects, steps, setup, related, image in audiences:
        item = guide('who-is-it-for/' + slug + '/', title, intro, "Who It's For", keywords, [
            s('Plan the finished project', planning),
            s('Projects to start with', 'Choose a small representative project before committing to a collection or batch.', table=(['Project', 'Preparation', 'Inspect'], projects)),
            s('Work through one complete sample', 'Keep the process and the finished result together so a later change can be compared.', steps),
            s('Choose the setup for the work', setup),
            s('Check before the next job', 'Keep the material identity, artwork version, device, module, focus method and job settings with the retained sample. Check text, placement, dimensions, edges and intended handling after cooling and any documented finishing. A new material batch or fixture deserves a fresh sample rather than relying on the old photograph.'),
        ], ['choose', 'l2Safety', 'novaFaq', 'settings'], related + ['support/before-you-buy/', 'support/material-settings/'], [('Can the same setup be reused after the material changes?', 'Recheck composition, thickness, focus, the matching setting and a small sample. A retained artwork file is not proof that a new batch will process identically.')], label={'studios':'Studios', 'diy-gifts':'DIY Gifts', 'classrooms':'Classrooms', 'small-businesses':'Small Businesses'}[slug], image=image)
        if slug == 'diy-gifts':
            item['illustration'] = 'wood-projects'

    for item in pages:
        for block in item['sections']:
            if block.get('anchor') in {'clean-workflow', 'workflow'}:
                block['ordered'] = True

    return [
        dict(path='software/', title='Laser Software for TOOCAA: Studio & LightBurn', description='Compare software workflows, learn TOOCAA Studio, and find setup, file-format and image-preparation guides for a documented machine configuration.', group='Software', keywords='TOOCAA software, TOOCAA Studio, LightBurn for L2, laser software comparison', sources=['studioFeatures', 'lightburn', 'novaConnection'], sections=[], label='Software', collections=[('Choose a software workflow', ['software/toocaa-studio/', 'software/comparison/']), ('Set up and prepare a file', ['tutorials/studio-setup/', 'tutorials/lightburn-setup/', 'tutorials/laser-file-formats/', 'tutorials/photo-preparation/']), ('Connection and preview help', ['troubleshooting/toocaa-studio-connection/', 'troubleshooting/lightburn-not-detecting/', 'troubleshooting/nova-camera-positioning-offset/'])]),
        dict(path='who-is-it-for/', title='TOOCAA for Studios, DIY Gifts, Classrooms & Small Businesses', description='Explore laser workflows for a creative studio, personalized gifts, supervised classroom projects and repeat small-business orders.', group="Who It's For", keywords='who is TOOCAA for, studio laser cutter, DIY gifts laser, classroom laser projects, small business laser engraver', sources=['choose', 'l2Safety'], sections=[], label="Who It's For", collections=[('Find your workflow', ['who-is-it-for/studios/', 'who-is-it-for/diy-gifts/', 'who-is-it-for/classrooms/', 'who-is-it-for/small-businesses/']), ('Plan your first setup', ['support/before-you-buy/', 'support/after-you-buy/', 'support/accessories/'])]),
    ]
