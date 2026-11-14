# expand.py CRAWL — print in-scope css.cua.edu URLs linked from crawled pages but not yet crawled.
import sys, glob, re, os
crawl = sys.argv[1]
have = set('/' + os.path.basename(f)[:-5].replace('__', '/') + '/' for f in glob.glob(crawl + '/*.html'))
skip = set(l.strip() for l in open(crawl + '/../skip.txt')) if os.path.exists(crawl + '/../skip.txt') else set()
SCOPE = re.compile(r'^/(events/page/\d+|event/[^/]+|venue/[^/]+|team-members/[^/]+|team-group/[^/]+|ideas_and_commentary/[^/]+|css_news/[^/]+|epistulae-no-\d+)/$')
out = set()
for f in glob.glob(crawl + '/*.html'):
    src = os.path.basename(f)
    s = open(f, encoding='utf-8', errors='ignore').read()
    i = s.find('id="content"'); s = s[i:] if i > 0 else s
    j = s.find('id="colophon"'); s = s[:j] if j > 0 else s
    for u in re.findall(r'href=["\'](?:https?:)?//(?:www\.)?css\.cua\.edu(/[^"\'#?]*)', s):
        if not u.endswith('/'): u += '/'
        ok = SCOPE.match(u) or (u.startswith('/humanitas_journal/') and u.count('/') == 3 and not src.startswith('humanitas_journal'))
        if ok and u not in have and u not in skip: out.add('https://css.cua.edu' + u)
print('\n'.join(sorted(out)))
