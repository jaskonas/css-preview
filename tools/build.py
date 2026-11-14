# build.py CRAWL_DIR SITE_DIR — convert archived css.cua.edu pages into Jekyll collection docs.
# Writes _news/, _commentary/, _epistulae/, _events/, _team/ docs, _data/groups.yml,
# _data/venues.yml, and uploads.txt (assets to mirror under /uploads/).
import sys, os, re, glob, json, html
from urllib.parse import urlparse, unquote, parse_qs
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

CRAWL, SITE = sys.argv[1], sys.argv[2]
UPLOAD_HOSTS = ('csscua.wpenginepowered.com', 'css.cua.edu', 'csscua.wpengine.com', 'www.css.cua.edu')
uploads = set()
report = []

def soup(path):
    return BeautifulSoup(open(path, encoding='utf-8', errors='ignore'), 'html.parser')

def strip_wayback(u):
    m = re.match(r'^(?:https?:)?//web\.archive\.org/web/\d+[a-z_]*/(.*)$', u or '')
    return m.group(1) if m else (u or '')

def local_upload(u):
    """Map a wp-content/uploads URL to /uploads/... and queue it for download."""
    u = strip_wayback(u)
    if u.startswith('//'): u = 'https:' + u
    p = urlparse(u)
    if p.netloc in UPLOAD_HOSTS and '/wp-content/uploads/' in p.path:
        rel = p.path.split('/wp-content/uploads/', 1)[1]
        uploads.add('https://csscua.wpenginepowered.com/wp-content/uploads/' + rel)
        return '/uploads/' + unquote(rel)
    return None

def local_link(u):
    u = strip_wayback(u)
    if not u: return u
    up = local_upload(u)
    if up: return up
    if u.startswith('//'): u = 'https:' + u
    p = urlparse(u)
    if p.netloc in ('css.cua.edu', 'www.css.cua.edu', 'csscua.wpenginepowered.com', 'csscua.wpengine.com'):
        path = p.path or '/'
        if not path.endswith('/') and '.' not in path.rsplit('/', 1)[-1]: path += '/'
        return path + (('#' + p.fragment) if p.fragment else '')
    return u

KEEP = {'a': ['href', 'title'], 'img': ['src', 'alt', 'title'], 'iframe': ['src', 'title', 'allowfullscreen', 'allow'],
        'td': ['colspan', 'rowspan'], 'th': ['colspan', 'rowspan'], 'ol': ['start', 'type'], 'blockquote': [], }
ALLOWED = {'p','a','em','strong','b','i','u','sup','sub','br','hr','h2','h3','h4','h5','h6','ul','ol','li','blockquote',
           'img','iframe','figure','figcaption','table','thead','tbody','tr','td','th','cite','q','small','pre','code'}

def media_id(src):
    src = strip_wayback(src or '')
    m = re.search(r'youtube(?:-nocookie)?\.com/embed/([\w-]{6,})', src)
    if m: return ('youtube', m.group(1))
    m = re.search(r'api\.soundcloud\.com%2Ftracks%2F(\d+)|api\.soundcloud\.com/tracks/(\d+)', src)
    if m: return ('soundcloud', m.group(1) or m.group(2))
    m = re.search(r'player\.vimeo\.com/video/(\d+)', src)
    if m: return ('vimeo', m.group(1))
    return (None, None)

def clean(el):
    """Return cleaned inner HTML of a content element."""
    if el is None: return ''
    el = BeautifulSoup(str(el), 'html.parser')
    for x in el.find_all(string=lambda t: isinstance(t, Comment)): x.extract()
    for x in el.select('script, style, noscript, form, .sharedaddy, .addtoany_share_save_container, .thememount-social-share, .vc_separator, .vc_empty_space, .screen-reader-text'):
        x.decompose()
    for h in el.find_all('h1'): h.name = 'h2'
    for t in el.find_all(True):
        if t.name in ALLOWED: continue
        t.unwrap()
    for t in el.find_all(True):
        keep = KEEP.get(t.name, [])
        for a in list(t.attrs):
            if a not in keep: del t[a]
        if t.name == 'img':
            src = t.get('src') or ''
            lu = local_upload(src)
            if lu: t['src'] = lu
            t['loading'] = 'lazy'
            if not t.get('alt'): t['alt'] = ''
        elif t.name == 'iframe':
            t['src'] = strip_wayback(t.get('src', ''))
            t['loading'] = 'lazy'
            wrap = el.new_tag('div', attrs={'class': 'embed'})
            t.wrap(wrap)
        elif t.name == 'a':
            if t.get('href'): t['href'] = local_link(t['href'])
    # drop empty paragraphs / headings
    changed = True
    while changed:
        changed = False
        for t in el.find_all(['p', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'strong', 'em', 'b', 'i', 'span', 'a', 'ul', 'ol', 'blockquote', 'figure']):
            if not t.get_text(strip=True).replace('\xa0', '') and not t.find(['img', 'iframe', 'br', 'hr']):
                t.decompose(); changed = True
    out = str(el)
    out = out.replace('\xa0', ' ')
    out = re.sub(r'(<br/>\s*){3,}', '<br/><br/>', out)
    out = re.sub(r'\n{3,}', '\n\n', out).strip()
    out = re.sub(r'^(\s*<br/>\s*)+|(\s*<br/>\s*)+$', '', out)
    # one block per line for readable diffs
    out = re.sub(r'(</(p|h[2-6]|ul|ol|blockquote|figure|div|table)>)\s*', r'\1\n', out)
    return out

def yq(s):
    return json.dumps(s, ensure_ascii=False) if s is not None else '""'

def write_doc(coll, slug, fm, body):
    d = os.path.join(SITE, '_' + coll); os.makedirs(d, exist_ok=True)
    lines = ['---']
    for k, v in fm.items():
        if v in (None, '', [], {}): continue
        if isinstance(v, list): lines.append(f"{k}: [{', '.join(yq(x) for x in v)}]")
        elif isinstance(v, (int, float)): lines.append(f"{k}: {v}")
        elif k == 'date': lines.append(f"{k}: {v}")
        else: lines.append(f"{k}: {yq(v)}")
    lines.append('---')
    if '{{' in body or '{%' in body: body = '{% raw %}\n' + body + '\n{% endraw %}'
    open(os.path.join(d, slug + '.html'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n\n' + body + '\n')

def text(el): return el.get_text(' ', strip=True) if el else ''

def excerpt_of(body_html, n=210):
    t = BeautifulSoup(body_html, 'html.parser')
    for p in t.find_all('p'):
        s = p.get_text(' ', strip=True)
        if len(s) > 40 and not re.match(r'^(remarks\s+)?by\s', s, re.I) and '•' not in s[:120]:
            s = re.sub(r'\s+', ' ', s)
            return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + '…'
    return ''


def nice_name(n):
    n = re.sub(r'\s+', ' ', n).strip().rstrip(',')
    words = [w for w in n.split() if w.lower() not in ('and', 'with', '&')]
    if words and all(w.isupper() for w in words if re.search('[A-Za-z]', w)):
        n = ' '.join(w if (re.fullmatch(r'[A-Z]\.', w) or w.lower() in ('and', 'with', '&')) else w.capitalize() for w in n.split())
        n = re.sub(r"\bMc(\w)", lambda m: 'Mc' + m.group(1).upper(), n)
    return n

def author_of(body_html):
    t = BeautifulSoup(body_html, 'html.parser').find('p')
    if not t: return None
    m = re.match(r'^(?:Remarks\s+)?by\s+(.{3,80}?)\s*(?:[•|]|$)', t.get_text(' ', strip=True), re.I)
    return nice_name(m.group(1)) if m else None

def slug_from(path):
    return re.sub(r'\.html$', '', os.path.basename(path)).split('__')[-1]

def page_title(s):
    t = s.select_one('.entry-title-wrapper .entry-title, .entry-title-wrapper h1, .entry-title-wrapper')
    return text(t)

def date_of(s):
    t = s.select_one('#content article time[datetime], #content time[datetime]')
    return t['datetime'] if t else None

# ── posts (news, commentary) ──
def build_posts(prefix, coll):
    for f in sorted(glob.glob(os.path.join(CRAWL, prefix + '__*.html'))):
        s = soup(f); slug = slug_from(f)
        art = s.select_one('#content article')
        if not art: report.append(f'no article: {f}'); continue
        fm = {'title': text(art.select_one('.entry-title')) or page_title(s), 'slug': slug, 'date': date_of(s)}
        media = art.select_one('.thememount-blog-media')
        if media:
            ifr = media.find('iframe'); img = media.find('img')
            if ifr:
                kind, mid = media_id(ifr.get('src'))
                if kind: fm[kind] = mid
                else: report.append(f'unknown iframe {f}: {ifr.get("src")}')
            elif img:
                fm['image'] = local_upload(img.get('src'))
        body = clean(art.select_one('.entry-content'))
        fm['author'] = author_of(body)
        if fm['author']:
            # drop a bare byline paragraph ("by NAME" / "By NAME • date") — the layout shows the author
            body = re.sub(r'^\s*<p>(?:<(?:strong|b|em|i)>)?\s*by\s+[^<]{3,90}?(?:</(?:strong|b|em|i)>)?</p>\s*', '', body, count=1, flags=re.I)
        fm['excerpt_text'] = excerpt_of(body)
        write_doc(coll, slug, fm, body)

build_posts('css_news', 'news')
build_posts('ideas_and_commentary', 'commentary')
build_posts('humanitas_journal', 'humanitas')

# ── epistulae (HTML editions) ──
from datetime import datetime
def parse_date(t):
    t = re.sub(r'\bSept\b\.?', 'Sep', t); t = re.sub(r'\b([A-Z][a-z]{2})[a-z]*\.', r'\1', t)
    for fmt in ('%B %d, %Y', '%b %d, %Y', '%B %Y', '%b %Y'):
        try: return datetime.strptime(t.strip(), fmt).strftime('%Y-%m-%d')
        except ValueError: pass
    return None

for f in sorted(glob.glob(os.path.join(CRAWL, 'epistulae-no-*.html'))):
    s = soup(f); slug = slug_from(f)
    ec = s.select_one('#content article .entry-content')
    if not ec: report.append(f'no content: {f}'); continue
    num = int(slug.rsplit('-', 1)[1])
    h1 = ec.find('h1'); title = text(h1) or page_title(s)
    fm = {'title': title, 'slug': slug, 'number': num}
    for h in list(ec.find_all('h2'))[:3]:
        t = text(h)
        m = re.match(r'No\.\s*\d+\s*·\s*(.+)$', t)
        if m: fm['date'] = parse_date(m.group(1)); h.decompose(); continue
        if t.startswith('By '): fm['author'] = t[3:].strip(); h.decompose()
    if h1: h1.decompose()
    body = clean(ec)
    fm['excerpt_text'] = excerpt_of(body)
    write_doc('epistulae', slug, fm, body)

# ── events (The Events Calendar) ──
for f in sorted(glob.glob(os.path.join(CRAWL, 'event__*.html'))):
    s = soup(f); slug = slug_from(f)
    title = text(s.select_one('.tribe-events-single-event-title'))
    sched = text(s.select_one('.tribe-events-schedule'))
    dm = re.search(r'([A-Z][a-z]+ \d{1,2}(?:, \d{4})?)', sched)
    day = dm.group(1) if dm else None
    if day and not re.search(r'\d{4}', day):
        ym = re.search(r'\d{4}', sched); day = day + ', ' + (ym.group(0) if ym else '')
    tm = sched.split('@', 1)[1].strip() if '@' in sched else None
    if not tm and ' - ' in sched: tm = sched  # multi-day span without times
    fm = {'title': title, 'slug': slug, 'date': parse_date(day) if day else None,
          'time': tm.replace(' - ', '–') if tm else None}
    if not fm['date']: report.append(f'event without date: {slug}: {sched}')
    det = s.select_one('.tribe-events-meta-group-details')
    if det:
        for a in det.find_all('a'):
            if a.get('href', '').startswith('http') and 'css.cua.edu' not in a['href']: fm['website'] = strip_wayback(a['href'])
    ven = s.select_one('.tribe-events-meta-group-venue a[href*="/venue/"]')
    if ven: fm['venue'] = urlparse(strip_wayback(ven['href'])).path.strip('/').split('/')[-1]
    desc = s.select_one('.tribe-events-single-event-description')
    if desc:
        for x in desc.select('.tribe-events, .tribe-common'): x.decompose()
    img = s.select_one('.tribe-events-event-image img')
    if img: fm['image'] = local_upload(img.get('src'))
    body = clean(desc)
    fm['excerpt_text'] = excerpt_of(body)
    write_doc('events', slug, fm, body)

# ── team: cards on listing pages (order, photo, position, org) + bio pages ──
def card_data(box):
    d = {}
    a = box.select_one('.thememount-team-title a') or box.select_one('a[href*="/team-members/"]')
    if not a: return None
    d['slug'] = urlparse(strip_wayback(a['href'])).path.strip('/').split('/')[-1]
    d['title'] = text(a)
    img = box.select_one('.thememount-team-img img')
    if img: d['photo'] = local_upload(img.get('src'))
    pos = box.select_one('.thememount-team-position')
    if pos: d['position'] = text(pos)
    data = box.select_one('.thememount-team-data')
    if data:
        bits = [str(x).strip() for x in data.children if isinstance(x, NavigableString) and not isinstance(x, Comment) and str(x).strip()]
        if bits: d['org'] = re.sub(r'\s+', ' ', ' '.join(bits))
    for l in box.select('.thememount-team-social-links a, .thememount-social-links a'):
        h = l.get('href', '')
        if h.startswith('mailto:'): d['email'] = h[7:]
        elif 'twitter.com/' in h: d['twitter'] = h.rstrip('/').rsplit('/', 1)[-1]
        elif 'linkedin.com' in h: d['linkedin'] = strip_wayback(h)
    d['groups'] = [urlparse(strip_wayback(g['href'])).path.strip('/').split('/')[-1] for g in box.select('.thememount-team-cat-links a')]
    return d

people, groups, group_titles = {}, {}, {}
def merge(d):
    cur = people.setdefault(d['slug'], {})
    for k, v in d.items():
        if k == 'groups': cur['groups'] = list(dict.fromkeys(cur.get('groups', []) + v))
        elif v and not cur.get(k): cur[k] = v

def cards_on(path):
    s = soup(path)
    for box in s.select('.thememount-team-box'):
        d = card_data(box)
        if d: merge(d); yield d['slug']

LISTING_GROUPS = {'advisory-council': ('Council of Advisors', '/advisory-council/'),
                  'css-staff': ('CSS Staff', '/css-staff/')}
for key, (title, url) in LISTING_GROUPS.items():
    f = os.path.join(CRAWL, key + '.html')
    if os.path.exists(f): groups[key] = {'title': title, 'url': url, 'members': list(dict.fromkeys(cards_on(f)))}

for f in sorted(glob.glob(os.path.join(CRAWL, 'team-group__*.html'))):
    key = slug_from(f)
    groups[key] = {'title': page_title(soup(f)).title() if page_title(soup(f)).isupper() else page_title(soup(f)),
                   'url': f'/team-group/{key}/', 'members': list(dict.fromkeys(cards_on(f)))}

# Visiting Fellows page: sections split by its h4 headings
f = os.path.join(CRAWL, 'visiting-fellows.html')
if os.path.exists(f):
    s = soup(f); sections = []; cur = None
    for el in s.select_one('#content').find_all(['h4', 'div']):
        if el.name == 'h4' and 'thememount-team-position' not in (el.get('class') or []) and el.find_parent(class_='thememount-team-box') is None:
            cur = {'title': text(el), 'members': []}; sections.append(cur)
        elif el.name == 'div' and 'thememount-team-box' in (el.get('class') or []) and cur is not None:
            d = card_data(el)
            if d: merge(d); cur['members'].append(d['slug'])
    keys = []
    for i, sec in enumerate(sections):
        k = 'vf-' + re.sub(r'[^a-z]+', '-', sec['title'].lower()).strip('-')
        groups[k] = {'title': sec['title'], 'url': '/visiting-fellows/', 'members': list(dict.fromkeys(sec['members']))}
        keys.append(k)
    groups['visiting-fellows-page'] = {'title': 'Visiting Fellows', 'url': '/visiting-fellows/', 'sections': keys}

# the homepage carousel is the reference set too
for box in soup(os.path.join(os.path.dirname(CRAWL), 'dl', 'home.html')).select('.thememount-team-box'):
    d = card_data(box)
    if d: merge(d)

for f in sorted(glob.glob(os.path.join(CRAWL, 'team-members__*.html'))):
    s = soup(f); slug = slug_from(f)
    left, right = s.select_one('.single-team-left'), s.select_one('.single-team-right')
    if not right: report.append(f'no team body: {f}'); continue
    d = {'slug': slug}
    if left:
        if left.find('h3'): d['title'] = text(left.find('h3'))
        img = left.find('img')
        if img: d['photo'] = local_upload(img.get('src'))
        d['groups'] = [urlparse(strip_wayback(g['href'])).path.strip('/').split('/')[-1] for g in left.select('.thememount-team-cat-links a')]
        for l in left.select('.thememount-team-social-links a'):
            h = l.get('href', '')
            if h.startswith('mailto:'): d['email'] = h[7:]
            elif 'twitter.com/' in h: d['twitter'] = h.rstrip('/').rsplit('/', 1)[-1]
    pos = right.select_one('.thememount-team-position')
    if pos: d['position'] = text(pos)
    em = right.select_one('.thememount-team-email a')
    if em and em.get('href', '').startswith('mailto:'): d['email'] = em['href'][7:]
    merge(d)
    tb = right.select_one('.thememount-team-title-block')
    if tb: tb.decompose()
    people[slug]['_body'] = clean(right)

for slug, d in people.items():
    if '_body' not in d: report.append(f'no bio page for {slug}')
    fm = {'title': d.get('title'), 'slug': slug, 'photo': d.get('photo'), 'position': d.get('position'), 'org': d.get('org'),
          'email': d.get('email'), 'twitter': d.get('twitter'), 'groups': d.get('groups')}
    write_doc('team', slug, fm, d.get('_body', ''))

# groups.yml
lines = ['# Team groups: listing order taken from the archived pages (generated by build.py).']
for k, g in groups.items():
    lines.append(f'{k}:')
    lines.append(f'  title: {yq(g["title"])}')
    lines.append(f'  url: {g["url"]}')
    if 'members' in g: lines.append('  members: [' + ', '.join(g['members']) + ']')
    if 'sections' in g: lines.append('  sections: [' + ', '.join(g['sections']) + ']')
open(os.path.join(SITE, '_data', 'groups.yml'), 'w').write('\n'.join(lines) + '\n')

# /team-group/<key>/ pages
os.makedirs(os.path.join(SITE, 'team-group'), exist_ok=True)
for k, g in groups.items():
    if not g['url'].startswith('/team-group/'): continue
    open(os.path.join(SITE, 'team-group', k + '.md'), 'w').write(
        f"---\nlayout: page\npermalink: {g['url']}\ntitle: {yq(g['title'])}\nwide: true\n---\n\n"
        f"{{% include team-group.html group=\"{k}\" %}}\n")

# ── venues: _data/venues.yml + /venue/<slug>/ pages ──
os.makedirs(os.path.join(SITE, 'venue'), exist_ok=True)
vlines = ['# Event venues (generated by build.py from the archived venue pages).']
for f in sorted(glob.glob(os.path.join(CRAWL, 'venue__*.html'))):
    s = soup(f); slug = slug_from(f)
    name = text(s.select_one('.tribe-events-header__title, h1'))
    addr_el = s.select_one('.tribe-events-pro-venue__meta-address')
    addr = ''
    if addr_el:
        for x in addr_el.select('a'): x.decompose()
        addr = re.sub(r'\s+,', ',', addr_el.get_text(' ', strip=True))
        addr = re.sub(r'\s+', ' ', addr).strip()
    mp = s.select_one('a[href*="google.com/maps"]')
    vlines += [f'{slug}:', f'  name: {yq(name)}', f'  url: /venue/{slug}/', f'  address: {yq(addr)}']
    if mp: vlines.append(f'  map: {yq(strip_wayback(mp["href"]))}')
    open(os.path.join(SITE, 'venue', slug + '.md'), 'w').write(
        f"---\nlayout: venue\npermalink: /venue/{slug}/\ntitle: {yq(name)}\nvenue: {slug}\nparent_title: Events\nparent_url: /events/\n---\n")
open(os.path.join(SITE, '_data', 'venues.yml'), 'w').write('\n'.join(vlines) + '\n')

# ── final pass: unlink internal links whose target isn't part of the rebuilt site ──
valid = {'/'}
for coll, perm in [('news', '/css_news/'), ('commentary', '/ideas_and_commentary/'), ('humanitas', '/humanitas_journal/'),
                   ('events', '/event/'), ('team', '/team-members/'), ('epistulae', '/')]:
    for f in glob.glob(os.path.join(SITE, '_' + coll, '*.html')):
        valid.add(perm + os.path.basename(f)[:-5] + '/')
for f in glob.glob(os.path.join(SITE, '**', '*.md'), recursive=True):
    m = re.search(r'^permalink:\s*(\S+)', open(f, encoding='utf-8').read(), re.M)
    if m: valid.add(m.group(1))
unlinked = {}
for f in glob.glob(os.path.join(SITE, '_*', '*.html')):
    if os.path.basename(os.path.dirname(f)) in ('_layouts', '_includes', '_site', '_data', '_sass'): continue
    src = open(f, encoding='utf-8').read()
    head, sep, body = src.partition('\n---\n')
    def fix(m):
        href = m.group(1)
        path = href.split('#')[0]
        if path.startswith('/uploads/'):
            if os.path.exists(os.path.join(SITE, unquote(path).lstrip('/'))): return m.group(0)
        elif path in valid or not path.startswith('/'): return m.group(0)
        unlinked[path] = unlinked.get(path, 0) + 1
        return m.group(2)
    body2 = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', fix, body, flags=re.S)
    if body2 != body: open(f, 'w', encoding='utf-8').write(head + sep + body2)
for k, v in sorted(unlinked.items()): report.append(f'unlinked {v}x {k}')

json.dump(report, open(os.path.join(os.path.dirname(CRAWL), 'build_report.json'), 'w'), indent=1)
open(os.path.join(os.path.dirname(CRAWL), 'uploads.txt'), 'w').write('\n'.join(sorted(uploads)) + '\n')
print('report:', *report, sep='\n  ')
print('uploads:', len(uploads))
