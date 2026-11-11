# In Their Own Words

A free static reading library pairing 13 editorial summaries of claims about Calvinism with verified excerpts from John Calvin, contextual commentary, and selected passages from the Westminster Confession.

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
- `index.template.html`: page structure and introductory copy.
- `style.css`: responsive layout, light/dark palettes, focus states, reduced motion, and print styles.
- `app.js`: search, topic filters, copy citation, deep links, and saved theme preference.

After editing data or the template, run:

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check app.js
```

Commit the generated `index.html` too, so the repository also works as a branch-served static site. GitHub Actions rebuilds it automatically. Python and Node are development tools only; the deployed site needs neither.

## Editorial policy

Every displayed quotation has an author or confessional attribution, precise location, and a link to the source text. Historical English translations are identified. Excerpt boundaries can omit punctuation surrounding the quoted phrase. Do not silently modernize quotations.

Claim headings are editorial summaries, not quotations from named critics. The founding draft’s modern critics’ quotations are not reproduced because this first version does not include a completed primary-source audit of those attributions. This release also does not reproduce every quotation in that draft.

The source text establishes what a writer said, not necessarily the truth or consistency of the writer’s theology. Context notes preserve qualifications relevant to a fair reading. Do not expand the site by adding plausible-sounding quotations from memory or AI output: inspect the actual source and document the reference first.

The initial collection was checked against the linked CCEL transcriptions and the Orthodox Presbyterian Church’s confession text on November 11, 2026. Links point to chapters, complete commentary transcriptions, or the full confession; use the displayed section/verse reference to locate the passage. Transcriptions can contain errors: compare historical scans when a textual question arises.

## Accessibility and privacy

Semantic headings and landmarks, a skip link, keyboard-operable native disclosures, visible focus, readable font sizes, topic button states, search announcements, reduced-motion support, and print styles are provided. Light/dark mode follows the device initially and remembers a manual preference locally. There are no cookies or analytics. Formal accessibility certification and visual browser testing have not been completed.

## Reuse

Code is MIT licensed. Original editorial text is CC BY 4.0. Historic quotations remain subject to their own public-domain status; see CONTENT-LICENSE.md. No endorsement by Calvin’s source hosts or any denomination is implied.
