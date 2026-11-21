import { execFileSync } from "node:child_process";
import { existsSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "out");
const scriptPath = join(repoRoot, "draw_news.py");

execFileSync("python3", [scriptPath, outDir], { stdio: "inherit" });

const target = join(outDir, "entry.png");
if (!existsSync(target)) {
  console.error(`entry.png was not written to ${outDir}`);
  process.exit(1);
}

const size = statSync(target).size;
console.log(`wrote ${target} (${size} bytes)`);
