# Center for the Study of Statesmanship — static site

A Jekyll rebuild of [css.cua.edu](https://web.archive.org/web/20250317025935/https://css.cua.edu/) as archived on
17 March 2025 — homepage and every sub-page (news, Ideas & Commentary, Epistulae, NHI Bulletins, Video & Audio,
events, team bios and groups) — reproducing its design and copy on the same architecture as jaskonas.com
(Jekyll / GitHub Pages, data-driven nav and lists, token-based Sass with light and dark modes, small vanilla JS).

```bash
bundle install
bundle exec jekyll serve   # http://localhost:4000
```

All content is native: images and PDFs are mirrored under `uploads/`, and URLs match the original site's paths.
