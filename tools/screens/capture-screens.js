// Captures assets/screens/*.png from the HomeCubbie app's web build, showing
// the fictional house in make-house.py. See README.md for when and how.
//
//   node tools/screens/capture-screens.js [path-to-app-repo] [base-url]
//
// Defaults: ../HomeCubbie beside this repository, http://localhost:8090.
// Uses a fresh browser profile each run, so nothing of anyone's real house
// can be in it: the app starts empty, writes one backup (the template for the
// table list and schema version), and is then restored from the fictional one.
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

const SITE = path.resolve(__dirname, "../..");
const APP = path.resolve(process.argv[2] || path.join(SITE, "../HomeCubbie"));
const BASE = process.argv[3] || "http://localhost:8090";
const { chromium } = require(path.join(APP, "node_modules/playwright"));

const SCREENS = [
  ["now", [["goto", "/"]]],
  ["home", [["goto", "/home"]]],
  ["thing", [["goto", "/home"], ["click", "Kitchen"], ["click", "Fridge"]]],
  ["policy", [["goto", "/records/policies"], ["click", "Car insurance"]]],
  ["costs", [["goto", "/costs"]]],
  ["house", [["goto", "/home/about"]]],
];

async function open(profile, scheme) {
  const ctx = await chromium.launchPersistentContext(profile, {
    viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: scheme, acceptDownloads: true,
  });
  return [ctx, ctx.pages()[0] || (await ctx.newPage())];
}

async function go(page, route) {
  await page.goto(BASE + route, { waitUntil: "load", timeout: 240000 });
  await page.waitForTimeout(2500);
}

(async () => {
  const work = fs.mkdtempSync(path.join(os.tmpdir(), "hc-screens-"));
  const profile = path.join(work, "profile");
  let [ctx, page] = await open(profile, "light");

  // 1. A template backup from the empty app: its manifest names every table.
  await go(page, "/");
  await go(page, "/settings/backup");
  const download = page.waitForEvent("download", { timeout: 60000 });
  await page.getByText("Create a backup now", { exact: true }).click();
  const template = path.join(work, "template.zip");
  await (await download).saveAs(template);
  fs.mkdirSync(path.join(work, "template"));
  execFileSync("unzip", ["-q", template, "-d", path.join(work, "template")]);

  // 2. The fictional house, written in that format.
  const house = path.join(work, "alder-street.zip");
  console.log(execFileSync("python3", ["-I", path.join(__dirname, "make-house.py"), path.join(work, "template"), house]).toString().trim());

  // 3. Restored the way a person would restore a backup.
  await go(page, "/settings/restore");
  const chooser = page.waitForEvent("filechooser", { timeout: 20000 });
  await page.getByText("Choose a backup file…", { exact: true }).click();
  await (await chooser).setFiles(house);
  await page.waitForTimeout(4000);
  await page.getByText("Replace my data", { exact: true }).last().click();
  await page.waitForTimeout(8000);
  const restored = await page.evaluate(() => document.body.innerText);
  if (!/rows are back/.test(restored)) throw new Error("The restore did not finish:\n" + restored.slice(0, 800));
  await ctx.close();

  // 4. Six screens, light and dark.
  for (const scheme of ["light", "dark"]) {
    [ctx, page] = await open(profile, scheme);
    for (const [name, steps] of SCREENS) {
      for (const [op, arg] of steps) {
        if (op === "goto") await go(page, arg);
        if (op === "click") { await page.getByText(arg, { exact: true }).first().click({ timeout: 20000 }); await page.waitForTimeout(1800); }
      }
      await page.mouse.move(0, 0);
      await page.waitForTimeout(600);
      const file = path.join(SITE, "assets/screens", `${name}-${scheme}.png`);
      await page.screenshot({ path: file });
      console.log("wrote", path.relative(SITE, file));
    }
    await ctx.close();
  }

  // 5. The link preview, built from the new Now screen.
  const browser = await chromium.launch();
  const og = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await og.goto("file://" + path.join(__dirname, "og.html"));
  await og.waitForTimeout(800);
  await og.screenshot({ path: path.join(SITE, "assets/og.png") });
  await browser.close();
  console.log("wrote assets/og.png");

  fs.rmSync(work, { recursive: true, force: true });
})().catch((e) => { console.error(e); process.exit(1); });
