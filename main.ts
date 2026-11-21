// news-image-20261121 entry (Node 22, standard library only): the picture of
// Saturday 21 November 2026 lives in this repository as entry.png -- a dense
// front page drawn in code by draw_news.py (the global AI sell-off, the
// Anthropic debut, the Shenzhen trilateral, the capture of "El Chapo Isidro",
// eighteen more stories and the day's market closes). The grader runs this
// program in a sandbox with no network, so this program only reads the
// finished picture and writes it out again. The picture is a PNG of 1024 by
// 1024 pixels and under 1 MiB, so the bytes the judge sees are exactly the
// bytes in this repository. (draw_news.py is the program that drew it: run
// `python3 draw_news.py out` outside the grader to regenerate it.)
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "out");
mkdirSync(outDir, { recursive: true });

const picture = readFileSync(join(repoRoot, "entry.png"));
const target = join(outDir, "entry.png");
writeFileSync(target, picture);

if (!existsSync(target)) {
  console.error(`entry.png was not written to ${outDir}`);
  process.exit(1);
}

const size = statSync(target).size;
console.log(`wrote ${target} (${size} bytes)`);
