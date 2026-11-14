# Usage: fetch.py OUTDIR url...   Fetches each css.cua.edu URL from the Wayback Machine (raw id_), paced, with retry.
import sys, os, time, urllib.request, urllib.error, hashlib, re, gzip
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
TS = "20250317025935"
def name(u):
    p = re.sub(r'^https?://css\.cua\.edu', '', u).strip('/') or 'home'
    return re.sub(r'[^A-Za-z0-9._-]+', '__', p) + '.html'
for u in sys.argv[2:]:
    f = os.path.join(out, name(u))
    if os.path.exists(f) and os.path.getsize(f) > 2000: continue
    for attempt in range(5):
        try:
            req = urllib.request.Request(f"https://web.archive.org/web/{TS}id_/{u}", headers={"User-Agent": "Mozilla/5.0 (archival research)"})
            data = urllib.request.urlopen(req, timeout=60).read()
            if data[:2] == b'\x1f\x8b': data = gzip.decompress(data)
            open(f, 'wb').write(data); print("ok", len(data), u, flush=True); break
        except urllib.error.HTTPError as e:
            print("http", e.code, u, flush=True)
            if e.code == 404: break
            time.sleep(20 * (attempt + 1))
        except Exception as e:
            print("err", type(e).__name__, u, flush=True); time.sleep(20 * (attempt + 1))
    time.sleep(3)
