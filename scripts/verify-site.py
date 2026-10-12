"""Check generated Astro routes, links, assets and metadata without a browser."""
from html.parser import HTMLParser
from pathlib import Path
import json, re
from urllib.parse import urlsplit, unquote

root = Path(__file__).resolve().parents[1]
dist = root / 'smoggy-star/dist'
public = root / 'smoggy-star/public'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs = []; self.ids = set(); self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); self.tags.append((tag, attrs))
        if 'id' in attrs: self.ids.add(attrs['id'])
        for key in ('href', 'src', 'data-src', 'poster'):
            if key in attrs: self.refs.append((key, attrs[key]))

pages = {('/' if f.parent == dist else '/' + f.parent.relative_to(dist).as_posix() + '/'): Page(f.read_text(encoding='utf-8')) for f in dist.rglob('index.html')}
errors = []; refs = 0
for route, page in pages.items():
    tags = page.tags
    for expected in [('html','lang','pt-BR'), ('main','id','conteudo'), ('video','data-matrix-video',None), ('meta','name','description'), ('button','data-menu-toggle',None)]:
        tag, key, value = expected
        if not any(t == tag and key in a and (value is None or a[key] == value) for t, a in tags): errors.append(f'{route}: missing {expected}')
    for key, ref in page.refs:
        parts = urlsplit(ref)
        if parts.scheme or parts.netloc: continue
        if not parts.path:
            if parts.fragment and unquote(parts.fragment) not in page.ids: errors.append(f'{route}: missing anchor {ref}')
            continue
        refs += 1
        target = parts.path
        if target.startswith('/'):
            canonical = target.rstrip('/') + '/'
            if canonical in pages:
                if parts.fragment and unquote(parts.fragment) not in pages[canonical].ids: errors.append(f'{route}: missing target anchor {ref}')
            elif not (dist / target.lstrip('/')).is_file(): errors.append(f'{route}: missing {key} {ref}')
    for tag, attrs in tags:
        if tag == 'video':
            if 'controls' in attrs:
                if not all(k in attrs for k in ('playsinline', 'aria-label', 'aria-describedby')) or attrs.get('preload') != 'metadata': errors.append(f'{route}: incomplete institutional player attributes')
                if any(k in attrs for k in ('muted', 'autoplay', 'loop', 'data-motion-video')): errors.append(f'{route}: institutional video must play manually with audio')
            elif not all(k in attrs for k in ('muted','loop','playsinline','poster','data-motion-video')): errors.append(f'{route}: incomplete animation attributes')
for css in (dist / '_astro').glob('*.css'):
    for ref in re.findall(r'url\([\"\']?([^\)\"\']+)', css.read_text(encoding='utf-8')):
        if ref.startswith('/') and not (dist/ref.lstrip('/')).is_file(): errors.append(f'CSS missing asset: {ref}')
if len(pages) != 11: errors.append(f'Expected eleven routes, got {len(pages)}')
if '/projetos/' not in pages: errors.append('Missing dedicated projects route')
if '/' in pages:
    home = pages['/']
    for obsolete in ('servicos', 'projetos'):
        if obsolete in home.ids: errors.append(f'Home still contains listing: {obsolete}')
    for expected in ('hero-title', 'about-title', 'institutional-video-title', 'dna-title', 'institutional-contact-title'):
        if expected not in home.ids: errors.append(f'Missing home section: {expected}')
    if not any(t == 'video' and a.get('class') == 'brand-banner-video' for t, a in home.tags): errors.append('Missing animated brand banner')
    if not any(ref == 'https://wa.me/5513996887824' for key, ref in home.refs): errors.append('Missing institutional WhatsApp CTA')
print(json.dumps({'routes': len(pages), 'local_references': refs, 'errors': errors}, indent=2, ensure_ascii=False))
raise SystemExit(bool(errors))
