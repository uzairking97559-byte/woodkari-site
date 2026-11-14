---
name: Woodkari Exports
description: Wooden and resin trays and boxes from Sambhal, shown on white and forest green and ordered on WhatsApp.
colors:
  forest-green: "#1d4a3a"
  forest-deep: "#143629"
  soft-gold: "#d6b877"
  brass: "#8a6a2c"
  paper: "#ffffff"
  stone: "#f2efe9"
  stone-deep: "#e8e4da"
  mist: "#eaf0ec"
  hairline: "#e2dfd6"
  ink: "#17201b"
  moss-soft: "#56605a"
  on-green-muted: "#cfdcd3"
typography:
  display:
    fontFamily: "Instrument Serif, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(76px, 9.4vw, 140px)"
    fontWeight: 400
    lineHeight: 0.9
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Instrument Serif, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(40px, 5.6vw, 76px)"
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: "-0.022em"
  title:
    fontFamily: "Instrument Serif, Iowan Old Style, Georgia, serif"
    fontSize: "25px"
    fontWeight: 400
    lineHeight: 1.15
  wordmark:
    fontFamily: "Instrument Serif, Iowan Old Style, Georgia, serif"
    fontSize: "36px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  product-name:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "18px"
    fontWeight: 500
    lineHeight: 1.3
  price:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "18px"
    fontWeight: 600
    fontFeature: "tnum, lnum"
  button:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.005em"
  label:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "12.5px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.02em"
rounded:
  tag: "2px"
  sm: "3px"
  round: "50%"
spacing:
  gutter: "18px"
  gutter-wide: "36px"
  section: "64px"
  section-wide: "96px"
  close: "88px"
  close-wide: "128px"
  container: "1280px"
components:
  button-primary:
    backgroundColor: "{colors.forest-green}"
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "12px 26px"
    height: "52px"
  button-primary-hover:
    backgroundColor: "{colors.forest-deep}"
    textColor: "{colors.paper}"
  button-line:
    textColor: "{colors.forest-green}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "12px 26px"
    height: "52px"
  button-line-hover:
    backgroundColor: "{colors.forest-green}"
    textColor: "{colors.paper}"
  button-inverse:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.forest-green}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "12px 26px"
    height: "52px"
  button-inverse-hover:
    backgroundColor: "{colors.soft-gold}"
    textColor: "{colors.forest-deep}"
  button-ghost:
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "12px 26px"
    height: "52px"
  button-ghost-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.forest-green}"
  header-whatsapp:
    backgroundColor: "{colors.forest-green}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: "8px 18px"
    height: "44px"
  icon-button:
    textColor: "{colors.ink}"
    rounded: "{rounded.round}"
    size: "44px"
  icon-button-hover:
    backgroundColor: "{colors.mist}"
    textColor: "{colors.forest-green}"
  whatsapp-fab:
    backgroundColor: "{colors.forest-green}"
    textColor: "{colors.paper}"
    rounded: "{rounded.round}"
    size: "56px"
  picture-tag:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "5px 7px"
  product-photo:
    backgroundColor: "{colors.stone}"
    rounded: "{rounded.sm}"
  price-tag:
    textColor: "{colors.forest-green}"
    typography: "{typography.price}"
  band-green:
    backgroundColor: "{colors.forest-green}"
    textColor: "{colors.on-green-muted}"
    padding: "96px 0"
  band-stone:
    backgroundColor: "{colors.stone}"
    textColor: "{colors.ink}"
    padding: "96px 0"
  footer:
    backgroundColor: "{colors.forest-deep}"
    textColor: "{colors.on-green-muted}"
---

# Design System: Woodkari Exports

## Overview

**Creative North Star: "The Green Showroom"**

A large Indian decor shop's catalogue, made by a small workshop. The page is mostly white paper with greige stone bands; forest green is the one brand field, laid down in whole panels (the desktop hero panel, the bulk band, the footer) and in the small things a buyer acts on (buttons, prices, links, the focus ring). A light, high-contrast serif carries the voice at large sizes; a plain grotesk carries every size, price, fact and button. Pictures lead: every section is built around a square photo or a full-bleed slideshow, and every picture that is not a plain photo of a real piece wears a small white label saying so.

Density is calm and catalogue-like: two product columns on a phone, three on a desktop, generous section spacing (64px phone, 96px desktop), hairline rules instead of boxes. Motion is slow and physical, on a single long-tail ease: headings rise out of a slot, card pictures are uncovered by a stone curtain, the hero crossfades with a slow zoom-out, and a tapped product picture travels into its product page.

The owner rejected two earlier looks, navy with gold and walnut brown ("blue achha nahi lag raha", "AI jaisi lag rahi hai"); this green world replaced both. A paper-grain texture on the green fields was tried and removed in the 15 Nov review.

**Key Characteristics:**
- White paper ground, greige stone bands, forest green as the single brand field.
- Gold appears only on green; on white or stone the metal is brass.
- Instrument Serif at display sizes only, always regular weight; Hanken Grotesk for everything a buyer reads to decide.
- 3px corners, hairline rules, flat surfaces; circles only for icon buttons and the WhatsApp button.
- Square photos on a stone ground, every non-real picture labelled.
- One ease (`cubic-bezier(.16,1,.3,1)`), press feedback on every tap, hover effects for mouse pointers only.

## Colors

A white-and-stone catalogue with one deep forest green and two metals used sparingly.

### Primary
- **Forest Green** (forest-green): the brand field. Desktop hero panel and the phone hero's text block, the bulk band, primary and header WhatsApp buttons, the floating WhatsApp button, every price, links, the active tab underline, the focus ring, text selection and the browser `theme-color`.
- **Forest Deep** (forest-deep): the footer ground and the hover state of primary buttons (wipes up from the bottom edge).

### Secondary
- **Soft Gold** (soft-gold): the warm accent on green only. Step numerals in the green band, the active slideshow progress bar on desktop, the price inside the slide name chip, footer column headings, footer link hover, and the inverse button's hover fill.
- **Brass** (brass): the metal on light grounds. Step numerals on white and stone, and the small rotated-square marks between ribbon phrases.

### Neutral
- **Paper** (paper): page ground, header, drawer, search sheet, sticky buy bar, inverse buttons, picture labels (at 94% opacity).
- **Stone** (stone): the greige band behind the workshop section and the ribbon, and the ground behind every product photo, so studio pictures with white backgrounds sit on one backdrop (photos multiply onto it).
- **Stone Deep** (stone-deep): the curtain that lifts off a product card's picture on reveal.
- **Mist** (mist): the round hover wash behind header icon buttons.
- **Hairline** (hairline): every rule: header and tab borders, list and FAQ dividers, fact rows, the sticky bar's top edge.
- **Ink** (ink): headings and body text on light grounds.
- **Moss Soft** (moss-soft): secondary text: short descriptions, fact labels, crumbs, FAQ answers, notes.
- **On-green Muted** (on-green-muted): body and step text inside the green band and the footer.

### Named Rules
**The Green Field Rule.** Forest green is laid down as a whole field or as the thing a buyer acts on. It is never a tint, a gradient wash or a decorative stripe; every price and every primary action is green, and nothing decorative is.

**The Gold-on-Green Rule.** Soft gold appears only on a green surface. On white or stone the same role goes to brass. A gold element on white is a defect.

## Typography

**Display Font:** Instrument Serif (with Iowan Old Style, Georgia, serif), self-hosted, regular and italic.
**Body Font:** Hanken Grotesk (with system-ui, -apple-system, Segoe UI, sans-serif), self-hosted variable 400-700, Latin and Latin Extended.

**Character:** A light, narrow, high-contrast serif that reads as a decor brand at large sizes, set against a friendly, plain grotesk that makes sizes and prices easy to read on a phone.

### Hierarchy
- **Display** (400, `clamp(76px, 9.4vw, 140px)` desktop, `clamp(46px, 14.4vw, 64px)` phone; line-height 0.9-0.92; -0.03em): the hero headline only, two lines that each rise out of a masked slot on load. On short desktop windows (height 800px or less) it drops to `clamp(64px, 7.4vw, 104px)`.
- **Headline** (400, `clamp(40px, 5.6vw, 76px)`, 0.98, -0.022em): every section heading, the closing heading, and the h1 of product and bulk pages. One scale for all of them.
- **Title** (400 serif, 25-30px, 1.05-1.15): FAQ questions (25px), drawer menu links (27px), the search field (26px), tile captions (30px), the ribbon phrases (21px), and the workshop paragraph, which is set large (`clamp(25px, 3vw, 40px)`, 1.2) and lit word by word as it scrolls into view.
- **Wordmark** (400 serif 31px phone / 36px desktop, -0.01em) over **SAMBHAL** (Hanken 600, 11px, tracking 0.42em): the centred logo in the header. The footer repeats the name at 34px and, as its signature, edge to edge at `min(30.5vw, 470px)` in a tone barely lighter than the footer ground.
- **Body** (400, 17px, 1.6): all running text; leads and FAQ answers capped at 32-44em.
- **Product name** (500, 16.5px phone / 18px desktop, 1.3) with a short line under it (14-15px, moss soft).
- **Price** (600, 17-18px on cards, 25px on product pages, tabular lining figures, forest green); the unit ("/ set of 2") in 400 moss soft.
- **Button** (600, 16px, 1.2, 0.005em).
- **Label** (600, 12.5px, 0.02em): picture labels and gallery captions. Footer column headings are the one uppercase label (600, 12.5px, tracking 0.16em, soft gold).

### Named Rules
**The Serif Speaks, the Sans Sells Rule.** Instrument Serif carries headings, the wordmark, questions and the ribbon; anything with a number, a size, a price, a fact or a button is Hanken Grotesk. Product names are sans, because they sit with their price.

**The Regular Serif Rule.** The serif is only ever weight 400. Emphasis comes from size and the slot-rise, never from bold or a faux weight.

## Layout

A centred container (max 1280px) with an 18px side gutter on phones and 36px from 760px. Sections are separated by space, not boxes: 64px on phones, 96px from 900px; the closing call sits 88px / 128px from the content above it, and the footer the same again below it. Full-bleed bands (green, stone) reuse the same 64px / 96px inner padding.

- **Header:** sticky, 62px phone / 76px desktop, three-column grid with the wordmark centred; a category tab row sits under it and tucks away upward while scrolling down, returning on scroll up.
- **Hero:** phone: a square slideshow (max 62svh) with the headline overlapping its lower edge on a gradient that melts into forest green. From 900px: a 46/54 split, green text panel left aligned to the container edge, slideshow right, height `min(100svh - 131px, 780px)`.
- **Product grid:** 2 columns (gap 30px 12px) on phones, 3 from 760px (gap 56px 28px); a 4-column variant for the bulk page.
- **Split blocks:** one column on phones, two equal columns with a 72px gap from 900px, picture and text alternating sides.
- **Scrollers:** use tiles and design strips scroll sideways with mandatory snap on phones, bleeding to the screen edge with the gutter kept as scroll padding; from 760px they become 4- and 6-column grids.
- **Product page:** gallery and buy column at 1.2fr / 1fr with a 72px gap from 960px; the buy column is sticky. On phones the gallery is a snap strip with a scroll-linked progress line, and a fixed buy bar (price and WhatsApp button) sits at the bottom.
- **Breakpoints:** 760px (gutter, grid columns), 900px (header, hero split, section spacing), 960px (product page).

The direction contract described a 4:5 phone slideshow with the text over the picture, and a desktop headline up to 96px. The shipped build moved to a square picture with the headline below its edge, and a desktop headline up to 140px; the build is the record.

## Elevation & Depth

Flat. Depth comes from tonal grounds (white, stone, green, deep green), hairlines, and photos, not from shadows. Two elements cast a shadow, both because they float over content: the header once the page scrolls, and the floating WhatsApp button. Text on photos gets a soft shadow on the phone hero only.

### Shadow Vocabulary
- **Header lift** (`box-shadow: 0 1px 0 #e2dfd6, 0 10px 30px -22px rgba(20,54,41,.5)`): under the sticky header after the page scrolls.
- **Floating button** (`box-shadow: 0 0 0 1.5px rgba(255,255,255,.5), 0 10px 26px -6px rgba(12,40,28,.5)`): the WhatsApp button, with a thin white ring so it reads on green.
- **Hero text** (`text-shadow: 0 2px 22px rgba(10,26,19,.45)`): phone hero headline over the picture's edge.

### Named Rules
**The Flat Catalogue Rule.** Cards, photos, bands and buttons have no shadow. Only what floats over the page (sticky header, floating button) is lifted.

## Shapes

Nearly square. Buttons, photos, product cards, tiles and the header WhatsApp button share one small 3px radius; picture labels and the slide name chip are 2px. Circles are kept for 44px icon buttons (menu, search, close, pause) and the 56px WhatsApp button. Rules are 1px hairlines; the search field is underlined with a 1.5px ink rule; the active tab is a 2px green underline that grows from the left. Pill shapes are not used.

## Components

### Buttons
Tactile and quiet: a solid block of colour with a fill that wipes up from the bottom edge on hover.
- **Shape:** 3px corners, minimum height 52px (48px in the sticky bar), padding 12px 26px, icon and label 10px apart.
- **Primary:** forest green with white text. The default action, usually "Chat on WhatsApp" or "Order on WhatsApp" with the WhatsApp glyph.
- **Line:** transparent with a 1px green inset ring and green text; the second action (email).
- **Inverse:** white with green text, used on green grounds; hover fill is soft gold with forest-deep text.
- **Ghost:** transparent with a 1px white ring (75%) and white text, used on green beside an inverse button; hover fill is white with green text.
- **Hover / Focus / Press:** on mouse pointers the hover colour wipes up from the bottom in 0.45s and a trailing arrow slides 5px right. Focus is a 2px green outline at 3px offset (white on green grounds). Press scales to 0.97 in 160ms.

### Picture labels
- **Style:** white at 94% opacity, ink text, label type (12.5px, 600), 2px corners, 5px 7px padding, bottom-left of the picture (top-right on tiles and slides).
- **Wording:** "Design picture", "Styled picture", "Our piece, plain photo".

### Product cards
- **Corner Style:** 3px on the photo; the card itself has no box.
- **Background:** square photo on stone; studio photos multiply onto the stone so white backgrounds vanish. A second, in-use picture fades in on mouse hover.
- **Content:** name (sans 500), short line (moss soft), price (green 600, tabular).
- **Reveal:** a stone-deep curtain lifts off the photo while it settles from 1.12 scale; the text fades in after; cards on one row stagger left to right (0, 70, 120, 150ms).
- **Press:** photo scales to 0.98.

### Navigation
- **Header:** white, centred serif wordmark, menu (phone) and search icon buttons, "Made in Sambhal since 2008" note and a green WhatsApp button from 900px.
- **Tabs:** 15.5px Hanken 500 in ink, active tab 600 green with a 2px green underline; on phones the row scrolls sideways.
- **Drawer:** slides in from the left (88vw, max 400px) with serif 27px links on hairlines and a full-width primary button at its foot.
- **Search:** a sheet that drops from the top with a 26px serif field and photo results.

### Lists: steps, facts, questions
- **Steps:** numbered rows on hairlines with a 32px serif numeral in brass (soft gold on green), bold step and moss-soft detail.
- **Facts:** two-column rows (label 8.2em, moss soft 500) on hairlines.
- **Questions:** serif 25px summaries on hairlines with a plus that turns to a cross (135°), answers open by height animation; only one open at a time.

### Hero slideshow
Four square resin-tray pictures crossfade (1s) with a 7s slow zoom-out; the progress bars under the text are the clock (5.5s each), with a pause button beside them. A name chip in deep green with the price in soft gold sits on each picture. Swipe changes the picture on phones.

### Ribbon
A stone strip under the hero with serif 21px phrases in green, separated by small brass rotated squares, scrolling slowly (40s) with faded ends; it pauses on mouse hover.

### Floating WhatsApp button
A 56px green circle, bottom right, that steps aside (scales to 0.6 and fades) when the closing call or footer, which hold their own WhatsApp buttons, are on screen; hidden from 900px and on product pages with a buy bar.

### Footer
Forest-deep ground, a three-column grid of name and summary, shop links and contact, a hairline above the fine print on picture labels, and the name set edge to edge underneath in a tone barely off the ground, rising into place when it scrolls into view.

## Do's and Don'ts

### Do:
- **Do** lay forest green down as whole fields (hero panel, bulk band) and on every price and primary action.
- **Do** put soft gold only on green and use brass for the same roles on white and stone.
- **Do** set headings in Instrument Serif at weight 400, and sizes, prices, facts and buttons in Hanken Grotesk.
- **Do** keep corners at 3px (2px for picture labels) and reserve circles for icon buttons and the WhatsApp button.
- **Do** show products as square photos on the stone ground, and label every picture that is not a plain photo of a real piece.
- **Do** separate content with 1px hairlines and space, and keep cards, photos and bands flat.
- **Do** give every tappable thing a 160ms press response, keep hover effects behind a fine-pointer media query, and switch all motion off under reduced motion.
- **Do** use the one ease, `cubic-bezier(.16,1,.3,1)`, for state changes and reveals.

### Don't:
- **Don't** bring back navy with gold, or walnut brown, as the site palette; the owner rejected both.
- **Don't** put gold on a white or stone ground.
- **Don't** set the serif in bold, or set prices and facts in the serif.
- **Don't** use pill-shaped buttons; the header WhatsApp button was squared to 3px in the 15 Nov review.
- **Don't** add drop shadows to cards, photos or bands.
- **Don't** put a grain or noise texture on the green fields; it was removed in the 15 Nov review.
