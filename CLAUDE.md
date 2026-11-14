# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Jekyll site cloning the design and copy of the Center for the Study of Statesmanship homepage (css.cua.edu, Wayback capture 2025-03-17). It shares jaskonas.com's architecture; only the skin differs.

## Commands

```bash
bundle exec jekyll serve   # serve locally with live reload
bundle exec jekyll build   # build to _site/
```

## Architecture

- **Pages** are Markdown files at the root (`index.md`, `our-mission.md`). Each picks a `layout` in front matter.
- **Layouts** (`_layouts/`): `home.html` and `page.html` extend `default.html`, which wires the header, footer, fonts and JS.
- **Content is data-driven**: `_data/navigation.yml` (top nav + dropdowns), `_data/social.yml`, `_data/news.yml` (CSS News carousel), `_data/advisors.yml` (Council of Advisors carousel), `_data/staff.yml` (Our Staff grid). Edit these, not the layouts, to change copy.
- **Archived links**: anything not cloned links to `site.archive` + path (`archive: true` in nav, `path`/`slug` in news/team data).
- **Sass** in `_sass/`, compiled via `css/main.scss`. `_css-tokens.scss` holds all colours/fonts as CSS variables with a `[data-theme="dark"]` override; partials use only the semantic tokens.
- **JS** (`js/`, no build step): `css-theme.js` (dark-mode toggle), `css-scroll.js` (sticky header shrink), `css-nav.js` (mobile menu), `css-carousel.js` (prev/next over scroll-snap tracks).
- **Images**: `images/` (logos, hero, footer texture, favicon), `images/team/` (portraits referenced by `photo:` in team data).
