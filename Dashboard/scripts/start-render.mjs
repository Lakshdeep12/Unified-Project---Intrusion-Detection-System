import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const serverEntry = resolve(".output/server/index.mjs");

if (!existsSync(serverEntry)) {
  console.log("Production server output is missing; running build first.");

  const result = spawnSync("npm", ["run", "build"], {
    stdio: "inherit",
    shell: true,
  });

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

await import(pathToFileURL(serverEntry).href);
