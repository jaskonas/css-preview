# Import tools

Scripts used to rebuild the site from the Wayback Machine capture (2025-03-17). Not part of the Jekyll build.

```bash
python3 -m venv .venv && .venv/bin/pip install beautifulsoup4
python3 tools/fetch.py crawl <url>...            # fetch archived pages (paced, gzip-safe)
.venv/bin/python tools/expand.py crawl           # list in-scope linked pages not yet crawled
.venv/bin/python tools/build.py crawl .          # crawl/*.html → _news, _commentary, _epistulae, _events, _team, _humanitas,
                                                 #   _data/groups.yml, _data/venues.yml, team-group/, venue/, uploads.txt
python3 tools/fetch_uploads.py uploads.txt .     # mirror wp-content/uploads → uploads/
python3 tools/linkcheck.py _site                 # report internal links with no target
```

`build.py` expects the archived homepage at `../dl/home.html` relative to the crawl directory.
