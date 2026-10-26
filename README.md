<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo-on-dark.svg">
  <img src="assets/logo-on-light.svg" alt="Cabinwright" width="312" height="64">
</picture>

The website for **Cabinwright**, an open-source app store and tweak platform for Kia and
Hyundai head units running [NEMESIS](https://github.com/xwtk/hmg_nemesis). Served by GitHub
Pages at <https://cabinwright.github.io/>.

Not affiliated with Kia, Hyundai or Mobis.

| File | What |
|---|---|
| `index.html` | The landing page: what Cabinwright is, the store's apps (from [`apps/index.json`](https://cabinwright.github.io/apps/index.json) when it can, a built-in list when it can't), and three steps to start. |
| `docs/` | The docs: install, safety and undo, developers, roadmap. Plain HTML pages that share the site's nav. Detail goes here, not on the landing page. |
| `style.css` | Shared by every page. Static, no build step, no trackers, no web fonts. |
| `logo.svg` | Mark and wordmark; follows the viewer's light or dark scheme. |
| `assets/logo-on-dark.svg`, `assets/logo-on-light.svg` | The same, fixed for one background. |
| `logo-mark.svg` | The mark alone, transparent; follows light or dark. |
| `app-icon.svg`, `app-icon-512.png` | The mark on a round tile like the head unit's icons. |
| `favicon.svg`, `favicon.ico` (16, 32, 48), `favicon-32.png`, `apple-touch-icon.png` (180, from `assets/apple-touch-icon.svg`) | Browser icons. |
| `tools/render-icons.sh` | Renders the PNGs and the ICO from the SVGs with headless Firefox; `tools/pngtool.py` recovers transparency and packs the ICO (Python 3, standard library only). |

## Look

The colours are the head unit's own, as the Cabinwright API's `CarPage` uses them
([menu](https://github.com/cabinwright/menu), `api/ui`): night background `#121214`, cards
`#161618` with a `#313136` edge, icon tiles `#1F1F24` / `#3D3D44`, text `#B6C1C8`, muted
`#79838A`, and the highlight teal `#17BEB0`. The mark uses the stock icons' gradient,
`#34E0D5` to `#847FDC`. The light scheme uses the day colours (`#F0F0F0`, edge `#CBCBCB`) with
text and teal darkened to pass WCAG AA.

The mark is a cabin whose roof is a carpenter's square (the "wright"), over a screen. Only the
colours come from the head unit; no manufacturer logo, font or artwork is used.

## Editing

Open `index.html` in a browser, or serve the folder (`python3 -m http.server`) to try the live
app list. After changing an icon SVG, run `sh tools/render-icons.sh`.

## License

MIT (see `LICENSE`), Copyright (c) 2026 hazptr.
