"""Generate the committed, JavaScript-optional GitHub Pages entry point."""
import json
from pathlib import Path
from html import escape as e
root=Path(__file__).resolve().parent.parent
def build(data_file, template_file, output_file):
 data=json.loads((root/data_file).read_text())
 entries=[]
 for q in data:
  confessions=q.get('confessions', [])
  witness=''
  for conf in confessions:
   edition=('<p class="witness-edition">'+e(conf['edition'])+'</p>') if conf.get('edition') else ''
   context=('<p class="witness-context">'+e(conf['context'])+'</p>') if conf.get('context') else ''
   witness+=('<div class="witness"><p class="eyebrow">CONFESSIONAL WITNESS</p><blockquote>“'+e(conf['quote'])+'”</blockquote><a href="'+e(conf['url'])+'">'+e(conf['reference'])+' ↗</a>'+edition+context+'</div>')
  conf_label=f" · {len(confessions)} confessional {'excerpt' if len(confessions)==1 else 'excerpts'}" if confessions else ''
  supporting=q.get('supporting_quotes', [])
  supporting_html=''
  if supporting:
   supporting_html='<div class="supporting-voices"><h4>Supporting voices</h4>'
   for voice in supporting:
    supporting_html+=f'''<div class="witness supporting-voice"><blockquote>“{e(voice['quote'])}”</blockquote><p class="citation"><strong>{e(voice['author'])}</strong> · <a href="{e(voice['url'])}">{e(voice['reference'])} ↗</a><span>{e(voice['edition'])}</span></p><p class="witness-context">{e(voice['context'])}</p></div>'''
   supporting_html+='</div>'
  criticism=q.get('criticism')
  if criticism:
   claim_side=f'''<p class="eyebrow">THE CRITICISM</p><blockquote class="critic-quote"><h3>“{e(criticism['quote'])}”</h3></blockquote><p class="citation critic-citation"><strong>{e(criticism['author'])}</strong> · <a href="{e(criticism['url'])}">{e(criticism['reference'])} ↗</a><span>{e(criticism['edition'])}</span></p><p class="criticism-kind">{e(criticism['kind'])}</p><p class="critic-context">{e(criticism['context'])}</p>'''
  else:
   claim_side=f'''<p class="eyebrow">THE COMMON CLAIM</p><h3>{e(q['claim'])}</h3><p class="claim-note">Editorial summary · see our approach</p>'''
  entries.append(f'''<article class="entry" id="{q['id']}" data-topic="{e(q['topic'])}"><div class="claim-side"><span class="entry-number">{q['number']:02d}</span><span class="topic">{e(q['topic'])}</span>{claim_side}</div><div class="quote-side"><p class="eyebrow">IN HIS OWN WORDS</p><blockquote>“{e(q['quote'])}”</blockquote><p class="citation"><strong>{e(q['author'])}</strong> · <a href="{e(q['url'])}">{e(q['reference'])} ↗</a><span>{e(q.get('edition_label', 'Translation'))}: {e(q.get('edition', q.get('translation', '')))}</span></p>{supporting_html}<details><summary>The distinction & context{conf_label} <span aria-hidden="true">+</span></summary><div class="context"><h4>{e(q['title'])}</h4><p>{e(q['response'])}</p><p><strong>Read in context.</strong> {e(q['context'])}</p>{witness}</div></details><div class="entry-actions"><a href="{e(q['url'])}">Read the source ↗</a><button type="button" data-copy="{q['id']}" hidden>Copy citation</button><a href="#{q['id']}" class="permalink" aria-label="Permanent link: {e(q['title'])}"># Share entry</a></div></div></article>''')
 (root/output_file).write_text((root/template_file).read_text().replace('{{ENTRIES}}','\n'.join(entries)))
 print(f'Built {len(data)} entries into {output_file}')

build('quotes.json', 'index.template.html', 'index.html')
build('cessationists.json', 'cessationists.template.html', 'cessationists.html')
