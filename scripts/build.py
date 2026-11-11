"""Generate the committed, JavaScript-optional GitHub Pages collections."""
import json
from pathlib import Path
from html import escape as e

root = Path(__file__).resolve().parent.parent
ARROW = '<svg class="ui-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M7 17 17 7M7 7h10v10"/></svg>'


def source_link(item):
    return f'<a href="{e(item["url"])}">{e(item["reference"])} {ARROW}</a>'


def disclosure(label, content, classes='', adaptive=False):
    state = ' open data-mobile-collapse' if adaptive else ''
    return f'<details class="{classes}"{state}><summary>{e(label)} <span aria-hidden="true">+</span></summary>{content}</details>'


def build(data_file, template_file, output_file):
    data = json.loads((root / data_file).read_text())
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
            voices += f'<div class="witness supporting-voice"><blockquote>“{e(voice["quote"])}”</blockquote><p class="citation"><strong>{e(voice["author"])}</strong> · {source_link(voice)}<span>{e(voice["edition"])}</span></p><p class="witness-context">{e(voice["context"])}</p></div>'
        supporting_html = disclosure(f'More cessationist voices · {len(supporting)}', f'<div class="supporting-voices">{voices}</div>', 'supporting-disclosure', adaptive=True) if supporting else ''

        criticism = q.get('criticism')
        if criticism:
            critic_context = f'<p class="citation">{source_link(criticism)}<span>{e(criticism["edition"])}</span></p><p class="criticism-kind">{e(criticism["kind"])}</p><p class="critic-context">{e(criticism["context"])}</p>'
            critic_details = disclosure('Citation & context', critic_context, 'critic-details', adaptive=True)
            claim_side = f'<h3 class="mobile-entry-heading">{e(q["title"])}</h3><p class="eyebrow">THE CRITICISM</p><blockquote class="critic-quote"><p>“{e(criticism["quote"])}”</p></blockquote><p class="critic-author">{e(criticism["author"])}</p>{critic_details}'
        else:
            claim_side = f'<p class="eyebrow">THE COMMON CLAIM</p><h3>{e(q["claim"])}</h3><p class="claim-note">Editorial summary · see our approach</p>'

        edition = f'{e(q.get("edition_label", "Translation"))}: {e(q.get("edition", q.get("translation", "")))}'
        source_citation = f'<p class="citation source-citation">{source_link(q)}<span>{edition}</span></p>'
        context = f'<div class="context"><h4>{e(q["title"])}</h4><p>{e(q["response"])}</p><p><strong>Read in context.</strong> {e(q["context"])}</p></div>'
        source_details = disclosure('Citation & context', source_citation + context, 'entry-context', adaptive=True)
        entries.append(f'''<article class="entry" id="{q['id']}" data-topic="{e(q['topic'])}"><div class="claim-side"><span class="entry-number">{q['number']:02d}</span><span class="topic">{e(q['topic'])}</span>{claim_side}</div><div class="quote-side"><p class="eyebrow">IN HIS OWN WORDS</p><blockquote>“{e(q['quote'])}”</blockquote><p class="lead-author">{e(q['author'])}</p>{source_details}{supporting_html}{conf_html}<div class="entry-actions"><a href="{e(q['url'])}">Read the source {ARROW}</a><button type="button" data-copy="{q['id']}" hidden>Copy citation</button><a href="#{q['id']}" class="permalink" aria-label="Permanent link: {e(q['title'])}"># Share entry</a></div></div></article>''')
    (root / output_file).write_text((root / template_file).read_text().replace('{{ENTRIES}}', '\n'.join(entries)))
    print(f'Built {len(data)} entries into {output_file}')


build('quotes.json', 'index.template.html', 'index.html')
build('cessationists.json', 'cessationists.template.html', 'cessationists.html')
