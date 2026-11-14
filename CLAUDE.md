# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Jekyll site rebuilding the Center for the Study of Statesmanship website (css.cua.edu, Wayback capture 2025-03-17) — design and copy — on jaskonas.com's architecture. Every page is native; nothing links back to the archive.

## Commands

```bash
# Homebrew's default Ruby is 4.x; the gems live under Ruby 3.3
PATH=/opt/homebrew/opt/ruby@3.3/bin:$PATH bundle exec jekyll serve --livereload
PATH=/opt/homebrew/opt/ruby@3.3/bin:$PATH bundle exec jekyll build
```

Restart `jekyll serve` after editing `_config.yml` (the watcher doesn't reload it).

## Architecture

- **Collections** (`_config.yml`), one `.html` file per item with front matter + cleaned HTML body. Permalinks mirror the original WordPress URLs:
  - `_news/` → `/css_news/:name/` (layout `post`; `youtube` / `soundcloud` / `image` front matter drive the media slot)
  - `_commentary/` → `/ideas_and_commentary/:name/` (layout `post`)
  - `_epistulae/` → `/epistulae-no-N/` (layout `post`; issue metadata + PDF in `_data/epistulae.yml`)
  - `_events/` → `/event/:name/` (layout `event`; `venue` keys into `_data/venues.yml`)
  - `_team/` → `/team-members/:name/` (layout `person`)
- **Data**: `_data/groups.yml` (team groups and their member order — drives home carousels, Council/Staff/Visiting Fellows pages and `/team-group/*`), `epistulae.yml`, `bulletins.yml`, `venues.yml`, `sections.yml` (collection → parent section), `navigation.yml`, `social.yml`.
- **Pages** are Markdown at the root (`css-news.md`, `ideas-n-commentary.md`, `video-audio.md`, `epistulae.md`, `nhi-bulletins.md`, `events.md`, `advisory-council.md`, `css-staff.md`, `visiting-fellows.md`, `support-css.md`, `our-mission.md`, `humanitas-journal.md`), plus `team-group/*.md` and `venue/*.md`.
- **Includes**: `news-card.html`, `team-card.html`, `team-group.html` (grid or carousel for a group), `event-item.html`, `page-banner.html`, `section-title.html`, `icon.html`.
- **Uploads**: images and PDFs referenced by content live in `uploads/YYYY/MM/` (mirrors the old `wp-content/uploads/`). Site chrome images (logos, hero, footer texture) are in `images/`.
- **Sass** in `_sass/`, compiled via `css/main.scss`; `_css-tokens.scss` holds every colour/font as a CSS variable with a `[data-theme="dark"]` override.
- **JS** (`js/`, no build step): theme toggle, sticky-header shrink, mobile menu, carousel controls.
