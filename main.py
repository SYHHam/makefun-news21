#!/usr/bin/env python3
"""Draw the 21 November 2026 world news front page.

Writes /output/entry.png, 1024x1024, deterministic, no network.
Only stdlib + PIL. Run: python3 main.py
"""
import os
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except Exception:
    PIL_OK = False

W, H = 1024, 1024
OUT = os.environ.get("OUTPUT", "/output/entry.png")

PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (185, 28, 28)
RED_DARK = (153, 27, 27)
GRAY = (87, 83, 78)
LIGHT_LINE = (203, 196, 180)
SAGE = (221, 232, 213)
NAVY = (30, 42, 74)
SAND = (239, 227, 200)
MAP_OCEAN = (217, 230, 240)
MAP_LAND = (229, 217, 184)
MAP_LINE = (180, 168, 138)

BADGE_FILL = {"OFFICIAL": (21, 101, 52), "REPORTED": (87, 83, 78), "CLAIM": (217, 119, 6)}
BADGE_TEXT = {"OFFICIAL": (255, 255, 255), "REPORTED": (255, 255, 255), "CLAIM": (26, 26, 26)}
HOW_CHECKED = ("HOW WE CHECKED: OFFICIAL means an official count or statement, REPORTED means news "
                "reporting, CLAIM means one side's claim without confirmation. Sources named beside every story.")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SERIF_I = "DejaVuSerif-Italic.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(text, fnt, max_w):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, max_w, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    lines = wrap(text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def text_w(text, fnt):
    return fnt.getlength(text)


# ---------------------------------------------------------------- stories
HEROES = [
    {
        "num": 1,
        "label": "COP31: OVERTIME",
        "tag": "No deal · day 13",
        "loc": "ANTALYA, TÜRKIYE · CLIMATE",
        "loc_color": (29, 78, 216),
        "headline": "Climate summit runs into Saturday with no deal",
        "deck": "COP31 missed its Friday close. A draft with no mention of fossil fuels split nearly 200 countries; a third text is promised.",
        "source": "(AFP, Al Jazeera)",
        "art": "cop31",
        "art_label": "+1.5C LIMIT AT RISK",
        "badge": "REPORTED",
    },
    {
        "num": 2,
        "label": "SAUDI: MISSILES",
        "tag": "5 shot down",
        "loc": "RIYADH · JIZAN · WAR",
        "loc_color": (185, 28, 28),
        "headline": "Five Houthi missiles shot down over Saudi Arabia",
        "deck": "The Saudi-led coalition said three were destroyed over Riyadh before dawn and two over Jizan, a day after it bombed Hodeidah port.",
        "source": "(AFP, Dawn)",
        "art": "saudi",
        "art_label": "5 SHOT DOWN, RIYADH AND JIZAN",
        "badge": "REPORTED",
    },
    {
        "num": 3,
        "label": "PERU: QUAKE 6.7",
        "tag": "00:09 UTC · 108 km deep",
        "loc": "JUNÍN, PERU · EARTHQUAKE",
        "loc_color": (180, 83, 9),
        "headline": "Magnitude 6.7 earthquake shakes central Peru",
        "deck": "The deep quake near Carhuamayo was felt in Lima and along the coast. Peru's institute reported no deaths, damage or tsunami risk.",
        "source": "(USGS, IGP)",
        "art": "peru",
        "art_label": "00:09 UTC, M6.7",
        "badge": "OFFICIAL",
    },
]

GRID = [
    ("4", "KYIV: WARNING", "KYIV · WAR", "Zelensky: Crimea bridge 'will not stay'",
     "He warns of more double-tap strikes.", "Interview · NBC", "REPORTED"),
    ("5", "HORMUZ: DRONE", "STRAIT OF HORMUZ · WAR", "Iran says it shot down a US drone",
     "No confirmation from Washington.", "Iran's claim · IRIB", "CLAIM"),
    ("6", "IRAN: URANIUM", "TEHRAN · DIPLOMACY", "Iran: uranium stock stays in the country",
     "Minister still seeks a 'fair solution'.", "Statement · Tol", "OFFICIAL"),
    ("7", "TRUMP: AI TAX", "WASHINGTON · TECHNOLOGY", "Trump vows tax on data centres abroad",
     "'Tremendous' penalty; no details yet.", "Briefing · ABC", "REPORTED"),
    ("8", "CHINA-JAPAN", "BEIJING · DIPLOMACY", "China tells Japan to 'correct' its Taiwan words",
     "Tokyo says its stance is unchanged.", "Ministry · AFP", "OFFICIAL"),
    ("9", "DAVAO: 146 SAFE", "DAVAO · AVIATION", "Jet lands safely after engine fire alert",
     "Air Niugini 767 diverts after midnight.", "Airline · AP", "OFFICIAL"),
    ("10", "CANBERRA: AI", "CANBERRA · DIPLOMACY", "Australia and China agree to AI talks",
     "Albanese ends an 11-day trip.", "Agreed · ABC", "OFFICIAL"),
    ("11", "BITCOIN: $58,983", "WORLD · MARKETS", "Bitcoin trades below $59,000 on Saturday",
     "Down 3.9% in 24 hours; ether $1,625.", "CoinGecko · 02:08 UTC", "OFFICIAL"),
    ("12", "RUSSELL: P1", "LAS VEGAS · FORMULA ONE", "Russell fastest in final Las Vegas practice",
     "1:34.041 in a damp, messy session.", "Timing · Formula 1", "OFFICIAL"),
    ("13", "RAHUL: 124*", "WELLINGTON · CRICKET", "Rahul hits a century against New Zealand",
     "India 344 for 2 at tea, replying to 368.", "Tea, day 3 · AFP", "REPORTED"),
]

ALSO = [
    (14, "Kyiv Rih", "Strike kills 2, injures 42", "Kyiv Independent"),
    (15, "Copenhagen", "Russian expelled over plot", "Al Jazeera"),
    (16, "Antalya", "EU warns of a \"fossil summit\"", "AFP"),
    (17, "Antalya", "Panama may block climate deal", "Al Jazeera"),
    (18, "Antalya", "PLN signs clean-power deals", "Antara"),
    (19, "Yemen", "Houthis threaten Jeddah ports", "Al Jazeera"),
    (20, "Washington", "Vance on Iran strikes", "Reuters"),
    (21, "Washington", "Lawmaker vs SpaceX funds", "CNN"),
    (22, "Texas", "Execution takes 63 minutes", "ABC"),
    (23, "Los Angeles", "Jury convicts Palisades arsonist", "ABC"),
    (24, "Missouri", "$7.25bn Roundup deal approved", "AFP"),
    (25, "Vancouver", "Canada rests climate trial case", "AFP"),
    (26, "Pyongyang", "Kim tours factories", "AFP"),
    (27, "Sejong", "Freight train derails, none hurt", "Korea Herald"),
    (28, "Taipei", "Budget and payout passed", "Taipei Times"),
    (29, "Bangkok", "Arsenic plan for two rivers", "The Nation"),
    (30, "New Delhi", "Pakistani minister at SCO", "Dawn"),
    (31, "Eastern India", "Rain alerts as Akvan moves in", "ETV"),
    (32, "Myanmar", "Sanctions urged after ruling", "AP"),
    (33, "Port Louis", "Rating agency meets 15 states", "Al Jazeera"),
    (34, "Melbourne", "Cummins keeps captaincy", "ABC"),
    (35, "Las Vegas", "Verstappen to stewards", "Autosport"),
]

STATS = [
    ("Day 13", "of a COP31 summit planned to close on day 12"),
    ("5", "missiles shot down over Riyadh and Jizan"),
    ("6.7", "magnitude of the quake in Junín, Peru"),
    ("146", "people safe after a jet's emergency landing"),
    ("$58,983", "bitcoin early Saturday, down 3.9% in a day"),
    ("124*", "K L Rahul's score at tea in Wellington"),
]

REGIONS = [
    ("EUROPE 4", (29, 78, 216)),
    ("ASIA 10", (185, 28, 28)),
    ("MIDDLE EAST 5", (180, 83, 9)),
    ("AFRICA 1", (124, 58, 237)),
    ("AMERICAS 11", (15, 118, 110)),
    ("OCEANIA 3", (21, 128, 61)),
    ("GLOBAL 1", (87, 83, 78)),
]
REGION_W = [112, 280, 140, 60, 244, 84, 60]

PINS = [
    (1, 30.7, 36.9, 0, 0),
    (2, 46.7, 24.6, -8, 6),
    (3, -75.9, -11.2, 0, 0),
    (4, 30.5, 50.4, 0, 0),
    (5, 56.5, 26.5, 10, 4),
    (6, 51.4, 35.7, 2, -8),
    (7, -77.0, 38.9, 0, 0),
    (8, 116.4, 39.9, 0, 0),
    (9, 125.6, 7.1, 0, 0),
    (10, 149.1, -35.3, 0, 0),
    (11, -0.1, 51.5, 0, 0),
    (12, -115.1, 36.2, 0, 0),
    (13, 174.8, -41.3, -6, 0),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 66), (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-100, 20), (-110, 25), (-120, 34), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10), (-35, -15), (-40, -25), (-50, -30), (-60, -35), (-65, -45), (-70, -52), (-75, -40), (-75, -25), (-80, -15), (-80, -5)],
    [(-10, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15), (45, 11), (50, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30), (10, -15), (5, 0), (0, 5), (-8, 5), (-15, 10), (-10, 20)],
    [(-10, 36), (-5, 40), (-2, 44), (0, 48), (5, 53), (10, 57), (15, 58), (20, 60), (25, 65), (30, 70), (35, 68), (30, 60), (25, 55), (20, 50), (15, 45), (10, 44), (5, 43), (0, 40)],
    [(30, 70), (50, 70), (70, 72), (90, 75), (110, 75), (130, 72), (150, 70), (170, 66), (180, 65), (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (120, 30), (110, 20), (105, 10), (100, 5), (95, 10), (90, 20), (85, 25), (80, 15), (75, 10), (70, 20), (60, 25), (55, 28), (50, 30), (45, 35), (40, 38), (35, 36)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25), (145, -20), (140, -15), (135, -12), (130, -12), (125, -15), (120, -20), (115, -21)],
]

DATE_CHECK = (
    "DATE CHECK  Left out as Friday 20 November's news: Wall Street's fall into a correction, "
    "the Russian barrage that hit Kyiv's bridges, the missile that landed in Poland, the UK-EU deal "
    "and Cyclone Akvan's landfall. Older still: Voyager 1's light-day (18 Nov). Not confirmed when "
    "drawn, so not shown: BepiColombo in Mercury orbit, a final COP31 text."
)

FOOTER = "Every story here happened, or was first reported, on Saturday 21 November 2026. Officials' counts and claims are attributed."
FOOTER2 = "Sources named beside each story · original drawings"


# ---------------------------------------------------------------- art
def draw_star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(8):
        ang = math.pi * i / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SAGE)
    cx, cy, r = x + 62, y + h // 2 + 2, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(59, 130, 246), outline=(30, 64, 175), width=2)
    d.ellipse([cx - 18, cy - 20, cx + 2, cy - 2], fill=(34, 197, 94))
    d.ellipse([cx + 2, cy + 8, cx + 20, cy + 24], fill=(34, 197, 94))
    d.ellipse([cx - 26, cy + 6, cx - 8, cy + 18], fill=(34, 197, 94))
    tx = x + 128
    d.rounded_rectangle([tx, y + 12, tx + 16, y + h - 22], radius=8, fill=(255, 255, 255), outline=(120, 120, 120), width=1)
    d.rectangle([tx + 2, y + h - 34, tx + 14, y + h - 22], fill=(220, 38, 38))
    d.ellipse([tx - 3, y + h - 26, tx + 19, y + h - 6], fill=(220, 38, 38), outline=(120, 120, 120), width=1)
    kx, ky, kr = x + w - 52, y + h // 2 + 2, 30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=(60, 60, 60), width=2)
    d.line([kx, ky, kx, ky - 20], fill=(26, 26, 26), width=3)
    d.line([kx, ky, kx + 13, ky + 6], fill=(26, 26, 26), width=3)
    d.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(185, 28, 28))


def art_saudi(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    for sx, sy in [(28, 18), (90, 30), (150, 12), (210, 26), (268, 16), (300, 32)]:
        draw_star(d, x + sx, y + sy, 5, (250, 204, 21))
    base = y + h
    for bx, bw, bh in [(8, 34, 46), (48, 26, 62), (80, 40, 38), (126, 30, 56), (162, 36, 42), (204, 28, 66), (238, 34, 48), (278, 30, 58)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base - 1], fill=(15, 23, 42))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 204, 21))
    d.arc([x + 30, y + 2, x + 200, y + 70], start=200, end=340, fill=(250, 204, 21), width=2)
    d.arc([x + 120, y + 2, x + 300, y + 60], start=205, end=335, fill=(255, 255, 255), width=2)
    draw_star(d, x + 196, y + 22, 9, (250, 204, 21))
    draw_star(d, x + 286, y + 16, 8, (255, 255, 255))


def art_peru(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SAND)
    mid = y + h // 2
    pts = [(x + 8, mid)]
    import math
    seg = 0
    px = x + 8
    while px < x + w - 90:
        seg += 1
        px += 12
        amp = 4 if seg % 3 else 22
        pts.append((px, mid + amp if seg % 2 else mid - amp))
    pts.append((x + w - 88, mid))
    d.line(pts, fill=(185, 28, 28), width=3, joint="curve")
    hx = x + w - 78
    hy = y + h - 20
    d.polygon([(hx, hy - 16), (hx + 52, hy - 16), (hx + 26, hy - 34)], fill=(146, 64, 14))
    d.rectangle([hx + 4, hy - 16, hx + 48, hy + 14], fill=(217, 180, 130), outline=(120, 85, 40), width=1)
    d.rectangle([hx + 21, hy - 2, hx + 31, hy + 14], fill=(90, 60, 30))
    d.line([x + 8, y + h - 4, x + w - 8, y + h - 4], fill=(180, 168, 138), width=1)


def draw_badge(d, x_right, y, kind):
    """Attribution pill, right edge at x_right, top at y. Returns left edge."""
    fnt = font(SANS_B, 8)
    tw = int(fnt.getlength(kind))
    pad = 4
    w = tw + pad * 2
    h = 15
    x0 = int(x_right - w)
    d.rounded_rectangle([x0, y, x_right, y + h], radius=7, fill=BADGE_FILL[kind])
    d.text((x0 + pad, y + 3), kind, font=fnt, fill=BADGE_TEXT[kind])
    return x0


def draw_grid_art(d, num, x, y, w, h):
    """Full-width coloured illustration band for a grid story, top-left at (x, y), size w x h."""
    if num == "4":
        # bridge arc over water
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(203, 225, 240))
        d.rectangle([x, y + h - 8, x + w - 1, y + h - 1], fill=(29, 78, 216))
        d.arc([x + 20, y - 2, x + w - 20, y + 22], start=180, end=360, fill=(185, 28, 28), width=3)
        d.line([x + 20, y + 14, x + w - 20, y + 14], fill=INK, width=2)
        for px in (x + 45, x + 94, x + 143):
            d.line([px, y + 8, px, y + 14], fill=INK, width=2)
    elif num == "5":
        # ship hull on a dark sea + drone above
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 42, 74))
        d.polygon([(x + 30, y + 13), (x + 130, y + 13), (x + 118, y + 21), (x + 42, y + 21)],
                  fill=(226, 232, 240))
        d.rectangle([x + 70, y + 5, x + 90, y + 13], fill=(226, 232, 240))
        d.line([x + 80, y + 2, x + 80, y + 5], fill=(226, 232, 240), width=2)
        d.ellipse([x + 150, y + 3, x + 158, y + 11], fill=(220, 38, 38))
        d.line([x + 140, y + 7, x + 150, y + 7], fill=(250, 204, 21), width=1)
        d.line([x + 158, y + 7, x + 168, y + 7], fill=(250, 204, 21), width=1)
    elif num == "6":
        # atom: orbit ellipse + nucleus
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(254, 243, 199))
        cx, cy = x + w // 2, y + h // 2
        d.ellipse([cx - 34, cy - 9, cx + 34, cy + 9], outline=(29, 78, 216), width=2)
        d.line([cx - 30, cy + 7, cx + 30, cy - 7], fill=(29, 78, 216), width=2)
        d.line([cx - 30, cy - 7, cx + 30, cy + 7], fill=(29, 78, 216), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(185, 28, 28))
    elif num == "7":
        # data centre: chip + server racks
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 240))
        d.rectangle([x + 40, y + 3, x + 64, y + h - 4], outline=INK, width=2)
        d.rectangle([x + 46, y + 8, x + 58, y + h - 9], fill=(185, 28, 28))
        for px in (x + 46, x + 52, x + 58):
            d.line([px, y + 1, px, y + 3], fill=INK, width=1)
            d.line([px, y + h - 3, px, y + h - 1], fill=INK, width=1)
        for rx in (x + 140, x + 158, x + 176):
            d.rectangle([rx, y + 3, rx + 10, y + h - 4], fill=(30, 42, 74))
            for ry in range(y + 6, y + h - 6, 5):
                d.rectangle([rx + 2, ry, rx + 8, ry + 2], fill=(34, 197, 94))
    elif num == "8":
        # two flags: China red with stars, Japan white with red disc
        d.rectangle([x, y, x + w // 2 - 1, y + h - 1], fill=(185, 28, 28))
        draw_star(d, x + 18, y + 7, 5, (250, 204, 21))
        draw_star(d, x + 32, y + 5, 3, (250, 204, 21))
        draw_star(d, x + 34, y + 12, 3, (250, 204, 21))
        d.rectangle([x + w // 2, y, x + w - 1, y + h - 1], fill=(255, 255, 255))
        d.ellipse([x + w // 2 + 28, y + 4, x + w // 2 + 58, y + h - 5], fill=(185, 28, 28))
        d.line([x + w // 2, y, x + w // 2, y + h - 1], fill=(150, 150, 150), width=1)
    elif num == "9":
        # jet in the sky over a runway strip
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(191, 219, 254))
        d.rectangle([x, y + h - 6, x + w - 1, y + h - 1], fill=(34, 197, 94))
        d.polygon([(x + 30, y + 13), (x + 110, y + 6), (x + 150, y + 6), (x + 132, y + 13),
                   (x + 148, y + 17), (x + 80, y + 17), (x + 70, y + 21), (x + 58, y + 17)],
                  fill=(255, 255, 255), outline=(30, 42, 74))
        d.ellipse([x + 118, y + 8, x + 124, y + 12], fill=(30, 42, 74))
    elif num == "10":
        # two flags: Australia blue with stars, China red with one star
        d.rectangle([x, y, x + w // 2 - 1, y + h - 1], fill=(29, 78, 216))
        draw_star(d, x + 22, y + 12, 7, (255, 255, 255))
        draw_star(d, x + 48, y + 6, 4, (255, 255, 255))
        draw_star(d, x + 52, y + 17, 4, (255, 255, 255))
        d.rectangle([x + w // 2, y, x + w - 1, y + h - 1], fill=(185, 28, 28))
        draw_star(d, x + w // 2 + 28, y + 12, 8, (250, 204, 21))
        d.line([x + w // 2, y, x + w // 2, y + h - 1], fill=(150, 150, 150), width=1)
    elif num == "11":
        # bitcoin coin + falling chart line
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255))
        d.line([(x + 40, y + 4), (x + 80, y + 8), (x + 120, y + 14), (x + 160, y + 20)],
               fill=(185, 28, 28), width=3, joint="curve")
        d.polygon([(x + 160, y + 20), (x + 152, y + 16), (x + 170, y + 14)], fill=(185, 28, 28))
        d.ellipse([x + 4, y + 3, x + 28, y + 21], fill=(247, 147, 26))
        d.text((x + 11, y + 6), "B", font=font(SANS_B, 13), fill=(255, 255, 255))
    elif num == "12":
        # checkered flag on a pole + race car
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 240))
        d.line([x + 8, y + 3, x + 8, y + 22], fill=INK, width=2)
        for r in range(2):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([x + 10 + c * 5, y + 3 + r * 5, x + 14 + c * 5, y + 7 + r * 5], fill=INK)
        d.rectangle([x + 10, y + 3, x + 29, y + 12], outline=INK, width=1)
        d.polygon([(x + 45, y + 17), (x + 65, y + 13), (x + 115, y + 13), (x + 145, y + 17),
                   (x + 155, y + 20), (x + 145, y + 22), (x + 55, y + 22)], fill=(185, 28, 28))
        d.rectangle([x + 83, y + 9, x + 109, y + 13], fill=(30, 42, 74))
        d.ellipse([x + 63, y + 19, x + 75, y + 23], fill=INK)
        d.ellipse([x + 125, y + 19, x + 137, y + 23], fill=INK)
    elif num == "13":
        # cricket pitch: bat, ball and stumps
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=(187, 247, 208))
        d.rectangle([x, y + h - 7, x + w - 1, y + h - 1], fill=(134, 239, 172))
        for sx in (x + 150, x + 156, x + 162):
            d.line([sx, y + 6, sx, y + 18], fill=(250, 204, 21), width=2)
        d.line([x + 150, y + 5, x + 163, y + 5], fill=(250, 204, 21), width=2)
        d.line([x + 40, y + 21, x + 95, y + 4], fill=(146, 64, 14), width=5)
        d.ellipse([x + 108, y + 12, x + 120, y + 22], fill=(185, 28, 28))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 22
    CW = W - 2 * MX
    y = 12

    # kicker
    f_kick = font(SANS_B, 12)
    left = "THE WORLD IN ONE DAY"
    right = "35 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((MX, y), left, font=f_kick, fill=RED_DARK)
    rw = text_w(right, f_kick)
    d.text((MX + CW - rw, y), right, font=f_kick, fill=INK)
    d.line([MX, y + 17, MX + CW, y + 17], fill=INK, width=1)
    y += 22

    # masthead, auto fit
    size = 56
    f_head = font(SERIF_B, size)
    while text_w("Saturday 21 November 2026", f_head) > CW and size > 40:
        size -= 2
        f_head = font(SERIF_B, size)
    d.text((MX, y), "Saturday 21 November 2026", font=f_head, fill=INK)
    y += size + 10

    # sub headline
    f_sub = font(SERIF_I, 16)
    sub = "Climate summit runs past its deadline · Five missiles shot down over Saudi Arabia · Strong quake shakes Peru"
    d.text(((W - text_w(sub, f_sub)) / 2, y), sub, font=f_sub, fill=INK)
    y += 22
    d.line([MX, y, MX + CW, y], fill=INK, width=2)
    y += 6

    # stat strip
    col_w = CW / 6
    f_num = font(SANS_B, 24)
    f_lab = font(SANS, 10)
    stat_top = y
    for i, (num, lab) in enumerate(STATS):
        cx = MX + i * col_w
        d.text((cx + 4, y), num, font=f_num, fill=INK)
        ly = y + 30
        for ln in wrap(lab, f_lab, col_w - 12):
            d.text((cx + 4, ly), ln, font=f_lab, fill=GRAY)
            ly += 11
        if i > 0:
            d.line([cx, y + 2, cx, y + 50], fill=LIGHT_LINE, width=1)
    y = stat_top + 52
    d.line([MX, y, MX + CW, y], fill=INK, width=1)
    y += 6

    # region bar
    f_reg = font(SANS_B, 10)
    rx = MX
    for (label, color), wdt in zip(REGIONS, REGION_W):
        d.rectangle([rx, y, rx + wdt - 2, y + 20], fill=color)
        tw = text_w(label, f_reg)
        d.text((rx + (wdt - 2 - tw) / 2, y + 4), label, font=f_reg, fill=(255, 255, 255))
        rx += wdt
    y += 26

    # heroes
    hero_w = 320
    hero_gap = 10
    hero_h = 234
    hero_top = y
    f_hlabel = font(SANS_B, 13)
    f_htag = font(SANS_B, 8)
    f_loc = font(SANS_B, 10)
    f_hhead = font(SERIF_B, 18)
    f_hdeck = font(SANS, 11)
    f_src = font(SANS, 9)
    for i, h in enumerate(HEROES):
        hx = MX + i * (hero_w + hero_gap)
        d.rectangle([hx, y, hx + hero_w - 1, y + 23], fill=RED)
        d.text((hx + 8, y + 4), h["label"], font=f_hlabel, fill=(255, 255, 255))
        tw = text_w(h["tag"], f_htag)
        tag_left = hx + hero_w - 8 - tw
        d.text((tag_left, y + 7), h["tag"], font=f_htag, fill=(255, 255, 255))
        draw_badge(d, tag_left - 8, y + 5, h["badge"])
        ay = y + 23
        if h["art"] == "cop31":
            art_cop31(d, hx, ay, hero_w, 74)
        elif h["art"] == "saudi":
            art_saudi(d, hx, ay, hero_w, 74)
        else:
            art_peru(d, hx, ay, hero_w, 74)
        d.rectangle([hx, ay + 74, hx + hero_w - 1, ay + 89], fill=h["loc_color"])
        d.text((hx + 8, ay + 77), h["art_label"], font=font(SANS_B, 9), fill=(255, 255, 255))
        ty = ay + 94
        d.text((hx, ty), str(h["num"]) + "  " + h["loc"], font=f_loc, fill=h["loc_color"])
        ty += 16
        ty = draw_wrapped(d, hx, ty, h["headline"], f_hhead, hero_w, INK, leading=21)
        ty += 2
        ty = draw_wrapped(d, hx, ty, h["deck"], f_hdeck, hero_w, INK, leading=14)
        ty += 3
        d.text((hx, ty), h["source"], font=f_src, fill=GRAY)
    y = hero_top + hero_h
    d.line([MX, y + 4, MX + CW, y + 4], fill=LIGHT_LINE, width=1)
    y += 10

    # grid, 2 rows x 5
    cell_w = 188
    cell_gap = 10
    row_h = 120
    f_glabel = font(SANS_B, 11)
    f_ghead = font(SERIF_B, 13)
    f_gdeck = font(SANS, 10)
    f_gsrc = font(SANS, 8)
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            num, label, loc, head, deck, src, badge = GRID[idx]
            gx = MX + col * (cell_w + cell_gap)
            gy = y + row * row_h
            d.text((gx, gy), num + " · " + label, font=f_glabel, fill=RED_DARK)
            draw_badge(d, gx + cell_w, gy, badge)
            d.text((gx, gy + 15), loc, font=font(SANS_B, 8), fill=GRAY)
            draw_grid_art(d, num, gx, gy + 26, cell_w, 24)
            hy = draw_wrapped(d, gx, gy + 52, head, f_ghead, cell_w, INK, leading=15)
            dy = draw_wrapped(d, gx, hy + 1, deck, f_gdeck, cell_w, INK, leading=12)
            d.text((gx, dy + 2), src, font=f_gsrc, fill=GRAY)
            if col < 4:
                d.line([gx + cell_w + 5, gy + 2, gx + cell_w + 5, gy + row_h - 14], fill=LIGHT_LINE, width=1)
    y += 2 * row_h
    d.line([MX, y + 2, MX + CW, y + 2], fill=INK, width=1)
    y += 8

    # map + also list
    map_w = 400
    list_w = CW - map_w - 12
    sec_top = y
    f_sec = font(SANS_B, 11)
    d.text((MX, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((MX + map_w + 12, y), "ALSO ON SATURDAY 21 NOVEMBER 2026 · 22 MORE STORIES", font=f_sec, fill=INK)
    y += 17
    map_x, map_y = MX, y
    map_h = 166
    d.rectangle([map_x, map_y, map_x + map_w - 1, map_y + map_h - 1], fill=MAP_OCEAN, outline=MAP_LINE, width=1)

    def proj(lon, lat):
        px = map_x + (lon + 180.0) / 360.0 * map_w
        py = map_y + (75.0 - lat) / 130.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAP_LAND, outline=MAP_LINE)
    f_pin = font(SANS_B, 8)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = text_w(t, f_pin)
        d.text((px - tw / 2, py - 5), t, font=f_pin, fill=(255, 255, 255))
    d.text((MX, map_y + map_h + 4), "Each number is the story with that number on this page.",
           font=font(SANS, 9), fill=GRAY)

    lx = MX + map_w + 12
    f_also = font(SANS, 10)
    f_also_b = font(SANS_B, 10)
    col_w2 = (list_w - 10) / 2
    ay = y
    for ci in range(2):
        ax = lx + ci * (col_w2 + 10)
        yy = ay
        for k in range(11):
            n, place, text, src = ALSO[ci * 11 + k]
            d.text((ax, yy), str(n), font=f_also_b, fill=RED_DARK)
            rest = place + ": " + text + " (" + src + ")"
            lines = wrap(rest, f_also, col_w2 - 22)
            ly = yy
            for ln in lines:
                d.text((ax + 22, ly), ln, font=f_also, fill=INK)
                ly += 12
            yy = max(ly, yy + 12)
            yy += 1
    y = sec_top + 17 + map_h + 22
    d.line([MX, y, MX + CW, y], fill=LIGHT_LINE, width=1)
    y += 6

    # date check box
    box_h = 56
    d.rectangle([MX, y, MX + CW - 1, y + box_h - 1], outline=RED, width=2)
    f_dc = font(SANS, 11)
    f_dc_b = font(SANS_B, 11)
    inner = MX + 10
    iw = CW - 20
    words = DATE_CHECK.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f_dc.getlength(trial) <= iw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    ly = y + 8
    for ln in lines:
        if ln.startswith("DATE CHECK"):
            d.text((inner, ly), "DATE CHECK", font=f_dc_b, fill=RED)
            rest = ln[len("DATE CHECK"):].strip()
            d.text((inner + text_w("DATE CHECK  ", f_dc_b), ly), rest, font=f_dc, fill=INK)
        else:
            d.text((inner, ly), ln, font=f_dc, fill=INK)
        ly += 15
    y += box_h + 5

    # how we checked legend
    f_hwc_b = font(SANS_B, 9)
    f_hwc = font(SANS, 9)
    prefix = "HOW WE CHECKED: "
    rest = HOW_CHECKED[len(prefix):]
    lw = text_w(prefix, f_hwc_b) + text_w(rest, f_hwc)
    lx0 = (W - lw) / 2
    d.text((lx0, y), prefix, font=f_hwc_b, fill=GRAY)
    d.text((lx0 + text_w(prefix, f_hwc_b), y), rest, font=f_hwc, fill=GRAY)
    y += 13

    # footer
    f_foot = font(SANS, 10)
    fw = text_w(FOOTER, f_foot)
    d.text(((W - fw) / 2, y), FOOTER, font=f_foot, fill=INK)
    y += 13
    f_foot2 = font(SANS, 9)
    fw2 = text_w(FOOTER2, f_foot2)
    d.text(((W - fw2) / 2, y), FOOTER2, font=f_foot2, fill=GRAY)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    return OUT


def fallback_copy():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base = os.getcwd()
    src = os.path.join(base, "entry.png")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(src, OUT)
    return OUT


if __name__ == "__main__":
    if PIL_OK:
        try:
            print(build())
        except Exception:
            print(fallback_copy())
    else:
        print(fallback_copy())
