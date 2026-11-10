# Taqwa Village website

A static, responsive website with an emerald-and-ivory design. Open index.html in a browser, or serve the folder locally:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Visit http://127.0.0.1:8000/index.html. Internet access is needed for CDN styles, icons, fonts, the homepage slider and remote images.

## Pages

- index.html — homepage
- about.html — story and values
- projects.html — project overview
- cottages.html — cottage concept and inquiry
- resort.html — hospitality concept and inquiry
- agro.html — nature and family experiences
- investment.html — information requests
- amenities.html — proposed amenities and FAQs
- gallery.html — filterable inspiration gallery with image previews
- contact.html — telephone, email, WhatsApp and address information
- booking.html — inquiry form and reviewable WhatsApp message
- privacy.html — website data handling
- terms.html — website and inquiry information

All pages are connected through navigation, breadcrumbs, project cards, related pages and footer links. Mobile navigation includes Home and Booking. New page content supports Bengali and English; the selected language is stored locally and persists across pages. Existing homepage body content and parts of the shared footer and modal remain Bengali.

## Editing

Edit homepage content in index.html. Its layout follows the supplied hand-drawn JPG: slogan / booking / logo, navigation and social links, a left project-image and video column, three stacked image cards on the right, a full-width slider, address strip and compact footer. Homepage slider controls are in home.js. The inner pages now reuse the homepage masthead, navigation, address bar and compact footer. build_pages.py reads these directly from index.html and refreshes the snapshots in templates/inner-header.html and templates/inner-footer.html; edit index.html to change the shared design. Edit inner-page content in build_pages.py, then run:

```powershell
python build_pages.py
```

This updates the homepage links and regenerates all 12 inner HTML pages. Direct edits to generated pages are replaced on regeneration. styles.css contains the shared styles; app.js handles existing homepage controls and dialogs; pages.js handles language persistence, gallery filters and the standalone inquiry form.

## Checks

```powershell
python check_site.py
node --check app.js
node --check pages.js
```

The checker validates internal page/anchor destinations, local script/style assets, unique IDs, one H1 per page, and reachability from the homepage.

Browser verification covered navigation, language persistence, gallery filtering and lightbox dismissal, inquiry preparation with the correct preselected interest, and all 12 new pages at a 390px viewport. No horizontal page overflow or console errors were observed. No test inquiry was transmitted.

## Booking and content

The standalone form prepares a message for review, then provides a WhatsApp link. It does not store bookings or collect payments. Sending the message and confirming details with a representative are separate steps. Images are stock lifestyle inspiration. New content describes proposed experiences; operating status, availability and commercial terms must come from the project team. Existing homepage claims have been retained from the supplied content.

Changes are local. No website has been deployed by this update.

Homepage reference refresh: verified desktop proportions, 390px mobile layout without horizontal overflow, mobile menu, slideshow next/pause controls, video information dialog, and internal links. The video panel links to project-video information; it is not an embedded live stream.

Site-wide design alignment: all 12 inner pages now match the homepage with framed ivory panels, emerald navigation and gold accents. Verified internal links, active page indicators, language persistence, mobile navigation and all 12 inner pages at 390px without horizontal overflow.
