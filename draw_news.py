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

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (29, 78, 137)
GREY = (90, 86, 78)
LIGHT = (232, 226, 212)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading=25, fill=INK):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, fill=RED, size=17):
    draw.text((x, y), text, font=font(SANS_B, size), fill=fill)
    return y + 24


def headline(draw, x, y, text, width, size=33, leading=40):
    fnt = font(SERIF_B, size)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=INK)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=4)

    # ---- Masthead ----
    d.text((512, 14), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.text((512, 78), "SATURDAY  \u00b7  21 NOVEMBER 2026  \u00b7  ONE DAY, ONE PICTURE",
           font=font(SANS_B, 19), fill=RED, anchor="ma")
    rule(d, 28, 110, 996, 3)

    # ---- Lead: Kyiv / Poland (left) + COP31 box (right) ----
    y = kicker(d, 28, 122, "KYIV  \u00b7  AND POLAND")
    y = headline(d, 28, y, "Russia\u2019s biggest barrage hits Kyiv \u2014 and lands in Poland", 600, 32, 38)
    y = para(d, 28, y + 4,
             "More than 400 drones and 110 missiles rain down overnight, "
             "27 of them ballistic; at least eight are killed in Kyiv as "
             "bridges and the power grid are hit. Two Russian missiles and "
             "a suspected drone then land in Poland \u2014 PM Donald Tusk "
             "calls it an \u201cintentional provocation\u201d.",
             font(SANS, 17), 600, 22)
    rule(d, 28, 348, 996, 2)

    # ---- COP31 box ----
    d.rectangle([664, 122, 996, 336], outline=RED, width=3)
    y2 = kicker(d, 680, 134, "ANTALYA  \u00b7  CLIMATE TALKS", fill=RED, size=16)
    y2 = headline(d, 680, y2, "COP31 stalls in overtime", 300, 26, 32)
    y2 = para(d, 680, y2 + 4,
              "The draft deal strips out every mention of fossil fuels; "
              "the $120bn adaptation target is dropped and the closing "
              "plenary suspended. Addis Ababa hosts COP32 in 2027.",
              font(SANS, 15), 300, 20)

    # ---- Three feature boxes ----
    boxes = [
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
    bx, bw, gap = 28, 310, 19
    for i, (kick, head, body) in enumerate(boxes):
        x0 = bx + i * (bw + gap)
        d.rectangle([x0, 352, x0 + bw, 566], outline=INK, width=2)
        yy = kicker(d, x0 + 14, 364, kick, fill=BLUE, size=14)
        yy = headline(d, x0 + 14, yy, head, bw - 28, 24, 30)
        para(d, x0 + 14, yy + 4, body, font(SANS, 16), bw - 28, 22)

    # ---- Three columns of short items ----
    rule(d, 28, 584, 996, 2)
    d.text((28, 594), "THE WORLD IN BRIEF", font=font(SANS_B, 18), fill=RED)
    cols = [
        ("EUROPE & THE WAR", [
            ("Zelensky calls Putin \u201cenemy and killer\u201d", "after Trump calls him a friend."),
            ("NATO jets scrambled over Poland", "Polish F-16s and Swedish Gripens answer."),
            ("France seeks a UN Security Council meeting", "after strikes hit the Austrian embassy."),
            ("Britain: Poland incursion \u201cutterly unacceptable\u201d", "says PM Andy Burnham."),
            ("Spain heads to a 29 November election", "as the conservatives gain."),
        ]),
        ("THE GULF & BEYOND", [
            ("Iran downs a US MQ-9 drone", "over the Strait of Hormuz, the 58th."),
            ("Lewis Pugh swims the Hormuz strait", "to spotlight the war\u2019s toll on wildlife."),
            ("Israeli strikes kill Palestinians in Gaza", "as West Bank violence continues."),
            ("Salvadoran troops in Haiti lose soldiers", "to explosives in Port-au-Prince."),
            ("Mongolia\u2019s president resigns", "with elections due within four months."),
        ]),
        ("ALSO ON SATURDAY", [
            ("Gen Z protests spread", "across 25 European countries."),
            ("GTA 6 smashes records", "about $4.9bn in day-one sales."),
            ("Palisades fire arsonist convicted", "for the deadly Los Angeles blaze."),
            ("FBI criminal database hacked", "as US outages continue, reports say."),
            ("EU approves \u20ac1bn defence aid for Ukraine", "as Russia rejects any peace deal."),
        ]),
    ]
    cx, cw = 28, 310
    for i, (title, items) in enumerate(cols):
        x0 = cx + i * (cw + 19)
        d.text((x0, 626), title, font=font(SANS_B, 16), fill=BLUE)
        yy = 652
        for head, tail in items:
            yy = para(d, x0, yy, "\u2022  " + head + " \u2014 " + tail,
                      font(SANS, 15), cw, 20)
            yy += 6

    # ---- Markets strip (Friday's closes) ----
    d.rectangle([28, 894, 996, 962], fill=LIGHT, outline=INK, width=2)
    d.text((44, 902), "FRIDAY\u2019S MARKETS \u2014 THE AI ROUT DEEPENS",
           font=font(SANS_B, 16), fill=RED)
    d.text((44, 924),
           "S&P 500  6,910.42  \u22123.70%      Dow  48,147.33  \u22121.93%      Nasdaq  22,617.73  \u22125.28%      VIX 35.89",
           font=font(SANS, 15), fill=INK)
    d.text((44, 944),
           "Nvidia  \u221214%      Anthropic  \u22129% (day two, $88.91)      Seventh straight loss; S&P and Dow in correction",
           font=font(SANS, 15), fill=INK)

    # ---- Footer ----
    rule(d, 28, 974, 996, 2)
    d.text((28, 984),
           "Sources: AP, Reuters, BBC, Le Monde, CNN, Investopedia. Every story was reported on 21 November 2026.",
           font=font(SANS, 14), fill=GREY)
    d.text((28, 1002),
           "Drawn in code with Pillow  \u00b7  make.fun news-image-20261121",
           font=font(SANS, 14), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
