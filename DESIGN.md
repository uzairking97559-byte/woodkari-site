---
name: Woodkari Exports
description: Wooden and resin trays and boxes from a Sambhal workshop, shown plainly and ordered on WhatsApp.
colors:
  royal-navy: "#15214a"
  zari-gold: "#c9a25a"
  antique-bronze: "#7d5a1c"
  antique-bronze-deep: "#5f4413"
  whatsapp-green: "#0f7a4c"
  whatsapp-green-deep: "#0b613c"
  night-ink: "#181a24"
  slate-soft: "#545766"
  paper-white: "#ffffff"
  warm-stone: "#f6f1e7"
  sand-hairline: "#e5dfd3"
  photo-field: "#f7f5f1"
  navy-cream-text: "#efe6d2"
typography:
  display:
    fontFamily: "Young Serif, Georgia, Times New Roman, serif"
    fontSize: "clamp(38px, 9.6vw, 74px)"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Young Serif, Georgia, Times New Roman, serif"
    fontSize: "clamp(30px, 4.2vw, 46px)"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  title-serif:
    fontFamily: "Young Serif, Georgia, Times New Roman, serif"
    fontSize: "26px"
    fontWeight: 400
    lineHeight: 1.1
  title:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.3
  body:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  body-small:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "14.5px"
    fontWeight: 400
    lineHeight: 1.35
  label:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "12.5px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.02em"
  price:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, sans-serif"
    fontSize: "16.5px"
    fontWeight: 600
    fontFeature: "tnum, lnum"
  logo:
    fontFamily: "Rozha One, Georgia, serif"
    fontSize: "26px"
    fontWeight: 400
    lineHeight: 1
    letterSpacing: "0.01em"
rounded:
  tag: "2px"
  base: "4px"
  logo-tile: "8px"
spacing:
  gutter-mobile: "16px"
  gutter-desktop: "32px"
  container: "1240px"
  section: "72px"
  section-tight: "56px"
  band-gap: "80px"
  close: "112px"
components:
  button-whatsapp:
    backgroundColor: "{colors.whatsapp-green}"
    textColor: "{colors.paper-white}"
    typography: "{typography.title}"
    rounded: "{rounded.base}"
    padding: "12px 24px"
    height: "52px"
  button-whatsapp-hover:
    backgroundColor: "{colors.whatsapp-green-deep}"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.night-ink}"
    rounded: "{rounded.base}"
    padding: "12px 24px"
    height: "52px"
  button-line-hover:
    backgroundColor: "{colors.night-ink}"
    textColor: "{colors.paper-white}"
  chip:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.night-ink}"
    rounded: "{rounded.base}"
    padding: "8px 18px"
    height: "42px"
  chip-selected:
    backgroundColor: "{colors.royal-navy}"
    textColor: "{colors.paper-white}"
  picture-tag:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.night-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    padding: "4px 8px"
  product-photo:
    backgroundColor: "{colors.photo-field}"
    rounded: "{rounded.base}"
  fact-bar:
    backgroundColor: "{colors.royal-navy}"
    textColor: "{colors.navy-cream-text}"
    padding: "8px 12px"
---

# Design System: Woodkari Exports

## Overview

**Creative North Star: "The Sambhal Showroom"**

A calm, well-lit showroom for a real workshop: white walls, square photos of each piece, and a royal-navy shopfront with a thread of gold. The pieces lead; type and colour step back so the tray, its size and its price are read first. It sits in the category standard of Indian home-decor shops at the level of Nicobar and Ellementry, played straight, with the bulk offer never more than one tap away.

Density is generous on a phone first: one idea per section, 72px between sections, hairline rules instead of boxes, photography square and edge-to-edge in its frame. Royal navy carries the brand moments (the fact bar, the fact ribbon, the bulk band, the footer) and zari gold is its ornament, used only on navy. Everything clickable to buy is WhatsApp green. Motion is slow and soft: the hero crossfades between four photos, a single ribbon of shop facts drifts across the screen, sections rise into place once.

The build refuses the craft-fair page: no cream-on-cream with a giant serif, no icon-card grids, no testimonial props. Every picture that is not a real photo says so on its face.

**Key Characteristics:**
- White ground, warm stone bands, royal navy brand bands with a 3px gold top rule.
- Young Serif for headings, Hanken Grotesk for everything a buyer reads to decide, Rozha One for the wordmark only.
- Square product photos on one pale field, 4px corners, no card chrome.
- WhatsApp green is the only buying colour.
- Slow ease-out motion; all of it stops under reduced motion.

## Colors

A white-and-stone shop floor framed by royal navy and threaded with gold, with one green reserved for the order button.

### Primary
- **Royal Navy** (#15214a): the brand surface. The top fact bar, the moving fact ribbon, the "how a bulk order works" band, the footer, the selected filter chip and the progress fill of the hero dots. Text on it is Navy Cream (#efe6d2) or white.

### Secondary
- **Zari Gold** (#c9a25a): ornament on navy only. The dots between bar facts, the diamonds in the ribbon, the 3px top rule of navy bands and the footer, step numbers inside the navy band, footer column labels and the footer's SAMBHAL line.
- **Antique Bronze** (#7d5a1c, deep #5f4413): the text accent on light grounds. Links, nav hover and current page, focus rings, text selection, step numbers on white and stone, the SAMBHAL line under the header logo, and the "bulk only" price.

### Tertiary
- **WhatsApp Green** (#0f7a4c, hover #0b613c): every WhatsApp action and nothing else, white label on it (5.4:1).

### Neutral
- **Night Ink** (#181a24): headings, body text, the outline button and its filled hover.
- **Slate Soft** (#545766): secondary copy, captions, short descriptions, breadcrumbs.
- **Paper White** (#ffffff): page ground, header (88% with blur), picture tags.
- **Warm Stone** (#f6f1e7): hero ground and the alternate full-width band.
- **Sand Hairline** (#e5dfd3): every rule and border on light grounds; on stone it darkens to #ddd3c1, on navy it is white at 16%.
- **Photo Field** (#f7f5f1): the field behind product and design photos while they load.

### Named Rules
**The Gold-On-Navy Rule.** Zari gold appears only on royal navy. On white it fails contrast and reads as decoration; on light grounds the accent is Antique Bronze.

**The One Green Rule.** WhatsApp green is the order button and the order button is WhatsApp green. No other element, state or illustration uses it.

## Typography

**Display Font:** Young Serif (with Georgia, Times New Roman)
**Body Font:** Hanken Grotesk (with system-ui, -apple-system, Segoe UI)
**Logo Font:** Rozha One (wordmark only)

**Character:** a soft, slightly old-shop serif for names and section heads, paired with a clear grotesk for every fact a buyer acts on: size, material, price, minimum.

### Hierarchy
- **Display** (400, clamp(38px, 9.6vw, 74px), 1.1, -0.015em): the home hero headline only, max 10.5em wide.
- **Headline** (400, clamp(30px, 4.2vw, 46px), 1.1): section heads, split-section heads and the closing call. Product page titles use clamp(32px, 4.4vw, 48px); the bulk page title clamp(36px, 5vw, 60px).
- **Serif title** (400, 19 to 26px, 1.1 to 1.2): photo captions on tiles (26px), slide names (21px), mobile menu links (22px), the fact ribbon (19px), step numbers (26px).
- **Title** (600, 17px, 1.3, sans): product names under a photo.
- **Body** (400, 17px, 1.6): running copy; leads at 18px in Slate Soft, capped near 30 to 36em.
- **Body small** (400, 14.5 to 16px): short descriptions, facts lists, breadcrumbs.
- **Price** (600, 16.5px on cards, 24px on the product page, tabular lining figures): the "per piece" suffix drops to 400 Slate Soft.
- **Label** (600, 12 to 12.5px, 0.02em): picture tags. Footer column heads are the one uppercase label (600, 13px, 0.14em, Zari Gold).

### Named Rules
**The Facts-In-Sans Rule.** Sizes, prices, minimums and materials are always set in Hanken Grotesk with tabular figures. The serif names things; it never carries a number a buyer must act on, except the ornamental step counters.

**The Wordmark-Only Rule.** Rozha One is the logo. It never sets a headline.

## Layout

A single 1240px container with 16px gutters on phones and 32px from 760px. Phones are the main screen: grids collapse to two columns of products, tile rows and design rows become horizontal snap-scrollers that bleed to the screen edge, and the product page gallery becomes a swipe strip of 88%-wide frames.

Sections are separated by 72px (56px when tight); full-width stone and navy bands sit 80px from what precedes them and carry 72px inner padding. The closing call has 112px above it; the footer starts 88px below.

The home hero is a split from 900px: text on the left (46%), aligned to the container edge, and a 54% slideshow on the right at min(100vh minus 150px, 760px) tall. Below 900px the slideshow is a square above the text.

The product grid is two columns (gaps 32px by 14px) up to 760px, then three (48px by 28px); bulk page grids go to four. Product pages split 1.2fr to 1fr from 960px with the buying column sticky at 96px; below that a sticky bottom bar carries the price and the WhatsApp button.

Breakpoints in use: 420px (header button drops its label), 760px, 900px, 960px.

## Elevation & Depth

Flat. Depth comes from tone (white, stone, navy) and from photography, never from lifted cards. The header is translucent white with an 8px backdrop blur over content. The only shadow in the shipped pages is the mobile menu's drop (`0 18px 30px -18px rgba(40,20,10,.35)`), which lifts the open panel off the page. Photos carry their own depth: captions on tiles and slides sit on a bottom gradient scrim (`linear-gradient(to top, rgba(18,12,8,.78), transparent)`).

### Named Rules
**The No-Lift Rule.** Cards, photos and buttons never take a shadow. Hover is a change of tone or a slow image zoom, not elevation.

## Shapes

Gently squared: 4px corners on photos, buttons, chips and tiles; 2px on the small picture tags; 8px on the logo tile. Borders are 1px hairlines (Sand Hairline), used as row rules in steps and facts lists and as list dividers, never as boxes around content. The outline button draws its 1px edge with an inset shadow so it keeps the same size as filled buttons. The one ornamental geometry is the gold diamond (6px square rotated 45 degrees) between ribbon facts, and the 3px gold dot between bar facts.

## Components

### Buttons
Plain and sure-footed; one green that means "order".
- **Shape:** gently squared (4px), 52px tall, 12px by 24px padding, 600 weight at 16.5px, an icon gap of 9px.
- **WhatsApp (primary):** WhatsApp Green with white label and the WhatsApp mark inline as SVG; deepens on hover. In the header it shrinks to 42px and drops its label under 420px.
- **Line (secondary):** transparent with a 1px Night Ink inset edge; fills ink with white text on hover. Inside the navy band it inverts to a white edge and fills white with navy text.
- **Text link with rule:** 600 Night Ink with a 1px underline rule, both turning Antique Bronze on hover; used for "see all" style moves.
- **Focus:** 2px Antique Bronze outline, 3px offset, everywhere.

### Chips
- **Style:** white, 1px Sand Hairline border, 4px corners, 42px tall, 500 weight 15px. Border turns ink on hover.
- **State:** the selected filter fills Royal Navy with white text. Chips scroll horizontally on phones.

### Cards / Containers
- **Product card:** no box. A square photo on the Photo Field with 4px corners, then the name (Title), a short line in Slate Soft, and the price. Bulk-only items show the price line in Antique Bronze.
- **Collection tile:** a 3:4 photo with the place name in 26px serif white on a dark bottom scrim; 72% wide in a snap row on phones, four across from 760px; the photo zooms to 1.04 over 1s on hover.
- **Bands:** Warm Stone and Royal Navy full-width bands hold split sections (square photo beside text, 64px gap from 900px).

### Navigation
- **Fact bar:** a slim Royal Navy strip above the header, 13px Navy Cream text, facts separated by gold dots.
- **Header:** sticky, 64px, translucent white with blur and a hairline bottom. Logo tile and Rozha One wordmark with a tracked SAMBHAL line left; nav links 500 at 15.5px in ink, Antique Bronze on hover and for the current page; WhatsApp button right.
- **Mobile menu:** a 44px icon toggle (burger to cross) under 900px opens a white panel below the header with 22px serif links on hairline rows and a full-width WhatsApp button.
- **Footer:** Royal Navy with a 3px gold top rule, three columns from 760px, gold uppercase column labels, white links turning gold on hover.

### Picture Tag (signature)
A small white label (2px corners, 12.5px 600) pinned to the top-left of any photo that is not a real photograph: "Design picture" or "Styled picture". It is part of the system, not an afterthought: every non-real picture carries one.

### Hero Slideshow (signature)
Four photos, resin trays first, crossfading over 1.1s with a slow 7s zoom from 1.07 to 1. Each slide links to its piece, with the name in 21px serif on a bottom scrim. Under the text sit progress dots: thin 2px tracks that fill Royal Navy over 5.5s, labelled with the piece name from 900px. Hover or focus pauses it.

### Fact Ribbon (signature)
A Royal Navy band under the hero where shop facts in 19px serif drift left on a 38s loop, separated by gold diamonds; it pauses on hover and is hidden from screen readers.

### Numbered Steps
A list with hairline rows, each led by a 26px serif counter in Antique Bronze (Zari Gold inside the navy band), a bold step and a Slate Soft line beneath.

### Sticky Buy Bar
On product pages under 960px, a fixed white bar with a hairline top holds the price (18px, tabular) and a full-width WhatsApp button, padded for the safe area.

## Do's and Don'ts

### Do:
- **Do** use WhatsApp Green (#0f7a4c) for every WhatsApp action and only for those.
- **Do** keep Zari Gold (#c9a25a) on Royal Navy (#15214a); use Antique Bronze (#7d5a1c) for links and accents on white or stone.
- **Do** show each piece as a square photo on the Photo Field with 4px corners, and put a "Design picture" or "Styled picture" tag on every picture that is not a real photo.
- **Do** set sizes, prices and minimums in Hanken Grotesk with tabular figures.
- **Do** separate content with 1px hairline rules and tone bands, 72px between sections.
- **Do** use the shared ease-out (cubic-bezier(.16,1,.3,1)) for every transition, and let reduced motion switch all motion off.

### Don't:
- **Don't** put gold text or gold rules on white or stone grounds.
- **Don't** give cards, photos or buttons a shadow, or wrap products in bordered boxes.
- **Don't** build grids of icon cards, testimonial blocks or client-logo strips.
- **Don't** set a headline in Rozha One, or a number a buyer acts on in the serif.
- **Don't** put a small uppercase label above a headline; tracked uppercase is for footer column heads only.
- **Don't** add a second moving element beside the hero slideshow and the fact ribbon; sections rise once and then stay still.
