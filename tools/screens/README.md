# The screenshots

`assets/screens/*.png` and `assets/og.png` are made here, from the real app.
Run this whenever a screen the site shows changes in the app.

## The house in them is invented

Every screen shows **14 Alder Street**, a house that does not exist.
`make-house.py` writes it as a HomeCubbie backup file. It has 13 places,
8 Things, 13 tasks on a schedule and one that happens once, car, home and
appliance policies, five billed accounts with one bill to pay, a few repairs
and the usual notes. Phone numbers are in the 555-01xx range, which
is reserved for fiction. Brand and model numbers name products, not people.

**Don't use the app's "Seed sample data" instead.** Only this invented house
goes on the site.

## Running it

1. In the app repository, serve its web build on a spare port. An exported
   build is the one to use, because it has nothing in it that only development
   has; the development server works too. Run it through
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
   - nine screens are captured in light and in dark, at 390 x 844 and 2x;
   - `og.html` is rendered to `assets/og.png`.

   When only the mark in `og.png` has changed, `--og-only` renders it again
   from the screens already in `assets/screens`. It needs no running app:

   ```sh
   node tools/screens/capture-screens.js --og-only
   ```

3. Stop the web server. `laptop-light.png` and `laptop-dark.png` come from the
   app repository instead, because they show a browser joined to a household's
   own server: `tools/web-app/laptop-picture.live.test.ts` there says how. It
   reads the same `make-house.py`.

4. Check the site in a browser in both themes before committing.

## When it breaks

- **The restore fails with "Error finalizing statement".** A database rule
  turned a row down, and the restore changed nothing. The rules are in the
  app's `src/db/migrations`. The first run found one: a Policy must have a
  provider.
- **It prints errors the app logged.** The web build runs in development, so
  an error shows as a red toast over the tab bar. The script closes it before
  each screenshot, because a release build has no such overlay, and prints
  every error at the end. Report them to the app. The first was a ring that
  handed an SVG group `origin`, which the web turns into an invalid
  `transform-origin` attribute.
- **A click times out.** A screen was renamed. The `SCREENS` list in
  `capture-screens.js` names the text it clicks: Kitchen, Fridge, Car insurance.
- **Now looks different.** Every date in `make-house.py` is written as it stood
  on 12 November 2026. Tasks, policies and the bill to pay move by the days
  since, and the other bills by the months, so any day shows nothing late, two
  due today, a handful this week and no cover run out. If Now still looks
  wrong, the app's rules for what's due have changed: move the dates written
  there. Costs is the exception: it's drawn by calendar year, so a capture in
  the first months of a year shows a short one.
