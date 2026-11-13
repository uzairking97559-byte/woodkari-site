#!/usr/bin/env python3
"""Builds the Woodkari shop (static HTML) into an output folder.

  python3 build/build.py v2        -> preview at /v2/ (noindex)
  python3 build/build.py .         -> live site at the root

Edit PRODUCTS, WHATSAPP and prices here, then rebuild. No other tooling.
"""
import html, json, os, sys, urllib.parse

OUT = sys.argv[1] if len(sys.argv) > 1 else "v2"
PREVIEW = OUT != "."
SITE = "https://woodkariexports.com"
BASE = SITE + ("" if OUT == "." else "/" + OUT)

# WhatsApp number in international form without "+", e.g. "9198XXXXXXXX".
# Empty = the button opens WhatsApp and lets the buyer pick the chat (preview only).
WHATSAPP = ""
EMAIL = "sales@woodkariexports.com"

PRODUCTS = [
    dict(slug="fluted-box-tray", name="Fluted Box Tray", cat="wood", price=1299,
         short="Acacia wood, scalloped rim",
         lede="An open box tray in acacia wood. The sides are cut into upright flutes and the rim is scalloped, then the whole piece is polished to a warm walnut tone.",
         uses="Keys and wallet by the door, a dressing table, a desk, or a gift hamper.",
         facts=[("Wood", "Acacia"), ("Finish", "Walnut-tone polish, by hand"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Can be changed", "Size, polish, a name engraved by laser")],
         imgs=[("fluted-life", "Fluted box tray on an entryway table holding keys and sunglasses", "Styled picture"),
               ("fluted-real1", "Fluted box tray, plain photo from the front", "Our piece, plain photo"),
               ("fluted-real2", "Fluted box tray, plain photo from the side", "Our piece, plain photo"),
               ("fluted-real3", "Fluted box tray, plain photo from above", "Our piece, plain photo"),
               ("fluted-life2", "Fluted box tray on a coffee table with a candle", "Styled picture")]),
    dict(slug="room-tray", name="Room Tray", cat="wood", price=1799,
         short="Acacia wood, with a four-box caddy",
         lede="A solid acacia board with one large round dip, two small ones and two long slots, and a four-box caddy that stands beside it. Hotels use it as the tea tray in a guest room.",
         uses="Kettle and cups in a guest room, or watch, phone and keys on a bedside table.",
         facts=[("Wood", "Acacia"), ("Finish", "Walnut-tone polish, by hand"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Can be changed", "Size, polish, a hotel name or logo engraved by laser")],
         imgs=[("room-life", "Room tray on a hotel desk with a kettle and two cups", "Styled picture"),
               ("room-real1", "Room tray, plain photo from the front", "Our piece, plain photo"),
               ("room-real2", "Room tray, plain photo from the side", "Our piece, plain photo"),
               ("room-real3", "Room tray, plain photo of the caddy", "Our piece, plain photo"),
               ("room-life2", "Room tray on a bedside table with a wallet, phone and watch", "Styled picture")]),
    dict(slug="gold-flake-resin-tray", name="Gold-flake Resin Tray", cat="resin", price=1299, mto=True,
         short="Black resin, gold flakes, leaf handles",
         lede="Black marbled resin with gold flakes poured over a wooden core, with two gold-tone metal leaf handles.",
         uses="A serving tray for guests, or a centre piece on a coffee table.",
         facts=[("Top", "Resin, poured by hand"), ("Core", "MDF wood board"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Made to order", "Each pour comes out a little different")],
         imgs=[("gold", "Black and gold resin tray with leaf handles on a dark table", "Design picture, made to order")]),
    dict(slug="navy-ivory-floral-tray", name="Navy & Ivory Floral Tray", cat="resin", price=1499, mto=True,
         short="16 × 8 in, cut-out handles",
         lede="An ivory tray with a navy floral pattern under clear resin, and a handle cut into each side.",
         uses="Tea for two, or a tray for the dressing table.",
         facts=[("Size", "16 × 8 inches"), ("Top", "Pattern under clear resin"), ("Core", "MDF wood board"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh")],
         imgs=[("navy", "Ivory tray with a navy floral pattern on a round table", "Design picture, made to order")]),
    dict(slug="red-chevron-tray", name="Red Chevron Tray", cat="resin", price=3299, mto=True,
         short="Red and white zigzag, white frame",
         lede="A white-framed rectangular tray with a red and white chevron pattern under clear resin.",
         uses="Breakfast in bed, or a bright tray for the kitchen counter.",
         facts=[("Top", "Pattern under clear resin"), ("Core", "MDF wood board"),
                ("Made in", "Our workshop in Sambhal, Uttar Pradesh"),
                ("Can be changed", "Colour of the pattern")],
         imgs=[("chevron", "White-framed tray with a red and white chevron pattern", "Design picture, made to order")]),
    dict(slug="black-white-floral-tray-set", name="Black & White Floral Tray Set", cat="resin", price=7999, unit="set of 2", mto=True,
         short="One round, one rectangular",
         lede="A round tray and a rectangular tray with a black and white floral pattern, in the look of bone inlay, sealed under resin.",
         uses="A pair for the dining table or the living room.",
         facts=[("In the set", "1 round tray and 1 rectangular tray"), ("Top", "Pattern under clear resin"),
                ("Core", "MDF wood board"), ("Made in", "Our workshop in Sambhal, Uttar Pradesh")],
         imgs=[("bw", "Round and rectangular black and white floral trays on a marble table", "Design picture, made to order")]),
]

CATS = [("all", "Everything"), ("wood", "Solid wood"), ("resin", "Resin trays")]


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


WA_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4Z"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.800-2-1-1 .9c-1-.4-2.1-1.5-2.5-2.5l.9-1-1-2Z" fill="currentColor" stroke="none"/></svg>'

CSS = r"""
:root{--paper:#fbf7f0;--card:#fffdf9;--ink:#2a1a12;--soft:#6a574a;--line:#e7dccb;--wood:#8b4a2b;--indigo:#1f3a6e;--indigo-d:#162b54;--go:#0f7a5f;--go-d:#0b624c;--r:6px}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.55 Mukta,system-ui,-apple-system,"Segoe UI",sans-serif;overflow-x:hidden}
img{max-width:100%;height:auto;display:block}
a{color:var(--indigo)}
h1,h2,h3{font-family:"Rozha One",Georgia,serif;font-weight:400;line-height:1.12;margin:0;color:var(--ink);text-wrap:balance}
.wrap{max-width:1120px;margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px 12px;z-index:9}
:focus-visible{outline:3px solid var(--indigo);outline-offset:2px}

/* header */
.top{background:var(--indigo);color:#f4ecdc;font-size:14px;text-align:center;padding:7px 12px;letter-spacing:.2px}
.hd{position:sticky;top:0;z-index:5;background:var(--paper);border-bottom:1px solid var(--line)}
.hd .wrap{display:flex;align-items:center;justify-content:space-between;height:60px}
.mark{font-family:"Rozha One",Georgia,serif;font-size:27px;color:var(--ink);text-decoration:none;letter-spacing:.3px;line-height:1}
.mark small{display:block;font:500 10.5px Mukta,sans-serif;letter-spacing:3.2px;color:var(--wood);margin-top:3px}
.nav{display:flex;gap:4px}
.nav a{font-weight:500;font-size:15.5px;color:var(--ink);text-decoration:none;padding:12px 10px;border-radius:var(--r)}
.nav a:hover{color:var(--indigo)}
.nav a[aria-current]{color:var(--indigo);box-shadow:inset 0 -2px 0 var(--indigo)}

/* the scalloped edge, taken from the rim of the fluted box */
.scallop{height:11px;background:radial-gradient(circle at 11px 0,transparent 10.5px,var(--c,var(--indigo)) 11px) repeat-x;background-size:22px 11px}
.scallop.up{transform:scaleY(-1)}

/* hero */
.hero{position:relative}
.hero picture img{width:100%;height:min(118vw,560px);object-fit:cover}
.hero-txt{padding:26px 0 8px}
.hero h1{font-size:clamp(34px,8.6vw,60px);max-width:13em}
.hero p{margin:12px 0 0;color:var(--soft);font-size:18px;max-width:30em}
.deva{font-size:15px;color:var(--wood);font-weight:500;margin:0 0 10px;letter-spacing:.2px}
@media(min-width:900px){
 .hero{display:grid;grid-template-columns:1.05fr 1fr;align-items:center;max-width:1120px;margin:28px auto 0;padding:0 16px;gap:44px}
 .hero picture img{height:520px;border-radius:var(--r)}
 .hero-txt{padding:0}
 .hero-txt .wrap{padding:0}
}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:50px;padding:12px 22px;border-radius:var(--r);font:700 17px Mukta,sans-serif;text-decoration:none;border:0;cursor:pointer;transition:background .18s,transform .18s}
.btn:active{transform:translateY(1px)}
.btn.go{background:var(--go);color:#fff}.btn.go:hover{background:var(--go-d)}
.btn.ind{background:var(--indigo);color:#fff}.btn.ind:hover{background:var(--indigo-d)}
.btn.line{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1.5px var(--ink)}.btn.line:hover{background:#f1e9dc}
.btn.wide{width:100%}
.row{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}

/* section heads */
.sec{padding:44px 0 8px}
.sec h2{font-size:clamp(27px,6.4vw,38px)}
.sec .sub{color:var(--soft);margin:6px 0 0;max-width:34em}
.chips{display:flex;gap:8px;margin:18px 0 4px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;min-height:44px;padding:9px 16px;border-radius:999px;border:1.5px solid var(--line);background:var(--card);font:500 16px Mukta,sans-serif;color:var(--ink);cursor:pointer}
.chip[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}

/* product grid */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:22px 12px;margin-top:16px}
@media(min-width:760px){.grid{grid-template-columns:repeat(3,1fr);gap:34px 22px}}
.p{text-decoration:none;color:var(--ink);display:block}
.p .ph{position:relative;aspect-ratio:1/1;border-radius:var(--r);overflow:hidden;background:#efe6d6}
.p .ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
.p:hover .ph img{transform:scale(1.035)}
.p .mto{position:absolute;left:8px;top:8px;background:rgba(251,247,240,.94);color:var(--ink);font-size:12.5px;font-weight:500;padding:3px 8px;border-radius:3px}
.p h3{font:500 17px/1.25 Mukta,sans-serif;margin:10px 0 2px}
.p .sh{color:var(--soft);font-size:14.5px;line-height:1.3;margin:0}
.p .pr{font-weight:700;font-size:17px;margin:4px 0 0;font-variant-numeric:tabular-nums}
.p .pr span{font-weight:400;color:var(--soft);font-size:14px}
.p[hidden]{display:none}

/* how to order */
.steps{counter-reset:s;display:grid;gap:14px;margin:20px 0 0;padding:0;list-style:none}
@media(min-width:760px){.steps{grid-template-columns:repeat(3,1fr);gap:22px}}
.steps li{counter-increment:s;background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:16px 16px 16px 58px;position:relative}
.steps li::before{content:counter(s);position:absolute;left:16px;top:14px;font:400 30px/1 "Rozha One",serif;color:var(--wood)}
.steps b{display:block;font-weight:700}
.steps span{color:var(--soft);font-size:16px}

/* indigo band */
.band{background:var(--indigo);color:#f4ecdc;margin-top:48px}
.band .wrap{padding:38px 16px 44px}
.band h2{color:#fff;font-size:clamp(27px,6.4vw,38px)}
.band p{max-width:33em;margin:10px 0 0;color:#dfe5f2}
.band .btn.line{color:#fff;box-shadow:inset 0 0 0 1.5px #fff}.band .btn.line:hover{background:rgba(255,255,255,.1)}
.band .btn.ind{background:#fff;color:var(--indigo)}.band .btn.ind:hover{background:#f1ead9}

/* workshop */
.shop2{display:grid;gap:22px;margin-top:18px}
@media(min-width:760px){.shop2{grid-template-columns:1fr 1fr;gap:40px;align-items:start}}
.facts{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}
.facts li{display:flex;gap:14px;padding:11px 0;border-bottom:1px solid var(--line)}
.facts b{flex:0 0 7.2em;font-weight:500;color:var(--soft)}

/* product page */
.crumb{font-size:15px;color:var(--soft);padding:14px 0 10px}
.crumb a{color:var(--soft)}
.pd{display:grid;gap:20px}
@media(min-width:900px){.pd{grid-template-columns:1.1fr 1fr;gap:48px;align-items:start}.buy{position:sticky;top:84px}}
.gal{display:flex;gap:8px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -16px;padding:0 16px;scrollbar-width:none}
.gal::-webkit-scrollbar{display:none}
.gal figure{flex:0 0 88%;scroll-snap-align:center;margin:0;position:relative}
.gal figure:only-child{flex-basis:100%}
.gal img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:var(--r);background:#fff}
.gal figcaption{position:absolute;left:8px;bottom:8px;background:rgba(251,247,240,.94);font-size:12.5px;padding:3px 8px;border-radius:3px}
@media(min-width:900px){.gal{display:grid;grid-template-columns:1fr 1fr;margin:0;padding:0;overflow:visible}.gal figure:first-child,.gal figure:only-child{grid-column:1/-1}}
.buy h1{font-size:clamp(30px,7.4vw,42px)}
.buy .pr{font-size:25px;font-weight:700;margin:10px 0 0;font-variant-numeric:tabular-nums}
.buy .pr span{font-size:15px;font-weight:400;color:var(--soft)}
.buy .note{font-size:15px;color:var(--soft);margin:4px 0 0}
.buy .lede{margin:16px 0 0}
.buy .uses{margin:10px 0 0;color:var(--soft)}
.buy .facts{margin-top:20px}
.buy .bulk{display:block;margin-top:14px;font-weight:500}
.stick{position:fixed;left:0;right:0;bottom:0;z-index:6;background:var(--paper);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;align-items:center;gap:12px}
.stick b{font-size:19px;white-space:nowrap;font-variant-numeric:tabular-nums}
.stick .btn{flex:1;min-height:48px}
@media(min-width:900px){.stick{display:none}}
@media(max-width:899px){body.has-stick{padding-bottom:78px}.buy .btn.go.wide{display:none}}

/* footer */
.ft{margin-top:56px;background:#f1e9dc}
.ft .wrap{padding:30px 16px 34px;display:grid;gap:22px}
@media(min-width:760px){.ft .wrap{grid-template-columns:1.3fr 1fr 1fr}}
.ft h3{font:700 15px Mukta,sans-serif;letter-spacing:.4px;margin:0 0 6px}
.ft p,.ft a{font-size:16px;color:var(--ink);margin:0}
.ft a{display:block;padding:5px 0}
.ft .fine{grid-column:1/-1;border-top:1px solid var(--line);padding-top:14px;font-size:14px;color:var(--soft)}
.pv{background:#fff3c4;color:#4a3b00;text-align:center;font-size:14px;padding:6px}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

JS = r"""
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){
  document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x===c)});
  var k=c.dataset.cat;document.querySelectorAll('.p').forEach(function(p){p.hidden=!(k==='all'||p.dataset.cat===k)});
});});
"""


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
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}/img/{image}">
<meta name="theme-color" content="#1f3a6e">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mukta:wght@400;500;700&family=Rozha+One&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
</head>
"""


def header(cur):
    def a(href, label, key):
        c = ' aria-current="page"' if key == cur else ""
        return f'<a href="{href}"{c}>{label}</a>'
    pv = '<div class="pv">Preview. Not the live site yet.</div>' if PREVIEW else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
{pv}<div class="top">Made by hand in Sambhal, Uttar Pradesh</div>
<header class="hd"><div class="wrap">
<a class="mark" href="./" aria-label="Woodkari home">Woodkari<small>SAMBHAL</small></a>
<nav class="nav" aria-label="Main">{a('./#shop','Shop','shop')}{a('bulk.html','Bulk orders','bulk')}</nav>
</div></header>
"""


def footer():
    return f"""<footer class="ft"><div class="wrap">
<div><h3>Woodkari Exports</h3><p>A small workshop in Sambhal, Uttar Pradesh. Wooden trays, boxes and resin pieces, made to order.</p></div>
<div><h3>Shop</h3><a href="./#shop">All pieces</a><a href="bulk.html">Bulk and hotel orders</a><a href="woodkari-catalogue-2026.pdf">Catalogue (PDF)</a></div>
<div><h3>Talk to us</h3><a href="{wa('Hello Woodkari, I have a question.')}">WhatsApp</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<p class="fine">Pictures marked "Styled picture" or "Design picture" show the look of the piece; wood grain and resin differ a little on every piece. Plain photos are of our own pieces.</p>
</div></footer>
"""


def card(p):
    k, alt, _ = p["imgs"][0]
    unit = f' <span>/ {e(p["unit"])}</span>' if p.get("unit") else ""
    mto = '<span class="mto">Made to order</span>' if p.get("mto") else ""
    return f"""<a class="p" data-cat="{p['cat']}" href="{p['slug']}.html">
<div class="ph"><img src="img/{k}-600.webp" alt="{e(alt)}" width="600" height="600" loading="lazy">{mto}</div>
<h3>{e(p['name'])}</h3><p class="sh">{e(p['short'])}</p><p class="pr">{rupee(p['price'])}{unit}</p></a>"""


def page_home():
    chips = "".join(f'<button class="chip" type="button" data-cat="{k}" aria-pressed="{"true" if k=="all" else "false"}">{e(v)}</button>' for k, v in CATS)
    cards = "\n".join(card(p) for p in PRODUCTS)
    return head("Woodkari: wooden trays and boxes, made by hand in Sambhal",
                "Acacia wood trays, boxes and resin trays from a small workshop in Sambhal, Uttar Pradesh. Order on WhatsApp, pay by UPI.",
                "", "fluted-life.jpg") + f"""<body>
{header('home')}
<main id="main">
<section class="hero">
<picture><source media="(min-width:900px)" srcset="img/fluted-life.webp"><img src="img/hero-p.webp" alt="A fluted acacia box tray on an entryway table, holding keys and sunglasses" width="960" height="1200" fetchpriority="high"></picture>
<div class="hero-txt"><div class="wrap">
<p class="deva">वुड + कारीगरी = Woodkari</p>
<h1>Wooden trays and boxes, made by hand in Sambhal.</h1>
<p>Acacia wood, cut and polished in our own workshop. Order on WhatsApp and pay by UPI.</p>
<div class="row"><a class="btn ind" href="#shop">See the pieces</a><a class="btn line" href="bulk.html">Bulk orders</a></div>
</div></div>
</section>

<section class="sec" id="shop"><div class="wrap">
<h2>The pieces</h2>
<p class="sub">Six to start. More come as the karigars finish them.</p>
<div class="chips" role="group" aria-label="Filter">{chips}</div>
<div class="grid">
{cards}
</div>
</div></section>

<section class="sec"><div class="wrap">
<h2>How to order</h2>
<ol class="steps">
<li><b>Message us on WhatsApp</b><span>Tap "Order on WhatsApp" on any piece. Tell us your city and PIN code.</span></li>
<li><b>We confirm</b><span>We tell you the delivery charge and the day it will leave the workshop.</span></li>
<li><b>Pay by UPI</b><span>You pay only after you have agreed to both. Then we pack and send it.</span></li>
</ol>
</div></section>

<section class="band"><div class="scallop" style="--c:var(--paper)"></div><div class="wrap">
<h2>Need 25 pieces or more?</h2>
<p>Hotels, gifting companies, shops and importers get a separate price sheet. We can engrave your name or logo by laser and change the size and polish.</p>
<div class="row"><a class="btn ind" href="bulk.html">Bulk and hotel orders</a><a class="btn line" href="woodkari-catalogue-2026.pdf">Catalogue (PDF)</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>The workshop</h2>
<div class="shop2">
<p class="sub" style="margin:0;color:var(--ink)">Sambhal has made wooden and horn pieces for generations. Ours is a small workshop there with four karigars. The wood is cut on a router, shaped and sanded by hand, and polished by hand. Resin is poured one tray at a time.</p>
<ul class="facts">
<li><b>Where</b><span>Sambhal, Uttar Pradesh</span></li>
<li><b>Who</b><span>Four karigars</span></li>
<li><b>Work we do</b><span>Router cutting, laser engraving, resin, hand polish</span></li>
<li><b>Wood</b><span>Acacia and mango</span></li>
</ul>
</div>
</div></section>
</main>
{footer()}
<script>{JS}</script>
</body></html>
"""


def page_product(p):
    unit = f' <span>/ {e(p["unit"])}</span>' if p.get("unit") else ""
    msg = f"Hello Woodkari, I want to order: {p['name']} ({rupee(p['price'])}).\nMy city and PIN code: "
    figs = "".join(
        f'<figure><img src="img/{k}.webp" alt="{e(alt)}" width="1200" height="1200"{"" if i==0 else " loading=lazy"}><figcaption>{e(cap)}</figcaption></figure>'
        for i, (k, alt, cap) in enumerate(p["imgs"]))
    facts = "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in p["facts"])
    ld = json.dumps({"@context": "https://schema.org", "@type": "Product", "name": p["name"],
                     "image": f"{BASE}/img/{p['imgs'][0][0]}.webp", "description": p["lede"],
                     "brand": {"@type": "Brand", "name": "Woodkari"},
                     "offers": {"@type": "Offer", "priceCurrency": "INR", "price": p["price"],
                                "availability": "https://schema.org/MadeToOrder" if p.get("mto") else "https://schema.org/InStock"}})
    mto = '<p class="note">Made to order. We tell you the making time on WhatsApp.</p>' if p.get("mto") else ""
    ogimg = p["imgs"][0][0] + (".jpg" if p["imgs"][0][0] in ("fluted-life", "room-life") else ".webp")
    return head(f"{p['name']} | Woodkari, Sambhal", p["lede"], p["slug"] + ".html", ogimg) + f"""<body class="has-stick">
{header('shop')}
<main id="main"><div class="wrap">
<p class="crumb"><a href="./#shop">All pieces</a> / {e(p['name'])}</p>
<div class="pd">
<div class="gal">{figs}</div>
<div class="buy">
<h1>{e(p['name'])}</h1>
<p class="pr">{rupee(p['price'])}{unit}</p>
<p class="note">Delivery charge is extra. We tell you the amount before you pay.</p>
{mto}
<div class="row"><a class="btn go wide" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
<p class="lede">{e(p['lede'])}</p>
<p class="uses"><b>Good for:</b> {e(p['uses'])}</p>
<ul class="facts">{facts}</ul>
<a class="bulk" href="bulk.html">Need 25 or more? See bulk orders</a>
</div>
</div>
</div></main>
<div class="stick"><b>{rupee(p['price'])}</b><a class="btn go" href="{e(wa(msg))}">{WA_ICON}Order on WhatsApp</a></div>
{footer()}
<script type="application/ld+json">{ld}</script>
</body></html>
"""


def page_bulk():
    msg = "Hello Woodkari, I want the bulk price sheet.\nCompany:\nPieces and quantity: "
    return head("Bulk and hotel orders | Woodkari, Sambhal",
                "Wooden trays, boxes and resin pieces made to order from 25 pieces: hotels, gifting companies, shops and importers.",
                "bulk.html", "room-life.jpg") + f"""<body>
{header('bulk')}
<main id="main">
<section class="sec" style="padding-top:28px"><div class="wrap">
<h1 style="font-size:clamp(32px,8vw,52px);max-width:13em">Bulk orders, from 25 pieces.</h1>
<p class="sub" style="font-size:18px">For hotels, gifting companies, shops and importers. Tell us the piece and the number, and we send the price sheet.</p>
<div class="row"><a class="btn go" href="{e(wa(msg))}">{WA_ICON}Ask on WhatsApp</a><a class="btn line" href="mailto:{EMAIL}?subject=Bulk%20price%20sheet">Email us</a><a class="btn line" href="woodkari-catalogue-2026.pdf">Catalogue (PDF)</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>What we make in bulk</h2>
<div class="grid">
<a class="p" href="room-tray.html"><div class="ph"><img src="img/room-life-600.webp" alt="Room tray on a hotel desk with a kettle and cups" width="600" height="600" loading="lazy"></div><h3>Room trays for hotels</h3><p class="sh">With your hotel name engraved</p></a>
<a class="p" href="fluted-box-tray.html"><div class="ph"><img src="img/fluted-studio-600.webp" alt="Fluted acacia box tray" width="600" height="600" loading="lazy"></div><h3>Box trays for gifting</h3><p class="sh">For hampers and staff gifts</p></a>
<a class="p" href="navy-ivory-floral-tray.html"><div class="ph"><img src="img/navy-600.webp" alt="Navy and ivory floral resin tray" width="600" height="600" loading="lazy"></div><h3>Resin trays</h3><p class="sh">Your colours and pattern</p></a>
</div>
</div></section>

<section class="sec"><div class="wrap">
<h2>Terms</h2>
<ul class="facts" style="margin-top:18px;max-width:640px">
<li><b>Minimum</b><span>25 pieces of one design</span></li>
<li><b>Making time</b><span>About 15 to 20 days for 100 pieces</span></li>
<li><b>Payment</b><span>50% advance, the rest before dispatch</span></li>
<li><b>Delivery</b><span>Courier or transport at the buyer's cost, quoted before dispatch</span></li>
<li><b>Custom work</b><span>Size, polish, colour, name or logo by laser</span></li>
<li><b>Wood</b><span>Acacia and mango, kiln-dried</span></li>
</ul>
</div></section>
</main>
{footer()}
</body></html>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    w = lambda name, s: open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)
    w("site.css", CSS.strip() + "\n")
    w("index.html", page_home())
    w("bulk.html", page_bulk())
    for p in PRODUCTS:
        w(p["slug"] + ".html", page_product(p))
    print("built", OUT, len(PRODUCTS) + 2, "pages")


main()
