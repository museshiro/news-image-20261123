#!/usr/bin/env python3
"""Draw the front page for Monday 23 November 2026 as a single PNG.

One image summing up the world's news of 23 November 2026: a newspaper
front page drawn programmatically with PIL, so every word is crisp and
legible. Deterministic: fixed text, fixed layout, no randomness, no
network. Run: python3 draw_frontpage.py  ->  writes entry.png (1024x1024).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 34
CW = W - 2 * MARGIN  # 956

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 34)
BLUE = (30, 70, 130)
TEAL = (14, 110, 110)
GREY = (96, 92, 84)
RULE = (150, 145, 130)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns the lines that fit `width` px."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, width, text, fnt, fill=INK, leading=None):
    """Draw a wrapped paragraph; returns the y below it."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centered(d, cx, y, text, fnt, fill=INK):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ma")
    return y + int(fnt.size * 1.25)


def hrule(d, x, y, width, weight=2, fill=INK):
    d.rectangle([x, y, x + width, y + weight - 1], fill=fill)
    return y + weight


def kicker(d, x, y, text, fill=RED):
    f = load(SANS_B, 19)
    d.text((x, y), text, font=f, fill=fill)
    return y + 26


def headline(d, x, y, width, text, size, fill=INK, leading=None):
    f = load(SERIF_B, size)
    lh = leading or int(size * 1.02)
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def story(d, x, y, width, kick, kick_fill, head, head_size, body, body_size=19):
    """A kicker + headline + body block; returns the y below it."""
    y = kicker(d, x, y, kick, kick_fill)
    y = headline(d, x, y, width, head, head_size)
    y += 5
    y = para(d, x, y, width, body, load(SERIF, body_size))
    return y


def short_item(d, x, y, width, lead, rest):
    """One 'Also today' item: bold lead-in + regular text."""
    bf = load(SERIF_B, 16)
    rf = load(SERIF, 16)
    words = (lead + " " + rest).split()
    n_bold = len(lead.split())
    lines, cur, cur_w = [], [], 0
    for i, w in enumerate(words):
        f = bf if i < n_bold else rf
        add = d.textlength((" " if cur else "") + w, font=f)
        if cur_w + add <= width:
            cur.append((w, f))
            cur_w += add
        else:
            lines.append(cur)
            cur, cur_w = [(w, f)], d.textlength(w, font=f)
    if cur:
        lines.append(cur)
    lh = 21
    for line in lines:
        cx = x
        for w, f in line:
            d.text((cx, y), w, font=f, fill=INK)
            cx += d.textlength(w + " ", font=f)
        y += lh
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -----------------------------------------------------
    y = 22
    y = hrule(d, MARGIN, y, CW, 3)
    y += 6
    y = centered(d, W // 2, y, "THE WORLD IN ONE DAY", load(SERIF_B, 56))
    y += 2
    d.text((MARGIN, y), "MONDAY, 23 NOVEMBER 2026",
           font=load(SANS_B, 17), fill=INK)
    d.text((W - MARGIN, y), "ONE IMAGE · ONE DAY",
           font=load(SANS_B, 17), fill=INK, anchor="ra")
    y += 28
    y = hrule(d, MARGIN, y, CW, 2)
    y += 8

    # ---- Lead story: COP31 -------------------------------------------
    y = kicker(d, MARGIN, y, "CLIMATE SUMMIT — ANTALYA, TURKEY", RED)
    y = headline(d, MARGIN, y, CW, "COP31 COLLAPSES", 78)
    y += 4
    y = para(d, MARGIN, y, CW,
             "The longest climate talks in history end with no deal, as the "
             "European Union rejects a pact that never once mentions fossil fuels.",
             load(SERIF_I, 25), fill=(40, 40, 40), leading=31)
    y += 8
    y = para(d, MARGIN, y, CW,
             "After more than two weeks of talks and 44 hours of overtime, "
             "delegates from nearly 200 countries failed on Sunday to adopt the "
             "\u201cAntalya Pact\u201d. The EU, Panama, the Marshall Islands and "
             "Norway refused a text stripped of every mention of fossil fuels. "
             "It is the first major breakdown since Copenhagen in 2009, and the "
             "United States — out of climate action — was not at the table.",
             load(SERIF, 18), leading=23)
    y += 6
    d.text((MARGIN, y),
           "LONGEST COP EVER  ·  FIRST BREAKDOWN SINCE COPENHAGEN 2009  ·  190+ COUNTRIES  ·  U.S. ABSENT",
           font=load(SANS_B, 14), fill=(60, 56, 48))
    y += 22
    y = hrule(d, MARGIN, y, CW, 2)
    y += 10

    # ---- Row 2: two columns ------------------------------------------
    col_w = (CW - 28) // 2
    x2 = MARGIN + col_w + 28
    y_row2 = y
    y_left = story(d, MARGIN, y_row2, col_w,
                   "STRAIT OF HORMUZ", RED,
                   "Tankers struck as mines stalk the Gulf", 30,
                   "At least three oil tankers were hit in and near the strait on "
                   "Friday and Saturday, and two more caught fire on Sunday after "
                   "striking naval mines. Attacks on shipping are at their highest "
                   "level since the war began.", 17)
    y_right = story(d, x2, y_row2, col_w,
                    "EUROPE — WAR IN UKRAINE", BLUE,
                    "Poland: fallen objects were Russian missiles", 30,
                    "Three objects that fell in south-east Poland on 20 November "
                    "were confirmed as Russian cruise missiles; NATO is to meet. "
                    "A Russian drone hit a flat block in Dymer, north of Kyiv, "
                    "killing 2 and leaving 11 missing.", 17)
    y = max(y_left, y_right) + 10
    y = hrule(d, MARGIN, y, CW, 2)
    y += 10

    # ---- Row 3: three columns ----------------------------------------
    col3 = (CW - 2 * 24) // 3
    xs = [MARGIN, MARGIN + col3 + 24, MARGIN + 2 * (col3 + 24)]
    y_row3 = y
    ends = []
    ends.append(story(d, xs[0], y_row3, col3,
                      "MARKETS", TEAL,
                      "Stocks plunge; Asia on alert", 25,
                      "U.S. shares fell sharply on Friday. Taiwan's market is down "
                      "17.5% in a week; its regulator has banned short-selling.", 16))
    ends.append(story(d, xs[1], y_row3, col3,
                      "WASHINGTON", BLUE,
                      "Democrats take Congress", 25,
                      "The party wins its largest House majority since 1992 after "
                      "flipping a North Carolina seat.", 16))
    ends.append(story(d, xs[2], y_row3, col3,
                      "MEXICO", RED,
                      "\u2018Chapo Isidro\u2019 captured", 25,
                      "Forces seize FBI-wanted cartel boss Fausto Isidro Meza-Flores "
                      "in Sinaloa; 11 die in firefights.", 16))
    y = max(ends) + 10
    y = hrule(d, MARGIN, y, CW, 2)
    y += 8

    # ---- Also today ---------------------------------------------------
    y = kicker(d, MARGIN, y, "ALSO TODAY", INK)
    items = [
        ("Libya.", "Suspected Ukrainian sea drones hit the Russian corvette "
         "Merkury at Benghazi; the ship capsized, 10 hurt."),
        ("Killer robots.", "128 states agree to pursue rules on lethal "
         "autonomous weapons by 2028."),
        ("Space.", "BepiColombo enters orbit around Mercury — only the "
         "second mission ever to do so."),
        ("Indonesia.", "Candy factory fire in Cikande, Banten: 24 body bags "
         "recovered, dozens still missing."),
        ("Lahore.", "The world's most polluted major city again, with an "
         "air-quality index of 538."),
        ("Sport.", "Alcaraz wins his first ATP Finals title; Marquez takes a "
         "record-tying eighth MotoGP crown; FIFA is set to confirm the UK as "
         "2035 Women's World Cup host."),
    ]
    half = (CW - 28) // 2
    y_l, y_r = y, y
    for i, (lead, rest) in enumerate(items):
        if i % 2 == 0:
            y_l = short_item(d, MARGIN, y_l, half, lead, rest) + 6
        else:
            y_r = short_item(d, MARGIN + half + 28, y_r, half, lead, rest) + 6
    y = max(y_l, y_r) + 2

    # ---- Footer -------------------------------------------------------
    y = hrule(d, MARGIN, y, CW, 2)
    y += 6
    d.text((MARGIN, y), "Sources: CNN · Reuters · BBC · AP · The Hindu · WCMU",
           font=load(SANS, 14), fill=GREY)
    d.text((W - MARGIN, y), "make.fun — news-image-20261123",
           font=load(SANS, 14), fill=GREY, anchor="ra")
    print("final y:", y)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
