#!/usr/bin/env python3
"""Make img/engraved-logo.webp (+ -600): our own logo shown as a laser engraving on the heart-handle serving board
(owner list 20 Nov, point 3: no "your logo" placeholder). A made-up picture: base = img/m-ow-08-b.webp (design OW-08, top view),
logo = build/logo_lockup.png (logo D), line under the name = EXPORTS as in the site header.
Usage: python3 build/engrave_logo.py [font.ttf for the EXPORTS line]"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SS = 3  # the mask is drawn 3x and scaled down, for clean edges

base = Image.open(os.path.join(ROOT, "img", "m-ow-08-b.webp")).convert("RGB")
W, H = base.size
lock = Image.open(os.path.join(ROOT, "build", "logo_lockup.png")).convert("RGBA")
a = np.asarray(lock).astype(np.float32) / 255
lum = a[..., :3].mean(-1)
alpha = a[..., 3]
# icon tile (left 380 px): the walnut square burns, the ivory W stays bare wood. wordmark (x 400+, y < 290): dark letters burn.
icon = Image.fromarray((np.where(lum[:, :380] < .6, alpha[:, :380], 0) * 255).astype(np.uint8))
word = Image.fromarray((np.where(lum[:290, 400:] < .5, alpha[:290, 400:], 0) * 255).astype(np.uint8))
icon = icon.crop(icon.getbbox()); word = word.crop(word.getbbox())

CX, TOP, LW = 600 * SS, 505 * SS, 400 * SS  # centre line of the board, top of the logo, width of the wordmark
m = Image.new("L", (W * SS, H * SS), 0)
iw = 150 * SS
ic = icon.resize((iw, round(iw * icon.height / icon.width)), Image.LANCZOS)
m.paste(ic, (CX - iw // 2, TOP))
wd = word.resize((LW, round(LW * word.height / word.width)), Image.LANCZOS)
y = TOP + ic.height + 34 * SS
m.paste(wd, (CX - LW // 2, y))
y += wd.height + 30 * SS
d = ImageDraw.Draw(m)
f = ImageFont.truetype(FONT, 30 * SS)
try: f.set_variation_by_axes([600])
except Exception: pass
txt, gap = "EXPORTS", 15 * SS
ws = [d.textlength(c, font=f) for c in txt]
x = CX - (sum(ws) + gap * (len(txt) - 1)) / 2
for c, w in zip(txt, ws):
    d.text((x, y), c, font=f, fill=255); x += w + gap
m = m.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(.55))

M = np.asarray(m).astype(np.float32) / 255
wood = np.asarray(base).astype(np.float32) / 255
rng = np.random.default_rng(20)
g = wood.mean(-1)
grain = g - np.asarray(Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255  # fine grain only
noise = np.asarray(Image.fromarray((rng.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))).astype(np.float32) / 255 - .5
scan = .5 + .5 * np.sin(np.arange(H) * np.pi / 1.5)[:, None]  # faint raster lines of the laser head, 3 px apart
depth = np.clip(.80 + grain * 4.5 + noise * .22 + (scan - .5) * .07, .5, 1.0) * M  # the burn follows the grain: soft bands take more
halo = np.asarray(m.filter(ImageFilter.GaussianBlur(3.2))).astype(np.float32) / 255
halo = np.clip(halo - M, 0, 1) * .16  # light scorch just outside the cut
burn = np.array([.36, .235, .15], np.float32)  # burnt wood: dark warm brown, the grain still shows through (multiply)
out = wood * (1 - depth[..., None] * (1 - burn)) * (1 - halo[..., None] * np.array([.5, .62, .72], np.float32))
# the cut sits a hair below the surface: a thin shadow under its top-left edge, a thin light on the far edge (light comes from top-left)
sh = np.clip(M - np.roll(np.roll(M, 1, 0), 1, 1), 0, 1)
hl = np.clip(np.roll(np.roll(M, 1, 0), 1, 1) - M, 0, 1)
out = out * (1 - .30 * sh[..., None]) + .05 * hl[..., None]
im = Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8))
for size, suffix in ((1200, ""), (600, "-600")):
    im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, "img", f"engraved-logo{suffix}.webp"), "WEBP", quality=84, method=6)
print("made img/engraved-logo.webp and -600")
