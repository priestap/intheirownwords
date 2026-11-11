"""Check static integrity; quotation accuracy requires reviewing the sources."""
import json
from html.parser import HTMLParser
from html import escape
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
collections=[('index.html','quotes.json',13),('cessationists.html','cessationists.json',6)]
for page_file,data_file,expected in collections:
    html=(root/page_file).read_text()
    page=Page(); page.feed(html)
    quotes=json.loads((root/data_file).read_text())
    assert len(page.ids)==len(set(page.ids)), f'Duplicate HTML IDs in {page_file}'
    assert page.articles==len(quotes)==expected
    assert len({q['id'] for q in quotes})==expected
    assert [q['number'] for q in quotes]==list(range(1,expected+1))
    assert '{{ENTRIES}}' not in html
    assert html.count('aria-current="page"')==1
    assert './#library' in page.links and './cessationists.html#library' in page.links
    for link in page.links:
        if link.startswith('#'):
            assert link[1:] in page.ids, f'Missing anchor {link}'
        elif link.startswith('./'):
            path,_,fragment=link.partition('#')
            target=root/path[2:]
            if target.is_dir(): target=target/'index.html'
            assert target.is_file(), f'Missing local file {link}'
            if fragment:
                linked_page=Page(); linked_page.feed(target.read_text())
                assert fragment in linked_page.ids, f'Missing linked anchor {link}'
        else:
            assert urlparse(link).scheme=='https', f'Unexpected URL {link}'
    for q in quotes:
        assert q['id'] in page.ids
        assert all(q.get(k) for k in ['quote','reference','author','response','context','verified'])
        assert q.get('translation') or q.get('edition')
        assert urlparse(q['url']).scheme=='https'
        assert escape(q['quote']) in html
        assert escape(q['reference']) in html
    print(f'PASS: {page_file}: {expected} cited entries, unique IDs, collection navigation, internal links, and local assets.')
quotes=json.loads((root/'quotes.json').read_text())
confessions=[c for q in quotes for c in q.get('confessions',[])]
assert len(confessions)==32, 'Expected 32 confessional excerpts'
helvetic_excerpts=[c for c in confessions if c['reference'].startswith('Second Helvetic Confession (1566)')]
assert len(helvetic_excerpts)==9, 'Expected nine Second Helvetic excerpts'
baptist_excerpts=[c for c in confessions if c['reference'].startswith('Second London Baptist Confession (1689)')]
assert len(baptist_excerpts)==8, 'Expected eight 1689 excerpts'
for conf in confessions:
    assert all(conf.get(k) for k in ['quote','reference','url'])
    assert urlparse(conf['url']).scheme=='https'
    assert escape(conf['quote']) in (root/'index.html').read_text(), 'Missing confession excerpt'
    assert escape(conf['reference']) in (root/'index.html').read_text(), 'Missing confession reference'
assert '{{ENTRIES}}' not in (root/'index.html').read_text()
modern=json.loads((root/'cessationists.json').read_text())
cessationist_confessions=[c for q in modern for c in q.get('confessions',[])]
assert len(cessationist_confessions)==6, 'Expected six cessationist confessional excerpts'
for c in cessationist_confessions:
    assert all(c.get(key) for key in ['quote','reference','url','edition','context','verified'])
    assert urlparse(c['url']).scheme=='https'
    html=(root/'cessationists.html').read_text()
    assert escape(c['quote']) in html and escape(c['reference']) in html
    assert escape(c['context']) in html
words_by_source={}
for q in modern:
    words_by_source[q['url']]=words_by_source.get(q['url'],0)+len(q['quote'].split())
    c=q['criticism']
    assert all(c.get(key) for key in ['quote','author','reference','edition','kind','context','verified','url'])
    assert urlparse(c['url']).scheme=='https'
    html=(root/'cessationists.html').read_text()
    assert escape(c['quote']) in html and escape(c['reference']) in html
    source=c['url'].split('#')[0]
    words_by_source[source]=words_by_source.get(source,0)+len(c['quote'].split())
supporting_count=0
for q in modern:
    voices=q.get('supporting_quotes',[])
    if q['id'] in ['miracles-today','prayer-for-healing','continuing-gifts']:
        assert voices, f"Missing supporting voice for {q['id']}"
    for voice in voices:
        assert all(voice.get(key) for key in ['quote','author','reference','edition','url','context','verified'])
        assert voice['author']!=q['author'], 'Supporting voice must add a different attribution'
        assert urlparse(voice['url']).scheme=='https'
        html=(root/'cessationists.html').read_text()
        assert all(escape(voice[key]) in html for key in ['quote','author','reference','edition','context'])
        source=voice['url'].split('#')[0]
        words_by_source[source]=words_by_source.get(source,0)+len(voice['quote'].split())
        supporting_count+=1
assert supporting_count==3, 'Expected three supporting excerpts'
assert all(count<=25 for count in words_by_source.values()), 'Modern excerpts exceed 25 words per source'
workflow=(root/'.github/workflows/pages.yml').read_text()
assert 'cessationists.html' in workflow and 'cessationists.json' in workflow
print('PASS: 32 Calvin confessional excerpts, six cessationist confessional excerpts, six attributed criticisms, three supporting excerpts, brief modern excerpts, and both collections packaged for GitHub Pages.')
