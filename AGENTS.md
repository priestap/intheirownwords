# Project conventions

- Use inline SVG icons with `currentColor` for interface arrows and other UI symbols that could render as emoji on iOS. Do not use Unicode arrow glyphs for links, navigation, downloads, or buttons.
- Decorative SVGs must have `aria-hidden="true"` and `focusable="false"`; retain descriptive text for the link or button.
- Edit the page templates and `scripts/build.py`, then regenerate both committed HTML pages with `python3 scripts/build.py`. Run `python3 scripts/check.py` and `node --check app.js` before finishing.
