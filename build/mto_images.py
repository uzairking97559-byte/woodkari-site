#!/usr/bin/env python3
"""Make web copies of the made-to-order design pictures.
Usage: python3 build/mto_images.py                 -> main pictures (img/m-<name>.webp 1200 px + img/m-<name>-600.webp)
       python3 build/mto_images.py NAME-a NAME-b   -> extra angles, ONLY after Jarvis has checked them against the main picture
       python3 build/mto_images.py ow OW-01 OW-03  -> acacia catalogue items, pictures a-f (img/m-ow-01-a.webp 1200 px + img/m-ow-01-a-600.webp)
Source: agency-research/businesses/woodkari/photos/ai/real/<name>.png (Friday, WK-DESIGNS-3 and WK-ANGLES-41);
        agency-research/businesses/woodkari/photos/ai/catalogue/OW-xx-a.png ... -f.png for the acacia catalogue (a = main picture on white)."""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/user/agency-research/businesses/woodkari/photos/ai/real"
REF = "/home/user/agency-research/businesses/woodkari/photos/reference/owner_13nov"
CAT = "/home/user/agency-research/businesses/woodkari/photos/ai/catalogue"

def make(name):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    for size, suffix in ((1200, ""), (600, "-600")):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{name}{suffix}.webp"), "WEBP", quality=78, method=6)

def make_ow(code):
    for x in "abcdef":
        im = Image.open(os.path.join(CAT, f"{code}-{x}.png")).convert("RGB")
        for size, suffix in ((1200, ""), (600, "-600")):
            im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{code.lower()}-{x}{suffix}.webp"), "WEBP", quality=78, method=6)


if sys.argv[1:2] == ["ow"]:
    for c in sys.argv[2:]:
        make_ow(c)
    print(len(sys.argv[2:]) * 6, "pictures")
    sys.exit()
names = sys.argv[1:] or [os.path.splitext(f)[0] for f in sorted(os.listdir(REF)) if not f.endswith(".md")]
for n in names:
    make(n)
print(len(names), "pictures")
