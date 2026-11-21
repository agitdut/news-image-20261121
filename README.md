# The Day in One Picture — Saturday, 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/agitdut/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/agitdut/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page that sums up the world's news of
Saturday, 21 November 2026, in a single 1024×1024 image.

## What is on the page

- **Lead story:** the global AI-driven market sell-off — the S&P 500 down
  3.7%, the Nasdaq turning negative for the year, the Nikkei down 5.1%.
- **Three featured stories:** Anthropic's $2 trillion stock-market debut
  stumbling, the Trump–Xi–Putin trilateral summit in Shenzhen, and
  Mexico's capture of FBI most-wanted cartel boss "El Chapo Isidro".
- **Eighteen more stories** from around the world: the Russian missile
  strike on Kryvyi Rih, the violation of Polish airspace, the ICJ's
  Rohingya genocide ruling on Myanmar, COP31 running past its deadline,
  Nvidia halting H200 chip exports to China, GTA 6's $3.79bn first day,
  BepiColombo reaching Mercury, a dengue breakthrough in Brazil, a
  magnitude 6.8 quake off Timor-Leste, a drone attack on a Russian cargo
  ship, UN talks on autonomous weapons, Vietnam ending the death penalty
  for drug trafficking, the EU's €7.9bn payment to Ukraine, a proposed
  3% EU tax on big tech, Iran's claimed downing of a US drone, Denmark's
  planned expulsion of a Russian envoy, tanker attacks near Hormuz, and
  Leeds United's 4–1 win at Chelsea.
- **A markets strip** with the day's index moves, and a source line.

Every fact was checked against reporting published on 21 November 2026
(AP, Reuters, BBC, NYT, Le Monde, CNN).

## How it works

`main.ts` (Node 22+) runs `draw_news.py`, a Pillow program that draws
the whole front page from fixed strings and fixed geometry — masthead,
lead story, featured row, markets strip, and a three-column story grid.
No network, no clock, no randomness: running it twice writes
byte-identical files.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024, under 1 MiB).

## Files

- `draw_news.py` — draws the front page.
- `main.ts` — entrypoint; runs the Python program and checks the output.
- `entry.png` — the generated front page.
- `package.json` — package metadata.
- `LICENSE` — MIT.
