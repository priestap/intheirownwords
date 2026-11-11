"""Check static integrity; quotation accuracy requires reviewing the sources."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
root=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.articles=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='article': self.articles+=1
        if tag=='a': self.links.append(a.get('href',''))
page=Page(); page.feed((root/'index.html').read_text())
quotes=json.loads((root/'quotes.json').read_text())
assert len(page.ids)==len(set(page.ids)), 'Duplicate HTML IDs'
assert page.articles==len(quotes)==13
for link in page.links:
    if link.startswith('#'): assert link[1:] in page.ids, f'Missing anchor {link}'
    elif link.startswith('./'): assert ((root/link[2:])/'index.html').is_file() if link=='./' else (root/link[2:]).is_file(), f'Missing local file {link}'
    else: assert urlparse(link).scheme=='https', f'Unexpected URL {link}'
for q in quotes:
    assert q['id'] in page.ids
    assert all(q[k] for k in ['quote','reference','translation','response','context','verified'])
    assert urlparse(q['url']).scheme=='https'
    assert q['quote'] in (root/'index.html').read_text()
assert '{{ENTRIES}}' not in (root/'index.html').read_text()
print(f'PASS: {len(quotes)} cited entries, unique IDs, internal links, and local assets.')
