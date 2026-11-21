#!/usr/bin/env python3
"""Saturday, 21 November 2026 -- The Day in One Picture.

Draws a one-page newspaper front page (1024 x 1024 PNG) summing up the
world news of Saturday 21 November 2026: one lead story, three featured
stories, eighteen more from around the world, plus a markets strip.

Everything on the page comes from fixed strings and fixed geometry: no
clock, no randomness, no network, so two runs write byte-identical
files. Usage: python3 draw_news.py [output-dir]
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
PAPER = (247, 242, 231)
INK = (28, 26, 23)
FADED = (107, 101, 92)
RULE = (201, 192, 174)
CRIMSON = (163, 31, 31)
LEAD_WASH = (238, 231, 213)
HAIRLINE = (216, 208, 190)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MARGIN = 28
COL_GAP = 12
COL_W = 314
COL_X = (MARGIN, MARGIN + COL_W + COL_GAP, MARGIN + 2 * (COL_W + COL_GAP))
RIGHT = 1024 - MARGIN

LEAD = {
    "kicker": "MARKETS  •  NEW YORK",
    "headline": "AI doubts trigger a global sell-off",
    "deck": (
        "The S&P 500 falls 3.7% and the Nasdaq turns negative for the year "
        "as investors ask whether vast AI spending will ever pay off. "
        "Tokyo's Nikkei drops 5.1%."
    ),
}

FEATURED = [
    {
        "kicker": "TECH  •  SAN FRANCISCO",
        "headline": "Anthropic's $2 trillion debut stumbles",
        "summary": (
            "Shares slide 8.5% a day after the blockbuster listing, as AI euphoria cools."
        ),
    },
    {
        "kicker": "DIPLOMACY  •  SHENZHEN",
        "headline": "Trump, Xi and Putin meet in Shenzhen",
        "summary": (
            "The three leaders hold a 90-minute trilateral summit at APEC."
        ),
    },
    {
        "kicker": "JUSTICE  •  SINALOA",
        "headline": "Mexico captures 'El Chapo Isidro'",
        "summary": (
            "Forces seize FBI most-wanted cartel boss Fausto Isidro Meza Flores in Guasave."
        ),
    },
]

GRID = [
    (
        "CONFLICT  •  KRYVYI RIH",
        "Russian missile hits Zelensky's hometown",
        "Two killed and 60 wounded in a strike on the centre of Kryvyi Rih.",
    ),
    (
        "SECURITY  •  WARSAW",
        "Russia violates Polish airspace",
        "Three objects, likely two missiles and a drone, cross into Poland; Britain's PM condemns the incursion.",
    ),
    (
        "JUSTICE  •  THE HAGUE",
        "Myanmar guilty of Rohingya genocide",
        "The International Court of Justice rules against Myanmar over its treatment of the Rohingya.",
    ),
    (
        "CLIMATE  •  ANTALYA",
        "COP31 talks run past deadline",
        "The climate summit overruns its Friday deadline with fossil fuels still splitting negotiators.",
    ),
    (
        "TECH  •  WASHINGTON",
        "Nvidia halts H200 exports to China",
        "The chipmaker stops shipments amid a US debate over advanced tech sales.",
    ),
    (
        "CULTURE  •  WORLDWIDE",
        "GTA 6 banks $3.79bn in a day",
        "Rockstar's blockbuster sets a launch record as its workers vote on union recognition.",
    ),
    (
        "SPACE  •  MERCURY",
        "BepiColombo reaches Mercury",
        "Europe and Japan's probe enters orbit around Mercury after an eight-year journey.",
    ),
    (
        "HEALTH  •  BRAZIL",
        "Mosquito trick cuts dengue 69%",
        "Releasing mosquitoes carrying a bacterium slashes dengue cases, Brazilian researchers report.",
    ),
    (
        "DISASTER  •  TIMOR-LESTE",
        "Magnitude 6.8 quake off Timor-Leste",
        "A strong undersea earthquake strikes; no tsunami threat is issued.",
    ),
    (
        "CONFLICT  •  GULF OF FINLAND",
        "Drone sets Russian cargo ship ablaze",
        "A drone attack ignites a Russian cargo vessel in the Gulf of Finland.",
    ),
    (
        "POLITICS  •  GENEVA",
        "UN agrees AI-weapons draft by 2028",
        "States agree to draft rules for autonomous weapons, but no binding commitment yet.",
    ),
    (
        "POLITICS  •  HANOI",
        "Vietnam ends death penalty for drugs",
        "Hanoi abolishes capital punishment for drug trafficking and speeds land seizures.",
    ),
    (
        "POLITICS  •  BRUSSELS",
        "EU sends Kyiv 7.9bn euros",
        "The bloc disburses its largest single payment yet to Ukraine.",
    ),
    (
        "POLITICS  •  BRUSSELS",
        "EU weighs 3% tax on big tech",
        "Council chief Costa puts a levy on tech giants' digital revenue into the 2028-34 budget draft.",
    ),
    (
        "SECURITY  •  HORMUZ",
        "Iran claims US drone downed",
        "Tehran says its forces shot down an American drone over the Strait of Hormuz.",
    ),
    (
        "SECURITY  •  COPENHAGEN",
        "Denmark to expel Russian envoy",
        "Copenhagen acts over an alleged assassination plot against US-Ukrainian rapper Kyivstoner.",
    ),
    (
        "ENERGY  •  HORMUZ",
        "Tanker attacks hit monthly high",
        "Strikes on tankers near Hormuz rise to a new high for the month; no casualties in the latest.",
    ),
    (
        "SPORT  •  LONDON",
        "Leeds stun Chelsea 4-1",
        "Noah Okafor scores twice as Leeds win at Stamford Bridge for the first time in 27 years.",
    ),
]

MARKETS_LABEL = "MARKETS"
MARKETS_LINE = (
    "S&P 500 6,910 ▼3.7%  •  Nikkei ▼5.1%  •  FTSE 100 10,346 ▼1.0%  •  "
    "Brent $89.95 ▲0.6%  •  Gold lowest since late 2025"
)

FOOTER = (
    "Sources: AP · Reuters · BBC · NYT · Le Monde · CNN — Every event happened, "
    "or was first reported, on Saturday, 21 November 2026."
)


def face(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, width):
    """Greedy word wrap; returns lines that fit inside `width` pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def clamp_lines(draw, text, font, width, max_lines):
    """Wrap text and clip to max_lines, adding an ellipsis when clipped."""
    lines = wrap_text(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        clipped = lines[-1]
        while clipped and draw.textlength(clipped + " …", font=font) > width:
            if " " in clipped:
                clipped = clipped.rsplit(" ", 1)[0]
            else:
                clipped = clipped[:-1]
        lines[-1] = clipped + " …"
    return lines


def draw_lines(draw, x, y, lines, font, leading, fill=INK):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centred(draw, y, text, font, fill=INK):
    width = draw.textlength(text, font=font)
    draw.text(((CANVAS - width) / 2, y), text, font=font, fill=fill)


def draw_masthead(draw):
    cx, cy, r = 58, 58, 22
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    draw.ellipse([cx - 9, cy - r, cx + 9, cy + r], outline=INK, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    centred(draw, 26, "THE DAY IN ONE PICTURE", face(SERIF_BOLD, 56))
    centred(
        draw,
        94,
        "SATURDAY, 21 NOVEMBER 2026  •  22 STORIES FROM AROUND THE WORLD",
        face(SANS, 15),
        fill=FADED,
    )
    draw.line([MARGIN, 118, RIGHT, 118], fill=INK, width=2)
    draw.line([MARGIN, 122, RIGHT, 122], fill=INK, width=1)
    return 132


def draw_lead(draw, top):
    height = 124
    draw.rectangle(
        [MARGIN, top, RIGHT, top + height], fill=LEAD_WASH, outline=RULE, width=1
    )
    inner = MARGIN + 18
    width = RIGHT - MARGIN - 36
    draw.text((inner, top + 13), LEAD["kicker"], font=face(SANS_BOLD, 13), fill=CRIMSON)
    draw.text(
        (inner, top + 33),
        LEAD["headline"],
        font=face(SERIF_BOLD, 34),
        fill=INK,
    )
    deck = clamp_lines(draw, LEAD["deck"], face(SANS, 15), width, 2)
    draw_lines(draw, inner, top + 78, deck, face(SANS, 15), 20)
    return top + height


def draw_featured(draw, top):
    height = 106
    for index, story in enumerate(FEATURED):
        x = COL_X[index]
        if index:
            draw.line(
                [x - COL_GAP // 2 - 1, top + 4, x - COL_GAP // 2 - 1, top + height - 4],
                fill=HAIRLINE,
                width=1,
            )
        draw.text(
            (x, top), story["kicker"], font=face(SANS_BOLD, 12), fill=CRIMSON
        )
        headline = clamp_lines(
            draw, story["headline"], face(SANS_BOLD, 17), COL_W, 2
        )
        bottom = draw_lines(draw, x, top + 18, headline, face(SANS_BOLD, 17), 21)
        summary = clamp_lines(
            draw, story["summary"], face(SANS, 13), COL_W, 2
        )
        draw_lines(draw, x, bottom + 6, summary, face(SANS, 13), 16)
    return top + height


def draw_centred_pair(draw, y, left, left_font, left_fill, right, right_font):
    """Draw two runs of text side by side, centred as one line."""
    total = draw.textlength(left, font=left_font) + draw.textlength(
        right, font=right_font
    )
    x = (CANVAS - total) / 2
    draw.text((x, y), left, font=left_font, fill=left_fill)
    draw.text(
        (x + draw.textlength(left, font=left_font), y),
        right,
        font=right_font,
        fill=INK,
    )


def draw_markets_strip(draw, top):
    draw.line([MARGIN, top, RIGHT, top], fill=RULE, width=1)
    draw_centred_pair(
        draw,
        top + 9,
        MARKETS_LABEL + "   ",
        face(SANS_BOLD, 14),
        CRIMSON,
        MARKETS_LINE,
        face(SANS, 14),
    )
    draw.line([MARGIN, top + 34, RIGHT, top + 34], fill=RULE, width=1)
    return top + 34


def draw_grid(draw, top):
    draw.text(
        (MARGIN, top),
        "MORE FROM AROUND THE WORLD",
        font=face(SANS_BOLD, 13),
        fill=INK,
    )
    grid_top = top + 30
    row_h = 80
    row_gap = 6
    for row in range(6):
        y = grid_top + row * (row_h + row_gap)
        for col in range(3):
            story = GRID[row * 3 + col]
            x = COL_X[col]
            kicker, headline, summary = story
            draw.text((x, y), kicker, font=face(SANS_BOLD, 11), fill=CRIMSON)
            head_lines = clamp_lines(
                draw, headline, face(SANS_BOLD, 15), COL_W, 2
            )
            bottom = draw_lines(draw, x, y + 15, head_lines, face(SANS_BOLD, 15), 18)
            sum_lines = clamp_lines(draw, summary, face(SANS, 12), COL_W, 2)
            draw_lines(draw, x, bottom + 1, sum_lines, face(SANS, 12), 14)
        if row < 5:
            line_y = y + row_h + 3
            draw.line([MARGIN, line_y, RIGHT, line_y], fill=HAIRLINE, width=1)
    return grid_top + 6 * row_h + 5 * row_gap


def draw_footer(draw, top):
    draw.line([MARGIN, top, RIGHT, top], fill=INK, width=1)
    centred(draw, top + 9, FOOTER, face(SANS, 12), fill=FADED)
    return top + 27


def compose_page():
    page = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(page)
    bottom = draw_masthead(draw)
    bottom = draw_lead(draw, bottom)
    bottom = draw_featured(draw, bottom + 12)
    bottom = draw_markets_strip(draw, bottom + 12)
    bottom = draw_grid(draw, bottom + 12)
    bottom = draw_footer(draw, bottom + 12)
    if bottom > CANVAS:
        raise SystemExit(f"layout overflow: content ends at y={bottom}")
    return page


def main(argv):
    out_dir = argv[1] if len(argv) > 1 else os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    image = compose_page()
    target = os.path.join(out_dir, "entry.png")
    image.save(target, format="PNG")
    print(f"wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
