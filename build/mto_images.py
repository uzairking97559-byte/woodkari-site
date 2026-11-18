#!/usr/bin/env python3
"""Make web copies of the made-to-order design pictures.
Usage: python3 build/mto_images.py                 -> main pictures (img/m-<name>.webp 1200 px + img/m-<name>-600.webp)
       python3 build/mto_images.py NAME-a NAME-b   -> extra angles, ONLY after Jarvis has checked them against the main picture
       python3 build/mto_images.py site OW-43 NAME  -> one real photo from photos/site (OW-43-a.jpg), made square (img/m-NAME.webp 1200 px + -600)
       python3 build/mto_images.py ow OW-01 OW-03  -> acacia catalogue items, pictures a-f (img/m-ow-01-a.webp 1200 px + img/m-ow-01-a-600.webp)
Source: agency-research/businesses/woodkari/photos/ai/real/<name>.png (Friday, WK-DESIGNS-3 and WK-ANGLES-41);
        agency-research/businesses/woodkari/photos/ai/catalogue/OW-xx-a.png ... -f.png for the acacia catalogue (a = main picture on white)."""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/user/agency-research/businesses/woodkari/photos/ai/real"
REF = "/home/user/agency-research/businesses/woodkari/photos/reference/owner_13nov"
INLAY = "/home/user/agency-research/businesses/woodkari/photos/ai/inlay"
CAT = "/home/user/agency-research/businesses/woodkari/photos/ai/catalogue"
SITE_PHOTOS = "/home/user/agency-research/businesses/woodkari/photos/site"

def make(name):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    for size, suffix in ((1200, ""), (600, "-600")):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{name}{suffix}.webp"), "WEBP", quality=78, method=6)

def make_ow(code):
    for x in "abcdef":
        im = Image.open(os.path.join(CAT, f"{code}-{x}.png")).convert("RGB")
        for size, suffix in ((1200, ""), (600, "-600")):
            im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{code.lower()}-{x}{suffix}.webp"), "WEBP", quality=78, method=6)


def make_site(code, name):
    """a real (non-square) photo OW-xx-a.jpg from photos/site -> square 1200/600 webp (photo centred on a blurred copy of itself, nothing cropped)"""
    from PIL import ImageFilter
    im = Image.open(os.path.join(SITE_PHOTOS, f"{code}-a.jpg")).convert("RGB")
    for size, suffix in ((1200, ""), (600, "-600")):
        bg = im.resize((size, size), Image.LANCZOS).filter(ImageFilter.GaussianBlur(size // 25))
        w, h = im.size
        k = size / max(w, h)
        fg = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
        bg.paste(fg, ((size - fg.width) // 2, (size - fg.height) // 2))
        bg.save(os.path.join(ROOT, "img", f"m-{name}{suffix}.webp"), "WEBP", quality=78, method=6)


if sys.argv[1:2] == ["site"]:  # python3 build/mto_images.py site OW-43 bone-inlay-coffee-table-43
    make_site(sys.argv[2], sys.argv[3])
    print(2, "pictures")
    sys.exit()
def make_inlay(code, name):
    """made pictures photos/ai/inlay/<code>-a..f.png: -a = main (img/m-<name>.webp), b..f = gallery (img/m-<name>-b.webp ...), each 1200 + -600"""
    n = 0
    for x in "abcdef":
        if code == "OW-42" and x == "a":  # -a shows the cube balanced on a corner: skipped; -e (flat cube) is the main picture
            continue
        p = os.path.join(INLAY, f"{code}-{x}.png")
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB")
        for size, suffix in ((1200, ""), (600, "-600")):
            tag = "" if x == ("e" if code == "OW-42" else "a") else "-" + x
            if code == "OW-42" and x == "e":
                for old in ("-a", "-e"):
                    for sfx in ("", "-600"):
                        q = os.path.join(ROOT, "img", f"m-{name}{old}{sfx}.webp")
                        if os.path.exists(q): os.remove(q)
            im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{name}{tag}{suffix}.webp"), "WEBP", quality=78, method=6)
        n += 1
    return n


if sys.argv[1:2] == ["inlay"]:  # python3 build/mto_images.py inlay OW-38 bone-inlay-coffee-table-38
    print(make_inlay(sys.argv[2], sys.argv[3]), "pictures")
    sys.exit()
if sys.argv[1:2] == ["ow"]:
    for c in sys.argv[2:]:
        make_ow(c)
    print(len(sys.argv[2:]) * 6, "pictures")
    sys.exit()
names = sys.argv[1:] or [os.path.splitext(f)[0] for f in sorted(os.listdir(REF)) if not f.endswith(".md")]
for n in names:
    make(n)
print(len(names), "pictures")
