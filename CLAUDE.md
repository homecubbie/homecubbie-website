# homecubbie.com — project instructions

The public website for HomeCubbie, an offline-first home maintenance and
records app for iOS and Android. Three static pages: a landing page, a privacy
policy, and a support page. The last two are **required fields in App Store
Connect**, which is why this site exists at all.

This repository is **not** the app. The app lives in a separate private
repository (`HomeCubbie`, sibling directory locally) and its rules — layering,
migrations, `npm run verify` — do not apply here and must not be imported.
Nothing from the app's source belongs in this repo.

## What this site is

Plain HTML and CSS, served by GitHub Pages from the `main` branch. There is no
build step, no framework, no package manager, no `node_modules`. Edit the HTML
and push; that is the whole deployment.

Keep it that way unless there is a reason that survives being said out loud. A
three-page marketing site does not need a bundler.

## Non-negotiables

1. **No third-party requests.** No CDN scripts, no Google Fonts, no analytics,
   no tag managers, no embeds, no cookies. The privacy page states in writing
   that this site loads nothing from anyone else — adding a request makes the
   site itself a liar about the product's central claim. The display typeface
   is self-hosted in `fonts/` for exactly this reason.
2. **The copy may not overstate the app.** Every factual claim here has to be
   true of the shipped app. See "Claims and where they come from" below.
3. **The nine words are fixed**, and are the app's: Property, Place, Thing,
   Task, Policy, Event, Note, Person, Account. Never write "asset", "item",
   "location", "occurrence" or "produce" in user-facing copy — not even in a
   marketing headline where it reads more naturally.
4. **Brand colours are the app's four**, copied into `:root` in `styles.css`
   and not re-picked by eye: Off-White `#F1F1F1`, Champagne `#D9B68C`, Warm
   Sand `#C8BFB1`, Deep Green `#4A5D4E`. Everything else is derived from them.
5. **No real personal data.** Screenshots must come from a seeded demo
   property, never the owner's actual house. A public repo preserves a mistake
   in git history even after the file is replaced.
6. Pages are hand-written, kebab-case filenames, and **every page works with
   JavaScript disabled**. There is exactly one script, inlined on each page:
   the theme toggle. It is progressive enhancement and must stay that way —
   the control is `display:none` until the script adds `.js` to `<html>`, so a
   reader without JavaScript is never shown a dead button, and the page still
   follows `prefers-color-scheme` as it always did. Do not add a second script
   without a reason that survives being said out loud.

7. **Theming is three-state**: the OS preference by default, or an explicit
   light/dark choice stored in `localStorage` and applied as `data-theme` on
   `<html>` before first paint. Every themed rule therefore needs all three
   selectors — bare `:root`, `@media (prefers-color-scheme: dark)
   :root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. A colour
   defined only inside the media query will not follow the toggle.

8. **The screenshots are theme-aware and cannot be `<picture>`.** A `<source
   media="(prefers-color-scheme: dark)">` only ever answers to the operating
   system, so it ignores the toggle. Each screen is a `div.screen` carrying
   `--shot-light` and `--shot-dark`, with the rules in `styles.css` choosing
   between them; the browser fetches only the one it paints. Keep the
   `role="img"` and `aria-label` — they are the only description a screen
   reader gets. **Both halves of every pair must exist**: a screen added in
   light only will show the wrong theme's image to half the readers.

## Where the artwork comes from

Nothing in `assets/` was drawn here. All of it is generated from, or copied
out of, the app repository:

| File | Source |
|---|---|
| `assets/mark.svg` | `assets/images/homecubbie-mark.svg` — the app's mark, unmodified |
| `assets/app-icon.png`, `assets/favicon.png` | `assets/images/icon.png`, `favicon.png` |
| `assets/screens/*.png` | rendered from `docs/reference/prototype.html` |
| the tokens in `styles.css` | `src/theme/palette.ts` and the prototype's `:root` block |

The screens were produced by driving `docs/reference/prototype.html` in
headless Chrome: a 390 x 844 viewport in an iframe (Chrome will not open a
window narrower than 500px, so the phone is an iframe inside a wider window and
the shot is cropped to it), `themePref` set to `light` and `dark` for the two
halves of each `<picture>`, and the empty `.toast`/`.sheet` scaffolding hidden.
The content is the fictional sample home — Honda CR-V, LG fridge, 14 Alder
Street — which is what rule 5 above is asking for.

**These are renders of the prototype, not captures of the shipped app.** The
prototype is the app's visual target and the two are meant to match, but no
test checks that they still do, and a marketing image showing a screen the app
does not have is exactly the kind of overstatement rule 2 exists to stop.
Before the site goes public, replace `assets/screens/` with real captures from
a device or simulator running the seeded sample home
(`src/dev/sample-home/seed-sample-home.ts`) — which is work the App Store
listing needs anyway.

## Claims and where they come from

The privacy page is the one that matters, because a false statement there is a
store-listing problem rather than a typo. Each of these was read out of the app
repository, not assumed, and each should be re-checked against it before being
changed:

| Claim on this site | Where it is true in the app repo |
|---|---|
| No network requests of any kind | `src/__tests__/no-network.test.ts` — fails the build on a call, a dependency, or a URL literal |
| No analytics or crash reporting | no such dependency in `package.json` |
| Camera only, never the photo library | `app.json` → `expo-image-picker`, `photosPermission: false` |
| Biometrics ask the OS and store nothing | `expo-local-authentication`; `docs/decisions.md` §158 |
| Local notifications only, no push | `plugins/with-push-disabled.ts`; the `aps-environment` entitlement is removed in `plugins/with-ios-privacy.ts` |
| Excluded from OS cloud backups | `plugins/with-backups-disabled.ts`; `app.json` → `allowBackup: false` |
| Strongest iOS file protection | `plugins/with-ios-privacy.ts`, `com.apple.developer.default-data-protection` |
| Backup export is user-initiated only | `expo-sharing`; `docs/reference/backup-format.md` |

**Nothing enforces this table.** The app's documentation is guarded by tests
that fail the build on drift; this repository is a different repository and no
test here can see the app. If the app ever gains a network call, the privacy
page keeps saying it does not, and nothing anywhere notices. So: when the app
changes what it collects, transmits, or asks permission for, changing this site
is part of that work, not a follow-up.

The app is not yet on the App Store. The landing page says "Coming to the App
Store" and links to nothing — replace that with the real link on the day it
ships, and not before.

## Deploying

Currently a **private** repository with Pages switched off, by intent — the
site is being written before the app ships.

To go live: make the repository public (GitHub Pages from a private repo needs
a paid plan, and the served pages are public either way), then Settings →
Pages → deploy from `main` / root. `CNAME` already contains `homecubbie.com`,
so set the custom domain to match, add the DNS records at the registrar, wait
for the certificate, and tick **Enforce HTTPS**. Do not hand either URL to App
Store Connect until `https://` loads clean.

`support@homecubbie.com` needs to exist and forward somewhere the owner reads
before the support page is submitted. Most registrars include free forwarding.
