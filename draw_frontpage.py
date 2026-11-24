#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026.

Build-time tool only: it renders entry.png with Pillow from the story list
below. The shipped program (main.ts) simply copies the rendered entry.png,
so grading runs need no font or imaging library at all.

Layout (1024 x 1024, black ink on white, one red accent):
  masthead -> lead block (COP31) with one line illustration -> four columns
  of headline-only briefs, 34 stories across 7 regions -> footer.
Deterministic: fixed text, fixed geometry, no randomness, no network.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 30
INK = (0, 0, 0)
PAPER = (255, 255, 255)
ACCENT = (166, 25, 46)          # single red accent, region labels only
GREY = (70, 70, 70)
HAIR = (150, 150, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_I = os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# ---------------------------------------------------------------- stories
# (region, headline, is_region_lead, one-line summary for the lead only)
STORIES = [
    ("EUROPE", "Russian missile hits Poland; NATO on alert", True,
     "Allies raise readiness after strike on Poland."),
    ("EUROPE", "UN opens debate on killer robots", False, ""),
    ("EUROPE", "BepiColombo slips into orbit around Mercury", False, ""),
    ("EUROPE", "Russian strikes cut power to 353,000 homes", False, ""),
    ("EUROPE", "EU firms warn leaders over budget cuts", False, ""),
    ("MIDDLE EAST", "Tanker hits mine in the Strait of Hormuz", True,
     "Mine blast adds to Hormuz shipping attacks."),
    ("MIDDLE EAST", "Oil falls as Middle East flows rise", False, ""),
    ("MIDDLE EAST", "IAEA urges Iran to reopen nuclear sites", False, ""),
    ("MIDDLE EAST", "Egypt sends 318th aid convoy to Gaza", False, ""),
    ("MIDDLE EAST", "Gaza aid squeezed as gas runs short", False, ""),
    ("NORTH AMERICA", "US stocks plunge in global sell-off", True,
     "Wall Street leads a global sell-off."),
    ("NORTH AMERICA", "Democrats take control of Congress", False, ""),
    ("NORTH AMERICA", "Iran war funding row raises shutdown risk", False, ""),
    ("NORTH AMERICA", "Migrant caravan marches on as Trump warns Mexico", False, ""),
    ("NORTH AMERICA", "Pentagon rebukes Canada over F-35 review", False, ""),
    ("LATIN AMERICA", "Mexico arrests drug lord 'Chapo Isidro'", True,
     "Arrest caps a week of cartel pressure."),
    ("LATIN AMERICA", "Rubio: Venezuela must rebuild rigged vote system", False, ""),
    ("LATIN AMERICA", "Drone attack hits Colombia police base", False, ""),
    ("LATIN AMERICA", "Three Salvadoran soldiers killed in Haiti", False, ""),
    ("LATIN AMERICA", "Argentina bonds slide as Milei odds fall", False, ""),
    ("AFRICA", "Libya oil pipeline restarts", True,
     "Restart lifts flows as oil prices fall."),
    ("AFRICA", "US urges arms halt and truce in Sudan", False, ""),
    ("AFRICA", "JNIM hits 30 Mali towns; 64 killed in Niger", False, ""),
    ("AFRICA", "Kenya transport strike over fuel prices", False, ""),
    ("SOUTH ASIA", "Lahore chokes as AQI hits 538", True,
     "Delhi second worst as smog grips the region."),
    ("SOUTH ASIA", "Bangladesh PM opens unity dialogue", False, ""),
    ("SOUTH ASIA", "Sri Lanka faces another IMF lifeline", False, ""),
    ("SOUTH ASIA", "Modi, Nepal PM launch Ayodhya-Janakpur train", False, ""),
    ("ASIA-PACIFIC", "Fire guts factory in Cikande", True,
     "Blaze engulfs plant west of Jakarta."),
    ("ASIA-PACIFIC", "India pile up 720/9; NZ hold on for draw", False, ""),
    ("ASIA-PACIFIC", "Beijing cuts margin rules to steady stocks", False, ""),
    ("ASIA-PACIFIC", "Yen slips back toward 160", False, ""),
    ("ASIA-PACIFIC", "Magnitude 5.1 quake shakes West Papua", False, ""),
]

LEAD_LINES = [
    "COP31 collapses in Antalya:",
    "no deal on fossil fuels",
    "as talks break down",
]
LEAD_DECK = ("Nations fail for the first time since 2009 to agree a final "
             "text, as oil falls and Hormuz burns.")

# Columns: (x, [(region, how many of that region's stories go here)]).
# Regions split across columns; every story is placed exactly once.
COL_PLAN = [
    (30, [("EUROPE", 5), ("MIDDLE EAST", 2)]),
    (274, [("MIDDLE EAST", 3), ("NORTH AMERICA", 5)]),
    (518, [("LATIN AMERICA", 5), ("AFRICA", 4)]),
    (762, [("SOUTH ASIA", 4), ("ASIA-PACIFIC", 5)]),
]
COL_W = 230
COL_TOP = 410
COL_BOTTOM = 978


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, region, x, y):
    """One small 12x12 line icon per region, in the accent colour."""
    s = 12
    if region == "EUROPE":                       # ring
        draw.ellipse([x, y, x + s, y + s], outline=ACCENT, width=2)
        draw.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], fill=ACCENT)
    elif region == "MIDDLE EAST":                # oil drop
        draw.polygon([(x + 6, y), (x + 11, y + 7), (x + 1, y + 7)],
                     outline=ACCENT)
        draw.arc([x + 1, y + 4, x + 11, y + 12], 0, 180,
                 fill=ACCENT, width=2)
    elif region == "NORTH AMERICA":              # star
        pts = [(6, 0), (7.6, 4.2), (12, 4.4), (8.6, 7.2), (9.8, 11.6),
               (6, 9.2), (2.2, 11.6), (3.4, 7.2), (0, 4.4), (4.4, 4.2)]
        draw.polygon([(x + px, y + py) for px, py in pts],
                     outline=ACCENT)
    elif region == "LATIN AMERICA":              # sun
        draw.ellipse([x + 3, y + 3, x + 9, y + 9], outline=ACCENT, width=2)
        for dx, dy in [(6, 0), (6, 12), (0, 6), (12, 6),
                       (2, 2), (10, 2), (2, 10), (10, 10)]:
            draw.line([x + 6, y + 6, x + dx, y + dy], fill=ACCENT, width=1)
    elif region == "AFRICA":                     # mountain
        draw.polygon([(x + 6, y), (x + 12, y + 12), (x, y + 12)],
                     outline=ACCENT, width=2)
        draw.line([x + 6, y, x + 9, y + 6], fill=ACCENT, width=1)
    elif region == "SOUTH ASIA":                 # waves
        for k in range(3):
            yy = y + 2 + k * 4
            draw.arc([x, yy, x + 6, yy + 4], 180, 360, fill=ACCENT, width=1)
            draw.arc([x + 6, yy, x + 12, yy + 4], 180, 360,
                     fill=ACCENT, width=1)
    else:                                        # ASIA-PACIFIC: globe
        draw.ellipse([x, y, x + s, y + s], outline=ACCENT, width=2)
        draw.line([x, y + 6, x + s, y + 6], fill=ACCENT, width=1)
        draw.arc([x + 4, y, x + 8, y + s], 270, 90, fill=ACCENT, width=1)


def draw_lead_art(draw, x0, y0, x1, y1):
    """One restrained line illustration: empty conference table, tanker,
    radar arcs. Black line work, one red sun."""
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    # red sun, top right
    draw.ellipse([x1 - 52, y0 + 14, x1 - 22, y0 + 44], fill=ACCENT)
    # radar arcs, top left
    cx, cy = x0 + 30, y0 + 34
    for r in (10, 20, 30):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 270, 0,
                 fill=INK, width=1)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=INK)
    # empty conference table with chairs
    ty = y0 + 96
    draw.polygon([(x0 + 60, ty), (x1 - 60, ty), (x1 - 40, ty + 34),
                  (x0 + 40, ty + 34)], outline=INK, width=2)
    for i in range(5):
        cxp = x0 + 78 + i * 34
        draw.rectangle([cxp, ty - 26, cxp + 18, ty - 6],
                       outline=INK, width=2)
    # papers on the table
    draw.rectangle([x0 + 118, ty + 8, x0 + 150, ty + 22],
                   outline=INK, width=1)
    draw.rectangle([x0 + 160, ty + 8, x0 + 192, ty + 22],
                   outline=INK, width=1)
    # tanker, bottom left
    hy = y1 - 34
    draw.polygon([(x0 + 16, hy), (x0 + 108, hy), (x0 + 96, hy + 16),
                  (x0 + 28, hy + 16)], fill=INK)
    draw.rectangle([x0 + 76, hy - 20, x0 + 96, hy], fill=INK)
    draw.rectangle([x0 + 56, hy - 12, x0 + 68, hy], fill=INK)
    # waves under the tanker
    for wx in (x0 + 14, x0 + 44, x0 + 74):
        draw.arc([wx, hy + 20, wx + 22, hy + 28], 180, 360,
                 fill=INK, width=1)
    # small flag on the table
    draw.line([x1 - 70, ty - 30, x1 - 70, ty], fill=INK, width=2)
    draw.polygon([(x1 - 70, ty - 30), (x1 - 46, ty - 24),
                  (x1 - 70, ty - 18)], fill=ACCENT)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    f_date = font(SANS_B, 13)
    f_badge = font(SANS_B, 12)
    d.text((MARGIN, 26), "SENIN, 23 NOVEMBER 2026", font=f_date, fill=INK)
    badge = "  34 CERITA  \u00b7  7 KAWASAN  "
    bw = d.textlength(badge, font=f_badge)
    bx = W - MARGIN - bw
    d.rectangle([bx - 4, 22, W - MARGIN + 4, 44], fill=ACCENT)
    d.text((bx, 26), badge, font=f_badge, fill=PAPER)
    f_name = font(SERIF_B, 62)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=f_name)
    d.text(((W - nw) / 2, 48), name, font=f_name, fill=INK)
    d.line([(MARGIN, 118), (W - MARGIN, 118)], fill=INK, width=3)
    d.line([(MARGIN, 123), (W - MARGIN, 123)], fill=INK, width=1)

    # ---------------------------------------------------------- lead block
    f_kick = font(SANS_B, 13)
    d.text((MARGIN, 138), "DUNIA  \u00b7  COP31", font=f_kick, fill=ACCENT)
    f_head = font(SERIF_B, 44)
    while max(d.textlength(ln, font=f_head) for ln in LEAD_LINES) > 630:
        f_head = font(SERIF_B, f_head.size - 1)
    y = 162
    for ln in LEAD_LINES:
        d.text((MARGIN, y), ln, font=f_head, fill=INK)
        y += f_head.size + 6
    assert len(LEAD_LINES) == 3, "lead headline must be exactly 3 lines"
    f_deck = font(SERIF, 18)
    deck = wrap(d, LEAD_DECK, f_deck, 630)
    assert len(deck) <= 2, f"deck wrapped to {len(deck)} lines"
    y = 316
    for ln in deck:
        d.text((MARGIN, y), ln, font=f_deck, fill=INK)
        y += 24
    # lead illustration, right of the text
    draw_lead_art(d, 680, 138, 994, 318)
    f_cap = font(SERIF_I, 11) if os.path.exists(SERIF_I) else font(SERIF, 11)
    cap = wrap(d, "An empty table in Antalya; a tanker in Hormuz.",
               f_cap, 314)
    y = 326
    for ln in cap:
        d.text((680, y), ln, font=f_cap, fill=GREY)
        y += 15
    d.line([(MARGIN, 396), (W - MARGIN, 396)], fill=INK, width=1)

    # ---------------------------------------------------------- columns
    f_region = font(SANS_B, 12)
    f_headline = font(SANS_B, 14)
    f_summary = font(SANS, 10)
    by_region = {}
    for region, head, lead, summ in STORIES:
        by_region.setdefault(region, []).append((head, lead, summ))
    consumed = {r: 0 for r in by_region}
    for cx, plan in COL_PLAN:
        items = []  # (kind, region, payload)
        for region, count in plan:
            take = by_region[region][consumed[region]:consumed[region] + count]
            assert len(take) == count, f"short on {region}"
            consumed[region] += count
            items.append(("header", region, None))
            for head, lead, summ in take:
                items.append(("brief", region, (head, lead, summ)))
        # measure fixed height, then spread the slack as inter-brief gap
        fixed, brief_count = 0, 0
        for kind, region, payload in items:
            if kind == "header":
                fixed += 26
            else:
                head, lead, summ = payload
                lines = wrap(d, head, f_headline, COL_W)
                assert len(lines) <= 2, f"brief over 2 lines: {head!r}"
                fixed += len(lines) * 18 + 2
                if lead:
                    s_lines = wrap(d, summ, f_summary, COL_W)
                    assert len(s_lines) == 1, f"summary over 1 line: {summ!r}"
                    fixed += 15
                brief_count += 1
        gap = (COL_BOTTOM - COL_TOP - fixed) / max(brief_count - 1, 1)
        gap = min(gap, 26)  # cap the spread so short columns stay tight
        y = COL_TOP
        n_items = len(items)
        for pos, (kind, region, payload) in enumerate(items):
            if kind == "header":
                draw_icon(d, region, cx, y + 1)
                d.text((cx + 18, y), region, font=f_region, fill=ACCENT)
                d.line([(cx, y + 20), (cx + COL_W, y + 20)], fill=HAIR,
                       width=1)
                y += 26
            else:
                head, lead, summ = payload
                lines = wrap(d, head, f_headline, COL_W)
                for ln in lines:
                    d.text((cx, y), ln, font=f_headline, fill=INK)
                    y += 18
                y += 2
                if lead:
                    d.text((cx, y), summ, font=f_summary, fill=GREY)
                    y += 15
                d.line([(cx, y), (cx + COL_W, y)], fill=HAIR, width=1)
                if pos < n_items - 1:  # gap only between briefs, never after last
                    y += gap
        assert y <= COL_BOTTOM + 1, f"column at x={cx} overflows: y={y}"
    for region, taken in consumed.items():
        assert taken == len(by_region[region]), (
            f"region {region}: {taken}/{len(by_region[region])} placed")

    # ---------------------------------------------------------- footer
    d.line([(MARGIN, 986), (W - MARGIN, 986)], fill=INK, width=1)
    f_foot = font(SANS, 10)
    d.text((MARGIN, 996),
           "All 34 stories were first reported on Monday 23 November 2026.",
           font=f_foot, fill=GREY)
    right = "THE WORLD TODAY  \u00b7  34 STORIES"
    rw = d.textlength(right, font=f_foot)
    d.text((W - MARGIN - rw, 996), right, font=f_foot, fill=GREY)

    img.save(out_path, format="PNG", optimize=True)
    n = sum(len(v) for v in by_region.values())
    print(f"briefs={n} lead=1 stories={n + 1} regions={len(by_region)} "
          f"size={os.path.getsize(out_path)}")


if __name__ == "__main__":
    main()
