# In Their Own Words

Two linked primary-source collections: **Calvin & Reformed** (`index.html`) and **Cessationists** (`cessationists.html`). Each collection has its own URL, introduction, sources, search, and topic filters. Collection navigation and all quotations work without JavaScript.

The Calvin collection pairs 13 editorial summaries of claims about Calvinism with verified excerpts from John Calvin, contextual commentary, and 32 confessional excerpts from the Westminster Confession, Canons of Dort, Heidelberg Catechism, Belgic Confession, Second London Baptist Confession (1689), and Second Helvetic Confession (1566).

Plain HTML, CSS, and JavaScript. No dependencies, account, tracking, external fonts, or build service. The full collection and source citations remain readable without JavaScript. All paths work on GitHub project Pages as well as a custom domain.

## Preview

Run `python3 -m http.server 4173` in this directory, then visit http://localhost:4173. You can also open index.html directly; clipboard support depends on browser security settings.

## Publish on GitHub Pages

1. Create a public GitHub repository and upload these files, preserving the `.github/workflows` directory.
2. Use `main` as the default branch (or change the branch in `.github/workflows/pages.yml`).
3. In the repository’s **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
4. Push to `main`, or run **Deploy to GitHub Pages** from the Actions tab. GitHub supplies the public URL after deployment.

No repository has been created or published by this project setup.

## Edit and verify

- `quotes.json`: entries, exact excerpts, citation references, translation metadata, context, and source URLs.
- `cessationists.json`: six verified modern excerpts from Thomas R. Schreiner, Sinclair B. Ferguson, and Richard B. Gaffin, Jr., with source editions and author-specific context.
- `index.template.html` and `cessationists.template.html`: page structure and introductory copy for each collection.
- `style.css`: responsive layout, light/dark palettes, focus states, reduced motion, and print styles.
- `app.js`: search, topic filters, copy citation, deep links, and saved theme preference.

After editing data or the template, run:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check app.js
```

Commit the generated `index.html` and `cessationists.html` too, so the repository also works as a branch-served static site. GitHub Actions rebuilds it automatically. Python and Node are development tools only; the deployed site needs neither.

## Editorial policy

Every displayed quotation has an author or confessional attribution, precise location, and a link to the source text. Historical English translations are identified. Excerpt boundaries can omit punctuation surrounding the quoted phrase. Do not silently modernize quotations.

Claim headings are editorial summaries, not quotations from named critics. The founding draft’s modern critics’ quotations are not reproduced because this first version does not include a completed primary-source audit of those attributions. This release also does not reproduce every quotation in that draft.

The source text establishes what a writer said, not necessarily the truth or consistency of the writer’s theology. Context notes preserve qualifications relevant to a fair reading. Do not expand the site by adding plausible-sounding quotations from memory or AI output: inspect the actual source and document the reference first.

The initial collection was checked against the linked CCEL transcriptions, the Orthodox Presbyterian Church’s confession text, and the historic confessional texts published by the Free Reformed Churches of North America on November 11, 2026. Eight excerpts from the Second London Baptist Confession (1689) were also checked against Reformed Baptist Seminary’s English text on that date. Links point to chapters, complete commentary transcriptions, or the full confession; use the displayed section/verse reference to locate the passage. Transcriptions can contain errors: compare historical scans when a textual question arises.

## Accessibility and privacy

Semantic headings and landmarks, a skip link, keyboard-operable native disclosures, visible focus, readable font sizes, topic button states, search announcements, reduced-motion support, and print styles are provided. Light/dark mode follows the device initially and remembers a manual preference locally. There are no cookies or analytics. Formal accessibility certification and visual browser testing have not been completed.

## Reuse

Code is MIT licensed. Original editorial text is CC BY 4.0. Historic quotations remain subject to their own public-domain status; see CONTENT-LICENSE.md. No endorsement by Calvin’s source hosts or any denomination is implied.

Nine Second Helvetic Confession excerpts were verified against the CCEL transcription of the English version in Philip Schaff’s *The Creeds of Christendom*, Volume III, Appendix, on November 11, 2026. Chapter references use the source’s Roman numerals. The footer’s “My confession of faith” links to the site creator’s personal statement, independently of the historical source collection.

## Cessationist collection

The six modern excerpts were checked against the linked primary-source articles on November 11, 2026. Each entry now includes an exact critical excerpt from R. T. Kendall, Sam Storms, or Michael Brown, with its own source and context. Broad descriptions of belief, criticisms of consequences, claims about motives, and interpretive disagreements are distinguished; a disagreement is not automatically treated as misrepresentation. Each source contributes at most 25 quoted words. Modern excerpts retain their existing copyright and are not included in the editorial CC BY license. Source references identify sections or paragraphs; the Themelios reference also identifies the printed page. The writers’ differences and the limits of each excerpt are noted. Claim headings are editorial summaries, not quotations attributed to critics.

The cessationist entries also include six **Confessional witness** excerpts inside their context disclosures: Westminster 5.3 and 1689 5.3 (miracles), Westminster 21.4 (prayer), 26.1 (shared gifts), 1.6 (illumination), and 1.1 (revelation). Each has source metadata, a verification date, and a note delimiting its relevance. No confessional excerpt is attached to the entry on motives: these standards do not establish why an individual holds a position.

Three supporting excerpts are visible directly below the lead quotations for miracles, healing, and continuing gifts. Editorial context and confessional witness remain in the context disclosures. John MacArthur’s 1971 Grace to You sermon contributes two brief excerpts; the OPC’s 1978 committee report contributes one on healing and prayer. Each supporting voice has a precise reference, edition, source link, context, and verification date. The report’s study status is explicit.
