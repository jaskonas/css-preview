# linkcheck.py SITE_BUILD_DIR — report internal href/src targets that don't exist in the built site.
import sys, os, re
from urllib.parse import urlparse, unquote
root = sys.argv[1]; bad = {}
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'): continue
        page = os.path.join(dp, f); rel = '/' + os.path.relpath(page, root)
        for m in re.finditer(r'(?:href|src)="([^"]+)"', open(page, encoding='utf-8', errors='ignore').read()):
            u = m.group(1)
            p = urlparse(u)
            if p.scheme or u.startswith(('mailto:', '#', '//', 'javascript:', 'data:')): continue
            path = unquote(p.path)
            if not path.startswith('/'): path = os.path.normpath(os.path.join(os.path.dirname(rel), path))
            t = os.path.join(root, path.lstrip('/'))
            if os.path.isdir(t): t = os.path.join(t, 'index.html')
            if not os.path.exists(t) and not os.path.exists(t + '.html'):
                bad.setdefault(path, set()).add(rel)
for k in sorted(bad): print(k, '  <-', ', '.join(sorted(bad[k])[:3]), f'(+{len(bad[k])-3})' if len(bad[k]) > 3 else '')
print('broken targets:', len(bad))
