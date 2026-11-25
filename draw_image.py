#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news broadsheet (1024x823, PNG).

Stdlib + PIL only. Deterministic: no time, no randomness, no network.
Renders entry.png next to this file (or to $DRAW_OUT when set).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 823
PAPER = (248, 243, 230)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (29, 106, 106)
SKY = (24, 44, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x, y, w, color, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def star(draw, cx, cy, r, fill):
    draw.polygon(
        [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
         (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
         (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
         (cx - r * 0.28, cy - r * 0.28)],
        fill=fill,
    )


def draw_rocket_panel(base, x, y, w, h):
    # render on a panel-local image so the earth arc cannot bleed outside it
    panel = Image.new("RGB", (w, h), SKY)
    draw = ImageDraw.Draw(panel)
    for sx, sy, r in [(40, 30, 4), (120, 18, 3), (210, 44, 4),
                      (300, 22, 3), (420, 36, 4), (520, 20, 3),
                      (580, 52, 4), (70, 90, 3), (470, 96, 3)]:
        star(draw, sx, sy, r, (255, 255, 220))
    # rocket body, nose-up, centre-right of panel
    rx, ry = w // 2 + 60, 55
    draw.polygon([(rx - 26, ry + 110), (rx - 26, ry + 30), (rx, ry - 10),
                  (rx + 26, ry + 30), (rx + 26, ry + 110)], fill=(240, 240, 235))
    draw.polygon([(rx - 26, ry + 30), (rx, ry - 10), (rx + 26, ry + 30)],
                 fill=(178, 34, 34))
    draw.rectangle([rx - 26, ry + 78, rx + 26, ry + 96], fill=(178, 34, 34))
    draw.ellipse([rx - 12, ry + 34, rx + 12, ry + 58], fill=(135, 206, 235),
                 outline=(20, 33, 61), width=2)
    draw.polygon([(rx - 26, ry + 110), (rx - 44, ry + 132), (rx - 26, ry + 122)],
                 fill=(178, 34, 34))
    draw.polygon([(rx + 26, ry + 110), (rx + 44, ry + 132), (rx + 26, ry + 122)],
                 fill=(178, 34, 34))
    draw.polygon([(rx - 14, ry + 110), (rx, ry + 148), (rx + 14, ry + 110)],
                 fill=(255, 165, 0))
    draw.polygon([(rx - 7, ry + 110), (rx, ry + 132), (rx + 7, ry + 110)],
                 fill=(255, 220, 80))
    # earth curve bottom-left (clipped to the panel by the local image)
    draw.ellipse([-260, h - 60, 180, h + 160], fill=(46, 110, 160))
    draw.ellipse([-160, h - 40, 60, h + 120], fill=(34, 92, 140))
    draw.text((14, h - 26), "LONG MARCH 2F  ·  JIUQUAN, CHINA",
              font=SANS_B(13), fill=(255, 255, 255))
    base.paste(panel, (x, y))


def draw_tower_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(58, 64, 84))
    # skyline
    for bx, bw, bh in [(0, 46, 52), (52, 34, 74), (96, 40, 44), (150, 30, 66),
                       (196, 44, 50), (250, 36, 80), (292, 24, 58)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(38, 42, 58))
    # PIF tower, tallest, centre
    tx = x + w // 2 - 16
    draw.rectangle([tx, y + 8, tx + 32, y + h], fill=(200, 204, 214))
    for wy in range(y + 16, y + h - 8, 12):
        draw.line([(tx + 4, wy), (tx + 28, wy)], fill=(120, 126, 142), width=1)
    draw.rectangle([tx - 3, y + 4, tx + 35, y + 10], fill=(160, 164, 176))
    # smoke puff at mid-tower
    for cx, cy, r in [(tx - 6, y + 62, 12), (tx + 38, y + 54, 10), (tx + 18, y + 48, 11)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    draw.text((x + 10, y + h - 22), "PIF TOWER  ·  RIYADH",
              font=SANS_B(12), fill=(255, 255, 255))


def draw_ship_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 90, 120))
    for wy in (y + h - 34, y + h - 20, y + h - 8):
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(90, 160, 200), width=2)
    # cargo ship
    draw.rectangle([x + 40, y + h - 62, x + w - 40, y + h - 38], fill=(120, 40, 40))
    draw.rectangle([x + w // 2 - 10, y + h - 92, x + w // 2 + 26, y + h - 62],
                   fill=(240, 240, 235))
    draw.line([(x + w // 2 + 8, y + h - 92), (x + w // 2 + 8, y + h - 104)],
              fill=(240, 240, 235), width=3)
    # drone + blast
    draw.ellipse([x + w - 52, y + 22, x + w - 36, y + 38], fill=(255, 220, 80))
    star(draw, x + w - 44, y + 30, 14, (255, 160, 40))
    # dark label strip so the white caption stays legible over the ship
    draw.rectangle([x, y, x + w, y + 24], fill=(16, 48, 66))
    draw.text((x + 10, y + 6), "GULF OF FINLAND", font=SANS_B(12),
              fill=(255, 255, 255))


def draw_chip_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 24, 32))
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 42, cy - 30, cx + 42, cy + 30], fill=(40, 40, 56),
                   outline=(201, 162, 39), width=2)
    draw.rectangle([cx - 20, cy - 14, cx + 20, cy + 14], fill=(201, 162, 39))
    for i in range(5):
        px = cx - 36 + i * 18
        draw.line([(px, cy - 44), (px, cy - 30)], fill=(180, 180, 190), width=3)
        draw.line([(px, cy + 30), (px, cy + 44)], fill=(180, 180, 190), width=3)
    for i in range(3):
        py = cy - 18 + i * 18
        draw.line([(cx - 56, py), (cx - 42, py)], fill=(180, 180, 190), width=3)
        draw.line([(cx + 42, py), (cx + 56, py)], fill=(180, 180, 190), width=3)
    # dark label strip so the white caption stays legible over the pins
    draw.rectangle([x, y, x + w, y + 24], fill=(10, 10, 14))
    draw.text((x + 10, y + 6), "U.S. FEDERAL COURT", font=SANS_B(12),
              fill=(255, 255, 255))


def draw_medal_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(112, 28, 28))
    cx, cy = x + w // 2, y + h // 2 + 8
    draw.polygon([(cx - 26, y + 8), (cx - 8, y + 8), (cx, cy - 26), (cx + 8, y + 8),
                  (cx + 26, y + 8), (cx + 12, cy - 18), (cx - 12, cy - 18)],
                 fill=(255, 255, 255))
    draw.polygon([(cx - 26, y + 8), (cx - 8, y + 8), (cx, cy - 26), (cx + 8, y + 8),
                  (cx + 26, y + 8), (cx + 12, cy - 18), (cx - 12, cy - 18)],
                 outline=(201, 162, 39), width=1)
    draw.ellipse([cx - 34, cy - 30, cx + 34, cy + 38], fill=(201, 162, 39),
                 outline=(150, 110, 20), width=3)
    draw.ellipse([cx - 20, cy - 16, cx + 20, cy + 24], fill=(232, 196, 90))
    draw.text((cx - 6, cy - 12), "★", font=SANS_B(26), fill=(150, 110, 20))
    # dark label strip so the white caption stays legible over the ribbon
    draw.rectangle([x, y, x + w, y + 24], fill=(70, 16, 16))
    draw.text((x + 10, y + 6), "WHITE HOUSE", font=SANS_B(12),
              fill=(255, 255, 255))


def draw_boat_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(20, 70, 90))
    for wy in (y + h - 30, y + h - 18, y + h - 8):
        draw.line([(x + 8, wy), (x + w - 8, wy)], fill=(90, 160, 200), width=2)
    # crowded boat
    draw.polygon([(x + 36, y + h - 52), (x + w - 36, y + h - 52),
                  (x + w - 52, y + h - 30), (x + 52, y + h - 30)], fill=(150, 90, 40))
    for i in range(6):
        hx = x + 62 + i * 20
        draw.ellipse([hx, y + h - 66, hx + 10, y + h - 56], fill=(240, 220, 190))
    draw.line([(x + w // 2, y + h - 52), (x + w // 2, y + h - 84)],
              fill=(120, 80, 40), width=3)
    draw.polygon([(x + w // 2, y + h - 84), (x + w // 2 + 34, y + h - 62),
                  (x + w // 2, y + h - 62)], fill=(240, 240, 235))
    draw.text((x + 10, y + 10), "BAY OF BENGAL", font=SANS_B(12),
              fill=(255, 255, 255))


def card(draw, x, y, w, kicker, headline, body, panel_fn):
    draw.rectangle([x, y, x + w, y + 262], outline=(180, 170, 150), width=1)
    panel_fn(draw, x + 1, y + 1, w - 2, 108)
    ty = y + 120
    draw.text((x + 10, ty), kicker, font=SANS_B(12), fill=RED)
    ty += 20
    ty = para(draw, x + 10, ty, headline, SERIF_B(19), w - 20, INK, 23)
    ty += 4
    para(draw, x + 10, ty, body, SANS(13), w - 20, (60, 60, 60), 17)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((W // 2, 12), "THE WORLD IN ONE DAY", font=SERIF_B(52),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 72), "SIX STORIES  ·  ONE PAGE", font=SANS_B(13),
           fill=(201, 162, 39), anchor="ma")
    rule(d, 0, 100, W, GOLD, 4)
    d.text((W // 2, 112), "WEDNESDAY, 25 NOVEMBER 2026",
           font=SANS_B(15), fill=INK, anchor="ma")
    rule(d, 24, 140, W - 48, INK, 1)

    # hero: space launch
    draw_rocket_panel(img, 24, 152, 636, 210)
    hy = 374
    hy = para(d, 24, hy, "FIRST PAKISTANI IN ORBIT", SERIF_B(36), 636, INK, 42)
    para(d, 24, hy + 6,
         "China's Shenzhou-24 blasts off for Tiangong with Muhammad Zeeshan Ali "
         "aboard — the first Pakistani in orbit and the first foreign astronaut "
         "ever to visit the Chinese space station.",
         SANS(15), 636, (60, 60, 60), 20)

    # right column: Riyadh tower
    draw_tower_panel(d, 684, 152, 316, 128)
    ry = 292
    ry = para(d, 684, ry, "HOUTHI DRONE HITS RIYADH'S TALLEST TOWER",
              SERIF_B(21), 316, INK, 25)
    para(d, 684, ry + 4,
         "Eleven wounded as a drone strikes the 385-metre PIF tower in the "
         "King Abdullah Financial District — the second hit on the landmark "
         "in under a week.",
         SANS(13), 316, (60, 60, 60), 17)

    # bottom row: four stories
    rule(d, 24, 500, W - 48, INK, 1)
    cards = [
        ("UKRAINE WAR", "Kyiv confirms strike on Russian ship",
         "Zelenskiy says Ukraine hit a Russian cargo vessel in the Gulf of "
         "Finland; Moscow calls the drone attacks \"terrorism\".",
         draw_ship_panel),
        ("U.S. — CHINA", "Huawei convicted in U.S. trial",
         "A federal jury convicts the Chinese telecoms giant over its Iran "
         "business in a sprawling criminal case.",
         draw_chip_panel),
        ("WASHINGTON", "Medal of Freedom for Giuliani",
         "President Trump awards Rudy Giuliani the nation's highest civilian "
         "honour at the White House.",
         draw_medal_panel),
        ("SOUTHEAST ASIA", "Malaysia to return 6,500 Rohingya",
         "PM Anwar says refugees will be sent back to Myanmar in December, "
         "days after the ICJ genocide ruling.",
         draw_boat_panel),
    ]
    x = 24
    for kicker, headline, body, panel_fn in cards:
        card(d, x, 516, 238, kicker, headline, body, panel_fn)
        x += 246

    # footer
    rule(d, 24, 792, W - 48, INK, 1)
    d.text((W // 2, 802), "Sources: Reuters · Xinhua · AP  —  All stories reported 25 November 2026",
           font=SANS(11), fill=(90, 90, 90), anchor="ma")

    out = os.environ.get("DRAW_OUT", os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png"))
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
