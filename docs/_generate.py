"""One-shot generator for the slide images embedded in README.md.

Run once: `py -3.13 docs/_generate.py`
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(__file__)

# Mom-friendly palette
BG_TOP     = (254, 246, 255)
BG_BOTTOM  = (233, 240, 255)
INK        = (45, 45, 68)
INK_SOFT   = (110, 110, 140)
PINK       = (255, 126, 182)
PINK_DEEP  = (255, 95, 163)
LAVENDER   = (199, 175, 255)
MINT       = (148, 222, 191)
SUN        = (255, 209, 102)
WHITE      = (255, 255, 255)


# Font helpers ------------------------------------------------------------
def _font(size: int, bold: bool = False):
    candidates_bold = [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/seguibl.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    candidates_reg = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    candidates = candidates_bold if bold else candidates_reg
    for p in candidates:
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def _emoji_font(size: int):
    for p in ("C:/Windows/Fonts/seguiemj.ttf", "C:/Windows/Fonts/seguisym.ttf"):
        if os.path.isfile(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
    return _font(size, bold=True)


def _vertical_gradient(w: int, h: int, top, bot) -> Image.Image:
    img = Image.new("RGB", (w, h), top)
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        d.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def _rounded(d: ImageDraw.ImageDraw, xy, radius: int, **kw):
    d.rounded_rectangle(xy, radius=radius, **kw)


def _text_w(d: ImageDraw.ImageDraw, text: str, font) -> int:
    bbox = d.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


# 1. Hero banner ----------------------------------------------------------
def make_hero():
    W, H = 1600, 600
    img = _vertical_gradient(W, H, BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    # soft blobs
    for cx, cy, rr, col in [
        (1350, 120, 220, (255, 233, 243, 0)),
        (200, 480, 260, (227, 215, 255, 0)),
    ]:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.ellipse((cx - rr, cy - rr, cx + rr, cy + rr),
                   fill=(col[0], col[1], col[2], 200))
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
        d = ImageDraw.Draw(img)

    title_font = _font(110, bold=True)
    sub_font   = _font(36)
    chip_font  = _font(26, bold=True)
    emoji_font = _emoji_font(140)

    # Baby emoji
    d.text((110, 130), "👶", font=emoji_font, embedded_color=True)

    # Title
    d.text((280, 180), "Baby Sign Helper", font=title_font, fill=INK)
    d.text((282, 330),
           "A friendly web app that reads baby sign language in real time.",
           font=sub_font, fill=INK_SOFT)

    # Pills (tech stack chips)
    chips = [("Vue 3", LAVENDER), ("Flask", MINT), ("PyTorch", PINK), ("MediaPipe", SUN)]
    x = 285
    y = 420
    for text, col in chips:
        w = _text_w(d, text, chip_font) + 44
        _rounded(d, (x, y, x + w, y + 56), radius=28, fill=col)
        tw = _text_w(d, text, chip_font)
        d.text((x + (w - tw) // 2, y + 12), text, font=chip_font, fill=WHITE)
        x += w + 14

    img.save(os.path.join(OUT, "hero.png"), optimize=True)
    print("wrote hero.png")


# 2. Architecture diagram -------------------------------------------------
def make_architecture():
    W, H = 1600, 700
    img = _vertical_gradient(W, H, BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    title = _font(40, bold=True)
    sub   = _font(22)
    label = _font(26, bold=True)
    body  = _font(20)

    d.text((60, 36), "How it works", font=title, fill=INK)
    d.text((60, 90),
           "Every 200 ms the browser snaps a frame and the backend returns the predicted sign.",
           font=sub, fill=INK_SOFT)

    # Five blocks in a row
    blocks = [
        ("Browser\nwebcam",    "JPEG frame\nevery 200 ms",         LAVENDER),
        ("Flask\n/api/predict","Receives frame,\nreturns JSON",    MINT),
        ("MediaPipe\nHand",    "Find hand bbox\n(21 landmarks)",   SUN),
        ("Crop + ResNet-18",   "224 px crop →\ncustom classifier", PINK),
        ("Big label\n+ voice", "Confidence,\nemoji, history",      LAVENDER),
    ]
    margin = 60
    gap = 30
    block_w = (W - 2 * margin - gap * (len(blocks) - 1)) // len(blocks)
    block_h = 280
    block_y = 220

    for i, (heading, desc, col) in enumerate(blocks):
        bx = margin + i * (block_w + gap)
        # shadow
        _rounded(d, (bx + 4, block_y + 6, bx + block_w + 4, block_y + block_h + 6),
                 radius=22, fill=(0, 0, 0, 0), outline=None)
        # card
        _rounded(d, (bx, block_y, bx + block_w, block_y + block_h),
                 radius=22, fill=WHITE, outline=col, width=4)
        # heading band
        _rounded(d, (bx, block_y, bx + block_w, block_y + 84),
                 radius=22, fill=col)
        # cover bottom of band so corners stay rounded only on top
        d.rectangle((bx, block_y + 60, bx + block_w, block_y + 84), fill=col)
        # heading text
        lines = heading.split("\n")
        ty = block_y + 12
        for ln in lines:
            tw = _text_w(d, ln, label)
            d.text((bx + (block_w - tw) // 2, ty), ln, font=label, fill=WHITE)
            ty += 30
        # description
        ty = block_y + 110
        for ln in desc.split("\n"):
            tw = _text_w(d, ln, body)
            d.text((bx + (block_w - tw) // 2, ty), ln, font=body, fill=INK)
            ty += 28

        # arrow to next
        if i < len(blocks) - 1:
            ax = bx + block_w + 4
            ay = block_y + block_h // 2
            d.polygon([(ax, ay - 10), (ax + gap - 6, ay), (ax, ay + 10)],
                      fill=INK_SOFT)

    # Footer caption
    cap = _font(20)
    d.text((60, 540),
           "All inference runs locally on your machine — frames never leave your computer.",
           font=cap, fill=INK_SOFT)

    img.save(os.path.join(OUT, "architecture.png"), optimize=True)
    print("wrote architecture.png")


# 3. Features slide -------------------------------------------------------
def make_features():
    W, H = 1600, 800
    img = _vertical_gradient(W, H, BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    title = _font(46, bold=True)
    sub   = _font(24)
    head  = _font(30, bold=True)
    body  = _font(22)
    big_e = _emoji_font(72)

    d.text((60, 40), "What you get", font=title, fill=INK)
    d.text((60, 100),
           "Tuned for moms — big text, friendly icons, no setup beyond `npm` and `python`.",
           font=sub, fill=INK_SOFT)

    cards = [
        ("📷", "Live camera",
         "Mirror-flipped preview\nworks on phone or laptop.", LAVENDER),
        ("🤖", "On-device AI",
         "ResNet-18 + MediaPipe\nrun locally, no cloud.", MINT),
        ("🔊", "Spoken word",
         "Reads the detected sign\naloud through the browser.", PINK),
        ("📝", "Recent signs",
         "Last 5 detected signs\nwith live timestamps.", SUN),
        ("🎯", "Smart confidence",
         "Green / yellow / grey bar\nhides noisy predictions.", LAVENDER),
        ("📱", "Mobile-first UI",
         "Big tap targets, soft\npastel theme, large fonts.", MINT),
    ]
    cols, rows = 3, 2
    gx, gy = 60, 200
    cw = (W - 2 * gx - 40 * (cols - 1)) // cols
    ch = 240

    for i, (emoji, h, txt, col) in enumerate(cards):
        c, r = i % cols, i // cols
        bx = gx + c * (cw + 40)
        by = gy + r * (ch + 40)
        _rounded(d, (bx, by, bx + cw, by + ch), radius=22,
                 fill=WHITE, outline=col, width=3)
        _rounded(d, (bx, by, bx + 12, by + ch), radius=22, fill=col)
        d.text((bx + 32, by + 24), emoji, font=big_e, embedded_color=True)
        d.text((bx + 32, by + 118), h, font=head, fill=INK)
        ty = by + 162
        for ln in txt.split("\n"):
            d.text((bx + 32, ty), ln, font=body, fill=INK_SOFT)
            ty += 28

    img.save(os.path.join(OUT, "features.png"), optimize=True)
    print("wrote features.png")


# 4. Signs grid -----------------------------------------------------------
def make_signs_grid():
    W, H = 1600, 720
    img = _vertical_gradient(W, H, BG_TOP, BG_BOTTOM)
    d = ImageDraw.Draw(img)

    title = _font(46, bold=True)
    sub   = _font(24)
    name  = _font(28, bold=True)
    big_e = _emoji_font(96)

    d.text((60, 40), "12 signs the app understands", font=title, fill=INK)
    d.text((60, 100),
           "Trained on the BABY-SIGN-LANGUAGE-RECOGNITION dataset (Sapienza University of Rome).",
           font=sub, fill=INK_SOFT)

    signs = [
        ("🍼", "Milk"), ("🍽️", "Eat"), ("🥤", "Drink"), ("⬇️", "Down"),
        ("👩", "Mom"), ("🙋", "Mine"), ("🚽", "Potty"), ("😢", "Sorry"),
        ("❤️", "I love you"), ("😠", "Mad / Grumpy"), ("😤", "Frustrated"), ("🤷", "Don't know"),
    ]
    palette = [LAVENDER, MINT, PINK, SUN]
    cols = 6
    rows = 2
    gx, gy = 60, 200
    cw = (W - 2 * gx - 24 * (cols - 1)) // cols
    ch = 220

    for i, (emoji, label) in enumerate(signs):
        c, r = i % cols, i // cols
        bx = gx + c * (cw + 24)
        by = gy + r * (ch + 30)
        col = palette[i % len(palette)]
        _rounded(d, (bx, by, bx + cw, by + ch), radius=20,
                 fill=WHITE, outline=col, width=3)
        d.text((bx + cw // 2 - 48, by + 20), emoji, font=big_e, embedded_color=True)
        tw = _text_w(d, label, name)
        d.text((bx + (cw - tw) // 2, by + ch - 52), label, font=name, fill=INK)

    img.save(os.path.join(OUT, "signs-grid.png"), optimize=True)
    print("wrote signs-grid.png")


if __name__ == "__main__":
    make_hero()
    make_architecture()
    make_features()
    make_signs_grid()
    print("\nDone. Generated:")
    for f in ("hero.png", "architecture.png", "features.png", "signs-grid.png"):
        p = os.path.join(OUT, f)
        size_kb = os.path.getsize(p) / 1024
        print(f"  docs/{f}  ({size_kb:.0f} KB)")
