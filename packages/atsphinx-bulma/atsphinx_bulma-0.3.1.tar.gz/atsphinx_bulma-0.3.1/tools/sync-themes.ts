/**
 * Sync Bulma and Bulmaswatch versions into themes.
 */
import bulma from "bulma/package.json";
import bulmaswatch from "bulmaswatch/package.json";

console.log(`Bulma version:       ${bulma.version}`);
console.log(`Bulmaswatch version: ${bulmaswatch.version}`);
console.log("");

const targets: { [path: string]: ((text: string) => string)[] } = {
  "src/atsphinx/bulma/themes/bulma_basic/theme.toml": [
    (text: string): string =>
      text.replace(
        /bulma_version = ".*"/,
        `bulma_version = "${bulma.version}"`,
      ),
    (text: string): string =>
      text.replace(
        /bulmaswatch_version = ".*"/,
        `bulmaswatch_version = "${bulmaswatch.version}"`,
      ),
  ],
  "docs/theme.rst": [
    (text) => {
      const lines = text.split("\n");
      const mark = lines.findIndex((line) =>
        line.includes(".. confval:: bulma_version"),
      );
      lines[mark + 2] = lines[mark + 2].replace(/".*"/, `"${bulma.version}"`);
      return lines.join("\n");
    },
    (text) => {
      const lines = text.split("\n");
      const mark = lines.findIndex((line) =>
        line.includes(".. confval:: bulmaswatch_version"),
      );
      lines[mark + 2] = lines[mark + 2].replace(
        /".*"/,
        `"${bulmaswatch.version}"`,
      );
      return lines.join("\n");
    },
  ],
};

for (const [path, rules] of Object.entries(targets)) {
  console.log(path);
  let content = await Bun.file(path).text();
  for (const rule of rules) {
    content = rule(content);
  }
  await Bun.write(path, content);
}
