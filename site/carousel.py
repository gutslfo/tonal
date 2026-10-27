"""Build the Tonal carousel: the English kit and its Levain results, 1080 x 1350, for LinkedIn.

    python site/carousel.py [out.pdf]

Writes site/carousel.html with every chapter as plain HTML, so the brand checker
reads all of it. Chromium then pours each chapter into 1080 x 1350 slides of its
colour, starting a new slide when the next block does not fit, and prints the
PDF only if the audit is clean: no text under 24 px, nothing past the padding,
no italic, both faces loaded, Red on one slide. The default output is the gift's
visual in Studio/Media.
"""
import functools, http.server, importlib.util, pathlib, sys, threading
from playwright.sync_api import sync_playwright

# Loaded under another name: check.py imports the kit's own build.py as "build".
_spec = importlib.util.spec_from_file_location("page_build", pathlib.Path(__file__).parent / "build.py")
_page = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_page)
COPY, esc, figures, md, size, tasks, tokens_css, number, ROOT, SITE = (getattr(_page, n) for n in
    "COPY esc figures md size tasks tokens_css number ROOT SITE".split())
import scan

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent.parent / "Studio" / "Media" / "linkedin" / "visuals" / "gift-01" / "tonal.pdf"
LANG = "en"
# The page says "below" and "further down"; a carousel goes on, not down.
ON = [("the prompt below", "the prompt that follows"), ("further down", "further on"), ("The post below", "The post that follows")]

CSS = """
@page{size:1080px 1350px;margin:0}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--c1);font-family:var(--f-body);font-synthesis:none;-webkit-font-smoothing:antialiased;
  font-variant-numeric:tabular-nums;overflow-wrap:break-word}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;padding:84px 88px;break-after:page;
  display:flex;flex-direction:column}
.slide:last-child{break-after:auto}
.slide.flow{display:block}
.slide.flow>:first-child,.slide.flow>:first-child>:first-child{margin-top:0}
.c1{background:var(--c1);color:var(--c2)} .c3{background:var(--c3);color:var(--c2)} .c4{background:var(--c4);color:var(--c2)}
.c6{background:var(--c6);color:var(--c1)} .c7{background:var(--c7);color:var(--c2)}
.spacer{flex:1 1 auto}
h1,h2,h3{font-family:var(--f-head);font-weight:700;text-transform:uppercase;letter-spacing:var(--head-track)}
h1{color:var(--c5);font-size:176px;line-height:.86}
h2{font-size:97px;line-height:.96;margin:0 0 56px}
h3{font-size:52px;line-height:.98;margin:72px 0 28px}
p{font-size:26px;line-height:1.5;margin:0 0 20px}
.lead{font-size:36px;line-height:1.42;max-width:24ch;margin:48px 0 0}
.how p{font-size:31px;line-height:1.55;margin-bottom:28px}
p.before{opacity:.7;margin-bottom:8px}
.meta,.ask,.label,.foot{font-size:24px;line-height:1.45}
.meta,.ask,.label{opacity:.75}
.meta{margin:-24px 0 40px}
.ask{margin:0 0 8px}
.side{padding-top:36px}
.side+.side{border-top:1px solid color-mix(in srgb,currentColor 20%,transparent);margin-top:28px}
.label{margin:0 0 12px}
.said{white-space:pre-line;overflow-wrap:anywhere}
.ln{font-size:24px;line-height:1.45;margin:0;overflow-wrap:anywhere}
.ln.gap{margin-top:17px}
@media screen{#deck{display:flex;flex-direction:column;align-items:center;gap:40px;padding:40px 0}}
"""

# Units are the children of a chapter; .groups, .group and .pair are walked into. A unit marked
# .keep never ends a slide: it moves on with the unit after it. One that does not fit even on a
# fresh slide is split into its children; a leaf that still does not fit is left for the audit.
JS = """
// Every heading keeps with the block after it, whoever wrote the markup.
const KEEP = 'h2,h3,.keep';
function paginate(){
  const deck = document.getElementById('deck'), H = 1350, PAD = 84;
  document.querySelectorAll('.group').forEach((g, i) => [...g.children].forEach(k => k.dataset.sec = i));
  for (const ch of [...document.querySelectorAll('section.chapter')]) {
    let slide;
    const fresh = () => { slide = document.createElement('div'); slide.className = 'slide flow ' + ch.dataset.c; deck.insertBefore(slide, ch); };
    // A 52 px heading's glyph box is taller than its line; the audit measures text, so this does too.
    const over = () => {
      const el = slide.lastElementChild, r = document.createRange(); r.selectNodeContents(el);
      return Math.max(el.getBoundingClientRect().bottom, r.getBoundingClientRect().bottom) > slide.getBoundingClientRect().top + H - PAD + 0.5;
    };
    const place = u => {
      if (u.classList.contains('break') && slide.children.length) fresh();
      slide.appendChild(u);
      if (!over()) return;
      u.remove();
      const carry = [];
      while (slide.lastElementChild && slide.lastElementChild.matches(KEEP)) {
        const k = slide.lastElementChild; k.remove(); carry.unshift(k);
      }
      if (slide.children.length) {
        fresh();
        // A text that moves on alone takes its pair's title with it.
        if (u.dataset.title && !carry.length) { const h = document.createElement('h3'); h.textContent = u.dataset.title; slide.appendChild(h); }
        carry.forEach(n => slide.appendChild(n)); slide.appendChild(u);
        if (!over()) return;
        u.remove();
      } else carry.forEach(n => slide.appendChild(n));
      if (u.matches('.group')) [...u.children].forEach(k => k.dataset.big = 1);  // taller than a slide: the audit allows the split
      if (u.children.length) [...u.children].forEach(place); else slide.appendChild(u);
    };
    // A section (.group) moves whole; it is split only if it does not fit on an empty slide.
    const units = [], walk = el => { for (const k of [...el.children]) k.matches('.groups,.pair') ? walk(k) : units.push(k); };
    walk(ch);
    fresh();
    units.forEach(place);
    ch.remove();
  }
}
function audit(){
  const RED = 'rgb(188, 42, 59)', out = {slides: 0, small: [], wide: [], low: [], italic: [], red: [], stranded: []};
  document.querySelectorAll('.slide').forEach((s, i) => {
    const b = s.getBoundingClientRect(), n = i + 1;
    // Its own selector, not KEEP: a guard that shares the rule it checks cannot catch that rule.
    let last = s.lastElementChild;
    while (last.matches('.group,.side') && last.lastElementChild) last = last.lastElementChild;  // the last line, not its wrapper
    if (s.classList.contains('flow') && last.matches('h1,h2,h3,.label,.ask,.before,.head')) out.stranded.push(n + ' ' + last.textContent.slice(0, 40));
    let red = getComputedStyle(s).backgroundColor === RED;
    const w = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const t = w.currentNode, el = t.parentElement;
      if (!t.textContent.trim()) continue;
      const cs = getComputedStyle(el), range = document.createRange(); range.selectNodeContents(t);
      const r = range.getBoundingClientRect(), say = n + ' ' + t.textContent.trim().slice(0, 40);
      if (parseFloat(cs.fontSize) < 24) out.small.push(say + ' ' + cs.fontSize);
      if (cs.fontStyle !== 'normal') out.italic.push(say);
      if (r.right > b.left + 1080 - 88 + 0.5) out.wide.push(say + ' ' + Math.round(r.right - b.left));
      if (r.bottom > b.top + 1350 - 84 + 0.5) out.low.push(say + ' ' + Math.round(r.bottom - b.top));
      if (cs.color === RED) red = true;
    }
    if (red) out.red.push(n);
  });
  out.split = [];
  const where = {};
  document.querySelectorAll('.slide').forEach((s, i) => s.querySelectorAll('[data-sec]:not([data-big])').forEach(k => (where[k.dataset.sec] ||= new Set()).add(i + 1)));
  for (const [sec, on] of Object.entries(where)) if (on.size > 1)
    out.split.push([...on].join('+') + ' ' + document.querySelector(`[data-sec="${sec}"]`).textContent.slice(0, 40));
  out.slides = document.querySelectorAll('.slide').length;
  out.fonts = [document.fonts.check('700 52px "Overused Grotesk"'), document.fonts.check('400 26px "Host Grotesk"')];
  return out;
}
"""


def on(s):
    for a, b in ON:
        s = s.replace(a, b)
    return s


def chapter(c, body, cls=""):
    return f'<section class="chapter{cls}" data-c="{c}">\n{body}\n</section>'


def said(text):
    return "".join(f'<p class="said">{esc(p)}</p>' for p in text.split("\n\n"))


def html_page():
    c, kit, req = COPY[LANG], ROOT / "kit" / LANG, tasks()[LANG]
    text = " ".join(c["method"] + c["proof_p"])
    for a, b in ON:
        assert a in text, f"nothing to turn on: {a}"
    fig = figures(LANG, c)

    cover = (f'<div class="slide c1"><div class="spacer"></div><h1>Tonal</h1>'
             f'<p class="lead">{esc(c["lede"])}</p><div class="spacer"></div></div>')
    how = chapter("c3", f'<h2 class="keep">{esc(c["how"])}</h2>\n' + "\n".join(f"<p>{esc(on(p))}</p>" for p in c["method"]), " how")

    pairs = []
    for t in scan.TASKS:
        sides = "".join(
            f'<div class="side" data-title="{esc(c["tasks"][t])}"><p class="label keep">{esc(c[cond])}</p>'
            f'{said((ROOT / "test" / "tasks" / LANG / f"{t}-{cond}.txt").read_text(encoding="utf-8").strip())}</div>'
            for cond in ("without", "with"))
        pairs.append(f'<div class="pair"><h3 class="break keep">{esc(c["tasks"][t])}</h3>'
                     f'<p class="ask keep">{esc(c["request"])}: {esc(req["intro"] + req[t] + req["tail"])}</p>{sides}</div>')
    proof = chapter("c6", f'<h2 class="keep">{esc(c["proof"])}</h2>\n'
                    + "\n".join(f"<p>{esc(on(p.format(**fig)))}</p>" for p in c["proof_p"]) + "\n" + "\n".join(pairs))

    prompt = (kit / "interview.txt").read_text(encoding="utf-8")
    # The prompt's headings are its lines in capitals; each one opens a section that moves whole.
    secs, sec, gap = [], [], False
    for ln in prompt.split("\n"):
        if not ln.strip():
            gap = True
            continue
        head = ln == ln.upper() and any(ch.isalpha() for ch in ln)
        if head and any(" head " not in s for s in sec):  # a section of headings only joins the next one
            secs.append(sec)
            sec = []
        sec.append(f'<p class="ln{" gap" if gap else ""}{" head keep" if head else ""}">{esc(ln)}</p>')
        gap = False
    secs.append(sec)
    prompt_ch = chapter("c1", f'<h2 class="keep">{esc(c["prompt"])}</h2>\n<p class="meta keep">'
                        f'{esc(c["chars"].format(n=number(size(prompt), LANG)))}</p>\n'
                        + "\n".join(f'<div class="group">{"".join(s)}</div>' for s in secs))

    where = chapter("c7", md(kit / "where-to-paste.md", LANG))
    tells = chapter("c4", md(kit / "tells.md", LANG, dashes_ok=True).replace('<p class="before">', '<p class="before keep">'))
    closer = (f'<div class="slide c1"><div class="spacer"></div><p class="lead">{esc(c["licence"])}</p>'
              f'<div class="spacer"></div><p class="foot">Pierre Tran, Taykon Studio</p></div>')

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>Tonal</title>
<style>
{tokens_css()}
{CSS}</style>
</head>
<body>
<div id="deck">
{cover}
{how}
{proof}
{prompt_ch}
{where}
{tells}
{closer}
</div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    page = SITE / "carousel.html"
    page.write_text(html_page(), encoding="utf-8", newline="\n")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        log_message = lambda *a: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(SITE)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            tab = browser.new_page(viewport={"width": 1080, "height": 1350})
            tab.emulate_media(media="print")
            tab.goto(f"http://127.0.0.1:{server.server_port}/carousel.html")
            tab.evaluate("document.fonts.ready")
            tab.evaluate("paginate()")
            a = tab.evaluate("audit()")
            problems = {k: a[k] for k in ("small", "wide", "low", "italic", "stranded", "split") if a[k]}
            if not all(a["fonts"]):
                problems["fonts"] = a["fonts"]
            if len(a["red"]) != 1:
                problems["red"] = a["red"]
            print(f"{a['slides']} slides  small {len(a['small'])}  wide {len(a['wide'])}  low {len(a['low'])}  "
                  f"italic {len(a['italic'])}  stranded {len(a['stranded'])}  split {len(a['split'])}  "
                  f"red on {a['red']}  fonts {a['fonts']}")
            if problems:
                for k, v in problems.items():
                    print(f"  {k}: {v[:8] if isinstance(v, list) else v}")
                raise SystemExit("carousel: audit failed, no PDF written")
            OUT.parent.mkdir(parents=True, exist_ok=True)
            tab.pdf(path=str(OUT), prefer_css_page_size=True, print_background=True)
            browser.close()
    finally:
        server.shutdown()
    print(f"{OUT}, {OUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
