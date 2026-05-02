import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const serverEntry = resolve(".output/server/index.mjs");

process.env.NITRO_HOST ||= process.env.HOST || "0.0.0.0";
process.env.NITRO_PORT ||= process.env.PORT || "3000";

if (!existsSync(serverEntry)) {
  console.error(
    "Production server output is missing. Run `npm run build` before `npm run start`.",
  );
  process.exit(1);
}

await import(pathToFileURL(serverEntry).href);
