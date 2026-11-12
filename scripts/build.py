"""Generate the committed, JavaScript-optional GitHub Pages collections."""
import json
import hashlib
from pathlib import Path
from html import escape as e

root = Path(__file__).resolve().parent.parent
ASSET_VERSION = hashlib.sha256((root / "style.css").read_bytes() + (root / "app.js").read_bytes()).hexdigest()[:12]
ARROW = '<svg class="ui-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 17 17 7M7 7h10v10"/></svg>'


def source_link(item):
    return f'<a href="{e(item["url"])}">{e(item["reference"])} {ARROW}</a>'


def disclosure(label, content, classes='', adaptive=False):
    state = ' open data-mobile-collapse' if adaptive else ''
    return f'<details class="{classes}"{state}><summary>{e(label)} <span aria-hidden="true">+</span></summary>{content}</details>'


COLLECTIONS = [
    ('quotes.json', 'index.template.html', 'index.html', 'Calvin & Reformed'),
    ('cessationists.json', 'cessationists.template.html', 'cessationists.html', 'Cessationism'),
    ('christs-return.json', 'christs-return.template.html', 'christs-return.html', 'Christ’s Return & His People'),
]


def collection_navigation(output_file):
    links = []
    for data_file, _, page_file, label in COLLECTIONS:
        count = len(json.loads((root / data_file).read_text()))
        href = './#library' if page_file == 'index.html' else f'./{page_file}#library'
        active = ' aria-current="page"' if page_file == output_file else ''
        state = '<span class="collection-state">Current collection</span>' if active else '<span class="collection-state">View collection</span>'
        links.append(f'<a href="{href}"{active}><span class="collection-name">{e(label)}</span><span class="collection-count">{count} entries</span>{state}</a>')
    return '<p class="collection-chooser-label">Choose a collection</p><nav class="collection-tabs" aria-label="Choose a collection">' + ''.join(links) + '</nav>'


def build(data_file, template_file, output_file):
    data = json.loads((root / data_file).read_text())
    if output_file == 'index.html':
        assert (root / 'assets/calvin-engraving.png').is_file(), 'Homepage Calvin portrait is missing'
    entries = []
    for q in data:
        confessions = q.get('confessions', [])
        witness = ''
        for conf in confessions:
            edition = f'<p class="witness-edition">{e(conf["edition"])}</p>' if conf.get('edition') else ''
            context = f'<p class="witness-context">{e(conf["context"])}</p>' if conf.get('context') else ''
            witness += f'<div class="witness"><blockquote>“{e(conf["quote"])}”</blockquote>{source_link(conf)}{edition}{context}</div>'
        conf_html = disclosure(f'Confessional witness · {len(confessions)}', f'<div class="context">{witness}</div>', 'confessional-disclosure') if confessions else ''

        supporting = q.get('supporting_quotes', [])
        voices = ''
        for voice in supporting:
            witness_label = f'<p class="eyebrow">{e(voice["witness_label"])}</p>' if voice.get('witness_label') else ''
            voices += f'<div class="witness supporting-voice">{witness_label}<blockquote>“{e(voice["quote"])}”</blockquote><p class="citation"><strong>{e(voice["author"])}</strong> · {source_link(voice)}<span>{e(voice["edition"])}</span></p><p class="witness-context">{e(voice["context"])}</p></div>'
        supporting_html = disclosure(f'{q.get("supporting_label", "More cessationist voices")} · {len(supporting)}', f'<div class="supporting-voices">{voices}</div>', 'supporting-disclosure', adaptive=True) if supporting else ''

        history = q.get('historical_witnesses')
        history_html = ''
        if history:
            profiles = ''
            for person in history['people']:
                links = ''.join(f'<li><span>{e(source["kind"])}</span>{source_link(source)}</li>' for source in person['sources'])
                profiles += f'''<li class="historical-person"><p class="eyebrow">{e(person['era'])}</p><h4>{e(person['name'])}</h4><p><strong>Belief.</strong> {e(person['belief'])}</p><p><strong>In practice.</strong> {e(person['ministry'])}</p><p class="historical-qualification">{e(person['qualification'])}</p><ul class="historical-sources" aria-label="Sources for {e(person['name'])}">{links}</ul></li>'''
            history_body = f'<div class="context historical-witnesses"><p>{e(history["intro"])}</p><p class="historical-scope">{e(history["scope"])}</p><ol class="historical-people">{profiles}</ol><p class="history-verification">Historical summaries and source references checked November 11, 2026. Belief, ministry, and qualifications are editorial summaries, not attributed quotations.</p></div>'
            history_html = disclosure(f'{history["title"]} · {len(history["people"])} examples', history_body, 'historical-disclosure')

        criticism = q.get('criticism')
        if criticism:
            critic_context = f'<p class="citation">{source_link(criticism)}<span>{e(criticism["edition"])}</span></p><p class="criticism-kind">{e(criticism["kind"])}</p><p class="critic-context">{e(criticism["context"])}</p>'
            original = f'<blockquote class="critic-quote"><p>“{e(criticism["quote"])}”</p></blockquote><p class="critic-author">{e(criticism["author"])}</p>{critic_context}'
            original_details = disclosure('Published criticism & context', original, 'published-criticism')
            claim_side = f'<p class="eyebrow">THE COMMON CLAIM</p><h3>{e(q["claim"])}</h3><p class="claim-note">Editorial summary · see the published criticism below</p>{original_details}'
        else:
            claim_side = f'<p class="eyebrow">THE COMMON CLAIM</p><h3>{e(q["claim"])}</h3><p class="claim-note">Editorial summary · see our approach</p>'

        edition = f'{e(q.get("edition_label", "Translation"))}: {e(q.get("edition", q.get("translation", "")))}'
        source_citation = f'<p class="citation source-citation">{source_link(q)}<span>{edition}</span></p>'
        context = f'<div class="context"><h4>{e(q["title"])}</h4><p>{e(q["response"])}</p><p><strong>Read in context.</strong> {e(q["context"])}</p></div>'
        scripture_links = ''.join(f'<li>{source_link(passage)}</li>' for passage in q.get('scriptures', []))
        if scripture_links:
            context += f'<div class="context scripture-links"><h4>Scripture to examine</h4><ul>{scripture_links}</ul></div>'
        creator = q.get('creator_statement')
        creator_html = ''
        if creator:
            creator_body = f'<div class="context"><p class="eyebrow">PERSONAL STATEMENT · SITE CREATOR</p><blockquote>“{e(creator["quote"])}”</blockquote><p class="citation">{source_link(creator)}</p><p>{e(creator["context"])}</p></div>'
            creator_html = disclosure('The creator’s position', creator_body, 'creator-disclosure')
        source_details = disclosure('Citation & context', source_citation + context, 'entry-context', adaptive=True)
        entries.append(f'''<article class="entry" id="{q['id']}" data-topic="{e(q['topic'])}"><button type="button" class="objection-toggle" aria-expanded="false" hidden><span class="objection-number">{q['number']:02d}</span><span>{e(q["claim"])}</span><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><path d="m6 9 6 6 6-6"/></svg></button><div class="claim-side"><span class="entry-number">{q['number']:02d}</span><span class="topic">{e(q['topic'])}</span>{claim_side}</div><div class="quote-side"><p class="eyebrow">{e(q.get("quote_label", "IN HIS OWN WORDS"))}</p><blockquote>“{e(q['quote'])}”</blockquote><p class="lead-author">{e(q['author'])}</p>{source_details}{supporting_html}{conf_html}{creator_html}{history_html}<div class="entry-actions"><a href="{e(q['url'])}">Read the source {ARROW}</a><button type="button" data-copy="{q['id']}" hidden>Copy citation</button><a href="#{q['id']}" class="permalink" aria-label="Permanent link: {e(q['title'])}"># Share entry</a></div></div></article>''')
    (root / output_file).write_text((root / template_file).read_text().replace('{{ENTRIES}}', '\n'.join(entries)).replace('{{COLLECTION_NAV}}', collection_navigation(output_file)).replace('{{ENTRY_COUNT}}', str(len(data))).replace('{{ASSET_VERSION}}', ASSET_VERSION))
    print(f'Built {len(data)} entries into {output_file}')


for data_file, template_file, output_file, _ in COLLECTIONS:
    build(data_file, template_file, output_file)
