# homecubbie.com — project instructions

The public website for HomeCubbie, an offline-first home maintenance and
records app for iOS and Android. Four static pages: a landing page, a privacy
policy, a support page and terms of use, plus a 404. The privacy and support
pages are **required fields in App Store Connect**, which is why this site
exists at all.

This repository is **not** the app. The app lives in a separate private
repository (`HomeCubbie`, sibling directory locally) and its rules — layering,
migrations, `npm run verify` — do not apply here and must not be imported.
Nothing from the app's source belongs in this repo.

## What this site is

Plain HTML and CSS, served by GitHub Pages from the `main` branch. There is no
build step, no framework, no package manager, no `node_modules`. Edit the HTML
and push; that is the whole deployment.

Keep it that way unless there is a reason that survives being said out loud. A
four-page marketing site does not need a bundler. `tools/screens/` holds the
scripts that make the screenshots; they run on a developer's machine against
the app's own web build, and nothing on the site depends on them.

## Non-negotiables

1. **No third-party requests.** No CDN scripts, no Google Fonts, no analytics,
   no tag managers, no embeds, no cookies. The privacy page states in writing
   that this site loads nothing from anyone else — adding a request makes the
   site itself a liar about the product's central claim. The display typeface
   is self-hosted in `fonts/` for exactly this reason.
2. **The copy may not overstate the app.** Every factual claim here has to be
   true of the shipped app. See "Claims and where they come from" below.
3. **Copy must match the screen beside it, and be plain.** A heading that
   promises a boiler service next to a screenshot of a fridge is the reader's
   first reason to distrust everything else on the page. Before changing a
   feature heading, look at the image it sits with. Keep the language
   region-neutral too — no "aeroplane mode", "council tax" or "buildings
   insurance" against screenshots priced in dollars; prefer the ordinary word
   that works everywhere. The sample home is American, so the copy is.

4. **The nine words are fixed**, and are the app's: Property, Place, Thing,
   Task, Policy, Event, Note, Person, Account. Never write "asset", "item",
   "location", "occurrence" or "produce" in user-facing copy — not even in a
   marketing headline where it reads more naturally.
5. **Brand colours are the app's four**, copied into `:root` in `styles.css`
   and not re-picked by eye: Off-White `#F1F1F1`, Champagne `#D9B68C`, Warm
   Sand `#C8BFB1`, Deep Green `#4A5D4E`. Everything else is derived from them.
6. **No real personal data.** Screenshots show the fictional 14 Alder Street
   in `tools/screens/make-house.py`, never a real house. **That rules out the
   app's own "Seed sample data"**: `src/dev/sample-home/sample-home-data.ts` is
   a real household's Notion export with only the serial numbers changed, which
   its own header says. A public repo preserves a mistake in git history even
   after the file is replaced.
7. Pages are hand-written, kebab-case filenames, and **every page works with
   JavaScript disabled**. There is exactly one script, inlined on each page:
   the theme toggle. It is progressive enhancement and must stay that way —
   the control is `display:none` until the script adds `.js` to `<html>`, so a
   reader without JavaScript is never shown a dead button, and the page still
   follows `prefers-color-scheme` as it always did. Do not add a second script
   without a reason that survives being said out loud.

8. **Theming is three-state**: the OS preference by default, or an explicit
   light/dark choice stored in `localStorage` and applied as `data-theme` on
   `<html>` before first paint. Every themed rule therefore needs all three
   selectors — bare `:root`, `@media (prefers-color-scheme: dark)
   :root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. A colour
   defined only inside the media query will not follow the toggle.

9. **The screenshots are theme-aware and cannot be `<picture>`.** A `<source
   media="(prefers-color-scheme: dark)">` only ever answers to the operating
   system, so it ignores the toggle. Each screen is a `div.screen` carrying
   `--shot-light` and `--shot-dark`, with the rules in `styles.css` choosing
   between them; the browser fetches only the one it paints. Keep the
   `role="img"` and `aria-label` — they are the only description a screen
   reader gets. **Both halves of every pair must exist**: a screen added in
   light only will show the wrong theme's image to half the readers.

## Where the artwork comes from

Nothing in `assets/` was drawn by hand. All of it is generated from, or
copied out of, the app repository:

| File | Source |
|---|---|
| `assets/mark.svg` | `assets/images/homecubbie-mark.svg` — the app's mark, unmodified |
| `assets/app-icon.png`, `assets/favicon.png` | `assets/images/icon.png`, `favicon.png` |
| `assets/screens/*.png` | captured from the app's web build by `tools/screens/capture-screens.js` |
| `assets/og.png` | `tools/screens/og.html`, rendered by the same script from the new Now screen |
| the icons inlined in `index.html` | `src/theme/icons.ts`, path for path (house, key, users, wrench, shield, coin, valve, receipt, scan, cal, search, history, file) |
| the tokens in `styles.css` | `src/theme/palette.ts` and the prototype's `:root` block |

The one exception is the sharing diagram in `index.html`, drawn inline as SVG
from the tokens, because the app has no picture of a house, a server and the
lines between them.

**The screens are real captures of the shipped app** (since 2026-11-12), not
renders of `docs/reference/prototype.html`, which stopped matching the app
when onboarding was removed and the Handbook became the House manual.
`tools/screens/README.md` says how to run them. In short: the app's web build
at 390 x 844 and 2x, a fresh browser profile, the fictional house restored from
a backup file the way a person restores one, then six screens in each theme.
The web build is the same code as the phone app; what it lacks is the phone's
status bar and its exact system fonts. Store screenshots still need a device,
and that is board #17's work.

## Claims and where they come from

The privacy page is the one that matters, because a false statement there is a
store-listing problem rather than a typo. Each of these was read out of the app
repository, not assumed, and each should be re-checked against it before being
changed:

| Claim on this site | Where it is true in the app repo |
|---|---|
| No network unless the household shares, and then only its own server | `src/__tests__/no-network.test.ts` — one file, `src/sync/server-client.ts`, may reach a network; it names no address, only `src/domain/sync/sync-session.ts` imports it, and anything else fails the build |
| No server of ours; sharing only through the household's own | `docs/decisions.md` §353; `server/README.md` |
| Encrypted on the phone; the server can't read the house | `docs/reference/sharing-security.md`; `server/__tests__/household-server.test.ts` › "holds nothing anyone could read" |
| The server answers only the home network | `server/__tests__/home-network.test.ts` (the audit's S-5) |
| The server contacts nobody | `server/__tests__/no-outgoing-calls.test.ts` |
| Invites: one use, ten minutes, no password | `server/__tests__/household-server.test.ts`; `docs/decisions.md` §353 |
| A browser is the one exception to "can't read" | `server/README.md`, "One exception: a browser" |
| Removing a phone changes the key; keys never in a backup | `docs/reference/sharing-security.md`, "A lost or stolen phone" |
| Plain http at home, and iOS's local network prompt | `docs/decisions.md` §371; `plugins/with-household-server-cleartext.ts`, `plugins/with-ios-privacy.ts` |
| Documents come down when first opened, or all on Wi-Fi if asked | `src/app/settings/sharing.tsx`, "Download every document on Wi-Fi" |
| Bills, plates and documents read on the phone | board #45 (Vision on iOS, Tesseract on Android), #387 (PDFKit, PDFium), #37 |
| Questions in Search need Apple's on-device model, iPhone only | board #47's commit (`427fcdc`) |
| "Twice a year", "every fall", "first Saturday of the month" | `src/domain/schedules/schedule-phrase.ts`, the table in its header |
| Weekly automatic backup, kept on the phone | `docs/reference/backup-format.md`, "Automatic backups" |
| On Android, a folder picked once gets every automatic backup and the readable copy; "Stop copying" ends it | `docs/decisions.md` §374, §379; `src/backup/backup-file.ts` `canKeepBackupFolder` (Android only); `src/app/settings/backup.tsx` |
| The readable copy leaves out "Hidden until tapped" | `docs/decisions.md` §379; `docs/reference/backup-format.md`, "The readable copy of the house" |
| One Property per install | `docs/reference/context.md` §4 |
| A ring per room and for the house: what came due in the last 30 days, open while anything is late | `docs/decisions.md` §381; `src/domain/queries/kept-up.ts` |
| "More than 250" common tasks, suggested by room, each with a schedule and a time estimate; nothing added until you say so | `src/domain/tasks/task-library.ts` (`LIBRARY_TASKS`, 277 on 2026-11-12), `src/domain/tasks/task-suggestions.ts`; the sheet's own sentence |
| "It looks like…" suggests a Policy, bill, receipt or manual, and says why | board #45; `src/domain/queries/scan-triage-view.ts` `SCAN_KINDS` |
| Renewal reminders | `src/domain/reminders/reminder-plan.ts`: a policy term reminds twice before it ends |
| People: call from the app, copy the email | `src/components/call-sheet.tsx`; `src/app/records/person/[id].tsx` (email is a copy row, not a compose link) |
| A year in review | `src/app/records/year/[year].tsx` (board #219, #358) |
| A deleted document comes back for 30 days | board #355, Settings › Recently deleted |
| iOS 16.4 or later; Android 7.0 or later | the Expo template's `ios.deploymentTarget` default `16.4` (`node_modules/expo/template.tgz`, Podfile); Android `minSdk` default 24 |
| No analytics or crash reporting | no such dependency in `package.json` |
| Camera only, never the photo library | `app.json` → `expo-image-picker`, `photosPermission: false`. Its prompt says photos go only to the household's own server, locked, and nothing to us: board #446, `e403ee41` |
| Files shared in from other apps stay on the phone, with no new permission | `plugins/with-share-target.ts` (Android), `plugins/with-share-extension.ts` (iPhone, "sends nothing"); `docs/decisions.md` §378, §380 |
| Biometrics ask the OS and store nothing | `expo-local-authentication`; `docs/decisions.md` §158 |
| While locked, the app switcher hides the screen: a full blur on iPhone, blank on Android 13 or later | the audit's S-7, commit `bd19a3c` (`expo-screen-capture` on iOS, `modules/recents-screenshot` on Android 13+) |
| Local notifications only, no push | `plugins/with-push-disabled.ts`; the `aps-environment` entitlement is removed in `plugins/with-ios-privacy.ts` |
| Excluded from OS cloud backups | `plugins/with-backups-disabled.ts`; `app.json` → `allowBackup: false` |
| Strongest iOS file protection | `plugins/with-ios-privacy.ts`, `com.apple.developer.default-data-protection` |
| A backup file is a plain, unencrypted zip | `docs/reference/backup-format.md` |

**Nothing enforces this table.** The app's documentation is guarded by tests
that fail the build on drift; this repository is a different repository and no
test here can see the app. If the app ever gains a network call, the privacy
page keeps saying it does not, and nothing anywhere notices. So: when the app
changes what it collects, transmits, or asks permission for, changing this site
is part of that work, not a follow-up.

The app is not yet in either store. The landing page says "Coming soon to
iPhone and Android" and links to no store — replace that with the real links on
the day it ships, and not before. Store badges are only for an app that is in
the store.

## Deploying

Currently a **private** repository with Pages switched off, by intent — the
site is being written before the app ships.

What homecubbie.com serves today (checked 2026-11-12): Squarespace's default
"Coming Soon" page. The domain's nameservers are Squarespace's
(`nsd1`–`nsd4.squarespacedns.com`) and its A records are Squarespace's, so
nothing from this repository is live. It has **no MX record**, so
`support@homecubbie.com` cannot receive mail yet.

A GitHub Pages site is always deployed by a GitHub Actions run, even from a
branch (GitHub's docs and its 2022 post, "GitHub Pages now uses Actions by
default"). On a public repository those runs are free and unlimited; on a
private one they spend the account's Actions minutes, and private Pages needs a
paid plan. The owner wants no Actions runs or charges, so which host serves
this site is the owner's decision.

To go live: make the repository public (GitHub Pages from a private repo needs
a paid plan, and the served pages are public either way), then Settings →
Pages → deploy from `main` / root. `CNAME` already contains `homecubbie.com`,
so set the custom domain to match, add the DNS records at the registrar, wait
for the certificate, and tick **Enforce HTTPS**. Do not hand either URL to App
Store Connect until `https://` loads clean.

`support@homecubbie.com` needs to exist and forward somewhere the owner reads
before the support page is submitted. Most registrars include free forwarding.
