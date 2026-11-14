#!/usr/bin/env python3
"""Make web copies of the made-to-order design pictures.
Usage: python3 build/mto_images.py                 -> main pictures (img/m-<name>.webp 1200 px + img/m-<name>-600.webp)
       python3 build/mto_images.py NAME-a NAME-b   -> extra angles, ONLY after Jarvis has checked them against the main picture
Source: agency-research/businesses/woodkari/photos/ai/real/<name>.png (Friday, WK-DESIGNS-3 and WK-ANGLES-41)."""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/home/user/agency-research/businesses/woodkari/photos/ai/real"
REF = "/home/user/agency-research/businesses/woodkari/photos/reference/owner_13nov"

def make(name):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGB")
    for size, suffix in ((1200, ""), (600, "-600")):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"m-{name}{suffix}.webp"), "WEBP", quality=78, method=6)

names = sys.argv[1:] or [os.path.splitext(f)[0] for f in sorted(os.listdir(REF)) if not f.endswith(".md")]
for n in names:
    make(n)
print(len(names), "pictures")
