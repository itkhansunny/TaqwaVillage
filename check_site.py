"""Check all static pages and their internal links without extra dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.assets = [], [], []
        self.headings = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'h1':
            self.headings += 1
        if tag == 'script' and attrs.get('src'):
            self.assets.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.assets.append(attrs.get('href', ''))

pages = {path.name: Page() for path in ROOT.glob('*.html')}
for name, page in pages.items():
    page.feed((ROOT / name).read_text(encoding='utf-8'))

graph = {name: set() for name in pages}
errors = []
for name, page in pages.items():
    if len(page.ids) != len(set(page.ids)):
        errors.append(f'{name}: duplicate IDs')
    if page.headings != 1:
        errors.append(f'{name}: expected one H1, found {page.headings}')
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        target = unquote(url.path) or name
        if target not in pages:
            errors.append(f'{name}: missing page {target}')
        else:
            graph[name].add(target)
            if url.fragment and url.fragment not in pages[target].ids:
                errors.append(f'{name}: missing anchor {href}')
        if href in ('', '#'):
            errors.append(f'{name}: placeholder link')
    for src in page.assets:
        if not urlsplit(src).scheme and not (ROOT / src).is_file():
            errors.append(f'{name}: missing asset {src}')

visited, queue = set(), ['index.html']
while queue:
    name = queue.pop()
    if name in visited:
        continue
    visited.add(name)
    queue.extend(graph[name] - visited)
if visited != set(pages):
    errors.append(f'Pages unreachable from home: {set(pages) - visited}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} pages; valid internal links and assets, unique IDs, one H1 per page, all pages reachable from home.')
