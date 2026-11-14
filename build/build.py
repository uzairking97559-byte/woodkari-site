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

# imgs: (file key, alt, caption). card: (studio key, in-use key) for the shop grid.
PRODUCTS = [
    dict(slug="navy-ivory-floral-tray", name="Navy & Ivory Floral Tray", cat="resin", price=1999, mto=True,
         short="Resin · 14 × 8 in, cut-out handles", card=("navy-front", "navy-top"),
         lede="An ivory tray with a navy floral pattern filled in resin, and a handle cut into each side.",
         uses="Tea for two, or a tray for the dressing table.",
         facts=[("Size", "14 × 8 inches (36 × 20 cm), rim 2 inches high"), ("Top", "Pattern filled in resin"), ("Core", "MDF wood board"),
                ("Made in", "Sambhal, Uttar Pradesh")],
         imgs=[("navy-front", "Ivory tray with a navy floral pattern on a wooden table", "Design picture, made to order"),
               ("navy-use", "Navy and ivory floral tray carrying two cups of tea and biscuits", "Design picture, made to order"),
               ("navy-top", "Navy and ivory floral tray seen from above on a white sheet", "Design picture, made to order")]),
    dict(slug="black-white-floral-tray-set", name="Black & White Floral Tray Set", cat="resin", price=6999, unit="set of 2", mto=True,
         short="Resin · one round, one rectangular", card=("bw-front", "bw-top"),
         lede="A round tray and a rectangular tray with a black and white floral pattern, in the look of bone inlay, filled in resin.",
         uses="A pair for the dining table or the living room.",
         facts=[("In the set", "1 round tray and 1 rectangular tray"), ("Size", "Rectangle 18 × 10 inches (46 × 25 cm). Round tray: size on request"), ("Top", "Pattern filled in resin"),
                ("Core", "MDF wood board"), ("Made in", "Sambhal, Uttar Pradesh")],
         imgs=[("bw-front", "Round and rectangular black and white floral trays on a wooden table", "Design picture, made to order"),
               ("bw-use", "Black and white floral trays with tea and snacks on a dining table", "Design picture, made to order"),
               ("bw-top", "Black and white floral trays side by side, seen from above", "Design picture, made to order")]),
    dict(slug="red-chevron-tray", name="Red Chevron Tray", cat="resin", price=2799, mto=True,
         short="Resin · 16 × 10 in, red and white zigzag", card=("chevron-front", "chevron-top"),
         lede="A white-framed rectangular tray with a red and white chevron pattern filled in resin.",
         uses="Breakfast in bed, or a bright tray for the kitchen counter.",
         facts=[("Size", "16 × 10 inches (41 × 25 cm), rim 2 inches high"), ("Top", "Pattern filled in resin"), ("Core", "MDF wood board"),
                ("Made in", "Sambhal, Uttar Pradesh")],
         imgs=[("chevron-front", "White-framed tray with a red and white chevron pattern on a wooden table", "Design picture, made to order"),
               ("chevron-use", "Red chevron tray carrying a glass jug and two glasses of water", "Design picture, made to order"),
               ("chevron-top", "Red chevron tray seen from above on a white sheet", "Design picture, made to order")]),
    dict(slug="gold-flake-resin-tray", name="Gold-flake Resin Tray", cat="resin", price=None, bulk_only=True, mto=True,
         short="Poured resin · gold flakes, leaf handles", card=("gold-front", "gold-top"),
         lede="Black marbled resin with gold flakes poured over an MDF board, with two gold-tone metal leaf handles. Made for bulk orders only.",
         uses="Serving trays for a hotel, a wedding or a company gift.",
         facts=[("Top", "Poured resin with gold flakes"), ("Core", "MDF wood board"), ("Handles", "Gold-tone metal leaves"),
                ("Size", "On request"), ("Made in", "Sambhal, Uttar Pradesh"), ("Orders", "Bulk only. Price on WhatsApp")],
         imgs=[("gold-front", "Black and gold resin tray with leaf handles on a wooden table", "Design picture, made to order"),
               ("gold-use", "Black and gold resin tray holding two bowls of pistachios and almonds", "Design picture, made to order"),
               ("gold-top", "Black and gold resin tray seen from above on a white sheet", "Design picture, made to order")]),
    dict(slug="fluted-box-tray", name="Fluted Box Tray", cat="wood", price=1299,
         short="Acacia · 11.5 × 7 × 3 in", card=("fluted-life2", "fluted-studio"),
         lede="An open box tray in acacia wood. The sides are cut into upright flutes and the rim is scalloped, then the piece is finished by hand to a warm walnut tone.",
         uses="Keys and wallet by the door, a dressing table, a desk, or a gift hamper.",
         facts=[("Size", "11.5 × 7 inches, 3 inches high (29 × 18 × 7.6 cm)"), ("Wood", "Acacia"), ("Finish", "Walnut-tone polish, finished by hand"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Goes with", "The Room Tray: same 11.5 inch side"),
                ("Other sizes", "Any size, on order"),
                ("Name or logo", "By laser, on 50 pieces or more of one design")],
         imgs=[("fluted-front", "Fluted box tray on a wooden table, seen from the front", "Styled picture"),
               ("fluted-use", "Fluted box tray on the floor by a door, holding car keys and a wallet", "Styled picture"),
               ("fluted-top", "Fluted box tray seen from above on a white sheet", "Styled picture"),
               ("fluted-real1", "Fluted box tray, plain photo from the front", "Our piece, plain photo"),
               ("fluted-real2", "Fluted box tray, plain photo from the side", "Our piece, plain photo"),
               ("fluted-real3", "Fluted box tray, plain photo from above", "Our piece, plain photo")]),
    dict(slug="room-tray", name="Room Tray", cat="wood", price=1799,
         short="Acacia · 15 × 11.5 in, with caddy", card=("room-front", "room-studio"),
         lede="A solid acacia board with one large round dip, two small ones and two long slots, and a four-box caddy that stands beside it. Made as the tea tray of a hotel guest room.",
         uses="Kettle and cups in a guest room, or watch, phone and keys on a bedside table.",
         facts=[("Size", "Tray 15 × 11.5 inches (38 × 29 cm). Caddy 10 inches long"), ("Wood", "Acacia"), ("Finish", "Walnut-tone polish, finished by hand"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Other sizes", "Any size, on order"),
                ("Name or logo", "A hotel name or logo by laser, on 50 pieces or more")],
         imgs=[("room-front", "Room tray on a wooden table with two cups of tea", "Styled picture"),
               ("room-use", "Room tray on a bedside table with a kettle, keys and a phone", "Styled picture"),
               ("room-top", "Room tray seen from above on a white sheet", "Styled picture"),
               ("room-real1", "Room tray, plain photo from the front", "Our piece, plain photo"),
               ("room-real2", "Room tray, plain photo from the side", "Our piece, plain photo"),
               ("room-real3", "Room tray, plain photo of the caddy", "Our piece, plain photo")])
]

CATS = [("all", "Everything"), ("wood", "Acacia wood"), ("resin", "Resin trays"), ("u1500", "Under ₹1,500")]

TILES = [("t-table", "On the table", "Black & White Tray Set", "black-white-floral-tray-set.html", "Black and white floral trays with tea and snacks", "Design picture"),
         ("navy-use-600", "Tea for two", "Navy & Ivory Floral Tray", "navy-ivory-floral-tray.html", "Navy and ivory floral tray carrying two cups of tea and biscuits", "Design picture"),
         ("t-gift", "For gifting", "Bulk, from 25 pieces", "bulk.html", "Black and gold resin tray with bowls of dry fruit", "Design picture"),
         ("t-room", "In the guest room", "Room Tray", "room-tray.html", "Room tray on a bedside table with a kettle", "Styled picture")]

SLIDES = [("navy-use", "navy-ivory-floral-tray"), ("bw-use", "black-white-floral-tray-set"),
          ("gold-use", "gold-flake-resin-tray"), ("chevron-use", "red-chevron-tray")]

DESIGNS = [("d2-coaster", "Resin coaster set"), ("d2-tissue", "Resin tissue box"), ("d2-roundbox", "Round box with resin lid"),
           ("d2-board", "Serving board"), ("d2-cutlery", "Cutlery and napkin stand"), ("d2-trivet", "Resin trivets")]


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


WA_ICON = '<svg class="i" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8.9c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.3Z"/></svg>'
ARROW = '<svg class="i" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path class="h" d="M4 7h16M4 12h16M4 17h16"/><path class="x" d="M6 6l12 12M18 6 6 18"/></svg>'
MAIL = '<svg class="i" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>'

CSS = r"""
@font-face{font-family:"Hanken Grotesk";font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/hanken-grotesk-latin.woff2) format("woff2");unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:"Hanken Grotesk";font-style:normal;font-weight:400 700;font-display:swap;src:url(fonts/hanken-grotesk-latin-ext.woff2) format("woff2");unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:"Young Serif";font-style:normal;font-weight:400;font-display:swap;src:url(fonts/young-serif-latin.woff2) format("woff2")}
@font-face{font-family:"Rozha One";font-style:normal;font-weight:400;font-display:swap;src:url(fonts/rozha-one-latin.woff2) format("woff2")}

:root{--bg:#fff;--stone:#f4ebdf;--stone-2:#eadfd0;--ink:#1c1a17;--dk:#3a2016;--dk-2:#4a2a1c;--soft:#5d564d;--line:#e4ddd2;--wood:#8b4a2b;--wood-d:#6e3920;--wa:#0f7a4c;--wa-d:#0b613c;--r:4px;
 --serif:"Young Serif",Georgia,"Times New Roman",serif;--sans:"Hanken Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif;--ease:cubic-bezier(.16,1,.3,1)}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.6 var(--sans);overflow-x:hidden;-webkit-tap-highlight-color:transparent;text-rendering:optimizeLegibility}
::selection{background:var(--wood);color:#fff}
img{max-width:100%;height:auto;display:block}
a{color:var(--wood);text-underline-offset:3px;text-decoration-thickness:1px}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.1;margin:0;color:var(--ink);text-wrap:balance;letter-spacing:-.01em}
p{text-wrap:pretty}
.i{flex:none}
.wrap{max-width:1240px;margin:0 auto;padding:0 16px}
@media(min-width:760px){.wrap{padding:0 32px}}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px 12px;z-index:20}
:focus-visible{outline:2px solid var(--wood);outline-offset:3px;border-radius:2px}
html{scrollbar-color:#c9bfb2 transparent;scrollbar-width:thin}

/* bar + header */
.pv{background:#fff3c4;color:#4a3b00;text-align:center;font-size:14px;padding:6px}
.bar{background:var(--dk);color:#f3e6d8;font-size:13px;white-space:nowrap;overflow:hidden;letter-spacing:.02em;text-align:center;padding:8px 12px}
.bar span+span::before{content:"";display:inline-block;width:3px;height:3px;border-radius:50%;background:#c89a7c;vertical-align:middle;margin:0 10px}
.hd{position:sticky;top:0;z-index:10;background:rgba(255,255,255,.96);border-bottom:1px solid var(--line)}
@supports (backdrop-filter:blur(8px)){.hd{background:rgba(255,255,255,.88);backdrop-filter:blur(8px)}}
.hd .wrap{display:flex;align-items:center;gap:20px;height:64px}
.mark{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);margin-right:auto}
.mark img{border-radius:8px}
.mark b{font:400 26px/1 "Rozha One",Georgia,serif;letter-spacing:.01em}
.mark small{display:block;font:600 11px/1 var(--sans);letter-spacing:.3em;color:var(--wood);margin-top:4px}
.nav{display:none;gap:4px}
.nav a{color:var(--ink);text-decoration:none;font-size:15.5px;font-weight:500;padding:10px 12px}
.nav a:hover{color:var(--wood)}
.nav a[aria-current]{color:var(--wood)}
@media(min-width:900px){.nav{display:flex}}
.menu{display:inline-grid;place-items:center;width:44px;height:44px;border:0;background:transparent;color:var(--ink);cursor:pointer;border-radius:var(--r);margin-left:-4px}
.menu:hover{background:var(--stone)}
.menu .x{display:none}.menu[aria-expanded=true] .x{display:block}.menu[aria-expanded=true] .h{display:none}
@media(min-width:900px){.menu{display:none}}
.mnav{position:absolute;left:0;right:0;top:100%;background:#fff;border-bottom:1px solid var(--line);box-shadow:0 18px 30px -18px rgba(40,20,10,.35);padding:8px 16px 18px}
.mnav[hidden]{display:none}
.mnav a{display:flex;justify-content:space-between;align-items:center;padding:15px 2px;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;font:400 22px/1.2 var(--serif)}
.mnav a:hover{color:var(--wood)}
.mnav .btn{margin-top:16px;width:100%;font:600 16.5px/1.2 var(--sans);border-bottom:0;justify-content:center;padding:12px 24px}
.mnav small{display:block;margin-top:12px;color:var(--soft);font-size:14.5px;text-align:center}
@media(min-width:900px){.mnav{display:none!important}}
.hd{position:sticky}
.hd .btn{min-height:42px;padding:8px 16px;font-size:15px}
@media(max-width:420px){.hd .btn span{display:none}.hd .btn{padding:8px 12px}}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:52px;padding:12px 24px;border-radius:var(--r);font:600 16.5px/1.2 var(--sans);text-decoration:none;border:0;cursor:pointer;transition:background-color .2s,color .2s,box-shadow .2s}
.btn.wa{background:var(--wa);color:#fff}.btn.wa:hover{background:var(--wa-d)}
.btn.dark{background:var(--ink);color:#fff}.btn.dark:hover{background:#000}
.btn.line{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--ink)}.btn.line:hover{background:var(--ink);color:#fff}
.btn.ghost{background:rgba(255,255,255,.08);color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.85)}.btn.ghost:hover{background:#fff;color:var(--ink)}
.btn.wood{background:var(--wood);color:#fff}.btn.wood:hover{background:var(--wood-d)}
.btn.wide{width:100%}
.row{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.lnk{display:inline-flex;align-items:center;gap:8px;font-weight:600;color:var(--ink);text-decoration:none;padding:10px 0;border-bottom:1px solid var(--ink)}
.lnk:hover{color:var(--wood);border-color:var(--wood)}

/* hero */
.hero{background:var(--stone);overflow:hidden}
.hero .tag,.split .tag,.bh .tag,.tile .tag{position:absolute;z-index:2;background:#fff;color:var(--ink);font:600 12px/1 var(--sans);padding:5px 8px;border-radius:2px}
.fig{position:relative}.fig .tag{left:10px;top:10px}
.tile .tag{left:10px;top:10px}
.hgrid{display:flex;flex-direction:column-reverse;padding:0}
.show{position:relative;aspect-ratio:1/1;overflow:hidden;background:#d9cbb9}
.slide{position:absolute;inset:0;opacity:0;visibility:hidden;transition:opacity 1.1s var(--ease),visibility 0s 1.1s;color:#fff;text-decoration:none}
.slide.on{opacity:1;visibility:visible;transition:opacity 1.1s var(--ease),visibility 0s}
.slide img{width:100%;height:100%;object-fit:cover;transform:scale(1.07);transition:transform 7s linear}
.slide.on img{transform:scale(1)}
.slide .tag{right:12px;top:12px}
.slide .nm{position:absolute;left:0;right:0;bottom:0;padding:56px 16px 16px;background:linear-gradient(to top,rgba(20,10,5,.66),rgba(20,10,5,0));font:500 15px/1.3 var(--sans);display:flex;justify-content:space-between;gap:12px;align-items:end}
.slide .nm b{font:400 21px/1.15 var(--serif)}
.hero .txt{padding:28px 16px 36px}
.hero h1{font-size:clamp(38px,9.6vw,74px);max-width:10.5em;letter-spacing:-.015em}
.hero p{margin:16px 0 0;color:var(--soft);font-size:18px;max-width:30em}
.dots{display:flex;gap:6px;margin-top:28px}
.dot{flex:1;max-width:120px;height:32px;padding:0;border:0;background:none;cursor:pointer;position:relative;text-align:left;font:500 12.5px/1 var(--sans);color:var(--soft)}
.dot::before{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:#d6c7b4}
.dot::after{content:"";position:absolute;left:0;top:0;height:2px;width:0;background:var(--dk)}
.dot span{position:absolute;left:0;top:10px;white-space:nowrap}
.dot[aria-current=true]{color:var(--ink)}
.dot[aria-current=true]::after{animation:fill var(--dur,5.5s) linear forwards}
.paused .dot[aria-current=true]::after{animation-play-state:paused}
@keyframes fill{to{width:100%}}
.rise{animation:rise .9s var(--ease) both}
.rise.d1{animation-delay:.08s}.rise.d2{animation-delay:.18s}.rise.d3{animation-delay:.3s}.rise.d4{animation-delay:.42s}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@media(min-width:900px){
 .hgrid{flex-direction:row;align-items:stretch;max-width:none;padding:0}
 .hero .txt{flex:1 1 46%;display:flex;flex-direction:column;justify-content:center;padding:64px 56px 64px max(32px,calc((100vw - 1240px)/2 + 32px))}
 .show{flex:0 0 54%;aspect-ratio:auto;height:min(calc(100vh - 150px),760px);min-height:540px}
 .dot span{display:block}
}
@media(max-width:899px){.dot span{display:none}.dots{margin-top:22px}}
/* fact ribbon */
.ribbon{background:var(--dk);color:#f3e6d8;overflow:hidden;white-space:nowrap;border-top:1px solid rgba(255,255,255,.08)}
.ribbon .track{display:inline-flex;gap:0;padding:15px 0;animation:slide 38s linear infinite}
.ribbon:hover .track{animation-play-state:paused}
.ribbon span{font:400 19px/1 var(--serif);padding:0 26px;display:inline-flex;align-items:center;gap:26px}
.ribbon span::after{content:"";width:6px;height:6px;border-radius:50%;background:#c98a63}
@keyframes slide{to{transform:translateX(-50%)}}
/* scroll reveal: visible by default, animated only when JS marks it */
.js .rv{opacity:0;transform:translateY(22px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.js .rv.in{opacity:1;transform:none}
.p .ph img:first-of-type,.p .ph img{transition:opacity .6s var(--ease),transform .9s var(--ease)}
.p:hover .ph img{transform:scale(1.03)}

/* section rhythm */
.sec{padding:72px 0 0}
.sec.tight{padding-top:56px}
.hdr{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:12px 32px;margin-bottom:28px}
.hdr h2{font-size:clamp(30px,4.2vw,46px)}
.hdr p{margin:10px 0 0;color:var(--soft);max-width:36em}
.stone{background:var(--stone);margin-top:80px;padding:72px 0}
.stone+.sec{padding-top:72px}

/* tiles */
.tiles{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;scrollbar-width:none}
.tiles::-webkit-scrollbar{display:none}
.tile{flex:0 0 72%;scroll-snap-align:start;position:relative;overflow:hidden;border-radius:var(--r);text-decoration:none;color:#fff;aspect-ratio:3/4;background:#3a2a20}
.tile img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ease)}
.tile:hover img{transform:scale(1.04)}
.tile .cap{position:absolute;inset:auto 0 0 0;padding:72px 18px 18px;background:linear-gradient(to top,rgba(18,12,8,.78),rgba(18,12,8,0));font:400 26px/1.1 var(--serif)}
.tile small{display:block;font:500 15px/1.3 var(--sans);margin-top:6px;color:#efe8de}
@media(min-width:760px){.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin:0;padding:0;overflow:visible}.tile{flex:none}}

/* shop */
.chips{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;margin:0 -16px 24px;padding:0 16px}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;min-height:42px;padding:8px 18px;border-radius:var(--r);border:1px solid var(--line);background:#fff;font:500 15px var(--sans);color:var(--ink);cursor:pointer;transition:border-color .2s,background-color .2s,color .2s}
.chip:hover{border-color:var(--ink)}
.chip[aria-pressed=true]{background:var(--dk);border-color:var(--dk);color:#fff}
@media(min-width:760px){.chips{margin:0 0 28px;padding:0}}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:32px 14px}
@media(min-width:760px){.grid{grid-template-columns:repeat(3,1fr);gap:48px 28px}}
.p{text-decoration:none;color:var(--ink);display:block}
.p[hidden]{display:none}
.p .ph{position:relative;aspect-ratio:1/1;overflow:hidden;background:#f7f5f1;border-radius:var(--r)}
.p .ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.p .ph .u{opacity:0;transition:opacity .6s var(--ease)}
.p:hover .ph .u,.p:focus-visible .ph .u{opacity:1}
.p .tag{position:absolute;left:10px;top:10px;z-index:1;background:#fff;color:var(--ink);font-size:12.5px;font-weight:600;letter-spacing:.02em;padding:4px 8px;border-radius:2px}
.p h3{font:600 17px/1.3 var(--sans);margin:14px 0 2px;letter-spacing:0}
.p .sh{color:var(--soft);font-size:14.5px;line-height:1.35;margin:0}
.p .pr{font-weight:600;font-size:16.5px;margin:6px 0 0;font-variant-numeric:tabular-nums lining-nums}
.p .pr span{font-weight:400;color:var(--soft);font-size:14px}
.p .pr.bo{color:var(--wood)}
@media(hover:none){.p .ph .u{display:none}}

/* bulk split */
.split{display:grid;gap:32px}
.split img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r)}
@media(min-width:900px){.split{grid-template-columns:1fr 1fr;gap:64px;align-items:center}.split.rev>:first-child{order:2}}
.split h2{font-size:clamp(30px,4.2vw,46px)}
.split .lead{color:var(--soft);margin:12px 0 0;max-width:32em}
.steps{list-style:none;margin:28px 0 0;padding:0;border-top:1px solid var(--line);counter-reset:s}
.steps li{counter-increment:s;display:grid;grid-template-columns:44px 1fr;gap:0 8px;padding:18px 0;border-bottom:1px solid var(--line)}
.steps li::before{content:counter(s);grid-row:span 2;font:400 26px/1.1 var(--serif);color:var(--wood)}
.steps b{font-weight:600}
.steps span{color:var(--soft);font-size:16px}
.stone .steps,.stone .steps li{border-color:#dccdbb}
.dark{background:var(--dk);color:#f3e6d8;margin-top:80px;padding:72px 0}
.dark h2{color:#fff}
.dark .lead,.dark .steps span{color:#e2cfbd}
.dark .steps,.dark .steps li{border-color:rgba(255,255,255,.16)}
.dark .steps li::before{color:#e0a985}
.dark .btn.line{color:#fff;box-shadow:inset 0 0 0 1px rgba(255,255,255,.8)}.dark .btn.line:hover{background:#fff;color:var(--dk)}
.dark+.sec{padding-top:72px}

/* designs on order */
.dz{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px 6px;scrollbar-width:none}
.dz::-webkit-scrollbar{display:none}
.dz a{flex:0 0 44%;scroll-snap-align:start;text-decoration:none;color:var(--ink)}
.dz .ph{position:relative}
.dz img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r);background:#f7f5f1}
.dz .tag{position:absolute;left:8px;top:8px;background:#fff;font-size:12px;font-weight:600;padding:3px 7px;border-radius:2px}
.dz b{display:block;font-weight:600;margin-top:10px;line-height:1.3;font-size:15.5px}
.dz i{font-style:normal;font-size:14.5px;color:var(--wood)}
@media(min-width:760px){.dz{display:grid;grid-template-columns:repeat(6,1fr);gap:20px;margin:0;padding:0;overflow:visible}.dz a{flex:none}}

/* workshop facts */
.facts{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}
.facts li{display:grid;grid-template-columns:8.5em 1fr;gap:12px;padding:13px 0;border-bottom:1px solid var(--line);font-size:16px}
.facts b{font-weight:500;color:var(--soft)}

/* product page */
.crumb{font-size:14.5px;color:var(--soft);padding:16px 0 12px}
.crumb a{color:var(--soft);text-decoration:none;display:inline-block;padding:8px 0}
.crumb a:hover{color:var(--wood)}
.pd{display:grid;gap:24px}
@media(min-width:960px){.pd{grid-template-columns:1.2fr 1fr;gap:64px;align-items:start}.buy{position:sticky;top:96px}}
.gal{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px;scrollbar-width:none}
.gal::-webkit-scrollbar{display:none}
.gal figure{flex:0 0 88%;scroll-snap-align:center;margin:0;position:relative}
.gal img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r);background:#f7f5f1}
.gal figcaption{position:absolute;left:10px;bottom:10px;background:#fff;font-size:12.5px;font-weight:500;padding:4px 8px;border-radius:2px}
@media(min-width:960px){.gal{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0;padding:0;overflow:visible}.gal.odd figure:first-child{grid-column:1/-1}}
.buy h1{font-size:clamp(32px,4.4vw,48px)}
.buy .pr{font-size:24px;font-weight:600;margin:14px 0 0;font-variant-numeric:tabular-nums lining-nums}
.buy .pr span{font-size:15px;font-weight:400;color:var(--soft)}
.buy .pr.bo{color:var(--wood);font-size:20px}
.buy .note{font-size:15px;color:var(--soft);margin:6px 0 0}
.buy .lede{margin:22px 0 0}
.buy .uses{margin:10px 0 0;color:var(--soft)}
.buy .facts{margin-top:24px}
.buy .more-l{margin-top:18px}
.stick{position:fixed;left:0;right:0;bottom:0;z-index:9;background:#fff;border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;align-items:center;gap:14px}
.stick b{font-size:18px;font-weight:600;white-space:nowrap;font-variant-numeric:tabular-nums}
.stick .btn{flex:1;min-height:48px}
@media(min-width:960px){.stick{display:none}}
@media(max-width:959px){body.has-stick{padding-bottom:80px}.buy .btn.wa.wide{display:none}}

/* bulk page */
.bh{display:grid;gap:28px;padding-top:24px}
.bh img{width:100%;aspect-ratio:1200/744;object-fit:cover;border-radius:var(--r)}
@media(min-width:900px){.bh{grid-template-columns:1fr 1.15fr;gap:64px;align-items:center;padding-top:48px}}
.bh h1{font-size:clamp(36px,5vw,60px)}
.bh p{color:var(--soft);font-size:18px;margin:14px 0 0;max-width:30em}
.grid.four{grid-template-columns:1fr 1fr}
@media(max-width:759px){.grid.more3 .p:nth-child(3){display:none}}
@media(min-width:760px){.grid.four{grid-template-columns:repeat(4,1fr)}}

/* close + footer */
.end{text-align:center;padding:112px 0 8px}
.end h2{font-size:clamp(30px,4.2vw,46px)}
.end p{color:var(--soft);margin:12px auto 0;max-width:30em}
.end .row{justify-content:center}
.ft{margin-top:88px;background:var(--dk);color:#e2d3c4}
.ft .wrap{padding:48px 16px 40px;display:grid;gap:28px}
@media(min-width:760px){.ft .wrap{grid-template-columns:1.4fr 1fr 1fr;padding:56px 32px 44px}}
.ft a.mark{display:flex;color:#fff;margin:0 0 14px;padding:0}
.ft .mark small{color:#d4a487}
.ft .fine{max-width:none}
.ft h3{font:600 13px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:#c9a88f;margin:0 0 10px}
.ft p{margin:0;font-size:15.5px;max-width:28em}
.ft a{display:block;color:#fff;text-decoration:none;padding:9px 0;font-size:15.5px}
.ft a:hover{color:#e7c9b6}
.ft .fine{grid-column:1/-1;border-top:1px solid rgba(255,255,255,.14);padding-top:18px;font-size:13.5px;color:#c9b3a1}
.fab{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:9;width:56px;height:56px;border-radius:50%;background:var(--wa);color:#fff;display:grid;place-items:center;box-shadow:0 8px 24px rgba(15,60,40,.28)}
.fab:hover{background:var(--wa-d)}.fab .i{width:28px;height:28px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
"""

JS = r"""
function wkFilter(k){
  document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.cat===k)});
  document.querySelectorAll('.p[data-cat]').forEach(function(p){
    var price=+p.dataset.price;
    p.hidden=!(k==='all'||p.dataset.cat===k||(k==='u1500'&&price>0&&price<1500));});
}
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){wkFilter(c.dataset.cat)})});
var f=new URLSearchParams(location.search).get('f');if(f)wkFilter(f);
(function(){
  var rm=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rv=document.querySelectorAll('.rv');
  if(rm||!('IntersectionObserver' in window)){rv.forEach(function(x){x.classList.add('in')});}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var t=en.target,d=0;
      if(t.classList.contains('p')||t.classList.contains('tile')){d=(Array.prototype.indexOf.call(t.parentNode.children,t)%3)*90}
      setTimeout(function(){t.classList.add('in')},d);io.unobserve(t)}})},{rootMargin:'0px 0px -8% 0px'});
    rv.forEach(function(x){io.observe(x)});}
  var sl=document.querySelectorAll('.slide'),dt=document.querySelectorAll('.dot'),hero=document.querySelector('.hero');
  if(!sl.length)return;var cur=0,tm=null,DUR=5500;
  function go(n){sl[cur].classList.remove('on');dt[cur].removeAttribute('aria-current');cur=(n+sl.length)%sl.length;
    sl[cur].classList.add('on');var d=dt[cur];d.setAttribute('aria-current','true');d.style.animation='none';d.offsetWidth;d.style.animation='';}
  function play(){if(rm)return;clearInterval(tm);tm=setInterval(function(){go(cur+1)},DUR);hero.classList.remove('paused')}
  function stop(){clearInterval(tm);hero.classList.add('paused')}
  dt.forEach(function(d){d.addEventListener('click',function(){go(+d.dataset.i);play()})});
  var show=document.querySelector('.show');show.addEventListener('mouseenter',stop);show.addEventListener('mouseleave',play);
  show.addEventListener('focusin',stop);show.addEventListener('focusout',play);
  document.addEventListener('visibilitychange',function(){document.hidden?stop():play()});
  if(rm)hero.classList.add('paused');play();
})();
"""

ORG_LD = json.dumps([
    {"@context": "https://schema.org", "@type": "WebSite", "name": "Woodkari", "alternateName": "Woodkari Exports", "url": SITE + "/"},
    {"@context": "https://schema.org", "@type": "Organization", "name": "Woodkari Exports", "alternateName": "Woodkari",
     "url": SITE + "/", "logo": SITE + "/icon-512.png", "email": EMAIL, "foundingDate": "2008",
     "address": {"@type": "PostalAddress", "addressLocality": "Sambhal", "addressRegion": "Uttar Pradesh", "addressCountry": "IN"},
     "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+" + WHATSAPP, "availableLanguage": ["en", "hi"]}}])


def head(title, desc, path, image):
    robots = '<meta name="robots" content="noindex">' if PREVIEW else ""
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Woodkari">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/img/{image}">
<meta name="theme-color" content="#1c1a17">
<link rel="preload" href="{UP}fonts/young-serif-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}fonts/hanken-grotesk-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{UP}favicon.ico" sizes="48x48">
<link rel="icon" type="image/svg+xml" href="{UP}icon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="{UP}icon-96.png">
<link rel="apple-touch-icon" href="{UP}apple-touch-icon.png">
<link rel="stylesheet" href="site.css">
<script>document.documentElement.className+=" js"</script>
</head>
"""


def header(cur):
    def a(href, label, key):
        c = ' aria-current="page"' if key == cur else ""
        return f'<a href="{href}"{c}>{label}</a>'
    pv = '<div class="pv">Preview. Not the live site yet.</div>' if PREVIEW else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
{pv}<div class="bar"><span>Made in Sambhal since 2008</span><span>Bulk from 25 pieces</span></div>
<header class="hd"><div class="wrap">
<a class="mark" href="./" aria-label="Woodkari home"><img src="{UP}icon-96.png" width="38" height="38" alt=""><span><b>Woodkari</b><small>SAMBHAL</small></span></a>
<nav class="nav" aria-label="Main">{a('./#shop','Shop','shop')}{a('bulk.html','Bulk orders','bulk')}{a('./#engraving','Name &amp; logo','eng')}{a('./#workshop','Workshop','ws')}</nav>
<a class="btn wa" href="{e(wa('Hello Woodkari, I have a question.'))}">{WA_ICON}<span>WhatsApp</span></a>
<button class="menu" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu">{MENU_ICON}</button>
</div>
<nav class="mnav" id="mnav" aria-label="Menu" hidden>
<a href="./#shop">Shop the pieces{ARROW}</a><a href="bulk.html">Bulk orders{ARROW}</a><a href="./#engraving">Name and logo engraving{ARROW}</a><a href="./#workshop">The workshop{ARROW}</a>
<a class="btn wa" href="{e(wa('Hello Woodkari, I have a question.'))}">{WA_ICON}Chat on WhatsApp</a>
<small>{EMAIL}</small>
</nav>
</header>
<script>(function(){{var b=document.querySelector('.menu'),n=document.getElementById('mnav');function t(o){{b.setAttribute('aria-expanded',o);n.hidden=!o}}b.addEventListener('click',function(){{t(n.hidden)}});n.addEventListener('click',function(ev){{if(ev.target.closest('a'))t(false)}});document.addEventListener('keydown',function(ev){{if(ev.key==='Escape'&&!n.hidden){{t(false);b.focus()}}}})}})();</script>
"""


def footer():
    return f"""<footer class="ft"><div class="wrap">
<div><a class="mark" href="./" aria-label="Woodkari home"><img src="{UP}icon-96.png" width="38" height="38" alt=""><span><b>Woodkari</b><small>SAMBHAL</small></span></a>
<p>Woodkari Exports, Sambhal, Uttar Pradesh. Wooden and resin trays and boxes, making since 2008. Bulk orders from 25 pieces; single pieces on WhatsApp.</p></div>
<div><h3>Shop</h3><a href="./#shop">All pieces</a><a href="bulk.html">Bulk and hotel orders</a><a href="./#engraving">Name and logo engraving</a></div>
<div><h3>Talk to us</h3><a href="{e(wa('Hello Woodkari, I have a question.'))}">WhatsApp +91 91197 93282</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<p class="fine">Pictures marked "Styled picture" or "Design picture" are made to show the look of a piece; wood grain and resin differ a little on every piece. Only pictures marked "plain photo" are photos of our own pieces.</p>
</div></footer>
"""


def price_html(p, cls="pr"):
    if p.get("bulk_only"):
        return f'<p class="{cls} bo">Bulk only · price on WhatsApp</p>'
    unit = f' <span>/ {e(p["unit"])}</span>' if p.get("unit") else ""
    return f'<p class="{cls}">{rupee(p["price"])}{unit}</p>'


def card(p):
    a, b = p["card"]
    alt = p["imgs"][0][1]
    tag = '<span class="tag">' + ("Design picture" if p.get("mto") else "Styled picture") + '</span>'
    return f"""<a class="p rv" data-cat="{p['cat']}" data-price="{p['price'] or 0}" href="{p['slug']}.html">
<div class="ph">{tag}<img src="{UP}img/{a}-600.webp" alt="{e(alt)}" width="600" height="600" loading="lazy"><img class="u" src="{UP}img/{b}-600.webp" alt="" width="600" height="600" loading="lazy"></div>
<h3>{e(p['name'])}</h3><p class="sh">{e(p['short'])}</p>{price_html(p)}</a>"""


def page_home():
    chips = "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="{"true" if k=="all" else "false"}">{e(v)}</button>' for k, v in CATS)
    cards = "\n".join(card(p) for p in PRODUCTS)
    tiles = "".join(f'<a class="tile rv" href="{h}"><span class="tag">{lab}</span><img src="{UP}img/{k}.webp" alt="{e(alt)}" width="540" height="720" loading="lazy"><span class="cap">{e(t)}<small>{e(sub)}</small></span></a>' for k, t, sub, h, alt, lab in TILES)
    byslug = {q["slug"]: q for q in PRODUCTS}
    slides = "".join(
        f'<a class="slide{" on" if i == 0 else ""}" href="{sl}.html" data-i="{i}"><img src="{UP}img/{k}.webp" alt="{e(byslug[sl]["imgs"][1][1] if k.endswith("-use") else byslug[sl]["imgs"][0][1])}" width="1200" height="1200"{" fetchpriority=high" if i == 0 else " loading=lazy"}><span class="tag">Design picture</span><span class="nm"><b>{e(byslug[sl]["name"])}</b><span>{"Bulk only" if byslug[sl].get("bulk_only") else rupee(byslug[sl]["price"])}</span></span></a>'
        for i, (k, sl) in enumerate(SLIDES))
    dots = "".join(f'<button class="dot" type="button" data-i="{i}" aria-label="Show {e(byslug[sl]["name"])}"{" aria-current=true" if i == 0 else ""}><span>{e(byslug[sl]["name"].split(" Tray")[0].replace(" Floral",""))}</span></button>' for i, (k, sl) in enumerate(SLIDES))
    ribbon_items = ["Made in Sambhal since 2008", "Bulk orders from 25 pieces", "Your name or logo from 50 pieces", "Acacia pieces in any size", "Finished by hand", "Order on WhatsApp"]
    ribbon = "".join(f"<span>{e(t)}</span>" for t in ribbon_items * 2)
    dz = "".join(f'<a href="{e(wa("Hello Woodkari, I want the bulk price of: " + n + chr(10) + "Quantity: "))}"><div class="ph"><img src="{UP}img/{k}.webp" alt="{e(n)}, design picture" width="600" height="600" loading="lazy"><span class="tag">Design picture</span></div><b>{e(n)}</b><i>Ask the bulk price</i></a>' for k, n in DESIGNS)
    bulk_msg = "Hello Woodkari, I want a bulk order.\nPiece:\nQuantity:\nCity: "
    return head("Woodkari: wooden trays and boxes from Sambhal, in bulk and single pieces",
                "Acacia wood and resin trays and boxes from Sambhal, Uttar Pradesh, making since 2008. Bulk orders from 25 pieces, a name or logo by laser from 50, and single pieces on WhatsApp.",
                "", "fluted-front.jpg") + f"""<body>
{header('home')}
<main id="main">
<section class="hero"><div class="hgrid">
<div class="txt">
<h1 class="rise d1">Trays and boxes, made in Sambhal.</h1>
<p class="rise d2">Making since 2008. Most of our orders are bulk, from 25 pieces of a design. Single pieces too, on WhatsApp.</p>
<div class="row rise d3"><a class="btn wa" href="{e(wa(bulk_msg))}">{WA_ICON}Bulk order on WhatsApp</a><a class="btn line" href="#shop">Shop the pieces</a></div>
<div class="dots rise d4" role="group" aria-label="Pictures">{dots}</div>
</div>
<div class="show">{slides}</div>
</div></section>
<div class="ribbon" aria-hidden="true"><div class="track">{ribbon}</div></div>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Where they go</h2></div></div>
<div class="tiles">{tiles}</div>
</div></section>

<section class="sec" id="shop"><div class="wrap">
<div class="hdr rv"><div><h2>The pieces</h2><p>Acacia wood from our workshop, and resin trays made to order in Sambhal. Prices are for one piece; delivery is extra.</p></div></div>
<div class="chips" role="group" aria-label="Filter the pieces">{chips}</div>
<div class="grid">
{cards}
</div>
</div></section>

<section class="dark" id="bulk"><div class="wrap split rv">
<div class="fig"><span class="tag">Styled picture</span><img src="{UP}img/room-life.webp" alt="Acacia room tray with a kettle and two cups on a bedside table" width="1200" height="1200" loading="lazy"></div>
<div>
<h2>Bulk orders, from 25 pieces.</h2>
<p class="lead">Bulk is most of our work. Hotels, gifting companies, shops and importers can order any piece from 25 of a design, and the acacia pieces in any size.</p>
<ol class="steps">
<li><b>Send the piece and the number</b><span>On WhatsApp or by mail, with your city.</span></li>
<li><b>We send the price</b><span>A 50% advance starts the order.</span></li>
<li><b>Made and sent</b><span>About 10 to 15 days for 100 pieces. Delivery is at your cost, quoted before it leaves.</span></li>
</ol>
<div class="row"><a class="btn wa" href="{e(wa(bulk_msg))}">{WA_ICON}Ask for a bulk price</a><a class="btn line" href="bulk.html">Bulk orders in detail</a></div>
</div>
</div></section>

<section class="sec" id="engraving"><div class="wrap split rev rv">
<div class="fig"><span class="tag">Design picture</span><img src="{UP}img/d-engraved-600.webp" alt="Wooden serving board with a sample logo engraved, design picture" width="600" height="600" loading="lazy"></div>
<div>
<h2>Your name or logo, by laser.</h2>
<p class="lead">On 50 pieces or more of one design, we engrave a hotel name, a company logo or a couple's names: room trays for a hotel, boxes and boards for staff gifts or a wedding.</p>
<div class="row"><a class="btn wa" href="{e(wa('Hello Woodkari, I want my name or logo engraved.' + chr(10) + 'Piece:' + chr(10) + 'Quantity: '))}">{WA_ICON}Ask about engraving</a></div>
</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr rv"><div><h2>Made on order, in bulk</h2><p>More designs the karigars make when you ask. These are for bulk orders only; tell us the piece and the quantity on WhatsApp.</p></div></div>
<div class="dz">{dz}</div>
</div></section>

<section class="stone" id="workshop"><div class="wrap split rv">
<div>
<h2>The workshop</h2>
<p class="lead">Woodkari is a workshop in Sambhal, Uttar Pradesh, at work since 2008. Four karigars cut the wood on a CNC router, engrave by laser and finish every piece by hand. Our resin trays are made with other makers in Sambhal.</p>
</div>
<ul class="facts">
<li><b>Since</b><span>2008</span></li>
<li><b>Where</b><span>Sambhal, Uttar Pradesh</span></li>
<li><b>Karigars</b><span>Four</span></li>
<li><b>Work</b><span>CNC router, laser engraving, resin, hand finishing</span></li>
<li><b>Wood</b><span>Acacia</span></li>
</ul>
</div></section>

<section class="sec"><div class="wrap split">
<div><h2>Buying one piece</h2><p class="lead">Every piece with a price can be ordered on its own, on WhatsApp.</p></div>
<ol class="steps" style="margin-top:0">
<li><b>Message us on WhatsApp</b><span>Tap "Order on WhatsApp" on any piece and tell us your city and PIN code.</span></li>
<li><b>We confirm</b><span>We tell you the delivery charge and the day it will be sent.</span></li>
<li><b>We pack and send it</b><span>Once you agree, the piece goes out to you.</span></li>
</ol>
</div></section>

<section class="end"><div class="wrap">
<h2>Tell us what you need.</h2>
<p>The piece, the size and how many. We reply on WhatsApp.</p>
<div class="row"><a class="btn wa" href="{e(wa('Hello Woodkari, I have a question.'))}">{WA_ICON}Chat on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}">{MAIL}{EMAIL}</a></div>
</div></section>
</main>
{footer()}
<script type="application/ld+json">{ORG_LD}</script>
<script>{JS}</script>
</body></html>
"""


def page_product(p):
    if p.get("bulk_only"):
        msg = f"Hello Woodkari, I want the bulk price of: {p['name']}.\nQuantity:\nCity: "
        btn = "Ask the bulk price"
        stick_l = "Bulk only"
    else:
        msg = f"Hello Woodkari, I want to order: {p['name']} ({rupee(p['price'])}).\nMy city and PIN code: "
        btn = "Order on WhatsApp"
        stick_l = rupee(p["price"])
    figs = "".join(
        f'<figure><img src="{UP}img/{k}.webp" alt="{e(alt)}" width="1200" height="1200"{"" if i==0 else " loading=lazy"}><figcaption>{e(cap)}</figcaption></figure>'
        for i, (k, alt, cap) in enumerate(p["imgs"]))
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in p["facts"])
    offer = {"@type": "Offer", "priceCurrency": "INR", "availability": "https://schema.org/MadeToOrder"}
    if p.get("price"):
        offer["price"] = p["price"]
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p["name"],
                     "image": f"{SITE}/img/{p['imgs'][0][0]}.webp", "description": p["lede"],
                     "brand": {"@type": "Brand", "name": "Woodkari"}, "offers": offer})
    notes = ""
    if not p.get("bulk_only"):
        notes += '<p class="note">Delivery is extra. We tell you the amount before you pay.</p>'
    if p.get("mto"):
        notes += '<p class="note">Made to order. We tell you the making time on WhatsApp.</p>'
    more = "\n".join(card(q) for q in [x for x in PRODUCTS if x["slug"] != p["slug"]][:3])
    ogimg = p["imgs"][0][0] + (".jpg" if p["imgs"][0][0] in ("fluted-front", "room-front") else ".webp")
    bulk_l = "" if p.get("bulk_only") else '<a class="lnk more-l" href="bulk.html">Need 25 or more? Bulk orders ' + ARROW + '</a>'
    return head(f"{p['name']} | Woodkari, Sambhal", p["lede"], p["slug"] + ".html", ogimg) + f"""<body class="has-stick">
{header('shop')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="./#shop">All pieces</a> / {e(p['name'])}</p>
<div class="pd">
<div class="gal{" odd" if len(p["imgs"])%2 else ""}">{figs}</div>
<div class="buy">
<h1>{e(p['name'])}</h1>
{price_html(p)}
{notes}
<div class="row"><a class="btn wa wide" href="{e(wa(msg))}">{WA_ICON}{btn}</a></div>
<p class="lede">{e(p['lede'])}</p>
<p class="uses"><b>Good for:</b> {e(p['uses'])}</p>
<ul class="facts">{facts}</ul>
{bulk_l}
</div>
</div>
<section class="sec"><div class="hdr"><div><h2>More pieces</h2></div></div><div class="grid more3">
{more}
</div></section>
</div></main>
<div class="stick"><b>{e(stick_l)}</b><a class="btn wa" href="{e(wa(msg))}">{WA_ICON}{btn}</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def page_bulk():
    msg = "Hello Woodkari, I want a bulk price.\nCompany:\nPiece and quantity:\nCity: "
    return head("Bulk and hotel orders | Woodkari, Sambhal",
                "Wooden trays, boxes and resin pieces made in Sambhal from 25 pieces of a design: for hotels, gifting companies, shops and importers.",
                "bulk.html", "room-front.jpg") + f"""<body>
{header('bulk')}
<main id="main">
<section><div class="wrap bh">
<div>
<h1>Bulk orders, from 25 pieces.</h1>
<p>Bulk is most of our work. We have made these pieces in Sambhal since 2008. For hotels, gifting companies, shops and importers: tell us the piece and the number, and we send the price on WhatsApp.</p>
<div class="row"><a class="btn wa" href="{e(wa(msg))}">{WA_ICON}Ask on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}?subject=Bulk%20order">{MAIL}Email us</a></div>
</div>
<div class="fig"><span class="tag">Styled picture</span><img src="{UP}img/bulk-hero.webp" alt="Acacia room tray with two cups of tea on a wooden table" width="1200" height="744"></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="hdr"><div><h2>What we make in bulk</h2></div></div>
<div class="grid four">
<a class="p" href="room-tray.html"><div class="ph"><img src="{UP}img/room-front-600.webp" alt="Room tray on a wooden table with two cups of tea" width="600" height="600" loading="lazy"><span class="tag">Styled picture</span></div><h3>Room trays for hotels</h3><p class="sh">A hotel name by laser, from 50 pieces</p></a>
<a class="p" href="fluted-box-tray.html"><div class="ph"><img src="{UP}img/fluted-front-600.webp" alt="Fluted acacia box tray on a wooden table" width="600" height="600" loading="lazy"><span class="tag">Styled picture</span></div><h3>Box trays for gifting</h3><p class="sh">For hampers and staff gifts</p></a>
<a class="p" href="navy-ivory-floral-tray.html"><div class="ph"><img src="{UP}img/navy-front-600.webp" alt="Navy and ivory floral resin tray" width="600" height="600" loading="lazy"><span class="tag">Design picture</span></div><h3>Resin trays</h3><p class="sh">Made to order in Sambhal</p></a>
<a class="p" href="{e(wa("Hello Woodkari, I want the bulk price of engraved serving boards.\nCompany:\nQuantity: "))}"><div class="ph"><img src="{UP}img/d-engraved-600.webp" alt="Wooden serving board with a logo engraved, design picture" width="600" height="600" loading="lazy"><span class="tag">Design picture</span></div><h3>Engraved serving boards</h3><p class="sh">Your logo by laser, from 50</p></a>
</div>
</div></section>

<section class="stone"><div class="wrap split">
<div>
<h2>Terms</h2>
<ul class="facts" style="margin-top:24px">
<li><b>Minimum</b><span>25 pieces of one design</span></li>
<li><b>Size</b><span>Acacia pieces in any size</span></li>
<li><b>Name or logo</b><span>By laser, from 50 pieces of one design</span></li>
<li><b>Making time</b><span>About 10 to 15 days for 100 pieces</span></li>
<li><b>Payment</b><span>50% advance to start the order</span></li>
<li><b>Delivery</b><span>At the buyer's cost, quoted before dispatch</span></li>
</ul>
</div>
<div>
<h2>How it starts</h2>
<ol class="steps">
<li><b>Send the piece and the number</b><span>On WhatsApp or by mail, with your city.</span></li>
<li><b>We send the price</b><span>A 50% advance starts the order.</span></li>
<li><b>Made and sent</b><span>About 10 to 15 days for 100 pieces.</span></li>
</ol>
<div class="row"><a class="btn wa" href="{e(wa(msg))}">{WA_ICON}Ask for a bulk price</a></div>
</div>
</div></section>
</main>
{footer()}
</body></html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    w = lambda name, s: open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)
    css = CSS.strip() + "\n"
    if PREVIEW:
        css = css.replace("url(fonts/", "url(../fonts/")
    w("site.css", css)
    w("index.html", page_home())
    w("bulk.html", page_bulk())
    for p in PRODUCTS:
        w(p["slug"] + ".html", page_product(p))
    if not PREVIEW:
        urls = [""] + [p["slug"] + ".html" for p in PRODUCTS] + ["bulk.html"]
        w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"<url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
        w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("built", OUT, len(PRODUCTS) + 2, "pages")


main()
