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
| `robots.txt`, `sitemap.xml` | every crawler welcome; the four pages and when each last changed |
| `llms.txt` | a short summary of the app and the pages, for AI assistants |
| `7332d2da18e62f4f7d2046984d08d77f.txt` | the IndexNow key, for telling Bing a page changed; see `CLAUDE.md` |
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
