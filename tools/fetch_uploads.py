# fetch_uploads.py LIST SITE_DIR — mirror wp-content/uploads URLs from the Wayback Machine into SITE_DIR/uploads/.
import sys, os, time, gzip, urllib.request, urllib.error
from urllib.parse import unquote, quote
TS = "20250317025935"
lst, site = sys.argv[1], sys.argv[2]
miss = []
for u in [l.strip() for l in open(lst) if l.strip()]:
    rel = unquote(u.split('/wp-content/uploads/', 1)[1])
    dest = os.path.join(site, 'uploads', rel)
    if os.path.exists(dest) and os.path.getsize(dest) > 0: continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    ok = False
    for attempt in range(4):
        try:
            req = urllib.request.Request(f"https://web.archive.org/web/{TS}im_/" + quote(u, safe=":/%"), headers={"User-Agent": "Mozilla/5.0 (archival research)"})
            r = urllib.request.urlopen(req, timeout=120); data = r.read()
            if data[:2] == b'\x1f\x8b': data = gzip.decompress(data)
            if data[:15].lstrip().lower().startswith((b'<!doctype', b'<html')): raise ValueError('got html')
            open(dest, 'wb').write(data); print('ok', len(data), rel, flush=True); ok = True; break
        except urllib.error.HTTPError as e:
            print('http', e.code, rel, flush=True)
            if e.code == 404: break
            time.sleep(15 * (attempt + 1))
        except Exception as e:
            print('err', type(e).__name__, rel, flush=True); time.sleep(15 * (attempt + 1))
    if not ok: miss.append(u)
    time.sleep(2)
open(lst + '.missing', 'w').write('\n'.join(miss) + '\n')
print('missing', len(miss))
