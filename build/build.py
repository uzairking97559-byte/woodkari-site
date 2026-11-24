#!/usr/bin/env python3
"""Builds the Woodkari shop (static HTML) into an output folder.

  python3 build/build.py v2        -> preview at /v2/ (noindex)
  python3 build/build.py .         -> live site at the root

Edit PRODUCTS, WHATSAPP and prices here, then rebuild. No other tooling.
Every fact below must be OWNER-said or READ from a source (agency-research ops/fact_check_14nov.md).
"""
import html, json, os, re, sys, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "v2"
PREVIEW = OUT != "."
SITE = "https://woodkariexports.com"
BASE = SITE + ("" if OUT == "." else "/" + OUT)
UP = "" if OUT == "." else "../"  # assets live at the root; a preview folder points one level up

PIXEL_ID = "1148906040829800"  # Meta Pixel ID (owner approved 19 Nov); empty = no pixel code on any page
WHATSAPP = "916397121223"
EMAIL = "sales@woodkariexports.com"

# imgs: (file key, alt, caption). card: (studio key, in-use key) for the shop grid.
PRODUCTS = [
    dict(slug="navy-ivory-floral-tray", name="Navy & Ivory Floral Tray", cat="resin", price=1999, mto=True,
         title="Navy & Ivory Floral Resin Tray, Made to Order | Woodkari",
         desc="Ivory tray with a navy floral pattern filled in resin and a handle cut into each side. 14 × 8 inches. Made to order in India.",
         short="Resin · 14 × 8 in, cut-out handles", card=("navy-top", "navy-front"),
         lede="An ivory tray with a navy floral pattern filled in resin, and a handle cut into each side.",
         uses="Tea for two, or a tray for the dressing table.",
         facts=[("Size", "14 × 8 inches (36 × 20 cm), rim 2 inches high"), ("Top", "Pattern filled in resin"), ("Core", "MDF wood board"),
                ("Made in", "India")],
         imgs=[("navy-front", "Navy and ivory floral tray on a wooden table", "Made to order"),
               ("navy-use", "Navy and ivory floral tray carrying two cups of tea and biscuits", "Made to order"),
               ("navy-top", "Navy and ivory floral tray seen from above", "Made to order"),
               ("navy-white", "Navy and ivory floral tray on a plain white background", "Made to order"),
               ("navy-side", "Navy and ivory floral tray seen from the side on a wooden table", "Made to order"),
               ("navy-close", "Navy and ivory floral tray: close view of the floral pattern and a cut-out handle", "Made to order"),
               ("navy-hands", "Navy and ivory floral tray held in two hands", "Made to order"),
               ("navy-stack", "Five navy and ivory floral trays stacked, for bulk orders", "Made to order")]),
    dict(slug="black-white-floral-tray-set", name="Black & White Floral Tray Set", cat="resin", price=6999, unit="set of 2", mto=True,
         title="Black & White Floral Resin Tray Set, Made to Order | Woodkari",
         desc="A round and a rectangular tray with a black and white floral pattern in the look of bone inlay, filled in resin. Made to order in India.",
         short="Resin · one round, one rectangular", card=("bw-top", "bw-front"),
         lede="A round tray and a rectangular tray with a black and white floral pattern, in the look of bone inlay, filled in resin.",
         uses="A pair for the dining table or the living room.",
         facts=[("In the set", "1 round tray and 1 rectangular tray"), ("Size", "Rectangle 18 × 10 inches (46 × 25 cm). Round tray: size on request"), ("Top", "Pattern filled in resin"),
                ("Core", "MDF wood board"), ("Made in", "India")],
         imgs=[("bw-front", "Black and white floral tray set, one round and one rectangular tray, on a wooden table", "Made to order"),
               ("bw-use", "Black and white floral tray set with tea and snacks on a dining table", "Made to order"),
               ("bw-top", "Black and white floral tray set, the two trays side by side, seen from above", "Made to order"),
               ("bw-white", "Black and white floral tray set on a plain white background", "Made to order"),
               ("bw-side-round", "Round tray of the black and white floral tray set, seen from the side", "Made to order"),
               ("bw-close", "Black and white floral tray set: close view of the floral pattern", "Made to order")]),
    dict(slug="red-chevron-tray", name="Red Chevron Tray", cat="resin", price=2799, mto=True,
         title="Red Chevron Resin Tray, 16 × 10 in, Made to Order | Woodkari",
         desc="White-framed tray with a red and white chevron pattern filled in resin. 16 × 10 inches, rim 2 inches high. Made to order in India.",
         short="Resin · 16 × 10 in, red and white zigzag", card=("chevron-top", "chevron-front"),
         lede="A white-framed rectangular tray with a red and white chevron pattern filled in resin.",
         uses="Breakfast in bed, or a bright tray for the kitchen counter.",
         facts=[("Size", "16 × 10 inches (41 × 25 cm), rim 2 inches high"), ("Top", "Pattern filled in resin"), ("Core", "MDF wood board"),
                ("Made in", "India")],
         imgs=[("chevron-front", "Red chevron tray: white frame and a red and white chevron pattern, on a wooden table", "Made to order"),
               ("chevron-use", "Red chevron tray carrying a glass jug and two glasses of water", "Made to order"),
               ("chevron-top", "Red chevron tray seen from above", "Made to order"),
               ("chevron-side", "Red chevron tray seen from the side on a wooden table", "Made to order"),
               ("chevron-hands", "Red chevron tray held in two hands", "Made to order"),
               ("chevron-stack", "Five red chevron trays stacked, for bulk orders", "Made to order")]),
    dict(slug="gold-flake-resin-tray", name="Gold-flake Resin Tray", cat="resin", price=None, bulk_only=True, mto=True,
         title="Gold-flake Resin Tray, Bulk Orders from 25 | Woodkari",
         desc="Made all of resin, black with gold flakes and two gold-tone leaf handles. Made to order in India, for bulk orders only, from 25 pieces. ₹799 each.",
         short="All resin · gold flakes, leaf handles", card=("gold-top", "gold-front"),
         lede="Made all of resin, black and marbled with gold flakes, with two gold-tone leaf handles. Made for bulk orders only, from 25 pieces.",
         uses="Serving trays for a hotel, a wedding or a company gift.",
         facts=[("Material", "All resin, no board inside"), ("Colour", "Black with gold flakes"), ("Handles", "Gold-tone leaves"),
                ("Size", "On request"), ("Made in", "India"), ("Orders", "Bulk only, from 25 pieces. ₹799 each")],
         imgs=[("gold-front", "Gold-flake resin tray, black with gold flakes and leaf handles, on a wooden table", "Made to order"),
               ("gold-use", "Gold-flake resin tray holding two bowls of pistachios and almonds", "Made to order"),
               ("gold-top", "Gold-flake resin tray seen from above", "Made to order"),
               ("gold-white", "Gold-flake resin tray on a plain white background", "Made to order"),
               ("gold-side", "Gold-flake resin tray seen from the side on a wooden table", "Made to order"),
               ("gold-close", "Gold-flake resin tray: close view of the gold flakes and a leaf handle", "Made to order"),
               ("gold-stack", "Four gold-flake resin trays stacked, for bulk orders", "Made to order")]),
    dict(slug="fluted-box-tray", name="Fluted Box Tray", cat="wood", price=1299,
         title="Acacia Fluted Box Tray, Bulk from 25 | Woodkari, India",
         desc="Open box tray in acacia wood with fluted sides and a scalloped rim, finished by hand. 11.5 × 7 × 3 inches. Made in our workshop in India.",
         short="Acacia · 11.5 × 7 × 3 in", card=("fluted-real1", None),
         lede="An open box tray in acacia wood. The sides are cut into upright flutes and the rim is scalloped, then the piece is finished by hand to a warm walnut tone.",
         uses="Keys and wallet by the door, a dressing table, a desk, or a gift hamper.",
         facts=[("Size", "11.5 × 7 inches, 3 inches high (29 × 18 × 7.6 cm)"), ("Wood", "Acacia"), ("Finish", "Walnut-tone polish, finished by hand"),
                ("Made in", "Our workshop in India"),
                ("Goes with", "The Room Tray: same 11.5 inch side"),
                ("Other sizes", "Any size, on order"),
                ("Name or logo", "By laser, on 50 pieces or more of one design")],
         imgs=[("fluted-real1", "Fluted box tray, plain photo from the front", "Our piece, plain photo"),
               ("fluted-real2", "Fluted box tray, plain photo from the side", "Our piece, plain photo"),
               ("fluted-real3", "Fluted box tray, plain photo from above", "Our piece, plain photo"),
               ("fluted-front", "Fluted box tray on a wooden table, seen from the front", "Styled picture"),
               ("fluted-use", "Fluted box tray on the floor by a door, holding car keys and a wallet", "Styled picture"),
               ("fluted-top", "Fluted box tray seen from above on a white sheet", "Styled picture")]),
    dict(slug="room-tray", name="Room Tray", cat="wood", price=1799,
         title="Room Tray for Hotels, Acacia Wood, Bulk from 25 | Woodkari",
         desc="Acacia board with round dips and slots, and a four-box caddy: the tea tray of a hotel guest room. 15 × 11.5 inches. Made in our workshop in India.",
         short="Acacia · 15 × 11.5 in, with caddy", card=("room-real1", None),
         lede="A solid acacia board with one large round dip, two small ones and two long slots, and a four-box caddy that stands beside it. Made as the tea tray of a hotel guest room.",
         uses="Kettle and cups in a guest room, or watch, phone and keys on a bedside table.",
         facts=[("Size", "Tray 15 × 11.5 inches (38 × 29 cm). Caddy 10 inches long"), ("Wood", "Acacia"), ("Finish", "Walnut-tone polish, finished by hand"),
                ("Made in", "Our workshop in India"),
                ("Other sizes", "Any size, on order"),
                ("Name or logo", "A hotel name or logo by laser, on 50 pieces or more")],
         imgs=[("room-real1", "Room tray, plain photo from the front", "Our piece, plain photo"),
               ("room-real2", "Room tray, plain photo from the side", "Our piece, plain photo"),
               ("room-real3", "Room tray, plain photo, front view", "Our piece, plain photo"),
               ("room-front", "Room tray on a wooden table with two cups of tea", "Styled picture"),
               ("room-use", "Room tray on a bedside table with a kettle, keys and a phone", "Styled picture"),
               ("room-top", "Room tray seen from above on a white sheet", "Styled picture")])
]

# owner D-334 (22 Nov 18:20): Fluted Box Tray and Room Tray off the site for now ("abhi unki zaroorat nahi"); their data stays here, their URLs redirect to trays.html
PRODUCTS_OFF = {"fluted-box-tray", "room-tray"}
PRODUCTS = [p for p in PRODUCTS if p["slug"] not in PRODUCTS_OFF]

CATS = [("all", "Everything"), ("wood", "Acacia wood"), ("resin", "Resin trays"), ("u1500", "Under ₹1,500")]

# owner list 20 Nov, point 2: product pictures, not only food and drink scenes (each picture is already on its own product page)
TILES = [("bw-front", "On the table", "Black & White Floral Tray Set", "black-white-floral-tray-set.html", "Black and white floral tray set, one round and one rectangular tray, on a wooden table", "Made to order"),
         ("m-bone-inlay-coffee-table-40-e", "In the living room", "Octagon coffee table, bone inlay", "design-ow-40.html", "Octagon coffee table, black and white bone inlay, in a living room", "Made to order"),
         ("m-resin-bathroom-set-1-e", "In the bathroom", "Bathroom set, ivory marble look", "design-bs-1.html", "Resin bathroom set, ivory marble look, on a bathroom counter", "Made to order"),
         ("gold-stack", "For hotels and gifting", "Gold-flake Resin Tray", "gold-flake-resin-tray.html", "Four gold-flake resin trays stacked, for bulk orders", "Made to order")]

SLIDES = [("navy-front", "navy-ivory-floral-tray"), ("bw-front", "black-white-floral-tray-set"),
          ("gold-front", "gold-flake-resin-tray"), ("chevron-front", "red-chevron-tray")]  # owner 18 Nov: no food or drink in the hero

DESIGNS = [("d-coaster", "Resin coaster set"), ("d-tissue", "Resin tissue box"), ("d-roundbox", "Round box with resin lid"),
           ("d-board", "Serving board"), ("d-cutlery", "Cutlery and napkin stand"), ("d-trivet", "Resin trivets")]

# designs.html: 41 design pictures made from the owner's reference PDFs (D-204; owner 15 Nov: "A sab laga do" =
# on the site now as "Design picture, made on order", price on WhatsApp). (group id, code prefix, heading, line, [(file, name)])
MTO = [
    ("painted", "PT", "Painted trays and bowls", "Wooden trays, bowls and boards with a painted (meena) design.", [
        ("wooden-meena-tray-3", "Round tray, peacock feathers"), ("wooden-meena-tray-1", "Oval tray, teal paisley"),
        ("wooden-meena-tray-2", "Tray and bowl, marigold on teal"), ("wooden-meena-tray-4", "Tray with handles, marigold garland"),
        ("wooden-meena-tray-5", "Tray, bowl and servers, red hibiscus"), ("wooden-meena-tray-6", "Bowls and spoon, parrots and mangoes"),
        ("wooden-meena-tray-7", "Round tray and bowls, pink lotus"), ("wooden-meena-tray-8", "Board, bowl and servers, small flowers"),
        ("wooden-meena-tray-9", "Tray, Warli village scene")]),
    ("bath", "BS", "Resin bathroom sets", "Soap dispenser, tumbler, tray and more, in resin.", [
        ("resin-bathroom-set-1", "Bathroom set, ivory marble look"), ("resin-bathroom-set-2", "Bathroom set, green malachite look"),
        ("resin-bathroom-set-3", "Bathroom set, rose quartz look"), ("resin-bathroom-set-4", "Bathroom set, amber tortoiseshell look"),
        ("resin-bathroom-set-5", "Bathroom set, jade green"), ("resin-bathroom-set-6", "Bathroom set, cream onyx look"),
        ("resin-bathroom-set-7", "Bathroom set, coral marble look")]),
    ("bowls", "RB", "Resin bowls and platters", "Bowls, platters and salad servers in resin.", [
        ("resin-tableware-1", "Platter, bowl and servers, sky blue"), ("resin-tableware-2", "Platter, bowls and servers, emerald swirl"),
        ("resin-tableware-3", "Bowls, divided platter and servers, amber"), ("resin-tableware-4", "Bowls, cake stand and servers, cobalt blue"),
        ("resin-tableware-5", "Bowls and vase, teal"), ("resin-tableware-6", "Bowls, platter and servers, blue marble")]),
    ("boards", "WB", "Wooden boards", "Chopping and serving boards, engraved by laser or with a resin pour.", [
        ("wooden-chopping-board-1", "Board, engraved sprig"), ("wooden-chopping-board-2", "Dark board, engraved flowers"),
        ("wooden-chopping-board-3", "Board with white resin pour and two spatulas"), ("wooden-chopping-board-4", "Board, engraved lotus"),
        ("wooden-chopping-board-5", "Board, engraved leaf branch"), ("wooden-chopping-board-6", "Slim board, engraved herb"),
        ("wooden-chopping-board-7", "Board with pink resin pour")]),
    ("candles", "CS", "Candle stands", "Wooden tealight holders and candle stands.", [
        ("wooden-candle-stand-1", "Hexagon tealight blocks, set of 7"), ("wooden-candle-stand-2", "Tapered tealight holders"),
        ("wooden-candle-stand-3", "Ridged pillar candle stands"), ("wooden-candle-stand-4", "Tall taper candle stands"),
        ("wooden-candle-stand-5", "Faceted candle blocks"), ("wooden-candle-stand-6", "Turned candle stands"),
        ("wooden-candle-stand-7", "Square tealight blocks")]),
    ("chests", "IC", "Inlay chests", "Chests of drawers and bedside chests with an inlay design.", [
        ("bone-inlay-chest-1", "Chest of drawers, blue floral inlay design"), ("bone-inlay-chest-2", "Chest of drawers, green floral inlay design"),
        ("bone-inlay-chest-3", "Bedside chest, blue floral inlay design"), ("bone-inlay-chest-4", "Bedside chest, blue and white inlay design"),
        ("bone-inlay-chest-5", "Chest of drawers, grey and white geometric inlay design"),
        ("bone-inlay-chest-6", "Stripe pattern 3-drawer bone inlay chest"),
        ("bone-inlay-chest-7", "4-drawer dyed bone inlay chest")]),
    ("tables", "OW", "Inlay tables", "Tables with a bone inlay pattern.", [
        ("bone-inlay-coffee-table-38", "Round drum coffee table, black and white bone inlay sunburst"),
        ("bone-inlay-coffee-table-39", "Small round drum coffee table, black and white bone inlay sunburst"),
        ("bone-inlay-coffee-table-40", "Octagon coffee table, black and white bone inlay"),
        ("bone-inlay-stool-41", "Round stool, black and white bone inlay honeycomb"),
        ("bone-inlay-side-table-42", "Cube side table, black and white bone inlay"),
        ("bone-inlay-coffee-table-43", "Round coffee table, black and white bone inlay flower pattern")]),
]
# groups whose codes do not start at 1 (OW-38..43 are the owner's own design numbers): group id -> number of its first item
MTO_START = {"tables": 38}
# approved text of a design, used as the page text instead of "Design <code>. <group line>"
MTO_TEXT = {
    "OW-38": "Round drum coffee table with a sunburst pattern on top and stripes down the side. Bone inlay, black and white. Two sizes: 36 in across × 16 in high, or 30 in across × 16 in high. Made to order in India.",
    "OW-40": "Eight-sided coffee table with a pattern of nested lines on the top and sides. Bone inlay, black and white. 40 in across, 17 in high. Made to order in India.",
    "OW-41": "Small round stool or side table with a honeycomb pattern all over. Bone inlay, black and white. 16 in across, 18 in high. Made to order in India.",
    "OW-42": "Cube side table with a diamond line pattern on every face. Bone inlay, black and white. 16 × 16 × 16 in. Made to order in India.",
    "OW-43": "Round coffee table with a flower pattern on top and a patterned band on the side. Bone inlay, black and white. 42 in across, 18 in high. Made to order in India.",
    "IC-6": "Stripe pattern 3-drawer bone inlay chest. Bone inlay on wood. Three sizes: W39 × D16 × H34 in, W42 × D16 × H34 in, or W48 × D16 × H34 in. Made to order in India. Size confirmed on order.",
    "IC-7": "4-drawer dyed bone inlay chest. Bone inlay on wood. Three sizes: H30 × W30 × D16 in, H32 × W40 × D16 in, or H32 × W46 × D18 in. Made to order in India. Size confirmed on order."}
# alt text of a design picture (from next_batch_inlay_chests.csv image_alt, without the size)
MTO_ALT = {"IC-6": "Stripe pattern 3-drawer bone inlay chest, made to order", "IC-7": "4-drawer dyed bone inlay chest, made to order"}
MTO_HOLD = {"OW-39"}  # designs kept off the site (OW-39 merged into OW-38 as its 30 in size, 18 Nov)
# one listing with several sizes: code -> [(size label, price)]; the card shows "From <lowest>"
MTO_SIZES = {"OW-38": [("36 × 16 in", 90900), ("30 × 16 in", 70900)],
             "IC-6": [("W39 × D16 × H34 in", 55900), ("W42 × D16 × H34 in", 58900), ("W48 × D16 × H34 in", 64900)],
             "IC-7": [("H30 × W30 × D16 in", 42900), ("H32 × W40 × D16 in", 54900), ("H32 × W46 × D18 in", 63900)]}
MTO_N = sum(len(g[4]) for g in MTO) - len(MTO_HOLD)
# Made-to-order designs that have an owner-set price (D-241/D-242, 18 Nov 2026: IC-2 Rs 74,900 incl. packing, delivery extra)
MTO_PRICE = {
    'IC-1': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
    'IC-2': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
    'IC-3': (46900, 'Price includes packing. Delivery extra.', 'About 3-drawer bedside 18 L × 14 W × 26 H in'),
    'IC-4': (46900, 'Price includes packing. Delivery extra.', 'About 3-drawer bedside 18 L × 14 W × 26 H in'),
    'IC-5': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
    'IC-6': (55900, 'Delivery extra. Size confirmed on order.', 'W39 × D16 × H34 in'),
    'IC-7': (42900, 'Delivery extra. Size confirmed on order.', 'H30 × W30 × D16 in'),
    'OW-38': (90900, 'Delivery extra.', 'Round, 36 in across, 16 in high'),
    'OW-39': (70900, 'Delivery extra.', 'Round, 30 in across, 16 in high'),
    'OW-40': (114900, 'Delivery extra.', 'Octagon, 40 in across, 17 in high'),
    'OW-41': (35900, 'Delivery extra.', 'Round, 16 in across, 18 in high'),
    'OW-42': (41900, 'Delivery extra.', 'Cube, 16 × 16 × 16 in'),
    'OW-43': (120900, 'Delivery extra.', 'Round, 42 in across, 18 in high'),
    'PT-1': (1299, 'Delivery extra.', 'About round tray 14 in'),
    'PT-2': (1699, 'Delivery extra.', 'About oval tray 18 × 9 in'),
    'PT-3': (2799, 'Delivery extra.', 'About tray 14 × 9 in + bowl 10 in'),
    'PT-4': (899, 'Delivery extra.', 'About rect tray with handles 14 × 10 in'),
    'PT-5': (3499, 'Delivery extra.', 'About tray 14 × 7 in, bowl 10 in, 2 servers'),
    'PT-6': (1799, 'Delivery extra.', 'About 2 bowls 5 in + 1 spoon'),
    'PT-7': (2799, 'Delivery extra.', 'About tray 14 in + 2 bowls (8 and 5 in)'),
    'PT-8': (3499, 'Delivery extra.', 'About board 16 × 10 in, bowl 9 in, 2 servers'),
    'PT-9': (1699, 'Delivery extra.', 'About rect tray with handles 16 × 10 in, Warli'),
    'WB-1': (499, 'Delivery extra.', 'About board 14 × 9 in, engraved'),
    'WB-2': (499, 'Delivery extra.', 'About board 14 × 9 in, engraved'),
    'WB-4': (499, 'Delivery extra.', 'About board 14 × 9 in, engraved'),
    'WB-5': (499, 'Delivery extra.', 'About board 14 × 9 in, engraved'),
    'WB-6': (499, 'Delivery extra.', 'About board 14 × 9 in, engraved'),
    'WB-7': (1499, 'Delivery extra.', 'About board 14 × 9 in with pink resin pour'),
    'WB-3': (1899, 'Delivery extra.', 'About board 14 × 9 in with white resin pour + 2 spatulas'),
    'CS-2': (999, 'Delivery extra.', 'About set of 3 holders 6-10 in'),
    'CS-3': (999, 'Delivery extra.', 'About set of 3 holders 6-10 in'),
    'CS-1': (699, 'Delivery extra.', 'About 7 hexagon blocks 3 in'),
    'CS-4': (699, 'Delivery extra.', 'About 5 taper holders 4-10 in'),
    'CS-5': (699, 'Delivery extra.', 'About 5 faceted blocks 4-10 in'),
    'CS-6': (799, 'Delivery extra.', 'About 2 stands 4-8 in'),
    'CS-7': (799, 'Delivery extra.', 'About 2 stands 4-8 in'),
    'RB-1': (2599, 'Delivery extra.', 'About round platter 12 in, bowl 7 in, 2 servers'),
    'RB-2': (3199, 'Delivery extra.', 'About platter 12 in, bowl 8 in, small bowl 4 in, 2 servers'),
    'RB-3': (2999, 'Delivery extra.', 'About bowl 10 in, bowl 5 in, 3-section dish 14 × 5 in, 2 servers'),
    'RB-4': (4199, 'Delivery extra.', 'About salad bowl 10 in + 2 servers, 3 small bowls 4 in, cake stand 10 in'),
    'RB-5': (2799, 'Delivery extra.', 'About 3 stacked bowls + 1 tall vase'),
    'RB-6': (3599, 'Delivery extra.', 'About bowl 10 in, bowl 7 in, small bowl 3 in, oblong platter 14 × 6 in, 2 servers'),
    'BS-1': (1899, 'Delivery extra.', 'About 3-piece resin set, pump 7 in tall'),
    'BS-2': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
    'BS-3': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
    'BS-4': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
    'BS-5': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
    'BS-6': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
    'BS-7': (1899, 'Delivery extra.', 'About 4-piece resin set, pump 7 in tall'),
}
BULK_ONLY_PRICE = {'OW-16': 399, 'OW-32': 399, 'gold-flake-resin-tray': 799}  # each, from 25 pieces


def mto_pr(code):
    """(price text, note) for a priced design, else ("Price on WhatsApp", None)"""
    if code in MTO_SIZES:
        return "From " + rupee(min(p for _, p in MTO_SIZES[code])), MTO_PRICE[code][1]
    if code in MTO_PRICE:
        return rupee(MTO_PRICE[code][0]), MTO_PRICE[code][1]
    return "Price on WhatsApp", None


def bulk_line(key):
    return f"{rupee(BULK_ONLY_PRICE[key])} each, from 25 pieces"


def mto_items():
    for gid, pre, title, line, items in MTO:
        for i, (f, n) in enumerate(items, MTO_START.get(gid, 1)):
            if f"{pre}-{i}" in MTO_HOLD: continue
            yield gid, f"{pre}-{i}", f, n


def mto_msg(code, n):
    return f"Hello Woodkari, I am asking about design {code}: {n}\nQuantity: "


# Acacia wood, made to order (code prefix OW). Batch 1, 16 Nov: 8 items, READ from agency-research
# businesses/woodkari/site/catalogue_batch1.csv (name, price_mode, site_price, bulk_price_25plus, label, material).
# price = one piece (None = "bulk only 500+": no single-piece price is shown). bulk = each at 25 or more
# (for a bulk-only item: the "from" price a piece). Sizes are NOT confirmed, so no size is stated anywhere.
# what = one plain sentence that only restates the name. views = what pictures a-f show (alt text), read off the pictures.
# Pictures: img/m-ow-01-a.webp ... -f.webp (+ -600), made by build/mto_images.py ow OW-01 ...
OW_GID, OW_TITLE, OW_CHIP = "acacia", "Acacia wood, made to order", "Acacia wood"
OW_LINE = "Trays, a bowl, a serving board, a coaster set and candle stands. Acacia wood; other woods on request. Each design shows its size; other sizes on request."
OW_MATERIAL = "Acacia wood. Other woods on request."
MG_TITLE, MG_CHIP = "Mango wood, made to order", "Mango wood"
MG_LINE = "A glass-lid box and an open tray, both with compartments. Mango wood; other woods on request. Each design shows its size."
OW_MATERIAL_MANGO = "Mango wood. Other woods on request."
OW_SIZE = "We confirm the size on WhatsApp."
OW_BULK_FROM = 25  # pieces: the lower price each starts here (single-piece items)
OW_BULK_MIN = 500  # pieces: the minimum for the "bulk only" items
OW = [
    dict(code="OW-01", size="14 × 10 × 1.5 in (36 × 25 × 3.8 cm)", name="Scalloped-edge rectangular tray", price=999, bulk=500,
         what="A rectangular tray with a scalloped edge.",
         views=["on a white background", "top view", "close-up of the scalloped edge", "side view",
                "in use on a table, holding a bowl of fruit and a napkin", "two trays stacked"]),
    dict(code="OW-03", size="6 in across, 3 in deep (15 × 7.5 cm)", name="Plain round wooden bowl", price=300, bulk=150, skip="f",
         what="A plain round wooden bowl.",
         views=["on a white background", "top view", "close-up of the rim", "side view",
                "in use, filled with apples and oranges", "three bowls nested one inside another"]),
    dict(code="OW-08", size="Board 14 × 9 in plus a 5 in handle (36 × 23 cm + 13 cm)", name="Serving board with heart-shaped handle", price=599, bulk=300,
         what="A serving board with a heart-shaped handle.",
         views=["on a white background", "top view", "close-up of the heart-shaped handle", "side view",
                "in use, with sliced bread, cheese and strawberries", "three boards fanned out"]),
    dict(code="OW-16", size="Coasters 4 × 4 in (10 × 10 cm), with a slotted stand", name="Square coaster set with slotted stand", price=None, bulk=350,
         what="A set of square coasters with a slotted stand.",
         views=["on a white background, coasters standing in the stand and one lying beside it", "top view",
                "close-up of the coasters in the slots", "side view",
                "in use on a kitchen counter, a cup of coffee on one coaster", "two sets side by side"]),
    dict(code="OW-18", size="16 × 11 × 2 in (41 × 28 × 5 cm)", name="Rectangular tray with handle cut-outs and sloped walls", price=1399, bulk=700,
         what="A rectangular tray with sloped walls and handle cut-outs.",
         views=["on a white background", "top view", "close-up of a handle cut-out", "side view",
                "in use, carrying a teapot, two cups of tea and biscuits", "two trays stacked"]),
    dict(code="OW-25", size="Set of 3, about 3, 6 and 9 in tall (8, 15, 22 cm)", name="Turned candle stands with metal tops, set of 3", price=1200, bulk=600, unit="set",
         what="A set of three turned candle stands with metal tops.",
         views=["on a white background", "top view", "close-up of a metal top", "side view, three heights",
                "in use, holding three taper candles", "the three stands grouped together"]),
    dict(code="OW-32", size="12 in across, 1 in rim (30 × 2.5 cm)", name="Round flat tray with low rim", price=None, bulk=350, skip="b",
         what="A round, flat tray with a low rim.",
         views=["on a white background", "top view", "close-up of the low rim", "side view",
                "in use, carrying a teapot and two cups of tea", "three trays stacked"]),
    dict(code="OW-33", size="16 × 11 × 2.5 in (41 × 28 × 6.4 cm)", name="Rectangular tray with oval handle cut-outs", price=1399, bulk=700,
         what="A rectangular tray with oval handle cut-outs.",
         views=["on a white background", "top view", "close-up of an oval handle cut-out", "side view",
                "in use, holding a loaf of bread, a jar of jam and a knife", "three trays stacked"]),
    dict(code="OW-36", wood="mango", size="8 × 8 × 3 in (20 × 20 × 7.6 cm)", name="9-compartment wooden box with glass lid", price=1899, bulk=699,
         what="Square box with nine compartments under a glass lid, for spices, dry fruit or small items.",
         views=["on a white background", "top view", "close-up of the corner and the glass lid", "side view",
                "in use, holding nine different spices", "three boxes stacked"]),
    dict(code="OW-37", wood="mango", size="4.75 × 4.75 × 1.25 in (12 × 12 × 3.2 cm)", name="4-compartment open wooden box", price=3399, bulk=None, pack=10,
         what="Small open tray with four compartments, for tea bags, sugar or snacks.",
         views=["on a white background", "top view", "close-up of a compartment and the corner", "side view",
                "in use, holding tea bags, sugar cubes, cardamom and biscuits", "three boxes stacked"]),
]
# Boxes, made to order (19 Nov batch, D-279). READ from agency-research businesses/woodkari/site/next_batch_inlay_chests.csv:
# only rows with a price and a real size (not "andaza"), box prices checked against each other (a larger box never costs less).
# sizes = [(size, price)]; pics = [(letter, alt text)]; the "e" size picture is used only where its labels equal a listed size.
BX_GID, BX_TITLE, BX_CHIP = "boxes", "Boxes, made to order", "Boxes"
BX_LINE = "Bone inlay boxes. Each design shows its sizes and prices."
BX = [
    dict(code="IC-N01", grp="boxes", name="Floral bone inlay jewellery box, small rectangular",
         sizes=[("150 x 100 mm", 1199), ("250 x 150 mm", 1799)],
         pics=[("a", "Floral bone inlay jewellery box, small rectangular, made to order"),
               ("b", "Floral bone inlay jewellery box, small rectangular, made to order, open"),
               ]),
]
# Painted pieces, hand-painted on wood (owner, D-280); same row rules; added to the painted group.
PXL = [
    dict(code="PX-01", grp="painted", name='Printed rectangular serving tray, painted print', sizes=[('10x10 in', 1499), ('14x10 in', 1699)],
         pics=[('a', 'Printed rectangular serving tray, painted print, made to order'), ('b', 'Printed rectangular serving tray, painted print, made to order, second view'), ('e', 'Printed rectangular serving tray, painted print, made to order, 10x10 in')]),
    dict(code="PX-02", grp="painted", name='Printed round serving tray', sizes=[('10 in', 1199), ('12 in', 1499), ('14x14 in', 1799)],
         pics=[('a', 'Printed round serving tray, made to order'), ('b', 'Printed round serving tray, made to order, second view'), ('e', 'Printed round serving tray, made to order, 10 in')]),
    dict(code="PX-03", grp="painted", name='Meena/pichwai round tray, set of 2', sizes=[('7x7 + 8x8 in pair', 899), ('10x10 in pair', 1099)],
         pics=[('a', 'Meena/pichwai round tray, set of 2, made to order'), ('b', 'Meena/pichwai round tray, set of 2, made to order, second view'), ('e', 'Meena/pichwai round tray, set of 2, made to order, 7x7 + 8x8 in pair')]),
    dict(code="PX-04", grp="painted", name='Printed oval tray, no handle', sizes=[('250x150 mm', 1499), ('12x8 in', 2999)],
         pics=[('a', 'Printed oval tray, no handle, made to order'), ('b', 'Printed oval tray, no handle, made to order, second view'), ('e', 'Printed oval tray, no handle, made to order, 250x150 mm')]),
    dict(code="PX-05", grp="painted", name='Gold-print floral painted tray, rectangular', sizes=[('10x14x2 in', 1199)],
         pics=[('a', 'Gold-print floral painted tray, rectangular, made to order'), ('b', 'Gold-print floral painted tray, rectangular, made to order, second view'), ('e', 'Gold-print floral painted tray, rectangular, made to order, 10x14x2 in')]),
    dict(code="PX-06", grp="painted", name='Meena rectangular tray', sizes=[('12x8 in', 2399)],
         pics=[('a', 'Meena rectangular tray, made to order'), ('b', 'Meena rectangular tray, made to order, second view'), ('e', 'Meena rectangular tray, made to order, 12x8 in')]),
    dict(code="PX-08", grp="painted", name='Large printed painted tray', sizes=[('16x12 in', 3599)],
         pics=[('a', 'Large printed painted tray, made to order'), ('b', 'Large printed painted tray, made to order, second view'), ('e', 'Large printed painted tray, made to order, 16x12 in')]),
    dict(code="PX-09", grp="painted", name='Small printed gift tray', sizes=[('8x10 in', 899)],
         pics=[('a', 'Small printed gift tray, made to order'), ('b', 'Small printed gift tray, made to order, second view'), ('e', 'Small printed gift tray, made to order, 8x10 in')]),
    dict(code="PX-10", grp="painted", name='Meena round bowl, mango wood', sizes=[('5 in', 899), ('8 in', 1199), ('10 in', 1399)],
         pics=[('a', 'Meena round bowl, mango wood, made to order'), ('b', 'Meena round bowl, mango wood, made to order, second view'), ('e', 'Meena round bowl, mango wood, made to order, 5 in')]),
    dict(code="PX-11", grp="painted", name='Floral-print serving bowl', sizes=[('6 in', 899), ('8 in', 1499), ('10 in', 2699)],
         pics=[('a', 'Floral-print serving bowl, made to order'), ('b', 'Floral-print serving bowl, made to order, second view')]),
    dict(code="PX-14", grp="painted", name='Nesting printed bowl set of 3', sizes=[('3, 4, 5 in set', 2399)],
         pics=[('a', 'Nesting printed bowl set of 3, made to order'), ('b', 'Nesting printed bowl set of 3, made to order, second view'), ('e', 'Nesting printed bowl set of 3, made to order, 3, 4, 5 in set')]),
    dict(code="PX-15", grp="painted", name='Printed plate and bowl set', sizes=[('plate 10 in + bowl 3 in', 2099), ('12 in + 6 in', 2999)],
         pics=[('a', 'Printed plate and bowl set, made to order'), ('b', 'Printed plate and bowl set, made to order, second view'), ('e', 'Printed plate and bowl set, made to order, plate 10 in + bowl 3 in')]),
    dict(code="PX-16", grp="painted", name='Printed round platter / plate', sizes=[('6 in', 1199), ('12 in', 1499)],
         pics=[('a', 'Printed round platter / plate, made to order'), ('b', 'Printed round platter / plate, made to order, second view'), ('e', 'Printed round platter / plate, made to order, 6 in')]),
]
PXL, BX = [p for p in PXL if p["code"] in {"PX-02", "PX-03", "PX-04", "PX-05", "PX-06", "PX-09", "PX-16"}], [b for b in BX if b["code"] == "IC-N01"]  # D-301 19 Nov: 5 back after Checker + owner OK; 21 Nov owner "photo laga do": PX-16 + IC-N01 (a,b only) back; PX-06 back after Checker 21 Nov; rest HIDDEN (owner D-288)
NB = PXL + BX  # D-301: the 5 painted pages. Rest HIDDEN 19 Nov (owner D-288: photos faulty; PXL + BX come back only after new photos pass full-size check + owner OK)
NB_BY = {x["code"]: x for x in NB}
PX_LINE = "Hand-painted on wood."
# ---- Listings of 22 Nov (owner: "100 listing tayyar rakho, approval karte hi live kar dena") ----
# Product data: agency-research businesses/woodkari/site/listings_22nov.csv (path can be changed with WK_LISTINGS_CSV).
# A code renders ONLY if (1) it is a line in build/listings_live.txt, (2) its CSV row has status READY, and (3) its main picture a has a row in
# build/photo_pass.csv (key m-<code>-a). Of its a/b/e pictures only those with a photo_pass row (and an existing source file) are shown or copied.
# build/listings_live.txt is empty today, so the built site is the same as before.
LST_CSV = os.environ.get("WK_LISTINGS_CSV", "/home/user/agency-research/businesses/woodkari/site/listings_22nov.csv")
LST_PHOTOS = os.environ.get("WK_LISTINGS_PHOTOS", "/home/user/agency-research/businesses/woodkari/photos/ai")  # np/NP-01-a.png, n100/N100-001-a.png
LST_VIEWS = {"a": "", "b": ", close view", "e": ", with its size marked"}


def load_listings():
    import csv
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        with open(os.path.join(base, "build", "listings_live.txt"), encoding="utf-8") as f:
            codes = [x.split("#")[0].strip() for x in f]
    except FileNotFoundError:
        return []
    codes = [c for c in codes if c]
    if not codes:
        return []
    with open(LST_CSV, newline="", encoding="utf-8") as f:
        rows = {r["code"].strip(): r for r in csv.DictReader(f)}
    with open(os.path.join(base, "build", "photo_pass.csv"), newline="", encoding="utf-8") as f:
        passed = {r["image_file"].strip() for r in csv.DictReader(f) if r["passed_by"].strip()}
    out = []
    for c in codes:
        r = rows.get(c)
        if not r:
            print("LISTING NOT LIVE (no CSV row):", c); continue
        if r["status"].strip() != "READY":
            print("LISTING NOT LIVE (status is not READY):", c); continue
        files = r["photos"].split()
        pics = [(x[:-4].rsplit("-", 1)[1], f"m-{c.lower()}-{x[:-4].rsplit('-', 1)[1]}", x) for x in files]  # (view letter, photo_pass key, source file)
        sub = "np" if c.startswith("NP-") else "n100"
        pics = [t for t in pics if t[1] in passed and os.path.exists(os.path.join(LST_PHOTOS, sub, t[2]))]  # per picture: only those with a photo_pass row are shown
        if not any(t[0] == "a" for t in pics):
            print("LISTING NOT LIVE (main picture a not in photo_pass.csv or file missing):", c); continue
        m = re.search(r"₹\s*([\d,]+)", r["price_text"])
        out.append(dict(code=c, name=r["title"], cat=r["category"], what=r["short_desc"], material=r["material"], size=r["size_text"], moq=r["moq"],
                        price=int(m.group(1).replace(",", "")) if m else None, price_text=r["price_text"], sub=sub,
                        pics=[(x, k, fn) for x, k, fn in pics]))
    return out


LST = load_listings()
LST_BY = {x["code"]: x for x in LST}


def lst_gid(cat):
    return "l-" + re.sub(r"[^a-z0-9]+", "-", cat.lower()).strip("-")


def lst_cats():
    seen = []
    for x in LST:
        if x["cat"] not in seen:
            seen.append(x["cat"])
    return sorted(seen)


def lst_images():
    """web copies (1200 and 600 px) of the pictures of live listings only; existing files are left alone"""
    if not LST:
        return
    from PIL import Image
    imgdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")
    for it in LST:
        for _, key, fn in it["pics"]:
            if os.path.exists(os.path.join(imgdir, key + ".webp")) and os.path.exists(os.path.join(imgdir, key + "-600.webp")):
                continue
            im = Image.open(os.path.join(LST_PHOTOS, it["sub"], fn)).convert("RGB")
            if im.width != im.height:
                n = max(im.size); sq = Image.new("RGB", (n, n), im.getpixel((0, 0))); sq.paste(im, ((n - im.width) // 2, (n - im.height) // 2)); im = sq
            for size, suf in ((1200, ""), (600, "-600")):
                im.resize((size, size), Image.LANCZOS).save(os.path.join(imgdir, key + suf + ".webp"), "WEBP", quality=78, method=6)


ALL_N = MTO_N + len(OW) + len(NB) + len(LST)  # every card on designs.html


def bx_key(code, x="a"):
    return f"m-{code.lower()}-{x}"


def bx_from(it):
    lo = min(p for _, p in it["sizes"])
    return ("From " if len(it["sizes"]) > 1 else "") + rupee(lo)


def bx_card(it, anchor=False):
    aid = f' id="{it["code"]}"' if anchor else ""
    return (f'<a class="p rv"{aid} href="{mto_page(it["code"])}"><div class="ph"><img src="{UP}img/{bx_key(it["code"])}-600.webp" alt="{e(it["pics"][0][1])}" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
            f'<h3>{e(it["name"])}</h3><p class="sh">Design {it["code"]} · made on order</p><p class="pr">{bx_from(it)}</p></a>')


def nb_grp(it):
    return (BX_GID, BX_CHIP) if it["grp"] == "boxes" else ("painted", "Painted trays and bowls")


def page_bx(it):
    code, n = it["code"], it["name"]
    lede = f"Design {code}. {n}." + (" Hand-painted on wood." if it["grp"] == "painted" else "") + " Made to order in India."
    top = bx_from(it)
    sizes_txt = ", ".join(f"{a} {rupee(b)}" for a, b in it["sizes"])
    msg = f"Hello Woodkari, I want to order design {code}: {n}.\nSize ({sizes_txt}):\nQuantity:\nMy city and PIN code: "
    keys = [bx_key(code, x) for x, _ in it["pics"]]
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(v)}" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if j == 0 else " loading=lazy"}><figcaption>Design picture · made to order</figcaption></figure>'
        for j, (k, (_, v)) in enumerate(zip(keys, it["pics"])))
    rows = "".join(f'<li><b>{e(a)}</b><span>{rupee(b)}</span></li>' for a, b in it["sizes"])
    more = "\n".join(bx_card(x) for x in [y for y in NB if y["grp"] == it["grp"] and y["code"] != code][:3])
    offer = {"@type": "AggregateOffer", "priceCurrency": "INR", "lowPrice": min(p for _, p in it["sizes"]), "highPrice": max(p for _, p in it["sizes"]), "availability": "https://schema.org/MadeToOrder"}
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": n, "sku": code, "image": f"{SITE}/img/{keys[0]}.webp",
                     "description": lede, "brand": {"@type": "Brand", "name": "Woodkari"}, "offers": offer})
    return head(fit_title(n, code), fit(f"{n}. Design {code}. Made to order. Sizes and prices: {sizes_txt}.", f"{n}. Made to order. {top}."),
                mto_page(code), f"{keys[0]}-600.webp") + f"""<body class="has-stick">
{header('mto')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="designs.html">Made to order</a> / <a href="designs.html#g-{nb_grp(it)[0]}">{e(nb_grp(it)[1])}</a> / {code}</p>
<div class="pd">
{gallery(keys, figs)}
<div class="buy">
<h1>{e(n)}</h1>
<p class="pr">{top}</p>
<ul class="facts">{rows}</ul>
<p class="note">Prices are for one piece. Delivery is extra. We tell you the amount on WhatsApp.</p>
<p class="note">Made to order. We tell you the making time on WhatsApp.</p>
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
<p class="lede">{e(lede)}</p>
<a class="lnk more-l" href="designs.html">All {ALL_N} designs{ARROW}</a>
</div>
</div>
{('<section class="sec"><div class="hdr rv"><div><h2>More made to order</h2></div></div><div class="grid more3">' + more + '</div></section>') if more else ''}
</div></main>
<div class="stick"><b>{e(top)}</b><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def ow_wood(it):
    return it.get("wood", "acacia")


def ow_key(code, x="a"):
    return f"m-{code.lower()}-{x}"


def ow_price_lines(it):
    """the two price lines of a single-piece item, or the one line of a bulk-only item"""
    if it["price"] and it.get("unit") == "set":
        return f"{rupee(it['price'])} for the set of 3", f"{OW_BULK_FROM} sets or more: {rupee(it['bulk'])} a set"
    if it.get("pack"):  # sold only in packs (D-430): the price is the pack price, never a single-piece price
        return f"Pack of {it['pack']} {rupee(it['price'])}", f"{OW_BULK_FROM} pieces or more: ask on WhatsApp."
    if it["price"] and it["code"] == "OW-36":
        return rupee(it["price"]), f"{OW_BULK_FROM} pieces or more: {rupee(it['bulk'])} per piece"  # D-366, D-378
    if it["price"]:
        return rupee(it["price"]), f"{OW_BULK_FROM} pieces or more: {rupee(it['bulk'])} each"
    if it["code"] not in BULK_ONLY_PRICE:
        return "Price on WhatsApp", ""
    return bulk_line(it["code"]), ""


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def mto_page(code):
    return f"design-{code.lower()}.html"


def mto_pics(f):
    """main picture first, then the extra angles that have been checked and converted (img/m-<f>-a.webp ... -e.webp)"""
    return [f"m-{f}"] + [f"m-{f}-{x}" for x in "abcdef" if os.path.exists(os.path.join(ROOT, "img", f"m-{f}-{x}.webp"))]


LATER = 'src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" data-src'  # hero pictures 2-4: a 1px blank until site.js loads them
PP = '<button class="pp" type="button" aria-label="Pause pictures" aria-pressed="false"><svg class="i-pause" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M7 5h3v14H7zM14 5h3v14h-3z"/></svg><svg class="i-play" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></button>'


def e(s):
    return html.escape(str(s), quote=True)


def rupee(n):
    s = str(int(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head: parts.insert(0, head)
        s = ",".join(parts + [tail])
    return "₹" + s


def wa(text):
    return "https://wa.me/" + WHATSAPP + "?text=" + urllib.parse.quote(text)


# SEO (17 Nov, seo_plan_16nov.md rows 10-11): titles carry the product kind and "Made to Order", kept to about 60 characters.
TITLE_MAX = 60
SEO_KIND = {"painted": "Painted ", "bath": "Resin ", "bowls": "Resin ", "candles": "Wooden ", "chests": "", "tables": "", OW_GID: "Acacia ", "mango": "Mango wood "}


def seo_name(gid, n):
    """the page's own name with the kind of piece in front (the kind is the group heading on designs.html)"""
    if gid == "boards":  # "Board, engraved sprig" -> "Wooden board, engraved sprig"; "Dark board" -> "Dark wooden board"
        return n.replace("Board", "Wooden board", 1) if n.startswith("Board") else n.replace(" board", " wooden board", 1)
    k = SEO_KIND.get(gid, "")
    return k + (n[0].lower() + n[1:] if k else n)


DESC_MAX = 160


def fit_title(seo, code):
    for t in (f"{seo} ({code}) | Made to Order", f"{seo} | Made to Order", f"{seo} ({code})"):
        if len(t) <= TITLE_MAX:
            return t
    return seo


def fit(*options):
    """the first text that fits DESC_MAX (else the last, shortest one)"""
    return next((t for t in options if len(t) <= DESC_MAX), options[-1])


WA_ICON = '<svg class="i" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3Z"/></svg>'
ARROW = '<svg class="i ar" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
MAIL = '<svg class="i" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7.5h16"/><path d="M4 12h16"/><path d="M4 16.5h16"/></svg>'
SEARCH_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/></svg>'
IG_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.6" cy="7.4" r=".5" fill="currentColor"/></svg>'
WA_OUT = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20l1.2-4.2A8 8 0 1 1 8.3 19z"/><path d="M9.4 8.9c0 3.1 2.6 5.7 5.7 5.7l1-1.4-1.8-.9-.9.7c-.9-.4-1.8-1.3-2.2-2.2l.7-.9-.9-1.8z"/></svg>'
X_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
# drawer menu: one small drawn mark per row, same grid and stroke as the header icons (owner list 20 Nov, point 7)
_DI = '<svg class="di" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
DR_ICON = {
    "all": _DI % '<rect x="4.5" y="4.5" width="6" height="6" rx="1"/><rect x="13.5" y="4.5" width="6" height="6" rx="1"/><rect x="4.5" y="13.5" width="6" height="6" rx="1"/><rect x="13.5" y="13.5" width="6" height="6" rx="1"/>',
    "wood": _DI % '<path d="M5 19C5 10.5 10.5 5 19 5c0 8.5-5.500 14-14 14Z"/><path d="M5 19 13.500 10.500"/>',
    "resin": _DI % '<path d="M12 3.800c3.400 3.900 5.500 7 5.500 9.900a5.500 5.500 0 0 1-11 0c0-2.900 2.100-6 5.500-9.900Z"/><path d="M9.300 14.300a2.800 2.800 0 0 0 2 2.300"/>',
    "logo": _DI % '<rect x="4" y="4" width="16" height="16" rx="3.500"/><path d="m8 9.500 1.700 5 2.300-4.200 2.300 4.200 1.700-5"/>',
    "bulk": _DI % '<path d="m4 8 8-4 8 4v8l-8 4-8-4Z"/><path d="m4 8 8 4 8-4M12 12v8"/>',
    "ws": _DI % '<path d="M4 20V11l5 3v-3l5 3V5.500h6V20Z"/><path d="M8 20v-2.500M12 20v-2.500"/>',
    "faq": _DI % '<circle cx="12" cy="12" r="8.500"/><path d="M9.700 9.700a2.300 2.300 0 1 1 3.500 2c-.8.500-1.200 1-1.200 1.800"/><circle cx="12" cy="16.200" r=".5" fill="currentColor"/>',
}
DR_ICON = {k: v.replace(".500", ".5").replace(".200", ".2").replace(".300", ".3").replace(".800", ".8") for k, v in DR_ICON.items()}
CHEV = '<svg class="i ar" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9.5 6 6 6-6 6"/></svg>'
TARR = '<svg class="ta" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
TBACK = '<svg class="tb" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>'
PLUS = '<svg class="pl" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'

CSS = r"""
@font-face{font-family:"Hanken Grotesk";font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/hanken-grotesk-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Hanken Grotesk";font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/hanken-grotesk-latin-ext.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Instrument Serif";font-style:normal;font-weight:400;font-display:swap;src:url(fonts/instrument-serif-latin.woff2) format("woff2")}
@font-face{font-family:"Instrument Serif";font-style:italic;font-weight:400;font-display:swap;src:url(fonts/instrument-serif-italic-latin.woff2) format("woff2")}

:root{--bg:#fff;--stone:#f2efe9;--stone-2:#e8e4da;--ink:#17201b;--soft:#56605a;--line:#e2dfd6;--green:#1d4a3a;--green-d:#143629;--green-l:#2b6450;--mist:#eaf0ec;--gold:#d6b877;--brass:#8a6a2c;--r:3px;
 --serif:"Instrument Serif","Iowan Old Style",Georgia,serif;--sans:"Hanken Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif;--ease:cubic-bezier(.16,1,.3,1)}
@view-transition{navigation:auto}
::view-transition-group(pic){animation-duration:.45s;animation-timing-function:cubic-bezier(.77,0,.175,1)}
::view-transition-group(hd){animation-duration:.3s}
.js .p.now .ph::after{display:none}.js .p.now *{transition:none!important}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:128px;scrollbar-color:#b9c4bc transparent;scrollbar-width:thin;scrollbar-gutter:stable;interpolate-size:allow-keywords}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--sans);overflow-x:hidden;-webkit-tap-highlight-color:transparent;text-rendering:optimizeLegibility;caret-color:var(--green)}
::selection{background:var(--green);color:#fff}
img{max-width:100%;height:auto;display:block}
a{color:var(--green);text-underline-offset:4px;text-decoration-thickness:1px}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.04;margin:0;color:var(--ink);text-wrap:balance;letter-spacing:-.012em}
p{text-wrap:pretty}
button{font:inherit;color:inherit}
.i{flex:none}
.wrap{max-width:1280px;margin:0 auto;padding:0 18px}
@media(min-width:760px){.wrap{padding:0 36px}}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px 12px;z-index:50}
:focus-visible{outline:2px solid var(--green);outline-offset:3px;border-radius:2px}
.pv{background:#fff3c4;color:#4a3b00;text-align:center;font-size:14px;padding:6px}

/* header */
.hd{position:sticky;top:0;z-index:20;pointer-events:none;view-transition-name:hd}
.hd::before{content:"";position:absolute;inset:0 0 auto;height:62px;z-index:1;background:#fff;pointer-events:auto;transition:box-shadow .3s}
.hd.min::before{box-shadow:0 1px 0 var(--line),0 10px 30px -22px rgba(20,54,41,.5)}
.hd-top{position:relative;z-index:2;pointer-events:auto;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;height:62px}
.hd-l{display:flex;align-items:center;gap:6px}
.hd-r{display:flex;align-items:center;justify-content:flex-end;gap:6px}
.ib{display:inline-grid;place-items:center;width:44px;height:44px;border:0;background:transparent;color:var(--ink);cursor:pointer;border-radius:50%;transition:background-color .2s,color .2s}
.hd-l .ib{margin-left:-10px}.hd-r .ib{margin-right:-10px}
.logo{display:block;text-align:center;text-decoration:none;color:var(--ink);line-height:1}
.logo b{display:block;font:400 31px/1 var(--serif);letter-spacing:-.01em}
.logo small{display:block;font:600 11px/1 var(--sans);letter-spacing:.42em;margin:5px 0 0 .42em;color:var(--ink)}
.hd-note{display:none;font-size:14px;color:var(--soft)}
.hd-wa{display:none}
.hd-r{gap:0}.hd-r .ib{width:38px;height:38px}
.hd-ig{margin-right:0!important}
.hd-l .search{margin-left:-6px}
.hd-sb{display:none}
@media(min-width:900px){
 .hd-top,.hd::before{height:76px}
 .logo b{font-size:36px}
 .hd-note{display:block}
 .hd-l .menu{display:none}
 .hd-wa{display:none}
 .hd-r .ib{margin-right:0}
 .hd-r{gap:14px}.hd-r .ib{width:28px;height:44px;border-radius:8px;margin:0}.hd-waic{margin-right:-5.5px!important}.hd-r .ib svg{width:22px;height:22px;stroke-width:1.6}
 .hd-l .ib.search{display:none}.hd-sb{order:0}.hd-ig{order:1}.hd-waic{order:2}
 .hd-sb{display:flex;align-items:center;gap:6px;width:168px;height:40px;padding:0 12px;border:1px solid var(--line);border-radius:999px;color:var(--soft);background:#fff}
 .hd-sb svg{flex:none;width:17px;height:17px}
 .hd-sb input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 14px/1 var(--sans);color:var(--ink)}
 .hd-sb input::-webkit-search-cancel-button{display:none}
 .hd-sb:focus-within{border-color:var(--green)}
}
.tabs{position:relative;background:#fff;pointer-events:auto;border-top:1px solid var(--line);border-bottom:1px solid var(--line);transition:transform .3s var(--ease),visibility 0s,box-shadow .3s}
.hd.sc .tabs{box-shadow:0 10px 30px -22px rgba(20,54,41,.5)}
.hd.min .tabs{transform:translateY(-101%);visibility:hidden;transition:transform .2s var(--ease),visibility 0s .2s}
.tabs nav{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:0 8px}
.tabs nav::-webkit-scrollbar{display:none}
.tabs a{position:relative;flex:none;padding:13px 12px;color:var(--ink);text-decoration:none;font-size:15.5px;font-weight:500;white-space:nowrap;transition:color .2s}
.tabs a::after{content:"";position:absolute;left:12px;right:12px;bottom:0;height:2px;background:var(--green);transform:scaleX(0);transform-origin:left;transition:transform .45s var(--ease)}
.tabs a[aria-current]{color:var(--green);font-weight:600}
.tabs a[aria-current]::after{transform:scaleX(1)}
@media(min-width:900px){.tabs nav{justify-content:center;gap:22px}.tabs a{padding:14px 12px}}

/* dialogs: drawer menu + search */
dialog{border:0;padding:0;color:var(--ink);max-width:none;max-height:none}
body:has(dialog[open]){overflow:hidden}
.drawer{position:fixed;inset:0 auto 0 0;margin:0;width:min(88vw,400px);height:100dvh;background:#fff;transform:translateX(-102%);transition:transform .25s var(--ease),overlay .25s allow-discrete,display .25s allow-discrete}
.drawer[open]{transform:none;transition-duration:.45s}
@starting-style{.drawer[open]{transform:translateX(-102%)}}
.drawer::backdrop,.srch::backdrop{background:rgba(12,30,22,.5);opacity:0;transition:opacity .25s,overlay .25s allow-discrete,display .25s allow-discrete}
.drawer[open]::backdrop,.srch[open]::backdrop{opacity:1;transition-duration:.45s}
@starting-style{.drawer[open]::backdrop,.srch[open]::backdrop{opacity:0}}
.dr-in{display:flex;flex-direction:column;height:100%;padding:10px 22px calc(26px + env(safe-area-inset-bottom));overflow-y:auto;overscroll-behavior:contain}
.dr-hd{display:flex;align-items:center;justify-content:space-between;height:56px;margin-bottom:6px}
.dr-hd b{font:400 26px/1 var(--serif)}
.dr-in .ib{margin-right:-10px}
.dr-nav a{display:flex;align-items:center;justify-content:space-between;padding:15px 0;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;font:400 27px/1.1 var(--serif);transition:color .2s}
.dr-ft{margin-top:auto;padding-top:26px}
.dr-ft p{margin:14px 0 0;font-size:14.5px;color:var(--soft);text-align:center}
.srch{position:fixed;inset:0 0 auto 0;margin:0;width:100%;max-height:100dvh;background:#fff;transform:translateY(-102%);transition:transform .25s var(--ease),overlay .25s allow-discrete,display .25s allow-discrete}
.srch[open]{transform:none;transition-duration:.4s}
@starting-style{.srch[open]{transform:translateY(-102%)}}
.sr-in{max-width:760px;margin:0 auto;padding:14px 18px 26px}
.sr-bar{display:flex;align-items:center;gap:8px;border-bottom:1.5px solid var(--ink)}
.sr-bar input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 26px/1.2 var(--serif);padding:14px 0;color:var(--ink)}
.sr-bar input::placeholder{color:#7b857f}
.sr-bar input::-webkit-search-cancel-button{display:none}
.sr-list{margin:10px 0 0;padding:0;list-style:none;max-height:min(62dvh,520px);overflow-y:auto;overscroll-behavior:contain}
.sr-list a{display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink)}
.sr-list img{width:56px;height:56px;object-fit:cover;border-radius:var(--r);background:var(--stone)}
.sr-list b{display:block;font-weight:500;line-height:1.3}
.sr-list small{color:var(--soft);font-size:14px}
.sr-none{padding:18px 0 4px;color:var(--soft)}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:12px 26px;border-radius:var(--r);font:600 16px/1.2 var(--sans);letter-spacing:.005em;text-decoration:none;border:0;cursor:pointer;transition:background-color .25s,color .25s,box-shadow .25s}
.btn .ar{transition:transform .4s var(--ease)}
.btn.pri{background:var(--green);color:#fff}
.btn.line{background:transparent;color:var(--green);box-shadow:inset 0 0 0 1px var(--green)}
.btn.inv{background:#fff;color:var(--green)}
.btn.ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.75)}
.btn.wide{width:100%}
.row{display:flex;flex-wrap:wrap;gap:10px;margin-top:26px}
.lnk{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:16px;color:var(--green);text-decoration:none;padding:6px 0;background:linear-gradient(currentColor,currentColor) left bottom/100% 1px no-repeat}
.lnk .ar{transition:transform .4s var(--ease)}
.tag{position:absolute;z-index:2;left:8px;bottom:8px;background:rgba(255,255,255,.94);color:var(--ink);font:600 11.5px/1 var(--sans);letter-spacing:.02em;padding:5px 7px;border-radius:2px}

.terms{max-width:46em}.terms h1{margin-bottom:10px}.terms h2{margin:30px 0 8px}.terms ol{padding-left:1.3em;margin:0}.terms li{margin:0 0 10px;line-height:1.55}.terms .row{margin-top:26px}
/* hero */
.hero{position:relative;background:var(--green);color:#fff;overflow:hidden}
.show{position:relative;aspect-ratio:4/5;max-height:84svh;width:100%;overflow:hidden;background:#27352d}
.slide{position:absolute;inset:0;opacity:0;visibility:hidden;color:#fff;text-decoration:none}
.slide.on{opacity:1;visibility:visible;transition:opacity 1s ease}
.slide img{width:100%;height:100%;object-fit:cover}
.slide.on img{animation:kb 7s linear both}
.paused .slide.on img{animation-play-state:paused}
@keyframes kb{from{transform:scale(1.08)}to{transform:scale(1)}}
.slide .tag{left:auto;right:10px;top:10px;bottom:auto}
.slide .nm{position:absolute;left:10px;top:10px;background:rgba(20,54,41,.88);padding:7px 10px;border-radius:2px;font:500 13px/1.2 var(--sans);display:flex;gap:10px}
.slide .nm span{color:var(--gold)}
.hero-txt{position:absolute;left:0;right:0;bottom:0;z-index:3;padding:90px 18px 16px;background:linear-gradient(to top,rgba(10,26,19,.9) 0%,rgba(10,26,19,.62) 46%,rgba(10,26,19,0) 100%);pointer-events:none}
.hero-txt>*{pointer-events:auto}
.hero h1{color:#fff;font-size:clamp(40px,12.2vw,56px);line-height:.98;white-space:nowrap}
.hero h1 .ln{display:inline-block;overflow:hidden;padding-bottom:.08em;vertical-align:top}
.hero h1 .ln+.ln{margin-left:.22em}
.hero h1 .ln>span{display:inline-block;transform:translateY(105%);animation:up .9s var(--ease) .1s forwards}
.hero h1 .ln:nth-child(2)>span{animation-delay:.18s}
@keyframes up{to{transform:none}}
.hero p{margin:8px 0 0;color:#eef3ef;font-size:17.5px;max-width:27em}
.hero p .more{display:none}
.hero .row{margin-top:18px}
.hero .btn.inv{display:none}
.fade{opacity:0;animation:fade .7s var(--ease) .3s forwards}
.fade.d2{animation-delay:.38s}.fade.d3{animation:fadeo .6s ease .45s forwards}
@keyframes fade{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes fadeo{to{opacity:1}}
.dots{display:flex;gap:6px;margin-top:20px}
.dot{flex:1;height:26px;padding:0;border:0;background:none;cursor:pointer;position:relative;text-align:left;font:500 12.5px/1 var(--sans);color:#c9d6cd}
.dot::before{content:"";position:absolute;left:0;right:0;top:11px;height:2px;background:rgba(255,255,255,.34)}
.dot::after{content:"";position:absolute;left:0;right:0;top:11px;height:2px;background:#fff;transform:scaleX(0);transform-origin:left}
.dot span{display:none}
.dot[aria-current=true]::after{animation:fill 5.5s linear forwards}
.paused .dot[aria-current=true]::after{animation-play-state:paused}
@keyframes fill{to{transform:scaleX(1)}}
@media(min-width:900px){
 .hero{display:grid;grid-template-columns:minmax(0,46fr) minmax(0,54fr);min-height:min(calc(100svh - 126px),780px)}
 .show{order:2;aspect-ratio:auto;max-height:none;height:100%;min-height:560px}
 .hero-txt{position:static;order:1;background:none;display:flex;flex-direction:column;justify-content:center;padding:64px 56px 56px max(36px,calc((100vw - 1280px)/2 + 36px))}
 .hero h1{font-size:clamp(72px,7.6vw,96px);white-space:normal}
 .hero h1 .ln{display:block}.hero h1 .ln+.ln{margin-left:0}
 .hero p{font-size:19px;color:#dbe6de;margin-top:18px}
 .fab{display:none}
 .hero p .more{display:inline}
 .hero .btn.pri{display:none}.hero .btn.inv{display:inline-flex}
 .dots{margin-top:44px;max-width:520px}
 .dot{height:40px}
 .dot span{display:block;position:absolute;left:0;top:24px;white-space:nowrap}
 .dot[aria-current=true]{color:#fff}
 .dot::after{background:var(--gold)}
 .slide .nm{left:auto;right:14px;top:auto;bottom:14px;font-size:14px;padding:9px 12px}
 .slide .tag{right:14px;top:14px}
}

/* ribbon */
.ribbon{background:var(--stone);color:var(--green);overflow:hidden;white-space:nowrap;border-bottom:1px solid var(--line)}
.ribbon .track{display:inline-flex;padding:14px 0;animation:slide 40s linear infinite}
.ribbon span{font:400 21px/1 var(--serif);padding:0 24px;display:inline-flex;align-items:center;gap:24px}
.ribbon span::after{content:"";width:6px;height:6px;transform:rotate(45deg);background:var(--brass)}
@keyframes slide{to{transform:translateX(-50%)}}

/* sections */
.sec{padding:64px 0 0}
@media(min-width:900px){.sec{padding-top:96px}}
.hdr{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:10px 32px;margin-bottom:26px}
.hdr h2,.split h2,.end h2,.bh h1,.buy h1{font-size:clamp(38px,5vw,62px)}
.hdr p{margin:10px 0 0;color:var(--soft);max-width:36em}
.band{margin-top:64px;padding:64px 0}
@media(min-width:900px){.band{margin-top:96px;padding:96px 0}}
.band.stone{background:var(--stone)}
.band.green{background:var(--green);color:#e3ece6}
.band.green h2{color:#fff}
.band.green .lead,.band.green .steps span{color:#cfdcd3}
.band.green .steps,.band.green .steps li{border-color:rgba(255,255,255,.18)}
.band.green .steps li::before{color:var(--gold)}
.band.stone .steps,.band.stone .steps li,.band.stone .facts,.band.stone .facts li{border-color:#d9d4c8}

/* product grid */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px 12px}
@media(min-width:760px){.grid{grid-template-columns:repeat(3,1fr);gap:56px 28px}}
.grid.four{grid-template-columns:1fr 1fr}
@media(min-width:760px){.grid.four{grid-template-columns:repeat(4,1fr)}}
@media(max-width:759px){.grid.more3 .p:nth-child(3){display:none}}
.p{text-decoration:none;color:var(--ink);display:block}
.p[hidden]{display:none}
.p .ph{position:relative;aspect-ratio:1/1;overflow:hidden;background:var(--stone);border-radius:var(--r)}
.p .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .7s var(--ease),transform 1.2s var(--ease)}
.p .ph .u{opacity:0}
.p:focus-visible .ph img{transform:scale(1.04)}
.p:focus-visible .ph .u{opacity:1}
@media(hover:none){.p .ph .u{display:none}}
.p h3{font:500 16.5px/1.3 var(--sans);letter-spacing:0;margin:13px 0 1px}
.p .sh{color:var(--soft);font-size:14px;line-height:1.35;margin:0}
.p .pr{font-weight:600;font-size:17px;margin:5px 0 0;color:var(--green);font-variant-numeric:tabular-nums lining-nums}
.p .pr span{font-weight:400;color:var(--soft);font-size:14px}
.p .pr.bo{font-size:15px}
.p.cc{display:flex;flex-direction:column}
.p.cc h3{font:500 16px/1.3 var(--sans);margin:10px 0 3px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.p.cc .sh{font-size:12.5px;line-height:1.4;letter-spacing:.01em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.p.cc .sh{margin-bottom:10px}
.p.cc .pr{margin:auto 0 0;min-height:32px;display:flex;align-items:center;font-size:17px}
.p.cc .pr.ask{align-self:flex-start;max-width:100%;height:32px;padding:0 10px;border:1px solid var(--green);border-radius:var(--r);font:600 12.5px/1 var(--sans);letter-spacing:0;color:var(--green);white-space:nowrap;box-sizing:border-box}
.p.cc .pr.ask span{font:inherit;color:inherit}
.p.cc .pr:not(.ask) span{margin-left:.3em}
.p.cc .pr.ask svg{flex:none}
.grid:has(> .p.cc){row-gap:22px}
@media(min-width:760px){.p h3{font-size:18px;margin-top:16px}.p .sh{font-size:15px}.p .pr{font-size:18px}.p.cc h3{font-size:17px;margin-top:12px}.p.cc .sh{font-size:13px}.p.cc .pr{font-size:18px}.p.cc .pr.ask{font-size:13px;padding:0 12px}.grid:has(> .p.cc){row-gap:24px}}

/* split blocks */
.split{display:grid;gap:30px}
@media(min-width:900px){.split{grid-template-columns:1fr 1fr;gap:72px;align-items:center}.split.rev>:first-child{order:2}}
.split .lead{margin:14px 0 0;max-width:32em;color:var(--soft)}
.fig{position:relative;overflow:hidden;border-radius:var(--r)}
.fig img{width:100%;aspect-ratio:1/1;object-fit:cover}
.js .fig.wipe{clip-path:inset(0 0 100% 0);transition:clip-path 1.1s var(--ease)}
.js .fig.wipe img{transform:scale(1.08);transition:transform 1.1s var(--ease)}
.js .fig.wipe.in{clip-path:inset(0)}
.js .fig.wipe.in img{transform:none}
.steps{list-style:none;margin:28px 0 0;padding:0;border-top:1px solid var(--line);counter-reset:s}
.steps li{counter-increment:s;display:grid;grid-template-columns:46px 1fr;gap:0 8px;padding:17px 0;border-bottom:1px solid var(--line)}
.steps li::before{content:counter(s);grid-row:span 2;font:400 32px/1 var(--serif);color:var(--brass)}
.steps b{font-weight:600}
.steps span{color:var(--soft);font-size:16px}
.facts{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}
.facts li{display:grid;grid-template-columns:8.2em 1fr;gap:12px;padding:13px 0;border-bottom:1px solid var(--line);font-size:16px}
.facts b{font-weight:500;color:var(--soft)}

/* tiles + designs scrollers */
.tiles,.dz{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -18px;padding:0 18px 6px;scrollbar-width:none}
.tiles::-webkit-scrollbar,.dz::-webkit-scrollbar{display:none}
.tile{flex:0 0 72%;scroll-snap-align:start;position:relative;overflow:hidden;border-radius:var(--r);text-decoration:none;color:#fff;aspect-ratio:3/4;background:#27352d}
.tile img{width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}
.tile .tag{left:auto;right:8px;top:8px;bottom:auto}
.tile .cap{position:absolute;inset:auto 0 0 0;padding:80px 18px 18px;background:linear-gradient(to top,rgba(10,26,19,.82),rgba(10,26,19,0));font:400 30px/1.05 var(--serif)}
.tile small{display:block;font:500 14.5px/1.3 var(--sans);margin-top:7px;color:#e6ede8}
.dz a{flex:0 0 44%;scroll-snap-align:start;text-decoration:none;color:var(--ink)}
.dz .ph{position:relative;overflow:hidden;border-radius:var(--r);background:var(--stone)}
.dz img{width:100%;aspect-ratio:1/1;object-fit:cover;transition:transform 1.2s var(--ease)}
.dz b{display:block;font-weight:500;margin-top:11px;line-height:1.3;font-size:15.5px}
.dz i{font-style:normal;font-size:14.5px;color:var(--green)}
@media(min-width:760px){.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;margin:0;padding:0;overflow:visible}.tile{flex:none}
 .dz{display:grid;grid-template-columns:repeat(6,1fr);gap:22px;margin:0;padding:0;overflow:visible}.dz a{flex:none}}

/* questions */
.faq{border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line)}
.faq summary{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:19px 0;cursor:pointer;list-style:none;font:400 25px/1.15 var(--serif);transition:color .2s}
.faq summary::-webkit-details-marker{display:none}
.faq .pl{flex:none;transition:transform .3s var(--ease)}
.faq details[open] .pl{transform:rotate(135deg)}
.faq details p{margin:0;padding:0 44px 22px 0;color:var(--soft);max-width:44em}
.faq details::details-content{block-size:0;overflow:hidden;transition:block-size .3s var(--ease),content-visibility .3s allow-discrete}
.faq details[open]::details-content{block-size:auto}

/* product page */
.crumb{font-size:14.5px;color:var(--soft);padding:16px 0 12px}
.crumb a{color:var(--soft);text-decoration:none;display:inline-block;padding:8px 0}
.pd{display:grid;gap:24px}
@media(min-width:960px){.pd{grid-template-columns:1.2fr 1fr;gap:72px;align-items:start}.buy{position:sticky;top:150px}}
.gal{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -18px;padding:0 18px;scrollbar-width:none}
.gal::-webkit-scrollbar{display:none}
.gal figure{flex:0 0 100%;scroll-snap-align:center;margin:0;position:relative}
.gal img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r);background:var(--stone)}
.galw{min-width:0}
.galp{display:none}
@supports (animation-timeline:scroll()){@media(max-width:959px){
 .galw{timeline-scope:--gal}
 .gal{scroll-timeline:--gal x}
 .galp{display:block;height:2px;margin-top:12px;background:var(--line)}
 .galp i{display:block;height:100%;background:var(--green);transform-origin:left;animation:galp linear both;animation-timeline:--gal}
}}
@keyframes galp{from{transform:scaleX(calc(1/var(--n)))}to{transform:scaleX(1)}}
.gal figcaption{position:absolute;left:8px;bottom:8px;background:rgba(255,255,255,.94);font:600 11.5px/1 var(--sans);padding:5px 7px;border-radius:2px}
.gal{margin:0;padding:0;gap:0;scroll-padding-inline:0}
.stage{position:relative}
.gnav{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.9);color:var(--ink);font:400 26px/1 var(--sans);display:grid;place-items:center;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.15);z-index:2}
.gnav:focus-visible,.th:focus-visible{outline:2px solid var(--green);outline-offset:2px}
.gprev{left:10px}.gnext{right:10px}
.gnav[disabled]{opacity:.35;cursor:default}
.thumbs{display:flex;gap:8px;overflow-x:auto;margin-top:10px;padding:2px;scrollbar-width:none}
.thumbs::-webkit-scrollbar{display:none}
.th{flex:0 0 64px;height:64px;padding:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--stone);cursor:pointer}
.th img{width:100%;height:100%;object-fit:cover;display:block;mix-blend-mode:multiply}
.th.on{border:2px solid var(--green)}
.galw.has-th .galp{display:none!important}
@media(min-width:960px){.th{flex-basis:76px;height:76px}}
.buy .pr{font-size:25px;font-weight:600;margin:14px 0 0;color:var(--green);font-variant-numeric:tabular-nums lining-nums}
.buy .pr span{font-size:15px;font-weight:400;color:var(--soft)}
.buy .pr.bo{font-size:20px}
.buy .note{font-size:15px;color:var(--soft);margin:6px 0 0}
.buy .ob .pr span{font-size:15px;font-weight:400;color:var(--soft)}.obp{list-style:none;margin:10px 0 4px;padding:0}.obp li{display:flex;flex-wrap:wrap;justify-content:space-between;gap:2px 12px;padding:8px 0;border-top:1px solid var(--line);font-size:16px}.obp li:last-child{border-bottom:1px solid var(--line)}.obp span{color:var(--soft)}.buy .ob .row{margin-top:16px}
.buy .lede{margin:22px 0 0}
.buy .uses{margin:10px 0 0;color:var(--soft)}
.buy .facts{margin-top:24px}
.buy .more-l{margin-top:20px}
.stick{position:fixed;left:0;right:0;bottom:0;z-index:15;background:#fff;border-top:1px solid var(--line);padding:10px 18px calc(10px + env(safe-area-inset-bottom));display:flex;align-items:center;gap:14px}
.stick{view-transition-name:stick}
::view-transition-new(stick):only-child{animation:rise .45s var(--ease) both}
::view-transition-old(stick):only-child{animation:sink .2s ease both}
@keyframes rise{from{transform:translateY(100%)}}
@keyframes sink{to{transform:translateY(100%)}}
.stick b{font-size:18px;font-weight:600;color:var(--green);white-space:nowrap;font-variant-numeric:tabular-nums}
.stick .btn{flex:1;min-height:48px;padding:10px 14px}
@media(min-width:960px){.stick{display:none}}
@media(max-width:959px){body.has-stick{padding-bottom:calc(70px + env(safe-area-inset-bottom))}.buy .btn.pri.wide{display:none}body.has-stick .fab{display:none}}

/* bulk page hero */
.bh{display:grid;gap:28px;padding-top:28px}
@media(min-width:900px){.bh{grid-template-columns:1fr 1.15fr;gap:72px;align-items:center;padding-top:56px}}
.bh p{color:var(--soft);font-size:18px;margin:16px 0 0;max-width:30em}
.bh .fig img{aspect-ratio:1200/744}

/* close + footer */
.end{text-align:center;padding:88px 0 0}
@media(min-width:900px){.end{padding-top:128px}}
.end p{color:var(--soft);margin:14px auto 0;max-width:30em}
.end .row{justify-content:center}
.ft{margin-top:88px;background:var(--green-d);color:#cfdcd3}
@media(min-width:900px){.ft{margin-top:128px}}
.ft .wrap{padding-top:52px;padding-bottom:40px;display:grid;gap:30px}
@media(min-width:760px){.ft .wrap{grid-template-columns:1.5fr 1fr 1fr;padding-top:72px;padding-bottom:48px}}
.ft .fl{display:flex;align-items:center;gap:12px;color:#fff;text-decoration:none;margin-bottom:16px}
.ft .fl img{border-radius:8px}
.ft .fl b{font:400 34px/1 var(--serif)}
.ft h3{font:600 12.5px/1 var(--sans);letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin:0 0 10px}
.ft p{margin:0;font-size:15.5px;max-width:28em}
.ft a.l{display:block;color:#fff;text-decoration:none;padding:9px 0;font-size:15.5px}
.ft .fine{grid-column:1/-1;max-width:none;border-top:1px solid rgba(255,255,255,.16);padding-top:20px;font-size:13.5px;color:#a9bbb0}
.fab{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:14;width:56px;height:56px;border-radius:50%;background:var(--green);color:#fff;display:grid;place-items:center;box-shadow:0 10px 26px -6px rgba(12,40,28,.5);transition:transform .4s var(--ease),background-color .2s}
.fab .i{width:27px;height:27px}

/* hover: only where a real pointer can hover (on a phone a tap leaves :hover stuck) */
@media(hover:hover) and (pointer:fine){
 .ib:hover{background:var(--mist);color:var(--green)}
 .hd-wa:hover{background:var(--green-d)}
 .tabs a:hover,.dr-nav a:hover,.faq summary:hover,.crumb a:hover,.sr-list a:hover b{color:var(--green)}
 .tabs a:hover::after{transform:scaleX(1)}
 .dr-nav a:hover .ar{transform:translateX(4px)}
 .btn:hover .ar,.lnk:hover .ar{transform:translateX(5px)}
 .btn.pri:hover{background:var(--green-d)}
 .btn.line:hover{background:var(--green);color:#fff}
 .btn.inv:hover{background:var(--gold);color:var(--green-d)}
 .btn.ghost:hover{background:#fff;color:var(--green)}
 .ribbon:hover .track{animation-play-state:paused}
 .p:hover .ph img{transform:scale(1.04)}
 .p:hover .ph .u{opacity:1}
 .tile:hover img,.dz a:hover img{transform:scale(1.05)}
 .ft a.l:hover{color:var(--gold)}
 .fab:hover{background:var(--green-d);transform:scale(1.06)}
}

/* scroll reveal: visible unless JS is running */
.js .rv{opacity:0;transform:translateY(14px);transition:opacity .7s var(--ease),transform .7s var(--ease)}
.js .rv:has(h2.mk)>:not(h2):not(:has(h2)),.js .rv:has(h2.mk)>div>p{opacity:0;transition:opacity .6s ease .15s}
.js .rv.in:has(h2.mk)>*,.js .rv.in:has(h2.mk)>div>p{opacity:1}
.js .rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){
 *,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}
 .hero h1 .ln>span{transform:none}.fade{opacity:1}
 .js .rv{opacity:1;transform:none}.js .fig.wipe{clip-path:none}.js .fig.wipe img{transform:none}
 @view-transition{navigation:none}
}
/* ===== review fixes, 14 Nov: paste at the END of the CSS string in build/build.py (order matters) ===== */

/* [1] phone hero: whole picture stays clear, headline sits on the picture's lower edge and melts into the green */
@media(max-width:899px){
 .show{aspect-ratio:1/1;max-height:62svh}
 .hero-txt{position:relative;margin-top:-150px;padding:74px 18px 14px;
  background:linear-gradient(to bottom,rgba(29,74,58,0) 0,rgba(29,74,58,.3) 34px,rgba(29,74,58,.62) 68px,rgba(29,74,58,.86) 104px,rgba(29,74,58,.96) 130px,var(--green) 152px)}
 .hero h1{font-size:clamp(46px,14.4vw,64px);line-height:.92;text-shadow:0 2px 22px rgba(10,26,19,.45)}
 .hero p{margin-top:10px;color:#dbe6de}
 .hero .row{flex-wrap:nowrap;gap:8px;margin-top:16px;max-width:440px}
 .hero .row .btn{flex:1 1 auto;padding:12px 12px;font-size:15.5px;white-space:nowrap;gap:8px}
 .hero .btn.pri{display:none}.hero .btn.inv{display:inline-flex}
 .dots{margin-top:6px;align-items:center}
 .dot{height:44px}.dot::before,.dot::after{top:21px}
}

/* [2] small real bugs */
@media(min-width:900px){a.fab{display:none}                        /* was meant to be hidden; the later .fab rule won the cascade */
 .hero{min-height:min(calc(100svh - 131px),780px)}}                /* header is 131px tall, not 126: the hero ran 5px past the fold */
.tiles,.dz{scroll-padding-inline:18px}                         /* mandatory snap was eating the left gutter on phones */
.hero :focus-visible,.band.green :focus-visible,.ft :focus-visible{outline-color:#fff}   /* green ring on green was invisible */
.slide:focus-visible{outline-color:#fff;outline-offset:-5px}
.tag,.gal figcaption{font-size:12px}
.crumb a{padding:12px 0}.lnk{min-height:44px}.ft a.l{padding:10px 0}
@media(min-width:900px){.hd-wa{min-height:44px}.dot{height:44px}}
.fab{box-shadow:0 0 0 1.5px rgba(255,255,255,.5),0 10px 26px -6px rgba(12,40,28,.5);transition:transform .45s var(--ease),opacity .3s,background-color .2s}
.fab.off{transform:scale(.6);opacity:0;pointer-events:none}

/* [3] hero pictures: pause button (the dots' fill animation is the clock) */
.pp{flex:none;display:grid;place-items:center;width:44px;height:44px;margin:0 -12px 0 0;padding:0;border:0;border-radius:50%;background:none;color:#fff;cursor:pointer}
.pp svg{grid-area:1/1}
.pp[aria-pressed=false] .i-play,.pp[aria-pressed=true] .i-pause{display:none}
@media(min-width:900px){.dots{position:relative}.pp{position:absolute;left:100%;top:-10px;margin:0 0 0 2px}.pp:hover{background:rgba(255,255,255,.12)}}
.slide .nm{opacity:0;transition:opacity .25s}                      /* name chips no longer print over each other mid-fade */
.slide.on .nm{opacity:1;transition:opacity .5s .7s}
@media(max-width:899px){.slide{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:10px}.slide img{position:absolute;inset:0}.slide .nm,.slide .tag{position:relative;left:auto;right:auto;top:auto;bottom:auto;max-width:calc(100% - 20px)}.slide .nm{order:1;flex-wrap:wrap;gap:2px 10px}.slide .tag{order:2}}   /* phone: name+price pill top-left, tag stacked under it */

/* [4] press feedback (tap highlight is switched off site-wide, so every tap needs an answer) */
.btn{transition:background-color .25s,color .25s,box-shadow .25s,transform .25s var(--ease)}
.btn:active{transform:scale(.97)}
.p .ph,.dz .ph{transition:transform .3s var(--ease)}
.p:active .ph,.dz a:active .ph{transform:scale(.98)}
.tile:active img{transform:scale(1.02)}
.ib:active,.fab:active{transform:scale(.92)}
.tabs a:active{color:var(--green)}

/* [5] display type: three clear sizes instead of one */
h1,h2{letter-spacing:-.022em}
.hdr h2{font-size:clamp(42px,6.4vw,88px);line-height:.96}.hdr p{margin-top:16px}
.end h2{font-size:clamp(46px,8vw,112px);line-height:.94}
@media(min-width:900px){.hero h1{font-size:clamp(76px,9.4vw,140px);line-height:.9;letter-spacing:-.03em}}
.hero h1 .ln{padding-top:.08em;margin-top:-.08em}
@media(min-width:900px) and (max-height:800px){.hero h1{font-size:clamp(64px,7.4vw,104px)}.hero-txt{padding-top:36px;padding-bottom:32px}.hero p{margin-top:14px}.dots{margin-top:28px}}

/* [6] reveals: headings rise out of a slot (same verb as the hero line); cards lift a curtain, then the words follow */
.js h2.mk{overflow:hidden;padding-bottom:.16em;margin-bottom:-.16em}
.js h2.mk>span{display:block;transform:translateY(112%);transition:transform .9s var(--ease)}
.js .in h2.mk>span{transform:none}
.js .p.rv{opacity:1;transform:none}
.js .p.rv .ph::after{content:"";position:absolute;inset:0;z-index:1;background:var(--stone-2);transform-origin:50% 100%;transition:transform .9s var(--ease)}
.js .p.rv .ph img{transition:opacity .7s var(--ease),transform .9s var(--ease)}
.js .rv:has(h2.mk){opacity:1;transform:none}
.js .p.rv.in .ph::after{transform:scaleY(0)}
.js .p.rv .ph img{transform:scale(1.12)}
.js .p.rv.in .ph img{transform:none}
.js .p.rv.in:focus-visible .ph img{transform:scale(1.04)}
@media(hover:hover) and (pointer:fine){.js .p.rv.in:hover .ph img{transform:scale(1.04)}}
.js .p.rv h3,.js .p.rv .sh,.js .p.rv .pr{opacity:0;transition:opacity .4s ease .1s}
.js .p.rv.in h3,.js .p.rv.in .sh,.js .p.rv.in .pr{opacity:1;transform:none}

/* [7] the workshop paragraph is the page's quiet centrepiece: large serif, lit word by word by the scroll (site.js) */
#workshop .lead{position:relative;max-width:21em;margin-top:18px;font:400 clamp(25px,3vw,40px)/1.2 var(--serif);letter-spacing:-.012em;color:var(--ink)}
#workshop .lead span{transition:opacity .25s linear}
.real{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:44px}
@media(min-width:900px){.real{gap:72px;margin-top:72px}}
.real figure{margin:0}
.real img{width:100%;aspect-ratio:4/3;object-fit:contain;mix-blend-mode:multiply}   /* white studio ground disappears into the stone band */
.real figcaption{margin-top:8px;text-align:center;font:600 12px/1.2 var(--sans);letter-spacing:.02em;color:var(--soft)}

/* [8] footer signature: the name, edge to edge, tone on tone */
.ft{overflow:hidden}
.mega{display:block;overflow:hidden;margin:0;text-align:center;white-space:nowrap;pointer-events:none;user-select:none;
 font:400 min(30.5vw,470px)/.82 var(--serif);letter-spacing:-.03em;color:#1e4d3c}
.mega span{display:block;transform:translateY(.05em)}
.js .mega span{transform:translateY(80%);transition:transform 1.5s var(--ease)}
.js .mega.in span{transform:translateY(.05em)}
@media(max-width:899px){.ft .wrap{padding-bottom:28px}}

/* [9] surfaces: paper grain on the green fields, soft ends on the ribbon, drifting picture in the split blocks */
:root{--grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n' color-interpolation-filters='sRGB'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='.3 0 0 0 .35 .3 0 0 0 .35 .3 0 0 0 .35 0 0 0 0 1'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
@supports (background-blend-mode:soft-light){
 .band.green,.ft{background-image:var(--grain);background-size:220px;background-blend-mode:soft-light}
 @media(min-width:900px){.hero{background-image:var(--grain);background-size:220px;background-blend-mode:soft-light}}
}
.ribbon{-webkit-mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent);mask-image:linear-gradient(90deg,transparent,#000 7%,#000 93%,transparent)}
.fig{overflow:clip}
@supports (animation-timeline:view()){
 .split .fig img{animation:drift linear both;animation-timeline:view();animation-range:entry 0% exit 100%}
 @keyframes drift{from{transform:scale(1.14) translateY(-5%)}to{transform:scale(1.14) translateY(5%)}}
}

/* [10] buttons: colour wipes up from the bottom edge (mouse only) */
.btn{position:relative;overflow:hidden;isolation:isolate}
.btn::after{content:"";position:absolute;inset:0;z-index:-1;background:var(--fill,var(--green-d));transform:translateY(101%);transition:transform .45s var(--ease)}
.btn.line{--fill:var(--green)}.btn.inv{--fill:var(--gold)}.btn.ghost{--fill:#fff}
.btn.pri:hover{background:var(--green)}.btn.line:hover,.btn.ghost:hover{background:transparent}.btn.inv:hover{background:#fff}
@media(hover:hover) and (pointer:fine){.btn:hover::after{transform:none}}
@media(hover:none),(pointer:coarse){.btn.line:hover{color:var(--green)}.btn.ghost:hover{color:#fff}.btn.inv:hover{color:var(--green)}}

@media(prefers-reduced-motion:reduce){
 .js h2.mk>span{transform:none}.js .mega span{transform:translateY(.05em)}
 .js .p.rv .ph::after{display:none}
 .js .p.rv .ph img,.js .p.rv h3,.js .p.rv .sh,.js .p.rv .pr{opacity:1;transform:none}
 .dot[aria-current=true]::after{transform:none}                        /* current picture stays marked when the fill animation is off */
 .pp{display:none}
}

/* press: 160 ms, on everything tappable (after the review block, so these win) */
a,button,summary{touch-action:manipulation}
button,.btn,.fab{-webkit-user-select:none;user-select:none}
.btn{transition:background-color .25s,color .25s,box-shadow .25s,transform .16s var(--ease)}
.p .ph,.dz .ph{transition:transform .16s var(--ease)}
.ib{transition:background-color .2s,color .2s,transform .16s var(--ease)}
.fab:active{transition-duration:.16s}
.tile:active img{transform:none}
.tile:active,.js .tile.in:active{transform:scale(.98)}
.dr-nav a:active,.sr-list a:active,.faq summary:active,.lnk:active,.ft a.l:active,.crumb a:active,.dot:active,.pp:active{opacity:.6}
/* [11] Taste Skill review, 15 Nov: one backdrop for the catalogue, one heading scale, no grain */
.p .ph img:first-child,.dz img,.gal img,.sr-list img{mix-blend-mode:multiply}
.gal figure{border-radius:var(--r);overflow:hidden;background:var(--stone)}
.gal img{background:none}
.hdr h2,.split h2,.end h2,.bh h1,.buy h1{font-size:clamp(40px,5.6vw,76px);line-height:.98}
.band.green,.ft,.hero{background-image:none}
.hd-wa{border-radius:var(--r)}
.tag,.gal figcaption{font-size:12.5px}
.real{margin-top:0;gap:12px;align-self:center}
@media(min-width:900px){.real{gap:20px;margin-top:0}}
.real img{aspect-ratio:1/1}
@media(prefers-reduced-motion:reduce){.js .p.rv .ph .u{opacity:0}.js .p.rv:hover .ph .u,.js .p.rv:focus-visible .ph .u{opacity:1}}

/* [12] designs.html: made-on-order designs (15 Nov) */
.mh{padding-top:28px}
.mh h1{font-size:clamp(44px,6vw,84px)}
.mh>p{color:var(--soft);font-size:18px;margin:14px 0 0;max-width:34em}
.chips{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:24px -18px 0;padding:0 18px 2px}
.chips::-webkit-scrollbar{display:none}
.chips a{flex:none;padding:9px 14px;border:1px solid var(--line);border-radius:var(--r);color:var(--ink);text-decoration:none;font-size:15px;font-weight:500;background:#fff;transition:border-color .2s,color .2s}
.chips a span{color:var(--soft);font-weight:400;margin-left:4px}
.chips a:active{border-color:var(--green);color:var(--green)}
@media(hover:hover) and (pointer:fine){.chips a:hover{border-color:var(--green);color:var(--green)}}
@media(min-width:900px){.mh{padding-top:56px}.chips{flex-wrap:wrap;margin:28px 0 0;padding:0}}
.mto-l{margin:30px 0 0}
.mto{scroll-margin-top:110px}.mto .p{scroll-margin-top:130px}
.mto .p:target .ph{outline:2px solid var(--green);outline-offset:3px}
/* ---- home v2 (owner list 20 Nov) ---- */
.topline{margin:0;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:2px 0;padding:8px 18px;background:var(--stone);color:var(--ink);font:500 13.5px/1.35 var(--sans);text-align:center}
.topline span+span::before{content:"";display:inline-block;width:5px;height:5px;margin:0 11px 2px;background:var(--brass);transform:rotate(45deg)}
@media(min-width:900px){.topline{font-size:14.5px;padding:9px 36px}.hero{min-height:min(calc(100svh - 170px),780px)}}
.more-w{margin:36px 0 0;text-align:center}.more-w[hidden]{display:none}.more-w .btn{min-width:min(100%,330px)}
.fig.eng{background:var(--stone)}.fig.eng img{mix-blend-mode:multiply}
/* the workshop: words only until real workshop photos arrive */
.ws{display:grid;gap:4px}
.ws h2{font-size:clamp(40px,5.6vw,76px);line-height:.98}
.split .fig.eng img{animation:none}
#workshop .lead{margin:18px 0 0;max-width:24em}
@media(min-width:900px){.ws{grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:72px;align-items:start}#workshop .lead{margin-top:8px}}
/* icons: one weight everywhere in the header and the drawer */
.hd .ib svg,.drawer .ib svg{width:23px;height:23px;stroke-width:1.5}
.menu svg path{transform-box:fill-box;transform-origin:left center;transition:transform .3s var(--ease)}
.menu svg path:nth-child(3){transform:scaleX(.62)}
.menu[aria-expanded=true] svg path:nth-child(3){transform:none}
.dr-nav a{justify-content:flex-start;gap:14px}
.dr-nav a>span{flex:1;min-width:0}
.dr-nav .di{flex:none;color:var(--green);transition:transform .3s var(--ease)}
.dr-nav .ar{flex:none;width:17px;height:17px;color:var(--soft);transition:transform .3s var(--ease)}
.dr-in{padding:0 0 calc(20px + env(safe-area-inset-bottom))}
.dm-hd{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;height:64px;padding:0 12px;border-bottom:1px solid var(--line)}
.dm-l{display:flex;align-items:center;gap:2px}
.dm-hd .ib{margin:0}
.dm-logo b{font-size:25px}.dm-logo small{font-size:9px;margin-top:3px}
.dm{position:relative;flex:1;overflow:hidden}
.dm .pane{position:absolute;inset:0;overflow-y:auto;overscroll-behavior:contain;padding:10px 0;background:#fff;transition:transform .32s var(--ease),opacity .32s var(--ease)}
.dm .sub{transform:translateX(100%);padding-top:0}
.dm.on .p0{transform:translateX(-28%);opacity:0}
.dm .sub.on{transform:none}
.dm a,.dm-back{display:flex;align-items:center;justify-content:space-between;width:100%;min-height:58px;padding:0 24px;border:0;background:none;color:var(--ink);text-decoration:none;font:400 18.5px/1.3 var(--sans);letter-spacing:.015em;text-align:left;cursor:pointer}
.dm .ta{flex:none;width:20px;height:20px;color:var(--ink);opacity:.75}
.dm-back{justify-content:flex-start;gap:12px;min-height:52px;margin-bottom:6px;background:var(--stone);color:var(--soft);font-size:16.5px}
.dm-back .tb{flex:none}
.dm a:active,.dm-back:active{background:var(--stone)}
@media(hover:hover) and (pointer:fine){.dm a:hover{color:var(--green)}}
.dm a:focus-visible,.dm-back:focus-visible{outline:2px solid var(--green);outline-offset:-4px}
@media(prefers-reduced-motion:reduce){.dm .pane{transition:none}}
.tg{display:contents}
.tm{display:none}
.hchips{margin-top:34px}
.chips a[aria-current]{border-color:var(--green);color:var(--green)}
@media(min-width:900px){.hchips{justify-content:center}}
@media(min-width:900px) and (hover:hover){
 .tabs nav{overflow:visible}
 .tg{display:block;position:relative}
 .tm{display:none;position:absolute;left:0;top:100%;z-index:30;min-width:230px;background:#fff;border:1px solid var(--line);box-shadow:0 18px 40px -22px rgba(20,54,41,.55);padding:8px 0}
 .tg:hover .tm,.tg:focus-within .tm{display:block}
 .tm a{display:flex;justify-content:space-between;gap:20px;padding:10px 18px;font-size:15px}
 .tm a::after{display:none}
 .tm a i{font-style:normal;color:var(--soft);font-weight:400}
 .tm a:first-child{font-weight:600;color:var(--green)}
}
.dr-nav a:active .di{transform:scale(.86)}
.dr-nav a:active .ar{transform:translateX(4px)}
@media(hover:hover) and (pointer:fine){.menu:hover svg path:nth-child(3){transform:none}.dr-nav a:hover .di{transform:translateY(-2px)}}
/* the drawer deals its rows in behind the panel: one short wave, gaps closing; the WhatsApp button only fades */
@media(prefers-reduced-motion:no-preference){
 .drawer[open] .dm .p0>a{animation:drin .5s var(--ease) var(--d,0ms) backwards}
}
@keyframes drin{from{opacity:0;transform:translateX(-18px)}}
@keyframes drfade{from{opacity:0}}
"""

JS = r"""
(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s,r){return (r||d).querySelector(s)}
  function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}

  /* header: shadow + tabs tuck away on the way down */
  var hd=$('.hd'),ly=scrollY,run=0,quiet=0; /* quiet: our own jumps (chips, drawer) never tuck the chip row */
  if(hd)addEventListener('scroll',function(){var y=scrollY,dy=y-ly;ly=y;
    if(Date.now()<quiet){run=0;hd.classList.remove('min');hd.classList.toggle('sc',y>8);return}
    run=(dy>0)===(run>0)?run+dy:dy; /* distance covered in the current direction */
    if(y<=220||run<-24)hd.classList.remove('min');else if(run>48)hd.classList.add('min');
    hd.classList.toggle('sc',y>8)},{passive:true});

  d.addEventListener('touchstart',function(){},{passive:true}); /* lets :active work on iOS */

  /* menu and search */
  function dlg(btn,id,onopen){var b=$(btn),g=d.getElementById(id);if(!b||!g||!g.showModal)return;
    b.addEventListener('click',function(){g.showModal();b.setAttribute('aria-expanded','true');if(onopen)onopen(g)});
    g.addEventListener('close',function(){b.setAttribute('aria-expanded','false')});
    g.addEventListener('click',function(ev){if(ev.target===g||ev.target.closest('[data-close]')||ev.target.closest('a'))g.close()});}
  dlg('.menu','drawer',function(g){var m=$('.dm',g);if(!m)return;m.classList.remove('on');$$('.dm .sub',g).forEach(function(p){p.classList.remove('on');p.inert=true});$('.p0',g).inert=false});
  $$('.dm [data-pane]').forEach(function(a){a.addEventListener('click',function(ev){var p=d.getElementById(a.dataset.pane),m=a.closest('.dm');if(!p)return;
    ev.preventDefault();ev.stopPropagation();m.classList.add('on');p.classList.add('on');p.inert=false;$('.p0',m).inert=true;p.scrollTop=0;var f=$('.dm-back',p);if(f)f.focus({preventScroll:true})})});
  $$('.dm-back').forEach(function(bk){bk.addEventListener('click',function(ev){ev.stopPropagation();var p=bk.closest('.pane'),m=bk.closest('.dm');
    m.classList.remove('on');p.classList.remove('on');p.inert=true;var t=$('.p0',m);t.inert=false;var a=$('[data-pane="'+p.id+'"]',t);if(a)a.focus({preventScroll:true})})});
  var sx=d.getElementById('sx'),items=sx?JSON.parse(sx.textContent):[],list=$('.sr-list'),inp=$('.sr-bar input'),none=$('.sr-none');
  function render(q){if(!list)return;q=(q||'').trim().toLowerCase();list.textContent='';var n=0;
    items.forEach(function(it){if(q&&(it.n+' '+it.s).toLowerCase().indexOf(q)<0)return;n++;
      var li=d.createElement('li'),a=d.createElement('a'),im=d.createElement('img'),sp=d.createElement('span'),b=d.createElement('b'),sm=d.createElement('small');
      a.href=it.u;im.src=it.i;im.alt='';im.width=56;im.height=56;im.loading='lazy';b.textContent=it.n;sm.textContent=it.s;
      sp.appendChild(b);sp.appendChild(sm);a.appendChild(im);a.appendChild(sp);li.appendChild(a);list.appendChild(li)});
    if(none)none.hidden=n>0;}
  dlg('.search','srch',function(){render('');if(inp){inp.value='';inp.focus()}});
  var hb=$('.hd-sb input'),sg=d.getElementById('srch');
  if(hb&&sg&&sg.showModal){var go=function(){if(sg.open)return;var v=hb.value;sg.showModal();render(v);if(inp){inp.value=v;inp.focus()}hb.value=''};hb.addEventListener('focus',go);hb.addEventListener('input',go)}
  if(inp){inp.addEventListener('input',function(){render(inp.value)});inp.addEventListener('keydown',function(ev){if(ev.key==='Escape'){ev.preventDefault();d.getElementById('srch').close()}})}

  /* page transition: only the tapped card's picture travels to the product page (and back) */
  $$('.p').forEach(function(a){a.addEventListener('click',function(){
    $$('[style*="view-transition-name"]').forEach(function(x){x.style.viewTransitionName=''});
    var im=$('.ph img',a);if(im)im.style.viewTransitionName='pic'})});

  /* shop filter from the category tabs. The page opens on the 12 "top" pieces; All pieces and Name & logo show every piece; Acacia wood and Resin go by material */
  var cards=$$('#shop .p[data-cat]'),shop=d.getElementById('shop'),names={all:'Trays & boxes',wood:'Acacia wood',resin:'Resin',logo:'Name & logo'},
    notes={top:'Every piece is made to order. Prices are for one piece; delivery is extra.',all:'Every piece is made to order. Prices are for one piece; delivery is extra.',wood:'Every acacia wood piece on the site.',resin:'Every resin piece on the site.',logo:'Any piece can carry your name or logo, on 50 pieces or more of one design.'};
  function filter(k){if(k!=='top'&&!names[k])k='all';var tab=k==='top'?'all':k;
    curTab=tab;if(typeof light==='function')light('');
    var was=cards.filter(function(p){return !p.hidden}),from=was.map(function(p){return p.getBoundingClientRect()});
    cards.forEach(function(p){p.hidden=!(k==='top'?p.hasAttribute('data-top'):k==='all'||k==='logo'||p.dataset.cat===k)});
    /* re-deal: cards already on show slide to their new place, returning ones settle in (unseen ones keep their scroll reveal) */
    if(!rm&&shop&&shop.animate)cards.forEach(function(p){if(p.hidden||!p.classList.contains('in'))return;var i=was.indexOf(p),r=p.getBoundingClientRect();
      if(i<0)p.animate([{opacity:0,transform:'scale(.96)'},{opacity:1,transform:'none'}],{duration:300,easing:'cubic-bezier(.16,1,.3,1)'});
      else if(from[i].left!==r.left||from[i].top!==r.top)p.animate([{transform:'translate('+(from[i].left-r.left)+'px,'+(from[i].top-r.top)+'px)'},{transform:'none'}],{duration:450,easing:'cubic-bezier(.16,1,.3,1)'})});
    var t=d.getElementById('shop-t'),n=d.getElementById('shop-n'),va=d.getElementById('viewall'),mo=d.getElementById('more');
    if(t)(t.firstElementChild||t).textContent=names[tab];if(n)n.textContent=notes[k];if(va)va.hidden=(tab==='all');if(mo)mo.parentNode.hidden=(k!=='top');}
  /* one scroller for every chip, drawer row and footer link that goes to a section of this page.
     It re-reads the target on every frame (cards hiding or showing, lazy pictures and the tucking header cannot make it miss),
     stops when the finger or wheel takes over, and ends exactly on the target. Reduced motion jumps. */
  var tween=0;
  function stopTween(){if(tween){cancelAnimationFrame(tween);tween=0;quiet=Date.now()+400}}
  ['touchstart','wheel','keydown','mousedown'].forEach(function(n){addEventListener(n,stopTween,{passive:true})});
  function open(){var h=$('.hd-top'),t=$('.tabs');return (h?h.offsetHeight:0)+(t?t.offsetHeight:0)} /* header bar plus chip row, whether the row is tucked away or not */
  function goal(el){return Math.max(0,Math.round(el.getBoundingClientRect().top+scrollY-open()-13))}
  function goTo(el){stopTween();quiet=Infinity;if(hd)hd.classList.remove('min');var from=scrollY,t0=performance.now(),dist=Math.abs(goal(el)-from),dur=Math.min(900,260+dist*.1);
    if(rm||dist<2){scrollTo({top:goal(el),behavior:'instant'});quiet=Date.now()+400;return}
    function step(now){var k=Math.min(1,(now-t0)/dur),e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
      scrollTo({top:from+(goal(el)-from)*e,behavior:'instant'});
      if(k<1)tween=requestAnimationFrame(step);else{tween=0;scrollTo({top:goal(el),behavior:'instant'});quiet=Date.now()+400}}
    tween=requestAnimationFrame(step)}

  /* the lit chip follows the section on screen */
  var curTab='all',secs=['shop','workshop','questions'].map(function(i){return d.getElementById(i)}).filter(Boolean);
  function light(href){var hit=null;
    $$('.tabs a').forEach(function(a){var on=href?a.getAttribute('href')===href:(a.dataset.cat?a.dataset.cat===curTab:false);
      if(on){a.setAttribute('aria-current','true');hit=a}else a.removeAttribute('aria-current')});
    var nav=hit&&hit.parentNode;if(nav&&nav.scrollTo&&nav.scrollWidth>nav.clientWidth)nav.scrollTo({left:Math.max(0,hit.offsetLeft-(nav.clientWidth-hit.offsetWidth)/2),behavior:rm?'auto':'smooth'})}
  var spy=0,lit='';
  function spyNow(){spy=0;if(!shop)return;var line=open()+40,cur=null;
    secs.forEach(function(s){if(s.getBoundingClientRect().top<=line)cur=s});
    var key=(cur&&cur.id!=='shop')?cur.id:'shop';if(key===lit)return;lit=key;
    light(key==='shop'?'':'./#'+key)}
  if(shop)addEventListener('scroll',function(){if(!spy)spy=requestAnimationFrame(spyNow)},{passive:true});

  if(shop){
    var go=[];
    $$('.tabs a, .drawer a, footer a, #viewall, #more').forEach(function(a){var h=a.getAttribute('href')||'',m=/^\.\/#([\w-]+)$/.exec(h);
      if(a.dataset.cat||a.id==='more'||(m&&d.getElementById(m[1])))go.push(a)});
    go.forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();
      var h=a.getAttribute('href')||'',m=/^\.\/#([\w-]+)$/.exec(h),dr=a.closest('.drawer');
      if(m&&!a.dataset.cat){var tg=d.getElementById(m[1]);try{history.replaceState(null,'',location.pathname+location.search+'#'+m[1])}catch(_){}
        lit=m[1];light('./#'+m[1]);setTimeout(function(){goTo(tg)},dr?40:0);return}
      var k=a.dataset.cat||'all';filter(k);lit='shop';
      try{history.replaceState(null,'',location.pathname+'?f='+k+'#shop')}catch(_){}
      if(a.id!=='more')setTimeout(function(){goTo(shop)},dr?40:0)})});
    var f=new URLSearchParams(location.search).get('f');if(f)filter(f);
    spyNow();
  }

  /* reveal on scroll: headings rise out of a slot, cards stagger by the real number of columns */
  $$('main h2').forEach(function(h){if(!h.closest('.rv'))return;var s=d.createElement('span');while(h.firstChild)s.appendChild(h.firstChild);h.appendChild(s);h.classList.add('mk')});
  var rv=$$('.rv,.wipe,.mega');
  if(rm||!('IntersectionObserver' in window)){rv.forEach(function(x){x.classList.add('in')})}
  else{var gap=[0,70,120,150],io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;var t=en.target,row=[t],pa=t.parentNode;
      /* cards on one visual row, and a whole side-scrolling strip, come in together, left to right; nothing is still hidden when it is swiped into view */
      if(pa.matches('.grid,.tiles,.dz,.real')){var top=t.offsetTop;row=$$('.rv',pa).filter(function(x){return !x.dataset.rv&&x.offsetTop===top})}
      row.forEach(function(x,i){x.dataset.rv=1;io.unobserve(x);setTimeout(function(){x.classList.add('in')},gap[Math.min(i,3)])})})},{rootMargin:'0px 0px -7% 0px'});
    rv.forEach(function(x){io.observe(x)});}

  /* the workshop paragraph lights up word by word as it is scrolled into the reading zone */
  var wl=$('#workshop .lead');
  if(wl&&!rm){var ws=wl.textContent.trim().split(/\s+/),offs=[],tk=false;wl.textContent='';
    ws.forEach(function(w,i){var s=d.createElement('span');s.textContent=w;wl.appendChild(s);if(i<ws.length-1)wl.appendChild(d.createTextNode(' '))});
    var sp=$$('span',wl);
    function measure(){var w=wl.offsetWidth||1;offs=sp.map(function(s){return s.offsetTop+s.offsetLeft/w*s.offsetHeight})}
    function lit(){tk=false;var r=wl.getBoundingClientRect(),vh=innerHeight;if(r.top>vh||r.bottom<0)return;
      var a=vh*.92,b=vh*.62;sp.forEach(function(s,i){var t=(a-(r.top+offs[i]))/(a-b);s.style.opacity=(.22+.78*(t<0?0:t>1?1:t)).toFixed(2)})}
    measure();lit();
    addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(lit)}},{passive:true});
    addEventListener('resize',function(){measure();lit()});
    if(d.fonts&&d.fonts.ready)d.fonts.ready.then(function(){measure();lit()});}

  /* the floating WhatsApp button steps aside where a WhatsApp button is already on screen */
  var fab=$('.fab');
  if(fab&&'IntersectionObserver' in window){var near=[],fo=new IntersectionObserver(function(es){es.forEach(function(en){var i=near.indexOf(en.target);
      if(en.isIntersecting&&i<0)near.push(en.target);else if(!en.isIntersecting&&i>=0)near.splice(i,1)});fab.classList.toggle('off',near.length>0)});
    $$('.end,.ft').forEach(function(x){fo.observe(x)});}

  /* hero pictures */
  var sl=$$('.slide'),dt=$$('.dot'),hero=$('.hero');
  if(sl.length&&hero){var cur=0,z=1,show=$('.show'),pb=$('.pp'),st={user:false,hov:false,foc:false,out:false},x0=null,y0=0,sw=false;
    /* later pictures are fetched one ahead, not all at first paint */
    function load(i){var im=$('img',sl[(i+sl.length)%sl.length]);if(im&&im.dataset.src){im.src=im.dataset.src;im.removeAttribute('data-src')}}
    /* the new picture fades in ON TOP; the old one stays solid underneath until it is covered (no dip to the dark ground) */
    function tidy(){sl.forEach(function(s,i){if(i!==cur)s.classList.remove('on')})}
    function go(n){n=(n+sl.length)%sl.length;if(n===cur)return;dt[cur].removeAttribute('aria-current');cur=n;load(n);
      var s=sl[n],was=s.classList.contains('on');s.style.zIndex=++z;s.classList.add('on');dt[n].setAttribute('aria-current','true');
      if(rm||(was&&getComputedStyle(s).opacity==='1'))tidy();setTimeout(function(){load(cur+1)},2500)}
    sl.forEach(function(s){s.addEventListener('transitionend',function(ev){if(ev.target===s&&s===sl[cur])tidy()})});
    function sync(){hero.classList.toggle('paused',st.user||st.hov||st.foc||st.out||d.hidden);
      if(pb){pb.setAttribute('aria-pressed',String(st.user));pb.setAttribute('aria-label',st.user?'Play pictures':'Pause pictures')}}
    /* the dot's fill animation is the only clock: when it ends, the next picture comes. Pausing the animation pauses everything */
    hero.addEventListener('animationend',function(ev){if(ev.animationName!=='fill')return;var c=cur,im=$('img',sl[(c+1)%sl.length]);load(c+1);
      function nx(){if(cur===c)go(c+1)} /* on a slow connection, wait for the next picture instead of fading to an empty frame */
      if(im&&im.decode)im.decode().then(nx,nx);else nx()});
    dt.forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.i)})});
    if(pb)pb.addEventListener('click',function(){st.user=!st.user;sync()});
    if(matchMedia('(hover:hover)').matches){show.addEventListener('mouseenter',function(){st.hov=true;sync()});show.addEventListener('mouseleave',function(){st.hov=false;sync()})}
    hero.addEventListener('focusin',function(ev){st.foc=ev.target!==pb&&ev.target.matches(':focus-visible');sync()});
    hero.addEventListener('focusout',function(){st.foc=false;sync()});
    d.addEventListener('visibilitychange',sync);
    if('IntersectionObserver' in window)new IntersectionObserver(function(es){st.out=!es[0].isIntersecting;sync()}).observe(hero);
    /* swipe on phones */
    show.addEventListener('touchstart',function(ev){x0=ev.touches[0].clientX;y0=ev.touches[0].clientY},{passive:true});
    show.addEventListener('touchend',function(ev){if(x0===null)return;var t=ev.changedTouches[0],dx=t.clientX-x0,dy=t.clientY-y0;x0=null;
      if(Math.abs(dx)>44&&Math.abs(dx)>Math.abs(dy)*1.5){sw=true;go(cur+(dx<0?1:-1));setTimeout(function(){sw=false},400)}},{passive:true});
    show.addEventListener('click',function(ev){if(sw){ev.preventDefault();sw=false}},true);
    addEventListener('load',function(){setTimeout(function(){load(1)},1200)});
    sync();}

  /* product gallery: arrows + small pictures (owner 16 Nov) */
  $$('.galw.has-th').forEach(function(w){var g=$('.gal',w),th=$$('.th',w),pv=$('.gprev',w),nx=$('.gnext',w),n=th.length,cur=0,lock=0;
    function show(i,smooth){i=Math.max(0,Math.min(n-1,i));lock=Date.now()+700;mark(i);g.scrollTo({left:i*g.clientWidth,behavior:(smooth&&!rm)?'smooth':'auto'})}
    function mark(i){if(i===cur)return;cur=i;th.forEach(function(t,j){t.classList.toggle('on',j===i);if(j===i)t.setAttribute('aria-current','true');else t.removeAttribute('aria-current')});
      pv.disabled=i===0;nx.disabled=i===n-1;var t=th[i];if(t&&t.scrollIntoView)t.scrollIntoView({block:'nearest',inline:'nearest'})}
    th.forEach(function(t,j){t.addEventListener('click',function(){show(j,true)})});
    pv.addEventListener('click',function(){show(cur-1,true)});nx.addEventListener('click',function(){show(cur+1,true)});
    var tk;g.addEventListener('scroll',function(){clearTimeout(tk);tk=setTimeout(function(){if(Date.now()<lock)return;mark(Math.round(g.scrollLeft/Math.max(1,g.clientWidth)))},80)},{passive:true});
    w.addEventListener('keydown',function(ev){if(ev.key==='ArrowRight'){show(cur+1,true)}else if(ev.key==='ArrowLeft'){show(cur-1,true)}});
  });
})();
"""

WA_PRINTED = "+91 63971 21223"  # as printed in the footer
# Organization: only what the footer and header print (name, Sambhal, Uttar Pradesh, the mail and the WhatsApp number). Home, designs.html, bulk.html.
ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Woodkari Exports", "alternateName": "Woodkari",
       "url": SITE + "/", "logo": SITE + "/icon-512.png", "email": EMAIL,
       "address": {"@type": "PostalAddress", "addressLocality": "Sambhal", "addressRegion": "Uttar Pradesh", "addressCountry": "IN"},
       "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": WA_PRINTED, "email": EMAIL}}
ORG_LD = json.dumps([
    {"@context": "https://schema.org", "@type": "WebSite", "name": "Woodkari", "alternateName": "Woodkari Exports", "url": SITE + "/"}, ORG])
ORG_ONLY_LD = json.dumps(ORG)

HELLO = "Hello Woodkari, I have a question."
BULK_MSG = "Hello Woodkari, I want a bulk order.\nPiece:\nQuantity:\nCity: "

# Every answer repeats a line already checked on this site (ops/checks/2026-11-14-site-v2.md).
FAQ = [("What is the minimum for a bulk order?", "Trays and boxes: 25 pieces of one design. Small pieces such as coasters and tissue boxes are made in larger lots; ask us."),
       ("Can you put our name or logo on the pieces?", "Yes, on the wooden pieces, by laser, on 50 pieces or more of one design: a hotel name, a company logo or a couple's names."),
       ("Can you change the size?", "The acacia pieces can be made in any size, on order."),
       ("How long does an order take?", "Wooden pieces: about 10 to 15 days for 100. Resin pieces: we tell you the time when you ask."),
       ("How does payment work?", "A single piece up to ₹10,000 is paid in full when you order, by UPI or bank transfer. For a piece above ₹10,000, such as furniture, and for a bulk order, a 50% advance starts the order and the rest is paid before dispatch."),
       ("Can I cancel or return a piece?", "You can cancel for free until we start making. Every piece is made for you, so there are no returns for a change of mind. If a piece arrives damaged, tell us on WhatsApp within 48 hours with an uncut unboxing video, and we replace it. The full terms are on the Order terms page."),
       ("Who pays for delivery?", "Delivery is at the buyer's cost. We tell you the amount before the order leaves."),
       ("Can I buy just one piece?", "Yes. Every piece with a price can be ordered on its own. Tap \"Order on WhatsApp\" on the piece and tell us your city and PIN code; we confirm the delivery charge, the time and how to pay.")]


def pixel():
    """Meta Pixel base code + three events. No advanced matching, no personal data."""
    if not PIXEL_ID:
        return ""
    return ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
            f"fbq('init','{PIXEL_ID}');fbq('track','PageView');"
            "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';"
            "if(h.indexOf('wa.me')>-1||h.indexOf('api.whatsapp.com')>-1)fbq('track','Contact');else if(h.indexOf('mailto:')===0)fbq('track','Lead')},true);"
            "document.addEventListener('DOMContentLoaded',function(){try{var s=document.querySelectorAll('script[type=\"application/ld+json\"]');for(var i=0;i<s.length;i++){var j=JSON.parse(s[i].textContent);if(j&&j['@type']==='Product'){var o=j.offers||{};"
            "fbq('track','ViewContent',{content_name:j.name,value:Number(o.lowPrice||o.price)||0,currency:'INR'});break}}}catch(x){}});</script>\n"
            f'<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1" alt=""></noscript>\n')


def head(title, desc, path, image):
    robots = '<meta name="robots" content="noindex">' if PREVIEW else ""
    # Google Analytics 4 (property "Woodkari Exports", stream "Woodkari Exports website", ID from Friday 17 Nov); live site only
    ga = "" if PREVIEW else '<script async src="https://www.googletagmanager.com/gtag/js?id=G-BMRGF7V5ZR"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","G-BMRGF7V5ZR")</script>'
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,interactive-widget=resizes-content">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
{ga}
{pixel()}<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Woodkari">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/img/{image}">
<meta name="theme-color" content="#1d4a3a">
<link rel="preload" href="{UP}fonts/instrument-serif-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}fonts/hanken-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{UP}favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="{UP}icon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="{UP}icon-96.png">
<link rel="apple-touch-icon" href="{UP}apple-touch-icon.png">
<link rel="stylesheet" href="site.css?v={ASSET_V["css"]}">
<script>document.documentElement.className+=" js";addEventListener("pagereveal",function(e){{var n=window.navigation&&navigation.activation;if(!e.viewTransition||!n||!n.from||document.querySelector('[style*="view-transition-name"]'))return;var im=document.querySelector('.p[href="'+n.from.url.split("/").pop().split(/[?#]/)[0]+'"] .ph img');if(im){{im.style.viewTransitionName="pic";im.closest(".p").classList.add("in","now")}}}})</script>
<script src="site.js?v={ASSET_V["js"]}" defer></script>
</head>
"""


ASSET_V = {"css": "0", "js": "0"}  # filled in main() from the file hashes


def search_data():
    items = []
    for p in PRODUCTS:
        sub = p["short"] + (" · " + bulk_line(p["slug"]) if p.get("bulk_only") else " · " + rupee(p["price"])) + " · " + ("Made to order" if p.get("mto") else "Plain photo of our piece")
        items.append({"n": p["name"], "s": sub, "u": p["slug"] + ".html", "i": f"{UP}img/{p['card'][0]}-600.webp"})
    for k, n in DESIGNS:
        items.append({"n": n, "s": "Made to order · in bulk", "u": wa("Hello Woodkari, I am asking about: " + n + "\nQuantity: "), "i": f"{UP}img/{k}.webp"})
    for it in OW:
        sub = rupee(it["price"]) if it["price"] and not it.get("pack") else ow_price_lines(it)[0]
        items.append({"n": it["name"], "s": f"Design {it['code']} · {ow_wood(it)} wood, made to order · {sub}", "u": mto_page(it["code"]), "i": f"{UP}img/{ow_key(it['code'])}-600.webp"})
    for it in NB:
        items.append({"n": it["name"], "s": f"Design {it['code']} · made to order, {bx_from(it)}", "u": mto_page(it["code"]), "i": f"{UP}img/{bx_key(it["code"])}-600.webp"})
    for it in LST:
        items.append({"n": it["name"], "s": f"Design {it['code']} · made to order, {it['price_text'].lower() if not it['price'] else it['price_text']}", "u": mto_page(it["code"]), "i": f"{UP}img/{it['pics'][0][1]}-600.webp"})
    for gid, code, f, n in mto_items():
        items.append({"n": n, "s": f"Design {code} · made to order, " + (mto_pr(code)[0] if code in MTO_PRICE else "price on WhatsApp"), "u": mto_page(code), "i": f"{UP}img/m-{f}-600.webp"})
    items.append({"n": "Bulk and hotel orders", "s": "Trays and boxes from 25 of one design · Styled picture", "u": "bulk.html", "i": f"{UP}img/room-front-600.webp"})
    return json.dumps(items).replace("</", "<\\/")


def header(cur):
    pv = '<div class="pv">Preview. Not the live site yet.</div>' if PREVIEW else ""
    tree = menu_tree()
    tabs = ""
    for g, gp, ss, tot in tree:
        c = ' aria-current="true"' if cur == gp else ""
        if len(ss) == 1:
            tabs += f'<div class="tg"><a href="{ss[0][1]}.html"{c}>{e(g)}</a></div>'
        else:
            tm = f'<a href="{gp}.html">All {e(g.lower())}</a>' + "".join(f'<a href="{p}.html">{e(n)}</a>' for n, p, c2 in ss)
            tabs += f'<div class="tg"><a href="{gp}.html"{c}>{e(g)}</a><div class="tm">{tm}</div></div>'
    tabs += f'<div class="tg"><a href="bulk.html"{" aria-current=true" if cur == "bulk" else ""}>Bulk orders</a></div>'
    top, panes = "", ""
    for i, (g, gp, ss, tot) in enumerate(tree):
        st = f'style="--d:{50 + i * 18}ms"'
        if len(ss) == 1:
            top += f'<a href="{ss[0][1]}.html" {st}>{e(g)}{TARR}</a>'
        else:
            top += f'<a href="{gp}.html" data-pane="pn-{gp}" {st}>{e(g)}{TARR}</a>'
            panes += (f'<div class="pane sub" id="pn-{gp}" inert><button class="dm-back" type="button">{TBACK}{e(g)}</button>'
                      f'<a href="{gp}.html">All</a>' + "".join(f'<a href="{p}.html">{e(n)}</a>' for n, p, c2 in ss) + "</div>")
    top += f'<a href="bulk.html" style="--d:{50 + len(tree) * 18}ms">Bulk and hotel orders{TARR}</a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
{pv}<header class="hd">
<div class="wrap hd-top">
<div class="hd-l"><button class="ib menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer">{MENU_ICON}</button><button class="ib search" type="button" aria-label="Search" aria-expanded="false" aria-controls="srch">{SEARCH_ICON}</button><span class="hd-note">Made in India since 2008</span></div>
<a class="logo" href="./" aria-label="Woodkari home"><b>Woodkari</b><small>EXPORTS</small></a>
<div class="hd-r"><a class="ib hd-ig" href="https://www.instagram.com/woodkariexports/" target="_blank" rel="noopener" aria-label="Instagram">{IG_ICON}</a><form class="hd-sb" role="search" onsubmit="return false">{SEARCH_ICON}<input type="search" placeholder="Search" aria-label="Search the pieces" autocomplete="off" enterkeyhint="search"></form><a class="hd-wa" href="{e(wa(HELLO))}">{WA_ICON}WhatsApp</a><a class="ib hd-waic" href="{e(wa(HELLO))}" aria-label="WhatsApp">{WA_OUT}</a></div>
</div>
<div class="tabs"><div><nav class="wrap" aria-label="Shop">{tabs}</nav></div></div>
</header>
<dialog class="drawer" id="drawer" aria-label="Menu"><div class="dr-in">
<div class="dm-hd"><div class="dm-l"><button class="ib" type="button" data-close aria-label="Close menu">{X_ICON}</button><a class="ib" href="{e(wa(HELLO))}" aria-label="WhatsApp">{WA_OUT}</a></div><a class="logo dm-logo" href="./" aria-label="Woodkari home"><b>Woodkari</b><small>EXPORTS</small></a><span></span></div>
<nav class="dm" aria-label="Menu"><div class="pane p0">{top}</div>{panes}</nav>
</div></dialog>
<dialog class="srch" id="srch" aria-label="Search"><div class="sr-in">
<div class="sr-bar"><input type="search" placeholder="Search trays, boxes, designs" aria-label="Search the pieces" autocomplete="off" enterkeyhint="search"><button class="ib" type="button" data-close aria-label="Close search">{X_ICON}</button></div>
<ul class="sr-list"></ul>
<p class="sr-none" hidden>Nothing by that name. <a href="{e(wa(HELLO))}">Ask us on WhatsApp</a>.</p>
</div></dialog>
<script type="application/json" id="sx">{search_data()}</script>
"""


def foot_cats():
    return "".join(f'<a class="l" href="{gp}.html">{e(g)}</a>' for g, gp, ss, tot in menu_tree())


def footer():
    return f"""<footer class="ft"><div class="wrap">
<div><a class="fl" href="./" aria-label="Woodkari home"><img src="{UP}icon-96.png" width="40" height="40" alt=""><b>Woodkari</b></a>
<p>Woodkari Exports, Sambhal, Uttar Pradesh. Wooden and resin trays and boxes, making since 2008. Bulk orders from 25 pieces; single pieces on WhatsApp.</p></div>
<div><h3>Shop</h3>{foot_cats()}<a class="l" href="designs.html">Made to order designs</a><a class="l" href="bulk.html">Bulk and hotel orders</a><a class="l" href="terms.html">Order terms</a><a class="l" href="refund-cancellation.html">Refund and cancellation</a><a class="l" href="shipping.html">Shipping and delivery</a><a class="l" href="privacy.html">Privacy policy</a><a class="l" href="about.html">About us</a><a class="l" href="contact.html">Contact us</a><a class="l" href="./#engraving">Name and logo engraving</a><a class="l" href="./#questions">Questions</a></div>
<div><h3>Talk to us</h3><a class="l" href="{e(wa(HELLO))}">WhatsApp +91 63971 21223</a><a class="l" href="mailto:{EMAIL}">{EMAIL}</a></div>
<p class="fine">Pictures marked "Made to order" or "Styled picture" are made to show the look of a piece; wood grain and resin differ a little on every piece. Only pictures marked "plain photo" are photos of our own pieces.</p>
</div>
<div class="mega" aria-hidden="true"><span>Woodkari</span></div></footer>
<a class="fab" href="{e(wa(HELLO))}" aria-label="Chat on WhatsApp">{WA_ICON}</a>
"""


def price_html(p, cls="pr"):
    if p.get("bulk_only"):
        return f'<p class="{cls}">{bulk_line(p["slug"])}</p>'
    unit = f' <span>/ {e(p["unit"])}</span>' if p.get("unit") else ""
    return f'<p class="{cls}">{rupee(p["price"])}{unit}</p>'


def card(p):
    a, b = p["card"]
    alt, cap = next((x[1], x[2]) for x in p["imgs"] if x[0] == a)
    lab = cap.split(",")[0] if cap.startswith("Design") else cap
    hov = f'<img class="u" src="{UP}img/{b}-600.webp" alt="" width="600" height="600" loading="lazy">' if b else ""
    return f"""<a class="p rv" data-cat="{p['cat']}" href="{p['slug']}.html">
<div class="ph"><img src="{UP}img/{a}-600.webp" alt="{e(alt)}" width="600" height="600" loading="lazy">{hov}<span class="tag">{lab}</span></div>
<h3>{e(p['name'])}</h3><p class="sh">{e(p['short'])}</p>{price_html(p)}</a>"""


# Categories (owner D-332, 22 Nov): a side menu like artychoke.in. A few top groups; each opens to "All" plus one page per product type.
# Every piece sits in exactly ONE product-type page (SUBS). A group or type with no live piece is left out of the menu and gets no page.
# (group name, group page, [(type name, page, intro)]); a group with one type is a single page and a direct link in the menu.
TAX = [
    ("Trays", "trays", [("Resin trays", "resin-trays"), ("Painted trays", "painted-trays"), ("Inlay trays", "inlay-trays"), ("Wooden trays", "wooden-trays")]),
    ("Tableware", "tableware", [("Bowls and platters", "bowls"), ("Boards", "boards"), ("Coasters", "coasters"), ("Napkin rings", "napkin-rings"),
                                ("Cake stands", "cake-stands"), ("Jars and jugs", "jars-and-jugs"), ("Kitchen and bar", "kitchen-and-bar")]),
    ("Home decor", "home-decor", [("Candle holders", "candle-holders"), ("Frames and mirrors", "frames-and-mirrors"), ("Clocks", "clocks"), ("Lamps", "lamps"),
                                  ("Decor and stands", "decor-and-stands")]),
    ("Boxes", "boxes", [("Jewellery boxes", "jewellery-boxes"), ("Tissue boxes", "tissue-boxes"), ("Gift and storage boxes", "gift-and-storage-boxes")]),
    ("Furniture", "furniture", [("Inlay chests", "inlay-chests"), ("Tables and stools", "tables-and-stools")]),
    ("Bathroom", "bathroom", [("Bathroom sets and vanity", "bathroom")]),
]
SUB_OF = {}  # page -> group page
for _g, _gp, _subs in TAX:
    for _n, _p in _subs:
        SUB_OF[_p] = _gp
LST_SUB = {"Coasters": "coasters", "Napkin rings": "napkin-rings", "Bowls": "bowls", "Boards": "boards", "Kitchen and bar": "kitchen-and-bar", "Bathroom": "bathroom",
           "Candle holders": "candle-holders", "Lamps": "lamps", "Clocks": "clocks", "Frames and mirrors": "frames-and-mirrors"}
LST_PAINTED = {"NP-06", "NP-08", "NP-09", "NP-10", "N100-024"}


def sub_of(key, name="", cat=""):
    """the one product-type page a piece belongs to"""
    fixed = {"navy-ivory-floral-tray": "resin-trays", "black-white-floral-tray-set": "resin-trays", "red-chevron-tray": "resin-trays", "gold-flake-resin-tray": "resin-trays",
             "fluted-box-tray": "wooden-trays", "room-tray": "wooden-trays",
             "d-coaster": "coasters", "d-tissue": "tissue-boxes", "d-roundbox": "gift-and-storage-boxes", "d-board": "boards", "d-cutlery": "kitchen-and-bar", "d-trivet": "kitchen-and-bar",
             "OW-01": "wooden-trays", "OW-18": "wooden-trays", "OW-32": "wooden-trays", "OW-33": "wooden-trays", "OW-37": "wooden-trays", "OW-03": "bowls", "OW-08": "boards",
             "OW-16": "coasters", "OW-25": "candle-holders", "OW-36": "gift-and-storage-boxes", "IC-N01": "jewellery-boxes",
             "PT-6": "bowls", "PT-8": "boards", "N100-096": "kitchen-and-bar", "N100-097": "bathroom", "NP-30": "jars-and-jugs", "N100-093": "jars-and-jugs", "N100-094": "jars-and-jugs"}
    if key in fixed:
        return fixed[key]
    if key.startswith("PX-") or key.startswith("PT-"):
        return "painted-trays"
    if key.startswith("BS-"):
        return "bathroom"
    if key.startswith("RB-"):
        return "bowls"
    if key.startswith("WB-"):
        return "boards"
    if key.startswith("CS-"):
        return "candle-holders"
    if key.startswith("IC-"):
        return "inlay-chests"
    if key.startswith("OW-"):
        return "tables-and-stools"
    low = name.lower()
    if cat in LST_SUB:
        return LST_SUB[cat]
    if cat == "Trays":
        if key in LST_PAINTED:
            return "painted-trays"
        if "inlay" in low or "mother-of-pearl" in low:
            return "inlay-trays"
        if low.startswith("resin") or "resin" in low.split(" and ")[0] or "wood and resin" in low:
            return "resin-trays"
        return "wooden-trays"
    if cat == "Decor":
        return "cake-stands" if ("cake stand" in low or "tier" in low) else "decor-and-stands"
    if cat == "Boxes":
        return "tissue-boxes" if "tissue" in low else ("jewellery-boxes" if "jewellery" in low else "gift-and-storage-boxes")
    raise SystemExit("NO CATEGORY for " + key + " " + name)


# Home page: a small curated set (owner D-332: "Home screen pe sirf achhe achhe product"). The first 12 of HOME_PICKS that are live are shown;
# HOME_SPARE fills any gap (while the 22 Nov listings are not live yet, the spare ones carry the page).
HOME_PICKS = ["navy-ivory-floral-tray", "black-white-floral-tray-set", "N100-001", "N100-003", "NP-16", "N100-042", "N100-075", "N100-060", "N100-072", "N100-028", "N100-095", "OW-38"]
HOME_SPARE = ["gold-flake-resin-tray", "red-chevron-tray", "d-coaster", "OW-01", "IC-1", "BS-1", "PT-1", "OW-36"]


def all_cards():
    """every piece on the site: list of (key, name, sub page, card html), in a fixed order"""
    items = []
    for p in PRODUCTS:
        items.append((p["slug"], p["name"], "", card(p)))
    for k, n in DESIGNS:
        href = e(wa("Hello Woodkari, I am asking about: " + n + chr(10) + "Quantity: "))
        items.append((k, n, "", f'<a class="p rv" href="{href}"><div class="ph"><img src="{UP}img/{k}.webp" alt="{e(n)}, design picture" width="480" height="480" loading="lazy"><span class="tag">Made to order</span></div>'
                      f'<h3>{e(n)}</h3><p class="sh">Made to order · in bulk</p><p class="pr bo">Ask on WhatsApp</p></a>'))
    for it in OW:
        items.append((it["code"], it["name"], "", ow_card(it)))
    for it in NB:
        items.append((it["code"], it["name"], "", bx_card(it)))
    for gid, code, f, n in mto_items():
        items.append((code, n, "", f'<a class="p rv" href="{mto_page(code)}"><div class="ph"><img src="{UP}img/m-{f}-600.webp" alt="{e(MTO_ALT.get(code, n + ", design picture"))}" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
                      f'<h3>{e(n)}</h3><p class="sh">Design {code} · made on order</p><p class="pr{"" if code in MTO_PRICE else " bo"}">{e(mto_pr(code)[0])}</p></a>'))
    for it in LST:
        items.append((it["code"], it["name"], it["cat"], lst_card(it)))
    lcat = {x["code"]: x["cat"] for x in LST}
    out = []
    for k, n, c, h in items:
        h = re.sub(r'data-cat="[^"]*" ', "", h, count=1)
        out.append((k, n, sub_of(k, n, lcat.get(k, "")), clean_card(h)))
    return out


ASK_ARR = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def clean_card(h):
    """owner 22 Nov 18:20: lighter cards on home and category pages. The picture badge goes; its words stay as small grey text in the
    line under the title (the footer note explains what "Made to order" / "Styled picture" / "plain photo" mean), unless that line already says made to order.
    "... on WhatsApp" becomes a small outlined button; a real price stays, smaller."""
    m = re.search(r'<span class="tag">([^<]*)</span>', h)
    tag = m.group(1) if m else ""
    if m:
        h = h.replace(m.group(0), "", 1)
    sh = re.search(r'<p class="sh">(.*?)</p>', h)
    if tag and sh and not (tag.lower() == "made to order" and re.search(r"made (on|to) order", sh.group(1), re.I)):
        h = h.replace(sh.group(0), f'<p class="sh">{sh.group(1)} · {tag[0].lower() + tag[1:]}</p>', 1)
    pr = re.search(r'<p class="pr( bo)?">([^<]*WhatsApp[^<]*)</p>', h)
    if pr:
        label = "Get price on WhatsApp" if pr.group(2) == "Price on WhatsApp" else pr.group(2)  # owner D-335
        h = h.replace(pr.group(0), f'<p class="pr ask"><span>{label}</span></p>', 1)
    return h.replace('<a class="p rv"', '<a class="p cc rv"', 1)


CARDS, CARD_BY = [], {}  # filled in main(), once every card builder exists


def menu_tree():
    """[(group name, group page, [(type name, page, count)], total)], only what has pieces"""
    cnt = {}
    for _, _, sp, _ in CARDS:
        cnt[sp] = cnt.get(sp, 0) + 1
    tree = []
    for g, gp, subs in TAX:
        ss = [(n, p, cnt[p]) for n, p in subs if cnt.get(p)]
        if ss:
            tree.append((g, gp, ss, sum(c for _, _, c in ss)))
    return tree


def home_picks():
    keys = [k for k in HOME_PICKS if k in CARD_BY]
    keys += [k for k in HOME_SPARE if k in CARD_BY and k not in keys][:max(0, 12 - len(keys))]
    keys = keys[:12]
    return keys, "\n".join(CARD_BY[k][2] for k in keys)


def faq_html():
    rows = "".join(f'<details name="faq"><summary>{e(q)}{PLUS}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    return f'<div class="faq rv">{rows}</div>'


def page_home():
    pick_keys, cards = home_picks()
    chips = "".join(f'<a href="{gp}.html">{e(g)}<span>{tot}</span></a>' for g, gp, ss, tot in menu_tree())
    tiles = "".join(f'<a class="tile rv" href="{h}"><span class="tag">{lab}</span><img src="{UP}img/{k}.webp" alt="{e(alt)}" width="1200" height="1200" loading="lazy"><span class="cap">{e(t)}<small>{e(sub)}</small></span></a>' for k, t, sub, h, alt, lab in TILES)
    byslug = {q["slug"]: q for q in PRODUCTS}
    hero_top = mto_pr("OW-38")[0]  # owner 18 Nov: inlay drum table room shot is the first hero picture
    slide0 = f'<a class="slide on" href="design-ow-38.html"><img src="{UP}img/m-bone-inlay-coffee-table-38-e.webp" alt="Round bone inlay drum coffee table with a black and white sunburst pattern, in a living room" width="1200" height="1200" fetchpriority=high><span class="tag">Design picture, made to order</span><span class="nm">Inlay drum coffee table<span>{hero_top}</span></span></a>'
    slides = slide0 + "".join(
        f'<a class="slide" href="{sl}.html"><img {LATER}="{UP}img/{k}.webp" alt="{e(next((a for kk, a, *_ in byslug[sl]["imgs"] if kk == k), byslug[sl]["name"]))}" width="1200" height="1200" decoding=async><span class="tag">Made to order</span><span class="nm">{e(byslug[sl]["name"])}<span>{bulk_line(sl) if byslug[sl].get("bulk_only") else rupee(byslug[sl]["price"])}</span></span></a>'
        for i, (k, sl) in enumerate(SLIDES))
    dots = '<button class="dot" type="button" data-i="0" aria-label="Show Inlay drum coffee table" aria-current=true><span>Inlay table</span></button>' + "".join(f'<button class="dot" type="button" data-i="{i + 1}" aria-label="Show {e(byslug[sl]["name"])}"><span>{e(byslug[sl]["name"].split(" Tray")[0].replace(" Floral", "").replace(" Resin", ""))}</span></button>' for i, (k, sl) in enumerate(SLIDES))
    ribbon_items = ["Made in India since 2008", "Trays and boxes in bulk from 25 pieces", "Your name or logo from 50 pieces", "Acacia pieces in any size", "Finished by hand", "Order on WhatsApp"]
    ribbon = "".join(f"<span>{e(t)}</span>" for t in ribbon_items * 2)
    # the strip under "Made on order, in bulk": the first design of each made-to-order group (the six loose design pictures moved up into the grid)
    first = {}
    for gid, code, f, n in mto_items():
        first.setdefault(gid, (code, f, n))
    dz = "".join(f'<a class="rv" href="{mto_page(code)}"><div class="ph"><img src="{UP}img/m-{f}-600.webp" alt="{e(MTO_ALT.get(code, n + ", design picture"))}" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div><b>{e(n)}</b><i>{e(mto_pr(code)[0])}</i></a>'
                 for code, f, n in (first[g] for g in ("painted", "bath", "bowls", "boards", "candles", "chests")))
    return head("Wooden & Resin Trays, Boxes in Bulk | Woodkari, India",
                "Acacia wood and resin trays and boxes from India, making since 2008. Bulk from 25 pieces, name or logo from 50, single pieces on WhatsApp.",
                "", "fluted-front.jpg") + f"""<body>
{header('all')}
<main id="main">
<p class="topline"><span>Every piece is made to order</span><span>Bulk from 25 pieces</span></p>
<section class="hero">
<div class="show">{slides}</div>
<div class="hero-txt">
<h1><span class="ln"><span>Made in</span></span><span class="ln"><span>India.</span></span></h1>
<p class="fade">Wooden trays and resin pieces.<span class="more"> Making since 2008. Most of our orders are bulk: trays and boxes from 25 of one design. Single pieces too, on WhatsApp.</span></p>
<div class="row fade d2"><a class="btn pri" href="#shop">Explore the collection{ARROW}</a><a class="btn inv" href="#shop">Explore the collection{ARROW}</a><a class="btn ghost" href="bulk.html">Bulk orders</a></div>
<div class="dots fade d3" role="group" aria-label="Pictures">{dots}{PP}</div>
</div>
</section>
<div class="ribbon" aria-hidden="true"><div class="track">{ribbon}</div></div>

<section class="sec" id="shop"><div class="wrap">
<div class="hdr rv"><div><h2 id="shop-t">Our best pieces</h2><p id="shop-n">Every piece is made to order. Prices are for one piece; delivery is extra.</p></div></div>
<div class="grid">
{cards}
</div>
<nav class="chips hchips" aria-label="Shop by kind">{chips}</nav>
</div></section>

<section class="band green" id="bulk"><div class="wrap split">
<div class="fig wipe"><img src="{UP}img/navy-stack.webp" alt="Five navy and ivory floral trays stacked, for bulk orders" width="1200" height="1200" loading="lazy"><span class="tag">Made to order</span></div>
<div class="rv">
<h2>For hotels, shops and gifting.</h2>
<p class="lead">Bulk is most of our work. Hotels, gifting companies, shops and importers can order our trays and boxes from 25 pieces of a design, and the acacia pieces in any size.</p>
<ol class="steps">
<li><b>Send the piece and the number</b><span>On WhatsApp or by mail, with your city.</span></li>
<li><b>We send the price</b><span>A 50% advance starts the order.</span></li>
<li><b>Made and sent</b><span>Wooden pieces: about 10 to 15 days for 100. Resin pieces: we tell you the time. Delivery is at your cost, quoted before it leaves.</span></li>
</ol>
<div class="row"><a class="btn inv" href="{e(wa(BULK_MSG))}">{WA_ICON}Discuss your order</a><a class="btn ghost" href="bulk.html">Bulk orders in detail{ARROW}</a></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Where they go</h2></div></div>
<div class="tiles">{tiles}</div>
</div></section>

<section class="sec" id="engraving"><div class="wrap split rev">
<div class="fig wipe eng"><img src="{UP}img/engraved-logo.webp" alt="Wooden serving board with the Woodkari Exports logo engraved by laser, design picture" width="1200" height="1200" loading="lazy"><span class="tag">Design picture</span></div>
<div class="rv">
<h2>Your name or logo, by laser.</h2>
<p class="lead">On 50 pieces or more of one design, we engrave a hotel name, a company logo or a couple's names: room trays for a hotel, boxes and boards for staff gifts or a wedding.</p>
<div class="row"><a class="btn pri" href="{e(wa('Hello Woodkari, I want my name or logo engraved.' + chr(10) + 'Piece:' + chr(10) + 'Quantity: '))}">{WA_ICON}Ask about engraving</a></div>
</div>
</div></section>

<section class="band stone" id="workshop"><div class="wrap ws">
<div class="rv"><h2>The workshop</h2></div>
<div class="rv">
<p class="lead">Woodkari is a workshop in India, at work since 2008. Four karigars cut the wood on a CNC router, engrave by laser and finish our wooden pieces by hand. Our resin trays are made with other makers near our workshop.</p>
</div>
</div></section>

<section class="sec" id="questions"><div class="wrap split" style="align-items:start">
<div class="rv"><h2>Questions buyers ask</h2><p class="lead">Not here? Ask us on WhatsApp.</p></div>
{faq_html()}
</div></section>

<section class="end"><div class="wrap rv">
<h2>Tell us what you need.</h2>
<p>The piece, the size and how many. We reply on WhatsApp.</p>
<div class="row"><a class="btn pri" href="{e(wa(HELLO))}">{WA_ICON}Chat on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}">{MAIL}{EMAIL}</a></div>
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_LD}</script>
</body></html>
"""


def page_product(p):
    if p.get("bulk_only"):
        msg = f"Hello Woodkari, I want to order: {p['name']} ({bulk_line(p['slug'])}).\nQuantity:\nMy city and PIN code: "
        btn = "Order on WhatsApp"
        stick_l = bulk_line(p["slug"])
    else:
        msg = f"Hello Woodkari, I want to order: {p['name']} ({rupee(p['price'])}).\nMy city and PIN code: "
        btn = "Order on WhatsApp"
        stick_l = rupee(p["price"])
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(alt)}" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if k == p["card"][0] else ""}{"" if i == 0 else " loading=lazy"}><figcaption>{e(cap)}</figcaption></figure>'
        for i, (k, alt, cap) in enumerate(p["imgs"]))
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in p["facts"])
    offer = {"@type": "Offer", "priceCurrency": "INR", "availability": "https://schema.org/MadeToOrder"}
    if p.get("price"):
        offer["price"] = p["price"]
    elif p["slug"] in BULK_ONLY_PRICE:
        offer["price"] = BULK_ONLY_PRICE[p["slug"]]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p["name"],
                     "image": f"{SITE}/img/{p['imgs'][0][0]}.webp", "description": p["lede"],
                     "brand": {"@type": "Brand", "name": "Woodkari"}, "offers": offer})
    notes = ""
    if p.get("bulk_only"):
        notes += '<p class="note">Delivery extra.</p>'
    else:
        notes += '<p class="note">Delivery is extra. We tell you the amount on WhatsApp.</p>'
    if p.get("mto"):
        notes += '<p class="note">Made to order. We tell you the making time on WhatsApp.</p>'
    more = "\n".join(card(q) for q in [x for x in PRODUCTS if x["slug"] != p["slug"]][:3])
    ogimg = {"fluted-box-tray": "fluted-front.jpg", "room-tray": "room-front.jpg"}.get(p["slug"], p["imgs"][0][0] + ".webp")
    bulk_l = "" if p.get("bulk_only") else '<a class="lnk more-l" href="bulk.html">Need 25 or more? Bulk orders' + ARROW + '</a>'
    pr = "" if p.get("bulk_only") else (f" {rupee(p['price'])} / {p['unit']}." if p.get('unit') else f" One piece {rupee(p['price'])}.")
    desc = fit(f"{p['desc']}{pr} Order on WhatsApp.", f"{p['desc']}{pr}")
    return head(p["title"], desc, p["slug"] + ".html", ogimg) + f"""<body class="has-stick">
{header(p['cat'])}
<main id="main"><div class="wrap">
<p class="crumb"><a href="./#shop">All pieces</a> / {e(p['name'])}</p>
<div class="pd">
{gallery([k for k, _a, _c in p["imgs"]], figs)}
<div class="buy">
<h1>{e(p['name'])}</h1>
{price_html(p)}
{notes}
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}{btn}</a></div>
<p class="lede">{e(p['lede'])}</p>
<p class="uses"><b>Good for:</b> {e(p['uses'])}</p>
<ul class="facts">{facts}</ul>
{bulk_l}
</div>
</div>
<section class="sec"><div class="hdr rv"><div><h2>More pieces</h2></div></div><div class="grid more3">
{more}
</div></section>
</div></main>
<div class="stick"><b>{e(stick_l)}</b><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}{btn}</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def gallery(keys, figs):
    """One big picture, arrows, and a row of small pictures below (owner 16 Nov, like adouerwood.com)."""
    n = len(keys)
    if n < 2:
        return f'<div class="galw" style="--n:{n}"><div class="gal">{figs}</div></div>'
    th = "".join(f'<button type="button" class="th{" on" if i == 0 else ""}" data-i="{i}" aria-label="Picture {i + 1} of {n}"><img src="{UP}img/{k}-600.webp" alt="" width="600" height="600" loading="lazy"></button>' for i, k in enumerate(keys))
    return (f'<div class="galw has-th" style="--n:{n}"><div class="stage"><div class="gal">{figs}</div>'
            f'<button type="button" class="gnav gprev" aria-label="Previous picture" disabled>&#8249;</button>'
            f'<button type="button" class="gnav gnext" aria-label="Next picture">&#8250;</button></div>'
            f'<div class="thumbs">{th}</div></div>')


def page_design(gid, pre, title, line, items, i):
    f, n = items[i - MTO_START.get(gid, 1)]
    code = f"{pre}-{i}"
    msg = mto_msg(code, n)
    pics = mto_pics(f)
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(MTO_ALT.get(code, n + ", design picture"))}{"" if j == 0 else ", another view"}" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if j == 0 else " loading=lazy"}><figcaption>Design picture · made to order</figcaption></figure>'
        for j, k in enumerate(pics))
    if code in MTO_SIZES:
        fl = [("Design", code), ("Kind", title), ("Made", "On order")] + [(f"Size {sz}", rupee(pp)) for sz, pp in MTO_SIZES[code]]
    else:
        fl = [("Design", code), ("Kind", title), ("Made", "On order"), ("Price", mto_pr(code)[0] if code in MTO_PRICE else "On WhatsApp")] + ([("Size", MTO_PRICE[code][2])] if code in MTO_PRICE else [])
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in fl)
    pr_txt, pr_note = mto_pr(code)
    others = [(j, x) for j, x in enumerate(items, MTO_START.get(gid, 1)) if j != i and f"{pre}-{j}" not in MTO_HOLD][:3]
    more = "\n".join(
        f'<a class="p rv" href="{mto_page(f"{pre}-{j}")}"><div class="ph"><img src="{UP}img/m-{ff}-600.webp" alt="{e(MTO_ALT.get(f"{pre}-{j}", nn + ", design picture"))}" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
        f'<h3>{e(nn)}</h3><p class="sh">Design {pre}-{j} · made on order</p><p class="pr{"" if f"{pre}-{j}" in MTO_PRICE else " bo"}">{e(mto_pr(f"{pre}-{j}")[0])}</p></a>'
        for j, (ff, nn) in others)
    lede = MTO_TEXT.get(code) or f"Design {code}. {line}"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": n, "sku": code,
                     "image": f"{SITE}/img/m-{f}.webp", "description": lede, "brand": {"@type": "Brand", "name": "Woodkari"},
                     "offers": dict({"@type": "Offer", "priceCurrency": "INR", "availability": "https://schema.org/MadeToOrder"}, **({"price": MTO_PRICE[code][0]} if code in MTO_PRICE else {}))})
    if code in MTO_SIZES:
        _d = json.loads(ld)
        _d["offers"] = [{"@type": "Offer", "priceCurrency": "INR", "price": pp, "name": sz, "availability": "https://schema.org/MadeToOrder"} for sz, pp in MTO_SIZES[code]]
        ld = json.dumps(_d)
    dline = MTO_TEXT.get(code) or line
    return head(fit_title(seo_name(gid, n), code), (fit(f"{n} (design {code}). {dline} Made to order. {pr_txt}. {pr_note}", f"{n}. Made to order. {pr_txt}. {pr_note}") if pr_note else fit(f"{n} (design {code}). {dline} Made to order; ask the price on WhatsApp.", f"{n}. {dline} Made to order; ask the price on WhatsApp.")), mto_page(code), f"m-{f}-600.webp") + f"""<body class="has-stick">
{header('mto')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="designs.html">Made to order</a> / <a href="designs.html#g-{gid}">{e(title)}</a> / {code}</p>
<div class="pd">
{gallery(pics, figs)}
<div class="buy">
<h1>{e(n)}</h1>
<p class="pr{"" if pr_note else " bo"}">{e(pr_txt)}</p>
<p class="note">{"Made to order. " + e(pr_note) if pr_note else "Made to order. We reply with the price on WhatsApp."}</p>
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}{"Order on WhatsApp" if pr_note else "Ask the price on WhatsApp"}</a></div>
<p class="lede">{e(lede)}</p>
<ul class="facts">{facts}</ul>
<a class="lnk more-l" href="designs.html">All {ALL_N} designs{ARROW}</a>
</div>
</div>
<section class="sec"><div class="hdr rv"><div><h2>More {e(title.lower())}</h2></div></div><div class="grid more3">
{more}
</div></section>
</div></main>
<div class="stick"><b>{e(pr_txt)}</b><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}{"Order on WhatsApp" if pr_note else "Ask on WhatsApp"}</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


DIRECT_SALE = {
    "OW-36": dict(msg="Namaste, mujhe 9 khaane wala mango wood gift box order karna hai.", top="₹1,899", unit="1 box", stick="₹1,899",
                  packs=[("Pack of 2", "₹2,799 · about ₹1,400 per box"), ("Pack of 4", "₹4,699 · about ₹1,175 per box"), ("Pack of 10", "₹11,199 · about ₹1,120 per box")],
                  bulk="25 pieces or more: ₹699 per piece. Bulk: delivery extra, 50% advance.", meta="One box ₹1,899, delivery in India included."),
    "OW-37": dict(msg="Namaste, mujhe 4 khaane wala mango wood box ka 10 ka pack order karna hai.", top="₹3,399", unit="Pack of 10 · about ₹340 per box", stick="Pack of 10 ₹3,399",
                  packs=[], bulk="25 pieces or more: ask on WhatsApp.", meta="Pack of 10 ₹3,399, delivery in India included."),
}


def ow_card(it, anchor=False):
    """a card for designs.html (anchor=True gives it the id that the chips and :target use) and for "More" rows"""
    top, _ = ow_price_lines(it)
    pr = f'<p class="pr">{top}</p>'
    aid = f' id="{it["code"]}"' if anchor else ""
    return (f'<a class="p rv"{aid} href="{mto_page(it["code"])}"><div class="ph"><img src="{UP}img/{ow_key(it["code"])}-600.webp" alt="{e(it["name"])}, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
            f'<h3>{e(it["name"])}</h3><p class="sh">Design {it["code"]} · {ow_wood(it)} wood</p>{pr}</a>')


def page_ow(it):
    """One acacia made-to-order item: same layout as page_design, with the price lines from the catalogue and no size."""
    code, n = it["code"], it["name"]
    top, second = ow_price_lines(it)
    if it["price"]:
        msg = f"Hello Woodkari, I want to order design {code}: {n} ({top}).\nQuantity:\nMy city and PIN code: "
        btn = stick_btn = "Order on WhatsApp"
        stick_l = top
        price = f'<p class="pr">{top}</p>\n<p class="note">{e(second)}</p>\n<p class="note">Delivery is extra. We tell you the amount on WhatsApp.</p>'
        meta_price = (f"{top}; {second[0].lower() + second[1:]}." if it.get("unit") == "set" else f"One piece {top}; {second[0].lower() + second[1:]}.")
    else:
        msg = f"Hello Woodkari, I want to order design {code}: {n} ({top}).\nQuantity:\nMy city and PIN code: "
        btn = stick_btn = "Order on WhatsApp"
        stick_l = top
        price = f'<p class="pr">{e(top)}</p>\n<p class="note">Delivery extra.</p>'
        meta_price = top + "."
    order_block = ""
    if code in DIRECT_SALE:
        # direct sale (25 Nov): prices and lines from agency-research businesses/woodkari/direct_sale_price_decision.md, version 2 (PROPOSED, owner haan before live)
        ds = DIRECT_SALE[code]
        msg = ds["msg"]
        btn = stick_btn = "Order now"
        stick_l = ds["stick"]
        price = ""
        packs = ('<ul class="obp">' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in ds["packs"]) + "</ul>\n") if ds["packs"] else ""
        order_block = f"""<div class="ob">
<p class="pr">{e(ds["top"])} <span>{e(ds["unit"])}</span></p>
{packs}<p class="note">Price includes delivery in India.</p>
<p class="note">Rs 200 advance starts the making. The balance is paid before dispatch. Or pay the full amount now.</p>
<p class="note">Made to order. After you pay, we message you on WhatsApp to confirm your order and the making time. You can cancel for free until we start making.</p>
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}Order now</a></div>
<p class="note">{e(ds["bulk"])}</p>
</div>"""
        meta_price = ds["meta"]
    meta_wood = "Acacia wood, other woods on request." if ow_wood(it) == "acacia" else OW_MATERIAL_MANGO
    shown = [(x, v) for x, v in zip("abcdef", it["views"]) if x not in it.get("skip", "")]
    keys = [ow_key(code, x) for x, _ in shown]
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(n)}, {e(v)}, design picture" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if j == 0 else " loading=lazy"}><figcaption>Design picture · made to order</figcaption></figure>'
        for j, (k, (_, v)) in enumerate(zip(keys, shown)))
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in
                    [("Design", code), ("Material", OW_MATERIAL if ow_wood(it) == "acacia" else OW_MATERIAL_MANGO), ("Size", it.get("size", OW_SIZE)), ("Made", "On order")])
    more = "\n".join(ow_card(x) for x in ([x for x in OW if x["code"] != code and ow_wood(x) == ow_wood(it)] + [x for x in OW if ow_wood(x) != ow_wood(it)])[:3])
    lede = f"Design {code}. {it['what']}"
    offer = {"@type": "Offer", "priceCurrency": "INR", "availability": "https://schema.org/MadeToOrder"}
    if it["price"]:
        offer["price"] = it["price"]
    elif code in BULK_ONLY_PRICE:
        offer["price"] = BULK_ONLY_PRICE[code]
    if it.get("pack"):  # the price is for the whole pack: say so in the offer and in the schema name, so it is never read as a single-piece price
        offer["name"] = f"Pack of {it['pack']}"
        offer["description"] = f"Price is for a pack of {it['pack']} pieces, delivery in India included."
        offer["eligibleQuantity"] = {"@type": "QuantitativeValue", "value": it["pack"], "unitText": "pieces"}
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": n + (f", pack of {it['pack']}" if it.get("pack") else ""), "sku": code,
                     "image": f"{SITE}/img/{keys[0]}.webp", "description": f"{lede} {OW_MATERIAL if ow_wood(it) == "acacia" else OW_MATERIAL_MANGO}", "material": ow_wood(it).capitalize() + " wood",
                     "brand": {"@type": "Brand", "name": "Woodkari"}, "offers": offer})
    return head(fit_title(seo_name(OW_GID if ow_wood(it) == "acacia" else "mango", n), code), fit(f"{it['what']} Design {code}. {meta_wood} Made to order. {meta_price}", f"{it['what']} {meta_wood} Made to order. {meta_price}"),
                mto_page(code), f"{keys[0]}-600.webp") + f"""<body class="has-stick">
{header('mto')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="designs.html">Made to order</a> / <a href="designs.html#g-{OW_GID if ow_wood(it) == 'acacia' else 'mango'}">{e(OW_CHIP if ow_wood(it) == 'acacia' else MG_CHIP)}</a> / {code}</p>
<div class="pd">
{gallery(keys, figs)}
<div class="buy">
<h1>{e(n)}</h1>
{order_block if order_block else price + chr(10) + '<p class="note">Made to order. We tell you the making time on WhatsApp.</p>' + chr(10) + '<div class="row"><a class="btn pri wide" href="' + e(wa(msg)) + '">' + WA_ICON + btn + '</a></div>'}
<p class="lede">{e(lede)}</p>
<ul class="facts">{facts}</ul>
<a class="lnk more-l" href="designs.html">All {ALL_N} designs{ARROW}</a>
</div>
</div>
<section class="sec"><div class="hdr rv"><div><h2>{"More in acacia wood" if ow_wood(it) == "acacia" else "More made to order"}</h2></div></div><div class="grid more3">
{more}
</div></section>
</div></main>
<div class="stick"><b>{e(stick_l)}</b><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}{stick_btn}</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def lst_card(it, anchor=False):
    aid = f' id="{it["code"]}"' if anchor else ""
    pr = e(it["price_text"])
    return (f'<a class="p rv"{aid} href="{mto_page(it["code"])}"><div class="ph"><img src="{UP}img/{it["pics"][0][1]}-600.webp" alt="{e(it["name"])}, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
            f'<h3>{e(it["name"])}</h3><p class="sh">Design {it["code"]} · made on order</p><p class="pr">{pr}</p></a>')


def page_lst(it):
    """One listing from the 22 Nov CSV: same layout as page_ow."""
    code, n = it["code"], it["name"]
    top = it["price_text"]
    if it["price"]:
        msg = f"Hello Woodkari, I want to order design {code}: {n} ({top}).\nQuantity:\nMy city and PIN code: "
        price = f'<p class="pr">{e(top)}</p>\n<p class="note">Minimum order: {e(it["moq"])}.</p>\n<p class="note">Delivery is extra. We tell you the amount on WhatsApp.</p>'
        meta_price = f"{top}; minimum order {it['moq']}."
    else:
        msg = f"Hello Woodkari, I want a price for design {code}: {n}.\nQuantity:\nMy city and PIN code: "
        price = f'<p class="pr">{e(top)}</p>\n<p class="note">Delivery extra.</p>'
        meta_price = top + "."
    keys = [k for _, k, _ in it["pics"]]
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(n)}{LST_VIEWS.get(x, "")}, design picture" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if j == 0 else " loading=lazy"}><figcaption>Design picture · made to order</figcaption></figure>'
        for j, (x, k, _) in enumerate(it["pics"]))
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in
                    [("Design", code), ("Material", it["material"]), ("Size", it["size"]), ("Minimum order", it["moq"]), ("Made", "On order")])
    more = "\n".join(lst_card(x) for x in [y for y in LST if y["cat"] == it["cat"] and y["code"] != code][:3])
    gid = lst_gid(it["cat"])
    offer = {"@type": "Offer", "priceCurrency": "INR", "availability": "https://schema.org/MadeToOrder"}
    if it["price"]:
        offer["price"] = it["price"]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": n, "sku": code,
                     "image": f"{SITE}/img/{keys[0]}.webp", "description": f"{it['what']} Material: {it['material']}.", "material": it["material"],
                     "brand": {"@type": "Brand", "name": "Woodkari"}, "offers": offer})
    return head(fit_title(n, code), fit(f"{n}. Design {code}. {it['material']}. Made to order. {meta_price}", f"{n}. Made to order. {meta_price}", f"{n}. Made to order."),
                mto_page(code), f"{keys[0]}-600.webp") + f"""<body class="has-stick">
{header('mto')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="designs.html">Made to order</a> / <a href="designs.html#g-{gid}">{e(it["cat"])}</a> / {code}</p>
<div class="pd">
{gallery(keys, figs)}
<div class="buy">
<h1>{e(n)}</h1>
{price}
<p class="note">Made to order. We tell you the making time on WhatsApp.</p>
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
<p class="lede">{e(it["what"])}</p>
<ul class="facts">{facts}</ul>
<a class="lnk more-l" href="designs.html">All {ALL_N} designs{ARROW}</a>
</div>
</div>
{('<section class="sec"><div class="hdr rv"><div><h2>More made to order</h2></div></div><div class="grid more3">' + more + '</div></section>') if more else ''}
</div></main>
<div class="stick"><b>{e(top)}</b><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def page_designs():
    OW_AC = [x for x in OW if ow_wood(x) == "acacia"]
    OW_MG = [x for x in OW if ow_wood(x) == "mango"]
    chips = f'<a href="#g-{OW_GID}">{e(OW_CHIP)}<span>{len(OW_AC)}</span></a><a href="#g-mango">{e(MG_CHIP)}<span>{len(OW_MG)}</span></a>' + (f'<a href="#g-{BX_GID}">{e(BX_CHIP)}<span>{len(BX)}</span></a>' if BX else "") + "".join(f'<a href="#g-{gid}">{e(title)}<span>{len(items)}</span></a>' for gid, pre, title, line, items in MTO).replace('Painted trays and bowls<span>%d</span>' % 9, 'Painted trays and bowls<span>%d</span>' % (9 + len(PXL)))
    groups = [f'<section class="sec mto" id="g-{OW_GID}"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(OW_TITLE)}</h2><p>{e(OW_LINE)}</p></div></div>\n<div class="grid four">{"".join(ow_card(it, True) for it in OW_AC)}</div>\n</div></section>',
              f'<section class="sec mto" id="g-mango"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(MG_TITLE)}</h2><p>{e(MG_LINE)}</p></div></div>\n<div class="grid four">{"".join(ow_card(it, True) for it in OW_MG)}</div>\n</div></section>',
              f'<section class="sec mto" id="g-{BX_GID}"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(BX_TITLE)}</h2><p>{e(BX_LINE)}</p></div></div>\n<div class="grid four">{"".join(bx_card(it, True) for it in BX)}</div>\n</div></section>']
    if not BX:
        groups = [g for g in groups if f'id="g-{BX_GID}"' not in g]
    for cat in lst_cats():
        its = [x for x in LST if x["cat"] == cat]
        chips += f'<a href="#g-{lst_gid(cat)}">{e(cat)}<span>{len(its)}</span></a>'
        groups.append(f'<section class="sec mto" id="g-{lst_gid(cat)}"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(cat)}</h2><p>Made to order in India. Price on WhatsApp unless shown.</p></div></div>\n<div class="grid four">{"".join(lst_card(x, True) for x in its)}</div>\n</div></section>')
    for gid, pre, title, line, items in MTO:
        cards = "".join(
            f'<a class="p rv" id="{pre}-{i}" href="{mto_page(f"{pre}-{i}")}"><div class="ph"><img src="{UP}img/m-{f}-600.webp" alt="{e(MTO_ALT.get(f"{pre}-{i}", n + ", design picture"))}" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
            f'<h3>{e(n)}</h3><p class="sh">Design {pre}-{i} · made on order</p><p class="pr{"" if f"{pre}-{i}" in MTO_PRICE else " bo"}">{e(mto_pr(f"{pre}-{i}")[0])}</p></a>'
            for i, (f, n) in enumerate(items, MTO_START.get(gid, 1)) if f"{pre}-{i}" not in MTO_HOLD)
        if gid == "painted":
            cards += "".join(bx_card(it, True) for it in PXL)
            line = line + " " + PX_LINE
        groups.append(f'<section class="sec mto" id="g-{gid}"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(title)}</h2><p>{e(line)}</p></div></div>\n<div class="grid four">{cards}</div>\n</div></section>')
    return head("Made to Order Trays, Bowls, Boards, Candle Stands | Woodkari",
                f"{ALL_N} designs made on order: acacia wood trays, painted trays and bowls, resin bathroom sets and tableware, wooden boards, candle stands and inlay chests.",
                "designs.html", "m-og.jpg") + f"""<body>
{header('mto')}
<main id="main">
<section><div class="wrap mh">
<h1>Made on order.</h1>
<p>{ALL_N} more designs. Every picture here is a design picture, made to show the piece. Every design shows its price; open one and order on WhatsApp.</p>
<nav class="chips" aria-label="Kinds of pieces">{chips}</nav>
</div></section>
{chr(10).join(groups)}
<section class="end"><div class="wrap rv">
<h2>Not the one you want?</h2>
<p>Send us a picture of the piece, the size and how many. We reply on WhatsApp.</p>
<div class="row"><a class="btn pri" href="{e(wa(HELLO))}">{WA_ICON}Chat on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}">{MAIL}{EMAIL}</a></div>
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_ONLY_LD}</script>
</body></html>
"""


def cat_page(slug, title, subs, group=None):
    """one category page. subs = the type pages whose pieces it lists. group = (group name, group page, [(type name, page, count)]) for the chips"""
    cards = [(k, n, h) for k, n, sp, h in CARDS if sp in subs]
    chips = ""
    gname, gp, ss, tot = group
    if len(ss) > 1:
        chips = '<nav class="chips" aria-label="Kinds of ' + e(gname.lower()) + '">' + f'<a href="{gp}.html"{" aria-current=true" if slug == gp else ""}>All<span>{tot}</span></a>' + "".join(
            f'<a href="{p}.html"{" aria-current=true" if slug == p else ""}>{e(n)}<span>{c}</span></a>' for n, p, c in ss) + "</nav>"
    first_img = re.search(r'img/([A-Za-z0-9_.-]+?)-?6?0?0?\.webp', cards[0][2])
    og = (first_img.group(1) if first_img else "m-og") + ".webp"
    crumb = f'<a href="./">Home</a> / ' + (f'<a href="{gp}.html">{e(gname)}</a> / ' if slug != gp and len(ss) > 1 else "") + e(title)
    n = len(cards)
    return head(f"{title} | Woodkari, India", f"{n} {title.lower()} made to order in India. Prices are for one piece; delivery is extra. Order on WhatsApp.", f"{slug}.html", og) + f"""<body>
{header(gp)}
<main id="main">
<section><div class="wrap mh">
<p class="crumb" style="padding-top:0">{crumb}</p>
<h1>{e(title)}</h1>
<p>{n} {"piece" if n == 1 else "pieces"}. Every piece is made to order. Prices are for one piece; delivery is extra.</p>
{chips}
</div></section>
<section class="sec cat"><div class="wrap">
<div class="grid four">{"".join(h for _, _, h in cards)}</div>
</div></section>
<section class="end"><div class="wrap rv">
<h2>Not the one you want?</h2>
<p>Send us a picture of the piece, the size and how many. We reply on WhatsApp.</p>
<div class="row"><a class="btn pri" href="{e(wa(HELLO))}">{WA_ICON}Chat on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}">{MAIL}{EMAIL}</a></div>
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_ONLY_LD}</script>
</body></html>
"""


def category_pages():
    out = {}
    for g, gp, ss, tot in menu_tree():
        grp = (g, gp, ss, tot)
        if len(ss) == 1:
            out[ss[0][1] + ".html"] = cat_page(ss[0][1], g, [ss[0][1]], grp)
            continue
        out[gp + ".html"] = cat_page(gp, g, [p for _, p, _ in ss], grp)
        for n, p, c in ss:
            out[p + ".html"] = cat_page(p, n, [p], grp)
    return out


TERMS_SINGLE = [
    "Every piece is made to order. We start making it once you have ordered and paid, by UPI or bank transfer. Orders placed from a product page with a price: Rs 200 advance starts the making, or you can pay the full amount. Other orders of 3 or more pieces: 50% advance. The balance is paid before dispatch. For a piece above ₹10,000, such as furniture, a 50% advance, and the rest before dispatch. We tell you the making time on WhatsApp.",
    "You can cancel for free until we start making. Once making has started, the order cannot be cancelled.",
    "Each piece is made for you, so we do not take returns for a change of mind.",
    "If a piece arrives damaged or is not what you ordered, tell us on WhatsApp within 48 hours of delivery, with an uncut unboxing video and photos. We replace it, or return your money if we cannot replace it. We pay the shipping for this.",
    "Handmade pieces differ a little: wood grain and colour change from piece to piece. This is not a defect.",
    "Delivery is extra. We tell you the amount on WhatsApp, unless the product page says the price includes delivery.",
]
TERMS_BULK = [
    "A 50% advance starts the order. The other 50% is paid before dispatch.",
    "If you cancel before making starts, we return your advance. Once making has started, the advance is not returned, because the pieces are made for you.",
    "If pieces arrive damaged, tell us within 48 hours of delivery, with an uncut unboxing video and photos. We replace them in your next lot, or give you a credit.",
    "Delivery is at your cost, quoted before dispatch.",
    "Our price is valid for 15 days from our message.",
]


def page_terms():
    """Order terms (owner 18 Nov: "dekho baaki log kya karte hain"; research in agency-research businesses/woodkari/site/order_terms_research_18nov.md)."""
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return head("Order Terms | Woodkari, India",
                "How ordering works at Woodkari: payment, cancellation, damage and delivery, for single pieces and for bulk orders.",
                "terms.html", "room-front.jpg") + f"""<body>
{header('terms')}
<main id="main">
<section class="sec"><div class="wrap terms">
<h1>Order terms</h1>
<p>Short and simple. If anything is unclear, ask us on WhatsApp.</p>
<h2>Single pieces</h2>
<ol>{li(TERMS_SINGLE)}</ol>
<h2>Bulk orders, 25 pieces or more of one design</h2>
<ol>{li(TERMS_BULK)}</ol>
<div class="row"><a class="btn pri" href="{e(wa(HELLO))}">{WA_ICON}Ask on WhatsApp</a></div>
</div></section>
</main>
{footer()}
</body></html>"""


def policy_page(title, desc, path, h1, intro, sections, extra=""):
    body = "".join(f"<h2>{e(h)}</h2>" + (f"<ol>{''.join('<li>' + e(x) + '</li>' for x in xs)}</ol>" if isinstance(xs, list) else f"<p>{e(xs)}</p>") for h, xs in sections)
    return head(title, desc, path, "room-front.jpg") + f"""<body>
{header('terms')}
<main id="main">
<section class="sec"><div class="wrap terms">
<h1>{e(h1)}</h1>
<p>{e(intro)}</p>
{body}{extra}
<div class="row"><a class="btn pri" href="{e(wa(HELLO))}">{WA_ICON}Ask on WhatsApp</a></div>
</div></section>
</main>
{footer()}
</body></html>"""


def page_privacy():
    return policy_page("Privacy Policy | Woodkari, India", "What Woodkari collects when you order, why, and how to ask us to delete it.", "privacy.html",
        "Privacy policy", "This page says what we collect when you contact or order from Woodkari Exports, and what we do with it.",
        [("What we collect", ["Your name, phone number and delivery address.", "The messages you send us on WhatsApp or by email, including pictures and videos you send for a damage claim."]),
         ("How we use it", ["We use your details to make, deliver and support your order.", "This site also uses Google Analytics and the Meta pixel to count visits and to measure our ads.", "We do not sell your details to anyone."]),
         ("Delete your details", "To have your details deleted, message us on WhatsApp +91 63971 21223 or write to " + EMAIL + ".")])


def page_refund():
    return policy_page("Refund and Cancellation | Woodkari, India", "How cancellation, returns and damage claims work at Woodkari, for single pieces and bulk orders.", "refund-cancellation.html",
        "Refund and cancellation", "Short and simple. The full order terms are on the Order terms page.",
        [("Single pieces", [TERMS_SINGLE[1], TERMS_SINGLE[2], TERMS_SINGLE[3]]),
         ("Bulk orders, 25 pieces or more of one design", [TERMS_BULK[1], TERMS_BULK[2]])])


def page_shipping():
    return policy_page("Shipping and Delivery | Woodkari, India", "How delivery works at Woodkari: single pieces and bulk orders.", "shipping.html",
        "Shipping and delivery", "Every piece is made to order. We tell you the making time on WhatsApp.",
        [("Single pieces", ["For products sold with a price that includes delivery (a single box or a pack), the price shown includes delivery in India.", TERMS_SINGLE[5], TERMS_SINGLE[3]]),
         ("Bulk orders, 25 pieces or more of one design", [TERMS_BULK[0], TERMS_BULK[3], TERMS_BULK[2]])])


def page_contact():
    return policy_page("Contact Us | Woodkari, India", "How to reach Woodkari Exports: WhatsApp and email.", "contact.html",
        "Contact us", "Woodkari Exports, Sambhal, Uttar Pradesh, India.",
        [("WhatsApp", "+91 63971 21223"), ("Email", EMAIL)])


def page_about():
    return policy_page("About Woodkari | India", "Woodkari Exports makes wooden and resin trays and boxes in India.", "about.html",
        "About Woodkari", "Woodkari Exports is a maker of wooden and resin trays and boxes in India.",
        [("What we make", "We make wooden trays and boxes. We cut the wood on a CNC router, engrave by laser and finish the wooden pieces by hand. Our resin trays are made with other makers near our workshop."),
         ("Who we make for", "Most of our work is bulk orders for hotels, gifting companies and shops. Single pieces are welcome too. Orders start on WhatsApp or by email.")])


def page_bulk():
    msg = "Hello Woodkari, I want a bulk price.\nCompany:\nPiece and quantity:\nCity: "
    return head("Wholesale & Bulk Trays and Boxes, from 25 | Woodkari, India",
                "Trays and boxes in bulk from 25 pieces of one design, made in India for hotels, gifting companies, shops and importers. Name or logo by laser from 50.",
                "bulk.html", "room-front.jpg") + f"""<body>
{header('bulk')}
<main id="main">
<section><div class="wrap bh">
<div>
<h1>Bulk orders, from 25 pieces.</h1>
<p>Bulk is most of our work. We have done this work since 2008. For hotels, gifting companies, shops and importers: tell us the piece and the number, and we send the price on WhatsApp.</p>
<div class="row"><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Ask on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}?subject=Bulk%20order">{MAIL}Email us</a></div>
</div>
<div class="fig wipe"><img src="{UP}img/bulk-hero.webp" alt="Acacia room tray with two cups of tea on a wooden table" width="1200" height="744"><span class="tag">Styled picture</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>What we make in bulk</h2></div></div>
<div class="grid four">
<a class="p rv" href="navy-ivory-floral-tray.html"><div class="ph"><img src="{UP}img/navy-front-600.webp" alt="Navy and ivory floral resin tray" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div><h3>Resin trays</h3><p class="sh">Made to order in India</p></a>
<a class="p rv" href="{e(wa("Hello Woodkari, I am asking about engraved serving boards.\nCompany:\nQuantity: "))}"><div class="ph"><img src="{UP}img/d-engraved-600.webp" alt="Wooden serving board with a logo engraved, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div><h3>Engraved serving boards</h3><p class="sh">Your logo by laser, from 50</p></a>
</div>
</div></section>

<section class="band stone"><div class="wrap split" style="align-items:start">
<div class="rv">
<h2>Terms</h2>
<ul class="facts" style="margin-top:26px">
<li><b>Minimum</b><span>Trays and boxes: 25 pieces of one design. Small pieces such as coasters and tissue boxes: larger lots, ask us</span></li>
<li><b>Size</b><span>Acacia pieces in any size</span></li>
<li><b>Name or logo</b><span>By laser, from 50 pieces of one design</span></li>
<li><b>Making time</b><span>Wooden pieces: about 10 to 15 days for 100. Resin pieces: we tell you</span></li>
<li><b>Payment</b><span>50% advance to start the order</span></li>
<li><b>Delivery</b><span>At the buyer's cost, quoted before dispatch</span></li>
</ul>
</div>
<div class="rv">
<h2>How it starts</h2>
<ol class="steps">
<li><b>Send the piece and the number</b><span>On WhatsApp or by mail, with your city.</span></li>
<li><b>We send the price</b><span>A 50% advance starts the order.</span></li>
<li><b>Made and sent</b><span>Wooden pieces: about 10 to 15 days for 100.</span></li>
</ol>
<div class="row"><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Discuss your order</a></div>
</div>
</div></section>

<section class="sec" id="questions"><div class="wrap split" style="align-items:start">
<div class="rv"><h2>Questions buyers ask</h2><p class="lead">Not here? Ask us on WhatsApp.</p></div>
{faq_html()}
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_ONLY_LD}</script>
</body></html>
"""


def llms_txt():
    """/llms.txt (seo_plan_16nov.md row 24): plain facts that the site already prints, and links to the main pages. Linked from nowhere."""
    def price(p):
        return bulk_line(p["slug"]) if p.get("bulk_only") else rupee(p["price"]) + (f" / {p['unit']}" if p.get("unit") else "")
    terms = [("Minimum", "Trays and boxes: 25 pieces of one design. Small pieces such as coasters and tissue boxes: larger lots, ask us"),
             ("Size", "Acacia pieces in any size"), ("Name or logo", "By laser, from 50 pieces of one design"),
             ("Making time", "Wooden pieces: about 10 to 15 days for 100. Resin pieces: we tell you"),
             ("Payment", "50% advance to start the order"), ("Delivery", "At the buyer's cost, quoted before dispatch")]
    L = ["# Woodkari Exports", "",
         "> Woodkari Exports, Sambhal, Uttar Pradesh. Wooden and resin trays and boxes, making since 2008. Bulk orders from 25 pieces; single pieces on WhatsApp.", "",
         "Woodkari is a workshop in India, at work since 2008. Four karigars cut the wood on a CNC router, engrave by laser and finish our wooden pieces by hand. Our resin trays are made with other makers near our workshop.", "",
         "Bulk is most of our work. Hotels, gifting companies, shops and importers can order our trays and boxes from 25 pieces of a design, and the acacia pieces in any size.", "",
         'Pictures marked "Made to order" or "Styled picture" are made to show the look of a piece; wood grain and resin differ a little on every piece. Only pictures marked "plain photo" are photos of our own pieces.', "",
         "## Contact", "",
         f"- WhatsApp: {WA_PRINTED} ({wa(HELLO).split('?')[0]})", f"- Email: {EMAIL}",
         "- How an order starts: send the piece and the number, on WhatsApp or by mail, with your city.", "",
         "## Main pages", "",
         f"- [Home and shop]({SITE}/): trays and boxes, acacia wood from our workshop, and resin trays made to order. Prices are for one piece; delivery is extra.",
         f"- [Bulk and hotel orders]({SITE}/bulk.html): bulk orders from 25 pieces, for hotels, gifting companies, shops and importers.",
         f"- [Made to order designs]({SITE}/designs.html): {ALL_N} more designs. Every picture there is a design picture, made to show the piece. Every design shows its price; order on WhatsApp.", "",
         "## Pieces", ""]
    L += [f"- [{p['name']}]({SITE}/{p['slug']}.html): {p['short']}; {price(p)}" for p in PRODUCTS]
    L += ["", "## Made to order designs, by kind", "",
          f"- [{OW_TITLE}]({SITE}/designs.html#g-{OW_GID}): {OW_LINE}",
          f"- [{MG_TITLE}]({SITE}/designs.html#g-mango): {MG_LINE}",
          f"- [{BX_TITLE}]({SITE}/designs.html#g-{BX_GID}): {BX_LINE}"]
    L += [f"- [{title}]({SITE}/designs.html#g-{gid}): {line}" for gid, pre, title, line, items in MTO]
    L += ["", "## Bulk terms (from the bulk page)", ""] + [f"- {a}: {b}" for a, b in terms]
    return "\n".join(L) + "\n"


def check_photos(pages):
    """Machine lock (mistakes 65, 70): every picture a page references must have a row in build/photo_pass.csv
    (a full-size Checker pass). Key = file name in img/ without "-600" and without the extension, e.g. m-px-02-a."""
    import csv, re
    with open(os.path.join(ROOT, "build", "photo_pass.csv"), newline="", encoding="utf-8") as f:
        passed = {r["image_file"].strip() for r in csv.DictReader(f) if r["passed_by"].strip()}
    used = set()
    for text in pages.values():
        used.update(m.group(1) for m in re.finditer(r"img/([A-Za-z0-9_.-]+?)(?:-600)?\.(?:webp|jpg|jpeg|png)", text))
    missing = sorted(used - passed)
    if missing:
        sys.exit("PHOTO NOT PASSED: " + ", ".join(missing) + "\nAdd a Checker row to build/photo_pass.csv first (full-size check, see mistakes 65 and 70).")


def main():
    global CARDS, CARD_BY
    CARDS = all_cards()
    CARD_BY = {k: (n, sp, h) for k, n, sp, h in CARDS}
    os.makedirs(OUT, exist_ok=True)
    pages = {}
    w = lambda name, s: pages.__setitem__(name, s)  # buffered: nothing is written until the photo check below passes
    css = CSS.strip() + "\n"
    if PREVIEW:
        css = css.replace("url(fonts/", "url(../fonts/")
    import hashlib
    ASSET_V["css"] = hashlib.md5(css.encode("utf-8")).hexdigest()[:8]
    ASSET_V["js"] = hashlib.md5((JS.strip() + "\n").encode("utf-8")).hexdigest()[:8]
    w("site.css", css)
    w("site.js", JS.strip() + "\n")
    w("index.html", page_home())
    w("bulk.html", page_bulk())
    w("terms.html", page_terms())
    for _n, _f in (("privacy.html", page_privacy), ("refund-cancellation.html", page_refund), ("shipping.html", page_shipping), ("contact.html", page_contact), ("about.html", page_about)):
        w(_n, _f())
    w("designs.html", page_designs())
    for name, text in category_pages().items():
        w(name, text)
    for gid, pre, title, line, items in MTO:
        for i in range(MTO_START.get(gid, 1), MTO_START.get(gid, 1) + len(items)):
            if f"{pre}-{i}" in MTO_HOLD: continue
            w(mto_page(f"{pre}-{i}"), page_design(gid, pre, title, line, items, i))
    for it in OW:
        w(mto_page(it["code"]), page_ow(it))
    for it in NB:
        w(mto_page(it["code"]), page_bx(it))
    for it in LST:
        w(mto_page(it["code"]), page_lst(it))
    for p in PRODUCTS:
        w(p["slug"] + ".html", page_product(p))
    if not PREVIEW:
        urls = [""] + [p["slug"] + ".html" for p in PRODUCTS] + ["designs.html"] + list(category_pages()) + [mto_page(it["code"]) for it in OW] + [mto_page(it["code"]) for it in NB] + [mto_page(it["code"]) for it in LST] + [mto_page(c) for _, c, _, _ in mto_items()] + ["bulk.html", "terms.html", "privacy.html", "refund-cancellation.html", "shipping.html", "contact.html", "about.html"]
        w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
        w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
        w("llms.txt", llms_txt())
    for src, dst in (("shop.html", "designs.html"), ("name-and-logo.html", "index.html"), ("fluted-box-tray.html", "trays.html"), ("room-tray.html", "trays.html")):
        w(src, f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Woodkari</title><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={dst}"><link rel="canonical" href="{SITE}/{dst}"><script>location.replace("{dst}")</script></head><body><p><a href="{dst}">Continue to Woodkari</a></p></body></html>\n')
    check_photos(pages)
    lst_images()
    for name, s in pages.items():
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)
    print("built", OUT, len(PRODUCTS) + 3 + ALL_N, "pages")


main()
