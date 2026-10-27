"""Audit the page in a real browser and test the copy button.

    python test/surfaces.py [shots-dir]

Serves site/ on localhost (the clipboard API needs a secure context), then for
each language at 390 and 1440 px: no horizontal scroll, no element past the
right edge, no visible text under 12 px, no italic, both brand faces loaded.
The copy button must hand the clipboard kit/<lang>/interview.txt byte for
byte. The system clipboard is read back too: Windows stores line breaks as
CRLF, so that read is compared with CRLF turned back into LF, and the CR count
is printed. Exits 1 on any failure. Needs Playwright (test tooling, not the kit).
"""
import functools, http.server, pathlib, sys, threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent.parent
SHOTS = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
AUDIT = """() => {
  const vw = innerWidth, small = [], wide = [], italic = [];
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) {
    const n = w.currentNode, el = n.parentElement;
    if (!n.textContent.trim() || !el.getClientRects().length) continue;
    const cs = getComputedStyle(el);
    if (parseFloat(cs.fontSize) < 12) small.push(el.tagName + ' ' + cs.fontSize + ' ' + n.textContent.trim().slice(0, 30));
    if (cs.fontStyle !== 'normal') italic.push(el.tagName + ' ' + n.textContent.trim().slice(0, 30));
    // Text can run past its box (a long URL) while the box itself stays inside.
    const range = document.createRange(); range.selectNodeContents(n);
    if (range.getBoundingClientRect().right > vw + 0.5 && !el.closest('.scroll'))
      wide.push('text ' + Math.round(range.getBoundingClientRect().right) + ' ' + n.textContent.trim().slice(0, 40));
  }
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width && r.right > vw + 0.5) wide.push(el.tagName + '.' + el.className + ' ' + Math.round(r.right));
  }
  return {scroll: document.documentElement.scrollWidth - vw, small, wide, italic,
          fonts: [document.fonts.check('700 40px "Overused Grotesk"'), document.fonts.check('400 16px "Host Grotesk"')]};
}"""


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / "site"))
    handler.log_message = lambda *a: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/index.html"
    fails = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for width in (390, 1440):
            ctx = browser.new_context(viewport={"width": width, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
            ctx.add_init_script("""const w = navigator.clipboard.writeText.bind(navigator.clipboard);
              navigator.clipboard.writeText = t => { window.__copied = t; return w(t); };""")
            page = ctx.new_page()
            page.goto(url)
            page.evaluate("document.fonts.ready")
            for lang in ("fr", "en", "es"):
                page.click(f'.lang button[value="{lang}"]')
                a = page.evaluate(AUDIT)
                problems = {k: a[k] for k in ("small", "wide", "italic") if a[k]}
                if a["scroll"] > 0:
                    problems["scroll"] = a["scroll"]
                if not all(a["fonts"]):
                    problems["fonts"] = a["fonts"]
                print(f"{width:>5} {lang}  scroll {a['scroll']}  small {len(a['small'])}  wide {len(a['wide'])}  "
                      f"italic {len(a['italic'])}  fonts {a['fonts']}")
                if problems:
                    fails.append((width, lang, problems))
                if SHOTS:
                    SHOTS.mkdir(parents=True, exist_ok=True)
                    page.screenshot(path=str(SHOTS / f"{lang}-{width}.png"), full_page=True)
                if width == 390:
                    button = page.locator(f'[data-lang="{lang}"] .copy')
                    button.click()
                    handed = page.evaluate("window.__copied").encode("utf-8")
                    clip = page.evaluate("navigator.clipboard.readText()")
                    want = (ROOT / "kit" / lang / "interview.txt").read_bytes()
                    same, back = handed == want, clip.replace("\r\n", "\n").encode("utf-8") == want
                    print(f"      copy {lang}: {len(want):,} bytes, handed identical {same}, clipboard identical "
                          f"after CRLF {back} ({clip.count(chr(13))} CR), label '{button.inner_text()}'")
                    if not (same and back):
                        fails.append((width, lang, "clipboard differs"))
            ctx.close()
        browser.close()
    server.shutdown()
    for f in fails:
        print("FAIL", f)
    print("surfaces: clean" if not fails else f"surfaces: {len(fails)} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
