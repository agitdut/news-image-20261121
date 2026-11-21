#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: one front page summing up Saturday
21 November 2026, drawn with Pillow at build time (the entry itself is the
finished entry.png, copied by main.ts).

Layout (1024x1024): masthead naming the day, a Kyiv/Poland lead beside a
COP31 box, three feature boxes (Wall Street, Brussels, health), three
columns of short items, a markets strip with Friday's closes and a
sources footer. About 22 distinct stories, every one reported on
21 November 2026.

Facts used (all reported 21 Nov 2026; sources AP, Reuters, BBC, Le Monde,
CNN, Investopedia, TradingView):
  Kyiv/Poland: Russia fires 400+ drones and 110+ missiles overnight
    (27 ballistic, some with cluster warheads); at least 8 killed in
    Kyiv, dozens wounded; bridges, railway stations and the power grid
    hit; nuclear plants cut output. A later double-tap strike on
    Kryvyi Rih kills a 7-year-old boy and a 20-year-old paramedic and
    wounds about 20. Two Russian Kh-101 missiles and a suspected
    jet-powered drone come down in Poland, 30-60 km inside its border;
    PM Donald Tusk calls it an "intentional provocation"; NATO jets
    (Polish F-16s, Swedish Gripens, a Dutch tanker) scramble; France
    seeks a UN Security Council meeting. A day earlier, Trump, Putin
    and Xi signed a peace declaration in Shenzhen.
  Antalya: COP31 spills into overtime on Saturday; the draft deal
    strips all references to fossil fuels and drops a $120bn adaptation
    finance target; the closing plenary was suspended on Friday at
    22:29 local time; Addis Ababa will host COP32 in 2027; the world
    is set to blow past the 1.5C Paris goal.
  Markets: Wall Street's AI rout deepens on Friday: S&P 500 6,910.42
    -3.70% (7th straight loss, in correction), Dow 48,147.33 -1.93%
    (in correction), Nasdaq 22,617.73 -5.28% (2026 gains wiped out),
    VIX 35.89; Nvidia -14%, Anthropic -9% on its second day, closing
    at $88.91 against an $83 IPO price.
  Brussels: PM Andy Burnham and EU leaders sign three agreements on
    food exports, carbon markets and youth mobility - the biggest
    post-Brexit agreements.
  Health: a trial of the pill daraxonrasib makes pancreatic cancer
    undetectable on scans in one in 12 patients.
  Shorts: Zelensky calls Putin an "enemy and killer" after Trump
    calls him a friend; Britain's Burnham calls the Poland incursion
    "utterly unacceptable"; France seeks a UNSC meeting; Spain heads
    to a 29 November election as conservatives gain; EU approves
    1 billion euros in defence aid for Ukraine; Iran says it downed a
    US MQ-9 drone over the Strait of Hormuz, the 58th; Lewis Pugh
    swims the strait to spotlight the war's toll on marine life;
    Israeli strikes kill Palestinians in Gaza; Salvadoran troops in
    Haiti lose soldiers to explosives; Mongolia's president resigns,
    elections due within four months; Gen Z protests spread across 25
    European countries; GTA 6 takes about $4.9bn in day-one sales;
    a man is convicted of starting the deadly Palisades fire in Los
    Angeles; the FBI criminal database is reportedly hacked.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 28
RIGHT = 996

PALETTE = {
    "paper": (246, 241, 230),
    "ink": (26, 26, 26),
    "red": (163, 18, 18),
    "blue": (29, 78, 137),
    "grey": (90, 86, 78),
    "wash": (232, 226, 212),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


class Typefaces:
    """Lazy loader for the four DejaVu faces used on the page."""

    _cache = {}

    @classmethod
    def get(cls, filename, size):
        key = (filename, size)
        if key not in cls._cache:
            cls._cache[key] = ImageFont.truetype(FONT_DIR + filename, size)
        return cls._cache[key]

    @classmethod
    def serif_bold(cls, size):
        return cls.get("DejaVuSerif-Bold.ttf", size)

    @classmethod
    def sans(cls, size):
        return cls.get("DejaVuSans.ttf", size)

    @classmethod
    def sans_bold(cls, size):
        return cls.get("DejaVuSans-Bold.ttf", size)


def split_lines(draw, text, face, max_width):
    """Greedy word wrap; returns the lines that fit inside max_width.

    A single word wider than the column is hard-split so it can never
    overflow the box it is drawn in.
    """
    lines, current = [], ""
    for word in text.split():
        while draw.textlength(word, font=face) > max_width:
            cut = 1
            while (cut < len(word)
                   and draw.textlength(word[:cut + 1], font=face) <= max_width):
                cut += 1
            lines.append(word[:cut])
            word = word[cut:]
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=face) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


class Canvas:
    """A 1024x1024 front page plus the small drawing vocabulary it needs."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["paper"])
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle([0, 0, PAGE_W - 1, PAGE_H - 1],
                            outline=PALETTE["ink"], width=4)

    def hline(self, y, x0=MARGIN, x1=RIGHT, weight=2, colour=None):
        self.draw.line([(x0, y), (x1, y)],
                       fill=colour or PALETTE["ink"], width=weight)

    def text_block(self, x, y, text, face, max_width, leading, colour=None):
        """Draw wrapped text; return the y just below the last line."""
        fill = colour or PALETTE["ink"]
        for line in split_lines(self.draw, text, face, max_width):
            self.draw.text((x, y), line, font=face, fill=fill)
            y += leading
        return y

    def label(self, x, y, text, colour=None, size=17):
        """Small bold uppercase kicker; returns the y below it."""
        self.draw.text((x, y), text, font=Typefaces.sans_bold(size),
                       fill=colour or PALETTE["red"])
        return y + 24

    def title(self, x, y, text, max_width, size=33, leading=40):
        """Bold serif headline; returns the y below it."""
        return self.text_block(x, y, text, Typefaces.serif_bold(size),
                               max_width, leading)

    def save(self, path="entry.png"):
        self.image.save(path, optimize=True)
        print("wrote", path, self.image.size)


# ---------------------------------------------------------------- content

LEAD = {
    "label": "KYIV  \u00b7  AND POLAND",
    "title": "Russia\u2019s biggest barrage hits Kyiv \u2014 and lands in Poland",
    "body": (
        "More than 400 drones and 110 missiles rain down overnight, "
        "27 of them ballistic; at least eight are killed in Kyiv as "
        "bridges and the power grid are hit. Two Russian missiles and "
        "a suspected drone then land in Poland \u2014 PM Donald Tusk "
        "calls it an \u201cintentional provocation\u201d."
    ),
}

COP_BOX = {
    "label": "ANTALYA  \u00b7  CLIMATE TALKS",
    "title": "COP31 stalls in overtime",
    "body": (
        "The draft deal strips out every mention of fossil fuels; "
        "the $120bn adaptation target is dropped and the closing "
        "plenary suspended. Addis Ababa hosts COP32 in 2027."
    ),
}

FEATURES = [
    ("NEW YORK  \u00b7  WALL STREET ROUT",
     "AI rout puts S&P and Dow in correction",
     "The S&P 500 falls 3.7% for a seventh straight loss; the "
     "Nasdaq drops 5.28%, wiping out its 2026 gains."),
    ("BRUSSELS  \u00b7  POST-BREXIT RESET",
     "UK and EU sign biggest post-Brexit deals",
     "PM Andy Burnham and EU leaders sign three agreements on food "
     "exports, carbon markets and youth mobility."),
    ("LONDON  \u00b7  HEALTH",
     "Pill makes pancreatic cancer undetectable",
     "A trial of daraxonrasib leaves tumours undetectable on scans "
     "in one in 12 patients."),
]

BRIEF_COLUMNS = [
    ("EUROPE & THE WAR", [
        ("Zelensky calls Putin \u201cenemy and killer\u201d",
         "after Trump calls him a friend."),
        ("NATO jets scrambled over Poland",
         "Polish F-16s and Swedish Gripens answer."),
        ("France seeks a UN Security Council meeting",
         "after strikes hit the Austrian embassy."),
        ("Britain: Poland incursion \u201cutterly unacceptable\u201d",
         "says PM Andy Burnham."),
        ("Spain heads to a 29 November election",
         "as the conservatives gain."),
    ]),
    ("THE GULF & BEYOND", [
        ("Iran downs a US MQ-9 drone",
         "over the Strait of Hormuz, the 58th."),
        ("Lewis Pugh swims the Hormuz strait",
         "to spotlight the war\u2019s toll on wildlife."),
        ("Israeli strikes kill Palestinians in Gaza",
         "as West Bank violence continues."),
        ("Salvadoran troops in Haiti lose soldiers",
         "to explosives in Port-au-Prince."),
        ("Mongolia\u2019s president resigns",
         "with elections due within four months."),
    ]),
    ("ALSO ON SATURDAY", [
        ("Gen Z protests spread", "across 25 European countries."),
        ("GTA 6 smashes records", "about $4.9bn in day-one sales."),
        ("Palisades fire arsonist convicted",
         "for the deadly Los Angeles blaze."),
        ("FBI criminal database hacked",
         "as US outages continue, reports say."),
        ("EU approves \u20ac1bn defence aid for Ukraine",
         "as Russia rejects any peace deal."),
    ]),
]

MARKET_LINES = [
    "S&P 500  6,910.42  \u22123.70%      Dow  48,147.33  \u22121.93%      "
    "Nasdaq  22,617.73  \u22125.28%      VIX 35.89",
    "Nvidia  \u221214%      Anthropic  \u22129% (day two, $88.91)      "
    "Seventh straight loss; S&P and Dow in correction",
]


# ---------------------------------------------------------------- sections

def render_masthead(page):
    d = page.draw
    d.text((512, 14), "THE WORLD IN ONE PAGE",
           font=Typefaces.serif_bold(56), fill=PALETTE["ink"], anchor="ma")
    d.text((512, 78),
           "SATURDAY  \u00b7  21 NOVEMBER 2026  \u00b7  ONE DAY, ONE PICTURE",
           font=Typefaces.sans_bold(19), fill=PALETTE["red"], anchor="ma")
    page.hline(110, weight=3)


def render_lead_and_cop(page):
    y = page.label(MARGIN, 122, LEAD["label"])
    y = page.title(MARGIN, y, LEAD["title"], 600, size=32, leading=38)
    page.text_block(MARGIN, y + 4, LEAD["body"], Typefaces.sans(17), 600, 22)
    page.hline(348)

    page.draw.rectangle([664, 122, RIGHT, 336], outline=PALETTE["red"], width=3)
    y2 = page.label(680, 134, COP_BOX["label"], size=16)
    y2 = page.title(680, y2, COP_BOX["title"], 300, size=26, leading=32)
    page.text_block(680, y2 + 4, COP_BOX["body"], Typefaces.sans(15), 300, 20)


def render_features(page):
    box_w, gap = 310, 19
    for i, (kick, head, body) in enumerate(FEATURES):
        x0 = MARGIN + i * (box_w + gap)
        page.draw.rectangle([x0, 352, x0 + box_w, 566],
                            outline=PALETTE["ink"], width=2)
        yy = page.label(x0 + 14, 364, kick, colour=PALETTE["blue"], size=14)
        yy = page.title(x0 + 14, yy, head, box_w - 28, size=24, leading=30)
        page.text_block(x0 + 14, yy + 4, body, Typefaces.sans(16),
                        box_w - 28, 22)


def render_brief_column(page, x0, heading, items, col_w):
    """One of the three 'world in brief' columns."""
    page.draw.text((x0, 626), heading,
                   font=Typefaces.sans_bold(16), fill=PALETTE["blue"])
    yy = 652
    for head, tail in items:
        yy = page.text_block(x0, yy, "\u2022  " + head + " \u2014 " + tail,
                             Typefaces.sans(15), col_w, 20)
        yy += 6
    return yy


def render_brief(page):
    page.hline(584)
    page.draw.text((MARGIN, 594), "THE WORLD IN BRIEF",
                   font=Typefaces.sans_bold(18), fill=PALETTE["red"])
    col_w, gap = 310, 19
    for i, (heading, items) in enumerate(BRIEF_COLUMNS):
        render_brief_column(page, MARGIN + i * (col_w + gap),
                            heading, items, col_w)


def render_markets(page):
    page.draw.rectangle([MARGIN, 894, RIGHT, 962], fill=PALETTE["wash"],
                        outline=PALETTE["ink"], width=2)
    page.draw.text((44, 902), "FRIDAY\u2019S MARKETS \u2014 THE AI ROUT DEEPENS",
                   font=Typefaces.sans_bold(16), fill=PALETTE["red"])
    for i, line in enumerate(MARKET_LINES):
        page.draw.text((44, 924 + i * 20), line,
                       font=Typefaces.sans(15), fill=PALETTE["ink"])


def render_footer(page):
    page.hline(974)
    page.draw.text((MARGIN, 984),
                   "Sources: AP, Reuters, BBC, Le Monde, CNN, Investopedia. "
                   "Every story was reported on 21 November 2026.",
                   font=Typefaces.sans(14), fill=PALETTE["grey"])
    page.draw.text((MARGIN, 1002),
                   "Drawn in code with Pillow  \u00b7  make.fun news-image-20261121",
                   font=Typefaces.sans(14), fill=PALETTE["grey"])


def build_page():
    page = Canvas()
    render_masthead(page)
    render_lead_and_cop(page)
    render_features(page)
    render_brief(page)
    render_markets(page)
    render_footer(page)
    return page


def main():
    build_page().save("entry.png")


if __name__ == "__main__":
    main()
