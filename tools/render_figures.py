"""Renders the README figures in assets/: cover.png, demo.gif, before-after.png.

usage:
  python tools/record_terminal.py <workdir> frames.pkl      # real run of Kaynak_Kodlar/main.py
  python tools/render_figures.py frames.pkl
Needs Pillow. Fonts (OFL) in tools/fonts/: Red Hat Display and Red Hat Mono. Emoji use Windows' Segoe UI Emoji
(C:/Windows/Fonts/seguiemj.ttf), the same glyphs Windows Terminal shows; elsewhere they are left out.
"""
import os, pickle, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "tools", "fonts")
OUT = os.path.join(ROOT, "assets")
EMOJI_FONT = "C:/Windows/Fonts/seguiemj.ttf"

# Folder yellow from the Windows folder icon the tool fills, on a paper-white desk; Windows Terminal for the CLI.
PAPER, INK, SUB, LINE = "#F7F4EE", "#1F2328", "#57606A", "#E4DED2"
FOLDER, FOLDER_DK, FOLDER_LT = "#F2B33D", "#D9921A", "#FCE4A8"
GREEN, BLUE = "#1A7F37", "#0969DA"
TERM_BG, TERM_FG, TERM_BAR = (12, 12, 12), (204, 204, 204), (32, 32, 32)

def font(name, size, weight):
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    f.set_variation_by_axes([weight])
    return f

DISPLAY = lambda s: font("RedHatDisplay.ttf", s, 800)
SEMI = lambda s: font("RedHatDisplay.ttf", s, 600)
BODY = lambda s: font("RedHatDisplay.ttf", s, 450)
MONO = lambda s: font("RedHatMono.ttf", s, 450)
MONO_B = lambda s: font("RedHatMono.ttf", s, 650)

def emoji_font(size):
    return ImageFont.truetype(EMOJI_FONT, size) if os.path.exists(EMOJI_FONT) else None

def is_emoji(ch):
    return ord(ch[0]) >= 0x2600 and ch not in "→─"

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]

def glow(im, xy, r, rgb, alpha):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=rgb + (alpha,))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r // 2)))

def shadow(im, box, r, offset=14, blur=24, alpha=70):
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(layer).rounded_rectangle([x0, y0 + offset, x1, y1 + offset], r, fill=(60, 45, 20, alpha))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))

def render_screen(frame, cols, rows, cw=11, ch=22, first=0, last=None):
    rows_data = frame["rows"][first:last]
    im = Image.new("RGB", (cols * cw, len(rows_data) * ch), TERM_BG)
    d = ImageDraw.Draw(im)
    f, ef = MONO(18), emoji_font(int(ch * 0.72))
    for y, row in enumerate(rows_data):
        for x, (char, fg, bg, bold) in enumerate(row):
            if not char.strip():
                continue
            if char == "→":  # Red Hat Mono has no arrow glyph: draw it
                ay = y * ch + ch // 2 + 1
                d.line([(x * cw + 1, ay), (x * cw + cw - 2, ay)], fill=TERM_FG, width=2)
                d.polygon([(x * cw + cw, ay), (x * cw + cw - 6, ay - 4), (x * cw + cw - 6, ay + 4)], fill=TERM_FG)
            elif is_emoji(char):
                if ef:
                    d.text((x * cw, y * ch + 2), char, font=ef, embedded_color=True)
            else:
                d.text((x * cw, y * ch + 1), char, font=f, fill=TERM_FG)
    return im

def terminal(im, xy, content, title="Smart File Organizer"):
    x0, y0 = xy
    w, h = content.width + 4, content.height + 46
    shadow(im, (x0, y0, x0 + w, y0 + h), 10, alpha=110)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 10, fill=TERM_BAR, outline=(60, 60, 60), width=2)
    d.rounded_rectangle([x0 + 10, y0 + 8, x0 + 300, y0 + 44], 8, fill=TERM_BG)
    d.text((x0 + 26, y0 + 15), title, font=MONO(17), fill=TERM_FG)
    bx, by = x0 + w - 118, y0 + 26  # minimise, maximise, close, drawn (the font lacks the symbols)
    d.line([(bx, by), (bx + 12, by)], fill=(170, 170, 170), width=2)
    d.rectangle([bx + 34, by - 6, bx + 46, by + 6], outline=(170, 170, 170), width=2)
    d.line([(bx + 70, by - 6), (bx + 82, by + 6)], fill=(170, 170, 170), width=2)
    d.line([(bx + 70, by + 6), (bx + 82, by - 6)], fill=(170, 170, 170), width=2)
    im.paste(content, (x0 + 2, y0 + 44))

def folder_icon(d, x, y, s, body=FOLDER, tab=FOLDER_DK):
    d.rounded_rectangle([x, y, x + s * 0.45, y + s * 0.3], s * 0.06, fill=tab)
    d.rounded_rectangle([x, y + s * 0.14, x + s, y + s * 0.78], s * 0.08, fill=body)

def file_icon(d, x, y, s):
    d.rounded_rectangle([x + s * 0.18, y, x + s * 0.82, y + s * 0.8], s * 0.08, fill="#FFFFFF", outline="#B8B0A2", width=2)
    for k in range(3):
        d.line([(x + s * 0.3, y + s * (0.25 + k * 0.15)), (x + s * 0.7, y + s * (0.25 + k * 0.15))], fill="#C9C1B3", width=2)

def chip(d, xy, text, f, fill, color, pad=(16, 8)):
    x, y = xy
    w = d.textlength(text, font=f)
    h = f.size + 2 * pad[1]
    d.rounded_rectangle([x, y, x + w + 2 * pad[0], y + h], 9, fill=fill)
    d.text((x + pad[0], y + pad[1] - 2), text, font=f, fill=color)
    return x + w + 2 * pad[0]

def cover(rec):
    W, H = 1800, 1000
    im = Image.new("RGBA", (W, H), PAPER)
    glow(im, (1500, 160), 420, (252, 228, 168), 170)
    glow(im, (950, 900), 360, (242, 179, 61), 60)
    d = ImageDraw.Draw(im)
    x, nx = 100, 100
    for t in ["Python", "Windows", "standard library"]:
        nx = chip(d, (nx, 120), t, SEMI(19), "#FFFFFF", INK) + 10
    folder_icon(d, x, 190, 86)
    d.text((x + 106, 178), "Smart File", font=DISPLAY(88), fill=INK)
    d.text((x - 4, 284), "Organizer", font=DISPLAY(88), fill=FOLDER_DK)
    d.text((x, 396), "Akıllı Dosya Düzenleyici", font=SEMI(32), fill=SUB)
    y = 462
    for line in wrap(d, "Point it at a messy folder like Downloads. It shows where every file will go, "
                        "asks once, then sorts them into folders by type without overwriting anything.", BODY(25), 600):
        d.text((x, y), line, font=BODY(25), fill=INK); y += 38
    d.text((x, y + 20), "Hüseyin Baran Işık", font=MONO(18), fill=SUB)

    last = rec["frames"][-1]
    shot = render_screen(last, rec["cols"], rec["rows"], cw=10, ch=20)
    terminal(im, (W - 100 - shot.width - 4, 120), shot)

    # card under the text: the folder after the run
    after = rec["after"]
    cx0, cy0, cw_, chh = x, y + 70, 400, 60 + 34 * len([a for a in after if a[1]])
    shadow(im, (cx0, cy0, cx0 + cw_, cy0 + chh), 16)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([cx0, cy0, cx0 + cw_, cy0 + chh], 16, fill="#FFFFFF", outline=LINE, width=2)
    d.text((cx0 + 22, cy0 + 16), "Downloads, afterwards", font=SEMI(21), fill=INK)
    yy = cy0 + 56
    for name, is_dir, kids in after:
        if not is_dir:
            continue
        folder_icon(d, cx0 + 22, yy + 2, 24)
        d.text((cx0 + 58, yy), name, font=MONO_B(18), fill=INK)
        n = f"{len(kids)} file{'s' if len(kids) != 1 else ''}"
        d.text((cx0 + cw_ - 22 - d.textlength(n, font=MONO(16)), yy + 2), n, font=MONO(16), fill=SUB)
        yy += 34
    return im.convert("RGB")

def demo(rec):
    cols, frames = rec["cols"], rec["frames"]
    cw, ch = 10, 21
    tw, th = cols * cw + 4, rec["rows"] * ch + 46
    W, H = tw + 100, th + 130
    base = Image.new("RGBA", (W, H), PAPER)  # flat: soft gradients band in a GIF palette
    d = ImageDraw.Draw(base)
    nx = chip(d, (50, 32), "Fig. 2", MONO_B(17), FOLDER, INK)
    d.text((nx + 16, 32), "Real run on a sample Downloads folder", font=SEMI(26), fill=INK)
    out, durs = [], []
    for i, fr in enumerate(frames):
        img = base.copy()
        terminal(img, (50, 88), render_screen(fr, cols, rec["rows"], cw=cw, ch=ch))
        out.append(img.convert("RGB").quantize(colors=200, method=Image.Quantize.FASTOCTREE))
        nxt = frames[i + 1]["t"] if i + 1 < len(frames) else fr["t"]
        durs.append(int(max(60, min(2500, (nxt - fr["t"] + fr["hold"]) * 1000))))
    out[0].save(os.path.join(OUT, "demo.gif"), save_all=True, append_images=out[1:], duration=durs, loop=0, optimize=True)

def before_after(rec):
    """Fig. 3: the real folder listing before and after the run."""
    def panel(im, x0, y0, w, title, items, expand):
        rows = sum(1 + (len(k) if expand and d_ else 0) for _, d_, k in items)
        h = 70 + rows * 32
        shadow(im, (x0, y0, x0 + w, y0 + h), 14)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 14, fill="#FFFFFF", outline=LINE, width=2)
        d.text((x0 + 24, y0 + 18), title, font=SEMI(24), fill=INK)
        y = y0 + 64
        for name, is_dir, kids in items:
            (folder_icon if is_dir else file_icon)(d, x0 + 24, y + 2, 22)
            d.text((x0 + 58, y), name + ("/" if is_dir else ""), font=MONO_B(18) if is_dir else MONO(18), fill=INK)
            y += 32
            if is_dir and expand:
                for k in kids:
                    file_icon(d, x0 + 58, y + 2, 20)
                    color = BLUE if k == "rapor_1.pdf" else SUB
                    d.text((x0 + 88, y), k, font=MONO(17), fill=color)
                    y += 32
        return h
    W = 1500
    im = Image.new("RGBA", (W, 1100), PAPER)  # cropped to the content below
    d = ImageDraw.Draw(im)
    nx = chip(d, (70, 40), "Fig. 3", MONO_B(17), FOLDER, INK)
    d.text((nx + 16, 40), "The same folder before and after", font=SEMI(28), fill=INK)
    h1 = panel(im, 70, 110, 560, "Downloads, before", rec["before"], expand=True)
    h2 = panel(im, 720, 110, 710, "Downloads, after", rec["after"], expand=True)
    d = ImageDraw.Draw(im)
    d.line([(645, 300), (700, 300)], fill=FOLDER_DK, width=5)
    d.polygon([(712, 300), (696, 290), (696, 310)], fill=FOLDER_DK)
    note_y = 110 + max(h1, h2) + 26
    d.text((70, note_y), "Blue: the second rapor.pdf became rapor_1.pdf because Belgeler/ already had one. "
                         "Eski Projeler/ is a folder, so it was left alone.", font=BODY(21), fill=SUB)
    return im.crop((0, 0, W, note_y + 60)).convert("RGB")

if __name__ == "__main__":
    rec = pickle.load(open(sys.argv[1], "rb"))
    cover(rec).save(os.path.join(OUT, "cover.png"), optimize=True)
    demo(rec)
    before_after(rec).save(os.path.join(OUT, "before-after.png"), optimize=True)
    print("figures ->", OUT)
