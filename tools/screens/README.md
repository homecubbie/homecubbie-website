# The screenshots

`assets/screens/*.png` and `assets/og.png` are made here, from the real app.
Run this whenever a screen the site shows changes in the app.

## The house in them is invented

Every screen shows **14 Alder Street**, a house that does not exist.
`make-house.py` writes it as a HomeCubbie backup file. It has 13 places,
8 Things, 13 tasks, car, home and appliance policies, five billed accounts, a
few repairs and the usual notes. Phone numbers are in the 555-01xx range, which
is reserved for fiction. Brand and model numbers name products, not people.

**Don't use the app's "Seed sample data" instead.** That sample is a real
household's Notion export with only the serial numbers changed. Its header in
`src/dev/sample-home/sample-home-data.ts` says so, and the site's rule 6 rules
it out.

## Running it

1. In the app repository, start its web build on a spare port. Run it through
   `~/.claude/bin/heavy-run`, so it doesn't overlap another heavy job:

   ```sh
   cd ../HomeCubbie
   CI=1 EXPO_NO_TELEMETRY=1 npx expo start --web --port 8090
   ```

2. From this repository:

   ```sh
   node tools/screens/capture-screens.js            # app at ../HomeCubbie, server at :8090
   node tools/screens/capture-screens.js <app> <url>
   ```

   It borrows Playwright from the app's `node_modules`, so this repository
   still has no package manager. It works in a fresh browser profile and
   deletes it afterwards. The steps:
   - the empty app writes one backup, whose manifest supplies the table list
     and schema version;
   - `make-house.py` writes 14 Alder Street in that format;
   - Settings › Restore loads it, as a person would restore a backup;
   - six screens are captured in light and in dark, at 390 x 844 and 2x;
   - `og.html` is rendered to `assets/og.png`.

3. Stop the web server, then check the site in a browser in both themes before
   committing.

## When it breaks

- **The restore fails with "Error finalizing statement".** A database rule
  turned a row down, and the restore changed nothing. The rules are in the
  app's `src/db/migrations`. The first run found one: a Policy must have a
  provider.
- **A click times out.** A screen was renamed. The `SCREENS` list in
  `capture-screens.js` names the text it clicks: Kitchen, Fridge, Car insurance.
- **Now looks different.** Due dates come from each schedule's start date in
  `make-house.py`, and the app works out what's due from today's date. Move
  the start dates so Now shows a couple of things today and a handful this
  week.
