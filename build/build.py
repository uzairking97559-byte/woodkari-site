#!/usr/bin/env python3
"""Builds the Woodkari shop (static HTML) into an output folder.

  python3 build/build.py v2        -> preview at /v2/ (noindex)
  python3 build/build.py .         -> live site at the root

Edit PRODUCTS, WHATSAPP and prices here, then rebuild. No other tooling.
Every fact below must be OWNER-said or READ from a source (agency-research ops/fact_check_14nov.md).
"""
import html, json, os, sys, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "v2"
PREVIEW = OUT != "."
SITE = "https://woodkariexports.com"
BASE = SITE + ("" if OUT == "." else "/" + OUT)
UP = "" if OUT == "." else "../"  # assets live at the root; a preview folder points one level up

WHATSAPP = "919119793282"
EMAIL = "sales@woodkariexports.com"
INSTAGRAM = "https://www.instagram.com/woodkariexports/"  # given by the owner, 18 Nov; no tracking query

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
               ("navy-top", "Navy and ivory floral tray seen from above on a white sheet", "Made to order"),
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
               ("chevron-top", "Red chevron tray seen from above on a white sheet", "Made to order"),
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
               ("gold-top", "Gold-flake resin tray seen from above on a white sheet", "Made to order"),
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

CATS = [("all", "Everything"), ("wood", "Acacia wood"), ("resin", "Resin trays"), ("u1500", "Under ₹1,500")]

TILES = [("t-table", "On the table", "Black & White Tray Set", "black-white-floral-tray-set.html", "Black and white floral tray set with tea and snacks", "Made to order"),
         ("navy-use-600", "Tea for two", "Navy & Ivory Floral Tray", "navy-ivory-floral-tray.html", "Navy and ivory floral tray carrying two cups of tea and biscuits", "Made to order"),
         ("fluted-life", "For gifting", "Box trays, bulk from 25", "bulk.html", "Fluted acacia box tray with keys, coins and sunglasses on a hall table", "Styled picture"),
         ("t-room", "In the guest room", "Room Tray", "room-tray.html", "Room tray on a bedside table with a kettle", "Styled picture")]

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
        ("bone-inlay-chest-5", "Chest of drawers, grey and white geometric inlay design")]),
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
    "OW-43": "Round coffee table with a flower pattern on top and a patterned band on the side. Bone inlay, black and white. 42 in across, 18 in high. Made to order in India."}
MTO_HOLD = {"OW-42", "OW-39"}  # designs kept off the site (OW-42 picture being redone; OW-39 merged into OW-38 as its 30 in size, 18 Nov)
# one listing with several sizes: code -> [(size label, price)]; the card shows "From <lowest>"
MTO_SIZES = {"OW-38": [("36 × 16 in", 90900), ("30 × 16 in", 70900)]}
MTO_N = sum(len(g[4]) for g in MTO) - len(MTO_HOLD)
# Made-to-order designs that have an owner-set price (D-241/D-242, 18 Nov 2026: IC-2 Rs 74,900 incl. packing, delivery extra)
MTO_PRICE = {
    'IC-1': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
    'IC-2': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
    'IC-3': (46900, 'Price includes packing. Delivery extra.', 'About 3-drawer bedside 18 L × 14 W × 26 H in'),
    'IC-4': (46900, 'Price includes packing. Delivery extra.', 'About 3-drawer bedside 18 L × 14 W × 26 H in'),
    'IC-5': (74900, 'Price includes packing. Delivery extra.', '4-drawer chest 30 L × 16 W × 30 H in'),
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
    dict(code="OW-36", wood="mango", size="8 × 8 × 3 in (20 × 20 × 7.6 cm)", name="9-compartment wooden box with glass lid", price=899, bulk=450,
         what="Square box with nine compartments under a glass lid, for spices, dry fruit or small items.",
         views=["on a white background", "top view", "close-up of the corner and the glass lid", "side view",
                "in use, holding nine different spices", "three boxes stacked"]),
    dict(code="OW-37", wood="mango", size="4.75 × 4.75 × 1.25 in (12 × 12 × 3.2 cm)", name="4-compartment open wooden tray", price=299, bulk=150,
         what="Small open tray with four compartments, for tea bags, sugar or snacks.",
         views=["on a white background", "top view", "close-up of a compartment and the corner", "side view",
                "in use, holding tea bags, sugar cubes, cardamom and biscuits", "three trays stacked"]),
]
ALL_N = MTO_N + len(OW)  # every card on designs.html


def ow_wood(it):
    return it.get("wood", "acacia")


def ow_key(code, x="a"):
    return f"m-{code.lower()}-{x}"


def ow_price_lines(it):
    """the two price lines of a single-piece item, or the one line of a bulk-only item"""
    if it["price"] and it.get("unit") == "set":
        return f"{rupee(it['price'])} for the set of 3", f"{OW_BULK_FROM} sets or more: {rupee(it['bulk'])} a set"
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
IG_ICON = '<svg class="i" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9" fill="currentColor" stroke="none"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18"/></svg>'
SEARCH_ICON = '<svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m16.5 16.5 4.5 4.5"/></svg>'
X_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><path d="M5 5l14 14M19 5 5 19"/></svg>'
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
@media(min-width:900px){
 .hd-top,.hd::before{height:76px}
 .logo b{font-size:36px}
 .hd-note{display:block}
 .hd-l .menu{display:none}
 .hd-wa{display:inline-flex;align-items:center;gap:8px;min-height:42px;padding:8px 18px;border-radius:999px;background:var(--green);color:#fff;font:600 14.5px/1 var(--sans);text-decoration:none;margin-left:8px;transition:background-color .2s}
 .hd-r .ib{margin-right:0}
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
@media(min-width:760px){.p h3{font-size:18px;margin-top:16px}.p .sh{font-size:15px}.p .pr{font-size:18px}}

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
/* [13] shop-style header and menu (owner 18 Nov) */
.sbox{display:flex;align-items:center;gap:9px;height:42px;padding:0 13px;border:1px solid var(--line);border-radius:var(--r);background:#fff;color:var(--soft);font:400 15px/1 var(--sans);cursor:text;text-align:left;min-width:0}
.sbox svg{flex:none;width:19px;height:19px}.sbox span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hd-r .sbox,.hd-r .ig{display:none}
.hd-s{display:flex;gap:8px;padding-top:9px;padding-bottom:9px}
.hd-s .sbox{flex:1}
.wa-s{flex:none;display:inline-flex;align-items:center;gap:7px;height:42px;padding:0 12px;border-radius:var(--r);background:var(--green);color:#fff;text-decoration:none;font:600 14px/1 var(--sans);white-space:nowrap}
.wa-s b{font-weight:600}
.tabs .hd-s a.wa-s{padding:0 12px;color:#fff}.tabs .hd-s a::after{display:none}
.hd-wa b{font-weight:600}
@media(min-width:900px){
 .hd-s{display:none}
 .hd-r .sm{display:none}
 .hd-r .sbox{display:flex;width:210px;flex:none}
 .hd-r .ig{display:inline-grid}
 .hd-r{gap:8px}
 .hd-wa{margin-left:2px}
 .tabs nav{gap:2px}.tabs a{padding:14px 9px;font-size:15px}.tabs a::after{left:9px;right:9px}
}
.tabs a .dn{margin-left:5px;vertical-align:-1px;transition:transform .25s var(--ease)}
.tabs a[aria-expanded=true] .dn{transform:rotate(180deg)}
.tabs a[aria-expanded=true]{color:var(--green)}
.tn{position:relative}
.sub{position:absolute;top:100%;left:0;right:0;z-index:30;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 18px 30px -22px rgba(20,54,41,.5)}
.sub[hidden],.sub-set[hidden]{display:none}
.tabs .sub a{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:14px 18px;font-size:16px;font-weight:500;white-space:nowrap;color:var(--ink)}
.tabs .sub a::after{display:none}
.sub a span{color:var(--soft);font-weight:400;font-size:14px}
@media(min-width:900px){.sub{right:auto;min-width:240px;border:1px solid var(--line);border-top:0}.tabs .sub a{padding:12px 18px}}
@media(hover:hover) and (pointer:fine){.tabs .sub a:hover{background:var(--mist);color:var(--green)}.sbox:hover{border-color:var(--green)}.wa-s:hover{background:var(--green-d)}}
.chips a[aria-current]{border-color:var(--green);color:var(--green);font-weight:600}
.dr-ft p a{color:var(--soft)}
.bulk-all{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 32px}
.bulk-all p{margin:0;font:400 clamp(26px,3.6vw,44px)/1.15 var(--serif);max-width:22em}
.eng-f{max-width:720px}
.ideas{list-style:none;margin:0;padding:0;display:grid;gap:0}
.ideas li{display:grid;gap:6px;padding:22px 0;border-top:1px solid var(--line)}
.ideas .n{font:400 32px/1 var(--serif);color:var(--brass)}
.ideas b{font:500 20px/1.3 var(--sans)}.ideas li>span:last-child{color:var(--soft)}
@media(min-width:900px){.ideas{grid-template-columns:repeat(3,1fr);gap:0 48px}}
.tile .cap small{opacity:.95}
.hero .slide .tag{max-width:80%}
"""


JS = r"""
(function(){
  var d=document,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s,r){return (r||d).querySelector(s)}
  function $$(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))}

  /* header: shadow + tabs tuck away on the way down */
  var hd=$('.hd'),ly=scrollY,run=0;
  if(hd)addEventListener('scroll',function(){var y=scrollY,dy=y-ly;ly=y;
    run=(dy>0)===(run>0)?run+dy:dy; /* distance covered in the current direction */
    if(y<=220||run<-24)hd.classList.remove('min');else if(run>48)hd.classList.add('min');
    hd.classList.toggle('sc',y>8)},{passive:true});

  d.addEventListener('touchstart',function(){},{passive:true}); /* lets :active work on iOS */

  /* menu and search */
  function dlg(btn,id,onopen){var bs=$$(btn),g=d.getElementById(id);if(!bs.length||!g||!g.showModal)return;
    bs.forEach(function(b){b.addEventListener('click',function(){g.showModal();bs.forEach(function(x){x.setAttribute('aria-expanded','true')});if(onopen)onopen(g)})});
    g.addEventListener('close',function(){bs.forEach(function(x){x.setAttribute('aria-expanded','false')})});
    g.addEventListener('click',function(ev){if(ev.target===g||ev.target.closest('[data-close]')||ev.target.closest('a'))g.close()});}
  dlg('.menu','drawer');
  var sx=d.getElementById('sx'),items=sx?JSON.parse(sx.textContent):[],list=$('.sr-list'),inp=$('.sr-bar input'),none=$('.sr-none');
  function render(q){if(!list)return;q=(q||'').trim().toLowerCase();list.textContent='';var n=0;
    items.forEach(function(it){if(q&&(it.n+' '+it.s).toLowerCase().indexOf(q)<0)return;n++;
      var li=d.createElement('li'),a=d.createElement('a'),im=d.createElement('img'),sp=d.createElement('span'),b=d.createElement('b'),sm=d.createElement('small');
      a.href=it.u;im.src=it.i;im.alt='';im.width=56;im.height=56;im.loading='lazy';b.textContent=it.n;sm.textContent=it.s;
      sp.appendChild(b);sp.appendChild(sm);a.appendChild(im);a.appendChild(sp);li.appendChild(a);list.appendChild(li)});
    if(none)none.hidden=n>0;}
  dlg('.search','srch',function(){render('');if(inp){inp.value='';inp.focus()}});
  if(inp){inp.addEventListener('input',function(){render(inp.value)});inp.addEventListener('keydown',function(ev){if(ev.key==='Escape'){ev.preventDefault();d.getElementById('srch').close()}})}

  /* page transition: only the tapped card's picture travels to the product page (and back) */
  $$('.p').forEach(function(a){a.addEventListener('click',function(){
    $$('[style*="view-transition-name"]').forEach(function(x){x.style.viewTransitionName=''});
    var im=$('.ph img',a);if(im)im.style.viewTransitionName='pic'})});

  /* category menu: one shared dropdown panel under the tab row (tap to open on phones, hover or click on desktop) */
  var tn=$('.tn'),sub=tn&&$('.sub',tn),gs=tn?$$('a.g',tn):[],openG=null,hov=matchMedia('(hover:hover) and (pointer:fine)');
  function closeSub(){if(!sub)return;sub.hidden=true;gs.forEach(function(a){a.setAttribute('aria-expanded','false')});openG=null}
  function openSub(a){if(!sub)return;$$('.sub-set',sub).forEach(function(x){x.hidden=x.dataset.for!==a.dataset.g});
    gs.forEach(function(x){x.setAttribute('aria-expanded',String(x===a))});sub.hidden=false;openG=a;
    var nr=$('nav',tn),l=a.getBoundingClientRect().left-tn.getBoundingClientRect().left,w=sub.offsetWidth,max=tn.clientWidth-w-8;
    if(innerWidth>=900)sub.style.left=Math.max(8,Math.min(l,max))+'px';else sub.style.left='0'}
  gs.forEach(function(a){
    a.addEventListener('click',function(ev){ev.preventDefault();if(openG===a)closeSub();else openSub(a)});
    a.addEventListener('mouseenter',function(){if(hov.matches&&innerWidth>=900)openSub(a)})});
  if(tn){tn.addEventListener('mouseleave',function(){if(hov.matches&&innerWidth>=900)closeSub()});
    d.addEventListener('click',function(ev){if(openG&&!ev.target.closest('.tn'))closeSub()});
    d.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&openG){var g=openG;closeSub();g.focus()}});
    addEventListener('scroll',function(){if(openG&&!hov.matches)closeSub()},{passive:true});}

  /* old links (index.html?f=wood) go to the new All pieces page */
  var old=new URLSearchParams(location.search).get('f');
  if(old&&d.getElementById('newarr'))location.replace('shop.html'+(old==='wood'?'?c=acacia':old==='resin'?'?c=resin-trays':''));

  /* All pieces: filter by kind with the chips (every card has data-cats) */
  var grid=d.getElementById('all-grid');
  if(grid){var pc=$$('.p',grid),chips=$$('#shop-chips a'),hh=d.getElementById('shop-h'),cn=d.getElementById('shop-n'),none=d.getElementById('shop-none'),
      nm={all:'All pieces'};chips.forEach(function(a){nm[a.dataset.c]=a.firstChild.textContent});
    $$('.tn a.g').forEach(function(a){nm[a.dataset.g]=a.textContent});
    function apply(k,push){if(!nm[k])k='all';var n=0;
      pc.forEach(function(p){var on=k==='all'||(' '+p.dataset.cats+' ').indexOf(' '+k+' ')>=0;p.hidden=!on;if(on)n++});
      chips.forEach(function(a){if(a.dataset.c===k||a.dataset.p===k)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
      $$('.tn nav a[data-has],.tn nav a[data-c]').forEach(function(a){var h=(a.dataset.has||a.dataset.c||'').split(' ');if(k!=='all'&&h.indexOf(k)>=0)a.setAttribute('aria-current','true');else if(a.dataset.c==='all'&&k==='all')a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
      if(hh)hh.textContent=nm[k];if(cn)cn.textContent=n;if(none)none.hidden=n>0;
      if(push){try{history.replaceState(null,'',location.pathname+(k==='all'?'':'?c='+k))}catch(_){}}}
    chips.forEach(function(a){a.addEventListener('click',function(ev){ev.preventDefault();apply(a.dataset.c,true);closeSub()})});
    apply(new URLSearchParams(location.search).get('c')||'all',false);}

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

WA_PRINTED = "+91 91197 93282"  # as printed in the footer
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
       ("Can you change the size?", "The acacia pieces (the Room Tray and the Fluted Box Tray) can be made in any size, on order."),
       ("How long does an order take?", "Wooden pieces: about 10 to 15 days for 100. Resin pieces: we tell you the time when you ask."),
       ("How does payment work?", "A single piece up to ₹10,000 is paid in full when you order, by UPI or bank transfer. For a piece above ₹10,000, such as furniture, and for a bulk order, a 50% advance starts the order and the rest is paid before dispatch."),
       ("Can I cancel or return a piece?", "You can cancel for free until we start making. Every piece is made for you, so there are no returns for a change of mind. If a piece arrives damaged, tell us on WhatsApp within 48 hours with an uncut unboxing video, and we replace it. The full terms are on the Order terms page."),
       ("Who pays for delivery?", "Delivery is at the buyer's cost. We tell you the amount before the order leaves."),
       ("Can I buy just one piece?", "Yes. Every piece with a price can be ordered on its own. Tap \"Order on WhatsApp\" on the piece and tell us your city and PIN code; we confirm the delivery charge, the time and how to pay.")]


# ---- Shop-style catalogue (owner 18 Nov): ONE list of every piece, used by All pieces, best sellers, new arrivals, category tiles.
# group key, label, [(leaf key, label)]. A group with no leaves is itself the category. Empty categories are left out of the menu.
SHOP_GROUPS = [("inlay", "Inlay furniture", [("inlay-chests", "Chests"), ("inlay-tables", "Tables")]),
               ("resin", "Resin", [("resin-trays", "Trays"), ("resin-bath", "Bathroom sets"), ("resin-bowls", "Bowls & plates")]),
               ("painted", "Painted trays & bowls", []), ("boards", "Wooden boards", []), ("acacia", "Acacia wood", []),
               ("mango", "Mango wood", []), ("candles", "Candle stands", [])]
MTO_CAT = {"painted": "painted", "bath": "resin-bath", "bowls": "resin-bowls", "boards": "boards", "candles": "candles", "chests": "inlay-chests", "tables": "inlay-tables"}
OW_EXTRA = {"OW-08": "boards", "OW-25": "candles"}  # acacia pieces that are also a board / candle stands
BEST = ["OW-38", "OW-40", "IC-1", "black-white-floral-tray-set"]  # best sellers row (owner's list, 18 Nov)
NEW_ARRIVALS = ["OW-37", "OW-36", "OW-33", "OW-25", "OW-18", "OW-08", "OW-03", "OW-01"]  # the pieces added last (git history, 18 Nov)
GROUP_PIC = {"inlay": "m-bone-inlay-coffee-table-40", "resin": "bw-top", "painted": "m-wooden-meena-tray-3", "boards": "m-wooden-chopping-board-2",
             "acacia": "m-ow-18-a", "mango": "m-ow-36-a", "candles": "m-wooden-candle-stand-3"}


def leaf_group(leaf):
    return next((g for g, _, ls in SHOP_GROUPS if g == leaf or any(l == leaf for l, _ in ls)), leaf)


def shop_items():
    """every card on the site: [dict(id, name, href, img, alt, price, sub, tag, cats, sort)]. Order: category order, then dearest first."""
    out = []
    for p in PRODUCTS:
        a = p["card"][0]
        alt, cap = next((x[1], x[2]) for x in p["imgs"] if x[0] == a)
        out.append(dict(id=p["slug"], name=p["name"], href=p["slug"] + ".html", img=f"{a}-600", alt=alt, sub=p["short"],
                        price=(bulk_line(p["slug"]) if p.get("bulk_only") else rupee(p["price"]) + (f" / {p['unit']}" if p.get("unit") else "")),
                        tag=cap, cats=["resin-trays"] if p["cat"] == "resin" else ["acacia"], sort=BULK_ONLY_PRICE["gold-flake-resin-tray"] if p.get("bulk_only") else p["price"]))
    for it in OW:
        top = ow_price_lines(it)[0]
        out.append(dict(id=it["code"], name=it["name"], href=mto_page(it["code"]), img=ow_key(it["code"]) + "-600", alt=it["name"] + ", design picture",
                        sub=f"Design {it['code']} · {ow_wood(it)} wood", price=top, tag="Made to order",
                        cats=[ow_wood(it)] + ([OW_EXTRA[it["code"]]] if it["code"] in OW_EXTRA else []),
                        sort=it["price"] or BULK_ONLY_PRICE.get(it["code"], 0)))
    for gid, code, f, n in mto_items():
        out.append(dict(id=code, name=n, href=mto_page(code), img=f"m-{f}-600", alt=n + ", design picture", sub=f"Design {code} · made on order",
                        price=mto_pr(code)[0], tag="Made to order", cats=[MTO_CAT[gid]], sort=(MTO_PRICE[code][0] if code in MTO_PRICE else 0)))
    order = [l for g, _, ls in SHOP_GROUPS for l in ([l for l, _ in ls] or [g])]
    out.sort(key=lambda x: (order.index(x["cats"][0]), -x["sort"], x["id"]))
    for x in out:
        x["cats"] = x["cats"] + sorted({leaf_group(c) for c in x["cats"]} - set(x["cats"]))
    return out


def shop_card(x, rv=True):
    return (f'<a class="p{" rv" if rv else ""}" data-cats="{" ".join(x["cats"])}" href="{x["href"]}"><div class="ph"><img src="{UP}img/{x["img"]}.webp" alt="{e(x["alt"])}" width="600" height="600" loading="lazy">'
            f'<span class="tag">{e(x["tag"])}</span></div><h3>{e(x["name"])}</h3><p class="sh">{e(x["sub"])}</p><p class="pr">{e(x["price"])}</p></a>')


def shop_menu():
    """(menu items, counts): only categories that have pieces"""
    items = shop_items()
    n = lambda k: sum(1 for x in items if k in x["cats"])
    groups = []
    for g, label, ls in SHOP_GROUPS:
        ls = [(l, t) for l, t in ls if n(l)]
        if n(g):
            groups.append((g, label, ls))
    return items, n, groups


def page_shop():
    items, n, groups = shop_menu()
    chips = f'<a href="shop.html" data-c="all" aria-current="true">All</a>' + "".join(
        f'<a href="shop.html?c={l}" data-c="{l}" data-p="{g}">{e(t)}</a>' for g, label, ls in groups for l, t in (ls or [(g, label)]))
    return head("All Pieces: Furniture, Trays, Bowls, Boards, Candle Stands | Woodkari",
                f"All {len(items)} pieces from Woodkari, India: bone inlay furniture, resin and painted trays, bowls, boards, acacia and mango wood, candle stands. Made to order.",
                "shop.html", "m-og.jpg") + f"""<body>
{header('all')}
<main id="main">
<section><div class="wrap mh">
<h1 id="shop-h">All pieces</h1>
<p><span id="shop-n">{len(items)}</span> pieces. Every piece can be made in bulk from 25. Pictures are design pictures, made to show the piece, unless marked plain photo. Open one and order on WhatsApp.</p>
<nav class="chips" id="shop-chips" aria-label="Kinds of pieces">{chips}</nav>
</div></section>
<section class="sec"><div class="wrap">
<div class="grid four" id="all-grid">{"".join(shop_card(x, False) for x in items)}</div>
<p class="sr-none" id="shop-none" hidden>Nothing in this kind yet. <a href="{e(wa(HELLO))}">Ask us on WhatsApp</a>.</p>
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


def page_engraving():
    """Name & logo page (owner 18 Nov). Only lines that are already on the site: wooden pieces, by laser, 50 or more of one design; 50% advance."""
    msg = "Hello Woodkari, I want my name or logo engraved.\nPiece:\nQuantity:\nCity: "
    ideas = [("Wedding return gifts", "Boxes and boards with the couple's names, for the guests."),
             ("Company gifts", "A company logo on boards and boxes for staff, clients and New Year hampers."),
             ("Hotel room sets", "A hotel name on every room tray, for the guest rooms.")]
    idea = "".join(f'<li class="rv"><span class="n">{i}</span><b>{e(t)}</b><span>{e(d)}</span></li>' for i, (t, d) in enumerate(ideas, 1))
    return head("Name & Logo Engraving on Wooden Trays, Boxes, Boards | Woodkari",
                "Your name or logo laser-engraved on wooden trays, boxes and boards, on 50 pieces or more of one design. For weddings, company gifts and hotels. Order on WhatsApp.",
                "name-and-logo.html", "d-engraved-600.webp") + f"""<body>
{header('eng')}
<main id="main">
<section><div class="wrap bh">
<div>
<h1>Your name or logo, by laser.</h1>
<p>We engrave a name or a logo on our wooden pieces. It is made for orders of 50 pieces or more of one design.</p>
<div class="row"><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Ask about engraving</a><a class="btn line" href="shop.html">See all pieces{ARROW}</a></div>
</div>
<div class="fig wipe"><img src="{UP}img/d-engraved-600.webp" alt="Wooden serving board with a sample logo engraved, design picture" width="600" height="600"><span class="tag">Made to order</span></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>What we engrave</h2><p>A name or a logo, by laser, on 50 pieces or more of one design. Wooden pieces: trays, boxes and boards.</p></div></div>
<ul class="facts eng-f rv">
<li><b>What</b><span>A name or a logo</span></li>
<li><b>How</b><span>By laser</span></li>
<li><b>How many</b><span>50 pieces or more of one design</span></li>
<li><b>On which pieces</b><span>The wooden pieces on this site</span></li>
</ul>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Ideas</h2></div></div>
<ol class="ideas">{idea}</ol>
</div></section>

<section class="band stone"><div class="wrap split" style="align-items:start">
<div class="rv"><h2>How to order</h2><p class="lead">Everything starts on WhatsApp.</p></div>
<div class="rv">
<ol class="steps">
<li><b>Message us on WhatsApp</b><span>Tell us the piece, how many, your city, and the name or logo you want on it.</span></li>
<li><b>We send the price</b><span>A 50% advance starts the order.</span></li>
<li><b>Made and sent</b><span>Wooden pieces: about 10 to 15 days for 100. Delivery is at your cost, quoted before it leaves.</span></li>
</ol>
<div class="row"><a class="btn pri" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
</div>
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_ONLY_LD}</script>
</body></html>
"""



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
<link rel="canonical" href="{SITE}/{path}">
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
<link rel="stylesheet" href="site.css">
<script>document.documentElement.className+=" js";addEventListener("pagereveal",function(e){{var n=window.navigation&&navigation.activation;if(!e.viewTransition||!n||!n.from||document.querySelector('[style*="view-transition-name"]'))return;var im=document.querySelector('.p[href="'+n.from.url.split("/").pop().split(/[?#]/)[0]+'"] .ph img');if(im){{im.style.viewTransitionName="pic";im.closest(".p").classList.add("in","now")}}}})</script>
<script src="site.js" defer></script>
</head>
"""


def search_data():
    items = []
    for p in PRODUCTS:
        sub = p["short"] + (" · " + bulk_line(p["slug"]) if p.get("bulk_only") else " · " + rupee(p["price"])) + " · " + ("Made to order" if p.get("mto") else "Plain photo of our piece")
        items.append({"n": p["name"], "s": sub, "u": p["slug"] + ".html", "i": f"{UP}img/{p['card'][0]}-600.webp"})
    for k, n in DESIGNS:
        items.append({"n": n, "s": "Made to order · in bulk", "u": wa("Hello Woodkari, I am asking about: " + n + "\nQuantity: "), "i": f"{UP}img/{k}.webp"})
    for it in OW:
        sub = rupee(it["price"]) if it["price"] else ow_price_lines(it)[0]
        items.append({"n": it["name"], "s": f"Design {it['code']} · {ow_wood(it)} wood, made to order · {sub}", "u": mto_page(it["code"]), "i": f"{UP}img/{ow_key(it['code'])}-600.webp"})
    for gid, code, f, n in mto_items():
        items.append({"n": n, "s": f"Design {code} · made to order, " + (mto_pr(code)[0] if code in MTO_PRICE else "price on WhatsApp"), "u": mto_page(code), "i": f"{UP}img/m-{f}-600.webp"})
    items.append({"n": "Bulk and hotel orders", "s": "Trays and boxes from 25 of one design · Styled picture", "u": "bulk.html", "i": f"{UP}img/room-front-600.webp"})
    return json.dumps(items).replace("</", "<\\/")


def nav_html(cur):
    """category menu: groups with a dropdown (JS fills one shared panel from .sub-set), leaves and pages as plain links"""
    _, n, groups = shop_menu()
    cc = lambda k: ' aria-current="true"' if k == cur else ""
    out = [f'<a href="shop.html" data-c="all"{cc("all")}>All pieces</a>']
    sets = []
    for g, label, ls in groups:
        if ls:
            has = " ".join([g] + [l for l, _ in ls])
            out.append(f'<a class="g" href="shop.html?c={g}" data-g="{g}" data-has="{has}" aria-haspopup="true" aria-expanded="false">{e(label)}<svg class="dn" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></a>')
            sets.append(f'<div class="sub-set" data-for="{g}" hidden><a href="shop.html?c={g}">All {e(label.lower())}</a>' + "".join(f'<a href="shop.html?c={l}">{e(t)}</a>' for l, t in ls) + "</div>")
        else:
            out.append(f'<a href="shop.html?c={g}" data-c="{g}" data-has="{g}">{e(label)}</a>')
    out.append(f'<a href="bulk.html"{cc("bulk")}>Bulk orders</a><a href="name-and-logo.html"{cc("eng")}>Name &amp; logo</a>')
    return "".join(out), "".join(sets)


def header(cur):
    pv = '<div class="pv">Preview. Not the live site yet.</div>' if PREVIEW else ""
    nav, sets = nav_html(cur)
    _, n, groups = shop_menu()
    dr = f'<a href="shop.html">All pieces{ARROW}</a>' + "".join(f'<a href="shop.html?c={g}">{e(label)}{ARROW}</a>' for g, label, ls in groups)
    box = f'<button class="sbox search" type="button" aria-label="Search" aria-expanded="false" aria-controls="srch">{SEARCH_ICON}<span>Search the pieces</span></button>'
    wab = f'<a class="hd-wa" href="{e(wa(HELLO))}">{WA_ICON}<span>WhatsApp</span> <b>{WA_PRINTED}</b></a>'
    # Instagram: link given by the owner, 18 Nov (INSTAGRAM above)
    ig = f'<a class="ib ig" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Woodkari on Instagram">{IG_ICON}</a>'
    return f"""<a class="skip" href="#main">Skip to content</a>
{pv}<header class="hd">
<div class="wrap hd-top">
<div class="hd-l"><button class="ib menu" type="button" aria-label="Menu" aria-expanded="false" aria-controls="drawer">{MENU_ICON}</button><span class="hd-note">Made in India since 2008</span></div>
<a class="logo" href="./" aria-label="Woodkari home"><b>Woodkari</b><small>EXPORTS</small></a>
<div class="hd-r"><button class="ib search sm" type="button" aria-label="Search" aria-expanded="false" aria-controls="srch">{SEARCH_ICON}</button>{box}{ig}{wab}</div>
</div>
<div class="tabs">
<div class="hd-s wrap">{box.replace('Search the pieces', 'Search')}<a class="wa-s" href="{e(wa(HELLO))}">{WA_ICON}<b>{WA_PRINTED}</b></a></div>
<div class="tn"><nav class="wrap" aria-label="Shop">{nav}</nav><div class="sub" hidden>{sets}</div></div>
</div>
</header>
<dialog class="drawer" id="drawer" aria-label="Menu"><div class="dr-in">
<div class="dr-hd"><b>Woodkari</b><button class="ib" type="button" data-close aria-label="Close menu">{X_ICON}</button></div>
<nav class="dr-nav" aria-label="Menu">
{dr}<a href="bulk.html">Bulk orders{ARROW}</a><a href="name-and-logo.html">Name and logo{ARROW}</a><a href="designs.html">Made to order designs{ARROW}</a><a href="./#workshop">The workshop{ARROW}</a><a href="./#questions">Questions{ARROW}</a>
</nav>
<div class="dr-ft"><a class="btn pri wide" href="{e(wa(HELLO))}">{WA_ICON}Chat on WhatsApp {WA_PRINTED}</a><p><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @woodkariexports</a></p><p>{EMAIL}</p></div>
</div></dialog>
<dialog class="srch" id="srch" aria-label="Search"><div class="sr-in">
<div class="sr-bar"><input type="search" placeholder="Search trays, boxes, designs" aria-label="Search the pieces" autocomplete="off" enterkeyhint="search"><button class="ib" type="button" data-close aria-label="Close search">{X_ICON}</button></div>
<ul class="sr-list"></ul>
<p class="sr-none" hidden>Nothing by that name. <a href="{e(wa(HELLO))}">Ask us on WhatsApp</a>.</p>
</div></dialog>
<script type="application/json" id="sx">{search_data()}</script>
"""


def footer():
    return f"""<footer class="ft"><div class="wrap">
<div><a class="fl" href="./" aria-label="Woodkari home"><img src="{UP}icon-96.png" width="40" height="40" alt=""><b>Woodkari</b></a>
<p>Woodkari Exports, Sambhal, Uttar Pradesh. Wooden and resin trays and boxes, making since 2008. Bulk orders from 25 pieces; single pieces on WhatsApp.</p></div>
<div><h3>Shop</h3><a class="l" href="shop.html">All pieces</a><a class="l" href="designs.html">Made to order designs</a><a class="l" href="bulk.html">Bulk and hotel orders</a><a class="l" href="terms.html">Order terms</a><a class="l" href="name-and-logo.html">Name and logo engraving</a><a class="l" href="./#questions">Questions</a></div>
<div><h3>Talk to us</h3><a class="l" href="{e(wa(HELLO))}">WhatsApp +91 91197 93282</a><a class="l" href="mailto:{EMAIL}">{EMAIL}</a><a class="l" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @woodkariexports</a></div>
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


def faq_html():
    rows = "".join(f'<details name="faq"><summary>{e(q)}{PLUS}</summary><p>{e(a)}</p></details>' for q, a in FAQ)
    return f'<div class="faq rv">{rows}</div>'


def page_home():
    items, n, groups = shop_menu()
    byid = {x["id"]: x for x in items}
    best = "".join(shop_card(byid[i]) for i in BEST)
    new = "".join(shop_card(byid[i]) for i in NEW_ARRIVALS)
    tiles = "".join(f'<a class="tile rv" href="shop.html?c={g}"><img src="{UP}img/{GROUP_PIC[g]}-600.webp" alt="{e(label)}" width="600" height="600" loading="lazy"><span class="cap">{e(label)}</span></a>' for g, label, ls in groups)
    ribbon_items = ["Made in India since 2008", "Trays and boxes in bulk from 25 pieces", "Your name or logo from 50 pieces", "Acacia pieces in any size", "Finished by hand", "Order on WhatsApp"]
    ribbon = "".join(f"<span>{e(t)}</span>" for t in ribbon_items * 2)
    dz = "".join(f'<a class="rv" href="{e(wa("Hello Woodkari, I am asking about: " + n_ + chr(10) + "Quantity: "))}"><div class="ph"><img src="{UP}img/{k}.webp" alt="{e(n_)}, design picture" width="480" height="480" loading="lazy"><span class="tag">Made to order</span></div><b>{e(n_)}</b><i>Ask on WhatsApp</i></a>' for k, n_ in DESIGNS)
    hero_top = mto_price_txt = mto_pr("OW-38")[0]
    return head("Wooden & Resin Trays, Boxes in Bulk | Woodkari, India",
                "Acacia wood and resin trays and boxes from India, making since 2008. Bulk from 25 pieces, name or logo from 50, single pieces on WhatsApp.",
                "", "m-bone-inlay-coffee-table-38-e.webp") + f"""<body>
{header('home')}
<main id="main">
<section class="hero">
<div class="show"><a class="slide on" href="design-ow-38.html"><img src="{UP}img/m-bone-inlay-coffee-table-38-e.webp" alt="Round bone inlay drum coffee table with a black and white sunburst pattern, in a living room" width="1200" height="1200" fetchpriority="high"><span class="tag">Design picture, made to order</span><span class="nm">Inlay drum coffee table<span>{hero_top}</span></span></a></div>
<div class="hero-txt">
<h1><span class="ln"><span>Made in</span></span><span class="ln"><span>India.</span></span></h1>
<p class="fade">Inlay furniture, wooden trays and resin pieces.<span class="more"> Making since 2008. Most of our orders are bulk: trays and boxes from 25 of one design. Single pieces too, on WhatsApp.</span></p>
<div class="row fade d2"><a class="btn pri" href="shop.html">Shop all pieces{ARROW}</a><a class="btn inv" href="shop.html">Shop all pieces{ARROW}</a><a class="btn ghost" href="bulk.html">Bulk orders</a></div>
</div>
</section>
<div class="ribbon" aria-hidden="true"><div class="track">{ribbon}</div></div>

<section class="sec" id="best"><div class="wrap">
<div class="hdr rv"><div><h2>Bestselling designs</h2><p>Prices are for one piece; delivery is extra.</p></div><a class="lnk" href="shop.html">All pieces{ARROW}</a></div>
<div class="grid four">{best}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Shop by kind</h2></div></div>
<div class="tiles">{tiles}</div>
</div></section>

<section class="sec" id="new"><div class="wrap">
<div class="hdr rv"><div><h2>New arrivals</h2></div><a class="lnk" href="shop.html">All pieces{ARROW}</a></div>
<div class="grid four" id="newarr">{new}</div>
</div></section>

<section class="band green" id="bulk"><div class="wrap split">
<div class="fig wipe"><img src="{UP}img/fluted-life.webp" alt="Fluted acacia box tray with keys, coins and sunglasses on a hall table" width="1200" height="1200" loading="lazy"><span class="tag">Styled picture</span></div>
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

<section class="sec" id="engraving"><div class="wrap split rev">
<div class="fig wipe"><img src="{UP}img/d-engraved-600.webp" alt="Wooden serving board with a sample logo engraved, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>
<div class="rv">
<h2>Your name or logo, by laser.</h2>
<p class="lead">On 50 pieces or more of one design, we engrave a hotel name, a company logo or a couple's names: room trays for a hotel, boxes and boards for staff gifts or a wedding.</p>
<div class="row"><a class="btn pri" href="name-and-logo.html">How it works{ARROW}</a><a class="btn line" href="{e(wa('Hello Woodkari, I want my name or logo engraved.' + chr(10) + 'Piece:' + chr(10) + 'Quantity: '))}">{WA_ICON}Ask on WhatsApp</a></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Made on order, in bulk</h2><p>More designs the karigars make when you ask. These are made for bulk orders only. Tell us the piece and the quantity on WhatsApp.</p></div></div>
<div class="dz">{dz}</div>
<p class="mto-l rv"><a class="lnk" href="shop.html">See all pieces{ARROW}</a></p>
</div></section>

<section class="band stone" id="workshop"><div class="wrap">
<div class="rv">
<h2>The workshop</h2>
<p class="lead">Woodkari is a workshop in India, at work since 2008. Four karigars cut the wood on a CNC router, engrave by laser and finish our wooden pieces by hand. Our resin trays are made with other makers near our workshop.</p>
</div>
<!-- TODO(workshop photos): the owner sends real workshop photos on 19 Nov; show them here. The tray picture was removed 18 Nov. -->
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
<p class="crumb"><a href="shop.html">All pieces</a> / {e(p['name'])}</p>
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
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(n)}, design picture{"" if j == 0 else ", another view"}" width="1200" height="1200"{(" style=" + chr(34) + "view-transition-name:pic" + chr(34)) if j == 0 else " loading=lazy"}><figcaption>Design picture · made to order</figcaption></figure>'
        for j, k in enumerate(pics))
    if code in MTO_SIZES:
        fl = [("Design", code), ("Kind", title), ("Made", "On order")] + [(f"Size {sz}", rupee(pp)) for sz, pp in MTO_SIZES[code]]
    else:
        fl = [("Design", code), ("Kind", title), ("Made", "On order"), ("Price", mto_pr(code)[0] if code in MTO_PRICE else "On WhatsApp")] + ([("Size", MTO_PRICE[code][2])] if code in MTO_PRICE else [])
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in fl)
    pr_txt, pr_note = mto_pr(code)
    others = [(j, x) for j, x in enumerate(items, MTO_START.get(gid, 1)) if j != i and f"{pre}-{j}" not in MTO_HOLD][:3]
    more = "\n".join(
        f'<a class="p rv" href="{mto_page(f"{pre}-{j}")}"><div class="ph"><img src="{UP}img/m-{ff}-600.webp" alt="{e(nn)}, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
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
<a class="lnk more-l" href="designs.html">All designs{ARROW}</a>
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
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": n, "sku": code,
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
{price}
<p class="note">Made to order. We tell you the making time on WhatsApp.</p>
<div class="row"><a class="btn pri wide" href="{e(wa(msg))}">{WA_ICON}{btn}</a></div>
<p class="lede">{e(lede)}</p>
<ul class="facts">{facts}</ul>
<a class="lnk more-l" href="designs.html">All designs{ARROW}</a>
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


def page_designs():
    OW_AC = [x for x in OW if ow_wood(x) == "acacia"]
    OW_MG = [x for x in OW if ow_wood(x) == "mango"]
    chips = f'<a href="#g-{OW_GID}">{e(OW_CHIP)}</a><a href="#g-mango">{e(MG_CHIP)}</a>' + "".join(f'<a href="#g-{gid}">{e(title)}</a>' for gid, pre, title, line, items in MTO)
    groups = [f'<section class="sec mto" id="g-{OW_GID}"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(OW_TITLE)}</h2><p>{e(OW_LINE)}</p></div></div>\n<div class="grid four">{"".join(ow_card(it, True) for it in OW_AC)}</div>\n</div></section>',
              f'<section class="sec mto" id="g-mango"><div class="wrap">\n<div class="hdr rv"><div><h2>{e(MG_TITLE)}</h2><p>{e(MG_LINE)}</p></div></div>\n<div class="grid four">{"".join(ow_card(it, True) for it in OW_MG)}</div>\n</div></section>']
    for gid, pre, title, line, items in MTO:
        cards = "".join(
            f'<a class="p rv" id="{pre}-{i}" href="{mto_page(f"{pre}-{i}")}"><div class="ph"><img src="{UP}img/m-{f}-600.webp" alt="{e(n)}, design picture" width="600" height="600" loading="lazy"><span class="tag">Made to order</span></div>'
            f'<h3>{e(n)}</h3><p class="sh">Design {pre}-{i} · made on order</p><p class="pr{"" if f"{pre}-{i}" in MTO_PRICE else " bo"}">{e(mto_pr(f"{pre}-{i}")[0])}</p></a>'
            for i, (f, n) in enumerate(items, MTO_START.get(gid, 1)) if f"{pre}-{i}" not in MTO_HOLD)
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


TERMS_SINGLE = [
    "Every piece is made to order. We start making it once you have ordered and paid, by UPI or bank transfer: the full price for a piece up to ₹10,000; for a piece above ₹10,000, such as furniture, a 50% advance, and the rest before dispatch. We tell you the making time on WhatsApp.",
    "You can cancel for free until we start making. Once making has started, the order cannot be cancelled.",
    "Each piece is made for you, so we do not take returns for a change of mind.",
    "If a piece arrives damaged or is not what you ordered, tell us on WhatsApp within 48 hours of delivery, with an uncut unboxing video and photos. We replace it, or return your money if we cannot replace it. We pay the shipping for this.",
    "Handmade pieces differ a little: wood grain and colour change from piece to piece. This is not a defect.",
    "Delivery is extra. We tell you the amount on WhatsApp.",
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
<div class="fig wipe"><img src="{UP}img/fluted-life.webp" alt="Fluted acacia box tray with keys, coins and sunglasses on a hall table" width="1200" height="1200"><span class="tag">Styled picture</span></div>
</div></section>

<section class="sec"><div class="wrap bulk-all rv">
<p>Every piece on the site can be made in bulk, from 25 pieces.</p>
<a class="lnk" href="shop.html">See all pieces{ARROW}</a>
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
         f"- [All pieces]({SITE}/shop.html): every piece on the site with its picture and price, in kinds.",
         f"- [Name and logo]({SITE}/name-and-logo.html): a name or logo by laser on 50 pieces or more of one design.",
         f"- [Bulk and hotel orders]({SITE}/bulk.html): bulk orders from 25 pieces, for hotels, gifting companies, shops and importers.",
         f"- [Made to order designs]({SITE}/designs.html): {ALL_N} more designs. Every picture there is a design picture, made to show the piece. Every design shows its price; order on WhatsApp.", "",
         "## Pieces", ""]
    L += [f"- [{p['name']}]({SITE}/{p['slug']}.html): {p['short']}; {price(p)}" for p in PRODUCTS]
    L += ["", "## Made to order designs, by kind", "",
          f"- [{OW_TITLE}]({SITE}/designs.html#g-{OW_GID}): {OW_LINE}",
          f"- [{MG_TITLE}]({SITE}/designs.html#g-mango): {MG_LINE}"]
    L += [f"- [{title}]({SITE}/designs.html#g-{gid}): {line}" for gid, pre, title, line, items in MTO]
    L += ["", "## Bulk terms (from the bulk page)", ""] + [f"- {a}: {b}" for a, b in terms]
    return "\n".join(L) + "\n"


def main():
    os.makedirs(OUT, exist_ok=True)
    w = lambda name, s: open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)
    css = CSS.strip() + "\n"
    if PREVIEW:
        css = css.replace("url(fonts/", "url(../fonts/")
    w("site.css", css)
    w("site.js", JS.strip() + "\n")
    w("index.html", page_home())
    w("bulk.html", page_bulk())
    w("terms.html", page_terms())
    w("designs.html", page_designs())
    w("shop.html", page_shop())
    w("name-and-logo.html", page_engraving())
    for gid, pre, title, line, items in MTO:
        for i in range(MTO_START.get(gid, 1), MTO_START.get(gid, 1) + len(items)):
            if f"{pre}-{i}" in MTO_HOLD: continue
            w(mto_page(f"{pre}-{i}"), page_design(gid, pre, title, line, items, i))
    for it in OW:
        w(mto_page(it["code"]), page_ow(it))
    for p in PRODUCTS:
        w(p["slug"] + ".html", page_product(p))
    if not PREVIEW:
        urls = [""] + [p["slug"] + ".html" for p in PRODUCTS] + ["designs.html"] + [mto_page(it["code"]) for it in OW] + [mto_page(c) for _, c, _, _ in mto_items()] + ["shop.html", "name-and-logo.html", "bulk.html", "terms.html"]
        w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
        w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
        w("llms.txt", llms_txt())
    print("built", OUT, len(PRODUCTS) + 3 + ALL_N, "pages")


main()
