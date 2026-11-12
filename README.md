# homecubbie.com

The public website for **HomeCubbie**, an offline-first home maintenance and
records app.

| | |
|---|---|
| `index.html` | landing page |
| `privacy.html` | privacy policy — a required URL in App Store Connect |
| `support.html` | support page — also a required URL |
| `terms.html` | terms of use |
| `404.html` | page not found |
| `tools/screens/` | makes the screenshots from the app's web build; see its README |

Plain HTML and CSS. No build step, no dependencies. Open `index.html` in a
browser to preview it, or run `python3 -m http.server` from this directory so
the root-relative links in `404.html` resolve.

To be hosted at `homecubbie.com`; `CLAUDE.md` says where that stands. Read
`CLAUDE.md` for the rules this site is written under. The main ones: it loads
nothing from third parties, and every claim it makes has to stay true of the
shipped app.

The typeface in `fonts/` is Bricolage Grotesque, used under the SIL Open Font
License; the licence text ships alongside it in `fonts/OFL.txt`.
