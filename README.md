# Center for the Study of Statesmanship — static site

A Jekyll rebuild of the homepage of [css.cua.edu](https://web.archive.org/web/20250317025935/https://css.cua.edu/)
as archived on 17 March 2025, reproducing its design and copy on the same
architecture as jaskonas.com (Jekyll / GitHub Pages, data-driven nav and lists,
token-based Sass with light and dark modes, small vanilla JS).

```bash
bundle install
bundle exec jekyll serve   # http://localhost:4000
```

Pages that were not cloned (Events, Donate, Epistulae, team bios, news posts, …)
link to their Wayback Machine snapshots via `site.archive` in `_config.yml`.
