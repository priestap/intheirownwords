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
collections=[('index.html','quotes.json',15),('cessationists.html','cessationists.json',7),('christs-return.html','christs-return.json',6)]
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
    assert all(link in page.links for link in ['./#library','./cessationists.html#library','./christs-return.html#library'])
    assert '{{COLLECTION_NAV}}' not in html
    assert not any(arrow in html for arrow in ['↗','↓','↑']), 'Use SVG arrows for iOS consistency'
    for link in page.links:
        if link.startswith('#'):
            assert link[1:] in page.ids, f'Missing anchor {link}'
        elif link.startswith('./'):
            path,_,fragment=link.partition('#')
            target=root/path[2:].split('?',1)[0]
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
history=next(q for q in quotes if q['id']=='evangelism')['historical_witnesses']
assert all(history.get(key) for key in ['title','intro','scope','people'])
assert len(history['people'])==7, 'Expected seven historical examples'
assert len({person['name'] for person in history['people']})==7
history_html=(root/'index.html').read_text()
for person in history['people']:
    assert all(person.get(key) for key in ['name','era','belief','ministry','qualification','sources','verified'])
    assert len(person['sources'])>=2, 'Belief and ministry each need source evidence'
    assert all(escape(person[key]) in history_html for key in ['name','era','belief','ministry','qualification'])
    for source in person['sources']:
        assert all(source.get(key) for key in ['reference','url','kind'])
        assert urlparse(source['url']).scheme=='https'
        assert escape(source['reference']) in history_html
print('PASS: seven historical profiles with separate evidence of belief and ministry, qualifications, and source references.')
confessions=[c for q in quotes for c in q.get('confessions',[])]
assert len(confessions)==34, 'Expected 34 confessional excerpts'
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
assert len(cessationist_confessions)==8, 'Expected eight cessationist confessional excerpts'
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
assert supporting_count==4, 'Expected four supporting excerpts'
assert all(count<=25 for count in words_by_source.values()), 'Modern excerpts exceed 25 words per source'
workflow=(root/'.github/workflows/pages.yml').read_text()
assert 'cessationists.html' in workflow and 'cessationists.json' in workflow
print('PASS: 34 Calvin confessional excerpts, eight cessationist confessional excerpts, seven attributed criticisms, four supporting excerpts, brief modern excerpts, and all three collections packaged for GitHub Pages.')

hope=json.loads((root/'christs-return.json').read_text())
hope_html=(root/'christs-return.html').read_text()
hope_words={}
hope_confessions=[]
for q in hope:
    assert q['supporting_label']=='More voices'
    assert q['scriptures']
    assert len(q['confessions'])>=1
    hope_confessions.extend(q['confessions'])
    for item in [q,q['criticism'],*q['supporting_quotes'],*([q['creator_statement']] if q.get('creator_statement') else [])]:
        assert all(item.get(key) for key in ['quote','reference','url','context','verified'])
        assert urlparse(item['url']).scheme=='https'
        assert all(escape(item[key]) in hope_html for key in ['quote','reference','context'])
        source=item['url'].split('#')[0]
        if not item.get('public_domain'):
            hope_words[source]=hope_words.get(source,0)+len(item['quote'].split())
    for passage in q['scriptures']:
        assert urlparse(passage['url']).scheme=='https'
        assert escape(passage['reference']) in hope_html
for c in hope_confessions:
    assert all(c.get(key) for key in ['quote','reference','url','edition','context','verified'])
    assert all(escape(c[key]) in hope_html for key in ['quote','reference','context'])
assert all(count<=25 for count in hope_words.values()), 'Hope collection modern excerpts exceed 25 words per source'
assert 'More cessationist voices' not in hope_html
assert 'christs-return.html' in workflow and 'christs-return.json' in workflow
print('PASS: new collection: six criticisms, six responses, ten supporting voices, ten confessional excerpts, Scripture links, and separate personal statements.')

class PublishedCriticisms(HTMLParser):
    def __init__(self):
        super().__init__(); self.disclosures=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='details' and 'published-criticism' in a.get('class','').split():
            self.disclosures.append(a)

for page_file,data_file,expected in collections:
    html=(root/page_file).read_text()
    parser=PublishedCriticisms(); parser.feed(html)
    assert len(parser.disclosures)==expected
    assert all('open' not in a and 'data-mobile-collapse' not in a for a in parser.disclosures), 'Published criticisms must stay closed by default at all widths'
    modern_critic_words={}
    for q in json.loads((root/data_file).read_text()):
        c=q['criticism']
        assert all(c.get(key) for key in ['author','quote','reference','url','edition','kind','context','verified'])
        assert all(escape(c[key]) in html for key in ['quote','author','reference','context'])
        entry=html.split('id="'+q['id']+'"',1)[1].split('</article>',1)[0]
        assert entry.index(escape(q['claim'])) < entry.index('class="published-criticism"') < entry.index(escape(c['quote']))
        assert urlparse(c['url']).scheme=='https'
        if not c.get('public_domain'):
            source=c['url'].split('#')[0]
            modern_critic_words[source]=modern_critic_words.get(source,0)+len(c['quote'].split())
    assert all(n<=25 for n in modern_critic_words.values()), 'Modern critic excerpts exceed 25 words per source'
print('PASS: all 28 editorial claims precede their attributed criticisms; source disclosures start closed and are excluded from automatic reopening.')

assert sum(len(q['supporting_quotes']) for q in hope)==10
for q in hope:
    assert any(item.get('early_christian') for item in [q,*q['supporting_quotes']]), 'Each Christ’s Return entry needs an ancient witness'
print('PASS: all six Christ’s Return entries include an identified early Christian witness with source and scope notes.')
