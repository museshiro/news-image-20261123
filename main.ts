// news-image-20261123: copy the rendered front page to the output dir.
// The image is drawn at build time by draw_frontpage.py (Pillow) and
// shipped in this repository as entry.png, so this program is fully
// deterministic: two runs write byte-identical output.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
