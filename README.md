# homecubbie.com

The public website for **HomeCubbie** — an offline-first home maintenance and
records app. Three static pages:

| | |
|---|---|
| `index.html` | landing page |
| `privacy.html` | privacy policy — a required URL in App Store Connect |
| `support.html` | support page — also a required URL |

Plain HTML and CSS. No build step, no dependencies. Open `index.html` in a
browser to preview, or `python3 -m http.server` from this directory if you want
the root-relative links in `404.html` to resolve.

Hosted on GitHub Pages at `homecubbie.com`. See `CLAUDE.md` for the rules this
site is written under — chiefly that it loads nothing from third parties, and
that its factual claims have to stay true of the shipped app.

The typeface in `fonts/` is Bricolage Grotesque, used under the SIL Open Font
License; the licence text ships alongside it in `fonts/OFL.txt`.
