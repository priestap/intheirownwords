'use strict';
const compactReading = matchMedia('(max-width: 620px)');
function setReadingDisclosures() {
  document.querySelectorAll('[data-mobile-collapse]').forEach(details => {
    details.open = !compactReading.matches;
  });
}
setReadingDisclosures();
compactReading.addEventListener('change', setReadingDisclosures);
const entries = [...document.querySelectorAll('.entry')];
const search = document.querySelector('#search');
const filters = document.querySelector('#filters');
const selectedTopics = new Set();
const topics = ['All topics', ...new Set(entries.map(entry => entry.dataset.topic))];
const buttons = topics.map(name => {
  const button = document.createElement('button');
  button.type = 'button'; button.textContent = name;
  button.setAttribute('aria-pressed', String(name === 'All topics'));
  button.addEventListener('click', () => {
    if (name === 'All topics') selectedTopics.clear();
    else if (selectedTopics.has(name)) selectedTopics.delete(name);
    else selectedTopics.add(name);
    update();
  });
  filters.append(button); return button;
});
function update() {
  const term = search.value.trim().toLocaleLowerCase();
  let count = 0;
  entries.forEach(entry => {
    const visible = (selectedTopics.size === 0 || selectedTopics.has(entry.dataset.topic)) && entry.textContent.toLocaleLowerCase().includes(term);
    entry.hidden = !visible; if (visible) count++;
  });
  buttons.forEach(button => button.setAttribute('aria-pressed', String(button.textContent === 'All topics' ? selectedTopics.size === 0 : selectedTopics.has(button.textContent))));
  document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'}`;
  document.querySelector('#empty').hidden = count !== 0;
  document.querySelector('#clear-topics').hidden = selectedTopics.size === 0;
  document.querySelector('#search-clear').hidden = search.value.length === 0;
  document.querySelector('#filter-count').textContent = selectedTopics.size ? ` · ${selectedTopics.size} selected` : '';
}
function reset() { selectedTopics.clear(); search.value = ''; update(); }
search.addEventListener('input', update);
document.querySelector('#clear-topics').addEventListener('click', () => {
  selectedTopics.clear();
  buttons[0].focus();
  update();
});
document.querySelector('#search-clear').addEventListener('click', () => {
  search.value = '';
  search.focus();
  update();
});
document.querySelector('#clear-search').addEventListener('click', () => { reset(); search.focus(); });
document.querySelector('.tools').hidden = false; filters.hidden = false;
document.querySelector('#topic-disclosure').hidden = false;
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.ctrlKey && !event.metaKey && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) { event.preventDefault(); search.focus(); }
});
let toastTimer;
function notify(message) { const toast = document.querySelector('#toast'); toast.textContent = message; toast.classList.add('visible'); clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove('visible'), 4000); }
document.querySelectorAll('[data-copy]').forEach(button => {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const entry = document.getElementById(button.dataset.copy);
    const quotation = entry.querySelector('.quote-side > blockquote').textContent;
    const citation = `${entry.querySelector('.lead-author').textContent} · ${entry.querySelector('.source-citation').textContent}`;
    const source = entry.querySelector('.source-citation a').href;
    try { await navigator.clipboard.writeText(`${quotation}\n— ${citation}\n${source}`); notify('Quotation and source copied.'); }
    catch { notify('Copy unavailable. Select the quotation and citation to copy them.'); }
  });
});
function revealHash() {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const entry = document.getElementById(id);
  if (entry?.classList.contains('entry')) { reset(); entry.querySelector('.entry-context').open = true; entry.scrollIntoView({ block: 'start' }); }
}
window.addEventListener('hashchange', revealHash);
revealHash();

const themeToggle = document.querySelector('#theme-toggle');
const systemTheme = matchMedia('(prefers-color-scheme: dark)');
let themeChoice;
try { themeChoice = localStorage.getItem('reading-theme'); } catch {}
function setTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelector('#theme-label').textContent = theme === 'dark' ? 'Light mode' : 'Dark mode';
  themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#131317' : '#fafafa';
}
setTheme(document.documentElement.dataset.theme || (systemTheme.matches ? 'dark' : 'light'));
themeToggle.hidden = false;
themeToggle.addEventListener('click', () => {
  themeChoice = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  setTheme(themeChoice);
  try { localStorage.setItem('reading-theme', themeChoice); } catch {}
});
systemTheme.addEventListener('change', event => { if (!themeChoice) setTheme(event.matches ? 'dark' : 'light'); });

// Keep native anchor behavior available when clipboard access is unavailable.
document.querySelectorAll('.permalink').forEach(link => {
  link.addEventListener('click', async () => {
    const url = new URL(link.getAttribute('href'), window.location.href).href;
    try {
      await navigator.clipboard.writeText(url);
      notify('Entry link copied.');
    } catch {
      notify('Link opened. Copy the address from your browser to share it.');
    }
  });
});

const smallerText = document.querySelector('#text-smaller');
const largerText = document.querySelector('#text-larger');
const resetText = document.querySelector('#text-reset');
let readingSize = 100;
try {
  const savedSize = Number(localStorage.getItem('reading-size'));
  if (Number.isFinite(savedSize) && savedSize >= 90 && savedSize <= 150) readingSize = Math.round(savedSize / 10) * 10;
} catch {}
function setReadingSize(size, announce = true) {
  readingSize = Math.min(150, Math.max(90, size));
  document.documentElement.style.setProperty('--reading-scale', readingSize / 100);
  resetText.textContent = `${readingSize}%`;
  smallerText.disabled = readingSize === 90;
  largerText.disabled = readingSize === 150;
  if (announce) document.querySelector('#text-size-status').textContent = `Reading text size ${readingSize} percent`;
  try { localStorage.setItem('reading-size', String(readingSize)); } catch {}
}
smallerText.addEventListener('click', () => setReadingSize(readingSize - 10));
largerText.addEventListener('click', () => setReadingSize(readingSize + 10));
resetText.addEventListener('click', () => setReadingSize(100));
setReadingSize(readingSize, false);
document.querySelector('#reading-controls').hidden = false;

const siteHeader = document.querySelector('.site-header');
const menuToggle = document.querySelector('#menu-toggle');
const siteNavigation = document.querySelector('#site-navigation');
const mobileNavigation = matchMedia('(max-width: 620px)');
function setMenuOpen(open, returnFocus = false) {
  siteHeader.classList.toggle('menu-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  if (open) siteNavigation.querySelector('a')?.focus();
  else if (returnFocus) menuToggle.focus();
}
siteHeader.classList.add('nav-ready');
menuToggle.hidden = false;
menuToggle.addEventListener('click', () => setMenuOpen(menuToggle.getAttribute('aria-expanded') !== 'true'));
siteNavigation.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenuOpen(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
    setMenuOpen(false, true);
  }
});
document.addEventListener('click', event => {
  if (!siteHeader.contains(event.target)) setMenuOpen(false);
});
siteHeader.addEventListener('focusout', event => {
  if (!siteHeader.contains(event.relatedTarget)) setMenuOpen(false);
});
mobileNavigation.addEventListener('change', () => setMenuOpen(false));
