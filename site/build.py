"""Build the Tonal page from the kit and the test results.

    python site/build.py

Writes site/index.html and copies the two web fonts it uses next to it. Every
language is written into the file as plain HTML, so the brand checker and a
reader without JavaScript see all of it; the switch only shows one at a time.
Colours, families and tracking come from Studio/Brand/design/tokens.css, read
at build time. The prompt is set exactly as kit/<lang>/interview.txt holds it,
because the copy button copies that text.
"""
import ast, html, pathlib, re, shutil, sys

SITE = pathlib.Path(__file__).parent
ROOT = SITE.parent
BRAND = ROOT.parent.parent / "Studio" / "Brand"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "test"))
from check import size
import scan

FONTS = ["overused-grotesk-bold.woff2", "host-grotesk.woff2"]
LICENCES = ["OverusedGrotesk-OFL.txt", "HostGrotesk-OFL.txt"]
LANGS = ["fr", "en", "es"]
DASH = re.compile("[\u2014\u2013]")
BEFORE = re.compile(r"^(Before|Not|Avant|Pas ça|Antes)\s?:")
UNREVIEWED = "Sin revisar: ningún hablante nativo ha leído todavía la versión en español de este kit."

COPY = {
    "en": {
        "lede": "An interview that reads texts you wrote and turns them into a voice file: a text you give ChatGPT, Claude or Gemini so that what it writes for you sounds like your brand.",
        "how": "How it works",
        "method": [
            "Paste the prompt below into a new chat with ChatGPT, Claude or Gemini, as your first message. It asks for three to five texts you wrote and like, and one you would hate to have written.",
            "It tells you what your texts do, then asks twelve questions at most, one per message. Each comes with answers drafted from your texts. Pick one, correct one, or say \"decide for me\". It talks to you in the language you write in.",
            "At the end it writes your voice file in two sizes, in plain text. The short one stays under 1,500 characters, the size of ChatGPT's custom instructions on the free plan. The full one stays under 8,000 and goes into a project or a skill. Where to paste each one is further down.",
        ],
        "prompt": "The prompt", "chars": "{n} characters.", "copy": "Copy the prompt", "done": "Copied",
        "templates": "The two templates",
        "templates_p": "The interview fills these in with your answers. They are already in the prompt; they are here so you can read them first.",
        "short": "The short file", "full": "The full file",
        "proof": "Levain, before and after",
        "proof_p": [
            "Levain is a fictional bakery. On 26 October 2026 an AI played its founder through this interview, with nobody editing anything between the first message and the voice file. The same five requests then went to Claude twice: once with nothing, and once with that voice file in its instructions.",
            "A script counted the tells it can see on the surface, such as emoji, hashtags and the words on the list. In the five texts written without the file it found {without}, and in the five written with it, {with}.",
            "A script cannot see an invented fact, or a text that no longer does its job, so all ten texts were also read by hand. Without the file, the reply says forty loaves \"each week\", a unit no request gave, and the page, the caption and the newsletter praise a taste or a crust no request mentioned. With the file, each text still does what its kind of text is for: the reply tells the customer how to make sure of a loaf, and the post ends on the address to write to. The file also got two things wrong. It repeats \"the next bake is for the day after tomorrow\" where that line contradicts the request, and the post adds \"so each bake is planned two days ahead\", which nobody gave.",
            "For the LinkedIn post, the file first asked what the post was for, because Levain had no LinkedIn text to learn from. The post below came after a one-line answer.",
            "This test ran on an earlier version of the kit, before the file took each kind of text's shape from your texts and asked only for the facts a text cannot do without. It has not been run again since.",
        ],
        "none": "none", "request": "The request", "without": "Without the file", "with": "With the file",
        "tasks": {"page": "The paragraph for the website", "instagram": "An Instagram caption", "reply": "A reply to an unhappy customer",
                  "newsletter": "The opening of a newsletter", "linkedin": "A LinkedIn post"},
        "licence": "Free, under the MIT licence.",
    },
    "fr": {
        "lede": "Un entretien qui lit des textes que vous avez écrits et en tire un fichier de voix : un texte que vous donnez à ChatGPT, Claude ou Gemini pour que ce qu'il écrit pour vous sonne comme votre marque.",
        "how": "Comment ça marche",
        "method": [
            "Collez le prompt ci-dessous dans une nouvelle conversation avec ChatGPT, Claude ou Gemini, comme premier message. Il vous demande trois à cinq textes que vous avez écrits et que vous aimez, et un texte que vous détesteriez avoir écrit.",
            "Il vous dit ce que font vos textes, puis pose douze questions au plus, une par message. Chacune vient avec des réponses rédigées à partir de vos textes. Choisissez-en une, corrigez-en une, ou dites « décide pour moi ». Il vous parle dans la langue où vous écrivez.",
            "À la fin, il écrit votre fichier de voix en deux tailles, en texte brut. Le fichier court reste sous 1 500 caractères, la taille des instructions personnalisées de ChatGPT en offre gratuite. Le fichier complet reste sous 8 000 et va dans un projet ou une compétence. Où coller chacun est expliqué plus bas.",
        ],
        "prompt": "Le prompt", "chars": "{n} caractères.", "copy": "Copier le prompt", "done": "Copié",
        "templates": "Les deux modèles",
        "templates_p": "L'entretien les remplit avec vos réponses. Ils sont déjà dans le prompt ; ils sont ici pour que vous puissiez les lire avant.",
        "short": "Le fichier court", "full": "Le fichier complet",
        "proof": "Levain, avant et après",
        "proof_p": [
            "Levain est une boulangerie fictive. Le 27 octobre 2026, une IA a joué son fondateur pendant cet entretien, sans que personne ne modifie rien entre le premier message et le fichier de voix. Les mêmes cinq demandes ont ensuite été envoyées deux fois à Claude : une fois sans rien, une fois avec ce fichier dans ses instructions.",
            "Un script a compté les tics qu'il peut voir en surface, comme les émojis, les hashtags et les mots de la liste. Dans les cinq textes écrits sans le fichier, il en a trouvé {without} ; dans les cinq écrits avec, {with}.",
            "Un script ne voit pas un fait inventé, alors les dix textes ont aussi été lus. Sans le fichier, la page prête au pain un « caractère franc et légèrement acidulé » que personne n'a décrit, et la publication LinkedIn promet « une vraie relation de confiance ». Avec le fichier, quatre des cinq textes s'en tiennent à la demande et aux textes du fondateur, à deux détails près. La page reprend une de ses phrases, « puis nous recommençons pour après-demain », qui contredit les quarante pains par jour de la demande. La réponse ajoute « Si la commande ne passe pas », une condition que personne n'a donnée.",
            "Avant le test, quatre conditions de réussite ont été fixées, dont celle-ci : aucun texte écrit avec le fichier n'est remplacé par une question ou une note. Le français échoue sur ce point. Pendant l'entretien, le fondateur joué par l'IA a choisi que Levain ne soit pas sur LinkedIn et qu'on lui demande avant d'écrire pour ce réseau. Le fichier l'a noté, et Claude a posé la question au lieu d'écrire la publication. Elle figure plus bas, telle quelle.",
        ],
        "none": "aucun", "request": "La demande", "without": "Sans le fichier", "with": "Avec le fichier",
        "tasks": {"page": "Le paragraphe du site", "instagram": "Une légende Instagram", "reply": "Une réponse à un client mécontent",
                  "newsletter": "L'ouverture d'une lettre d'information", "linkedin": "Une publication LinkedIn"},
        "licence": "Gratuit, sous licence MIT.",
    },
    "es": {
        "lede": "Una entrevista que lee textos que escribiste y saca de ellos un archivo de voz: un texto que le das a ChatGPT, Claude o Gemini para que lo que escribe por ti suene a tu marca.",
        "how": "Cómo funciona",
        "method": [
            "Pega el prompt de abajo en una conversación nueva con ChatGPT, Claude o Gemini, como primer mensaje. Te pide de tres a cinco textos que escribiste y te gustan, y uno que odiarías haber escrito.",
            "Te dice qué hacen tus textos y luego te hace doce preguntas como máximo, una por mensaje. Cada una llega con respuestas redactadas a partir de tus textos. Elige una, corrige una o di «decide tú». Te habla en el idioma en que escribes.",
            "Al final escribe tu archivo de voz en dos tamaños, en texto plano. El corto se queda por debajo de 1500 caracteres, el tamaño de las instrucciones personalizadas de ChatGPT en el plan gratuito. El completo se queda por debajo de 8000 y va en un proyecto o en una habilidad. Más abajo se explica dónde pegar cada uno.",
        ],
        "prompt": "El prompt", "chars": "{n} caracteres.", "copy": "Copiar el prompt", "done": "Copiado",
        "templates": "Las dos plantillas",
        "templates_p": "La entrevista las rellena con tus respuestas. Ya están dentro del prompt; aquí están para que las leas antes.",
        "short": "El archivo corto", "full": "El archivo completo",
        "proof": "Levain, antes y después",
        "proof_p": [
            "Levain es una panadería ficticia. El 27 de octubre de 2026, una IA hizo de su fundador durante esta entrevista, sin que nadie tocara nada entre el primer mensaje y el archivo de voz. Después, las mismas cinco peticiones fueron dos veces a Claude: una sin nada y otra con ese archivo en sus instrucciones.",
            "Un script contó los tics que puede ver en la superficie, como los emojis, los hashtags y las palabras de la lista. En los cinco textos escritos sin el archivo encontró {without}; en los cinco escritos con él, {with}.",
            "Un script no ve un dato inventado, así que los diez textos también se leyeron a mano. Sin el archivo, la web le da al pan un «sabor profundo, ligeramente ácido» que nadie describió, y la respuesta habla de «cuarenta piezas cada semana», una unidad que ninguna petición daba. Con el archivo, el texto para Instagram, la respuesta y el boletín se ciñen a la petición y a los textos del fundador. Dos textos añaden algo que nadie dio: la web dice que la masa madre se alimenta «por la mañana y por la tarde», y la publicación de LinkedIn promete «te diremos qué día se hornea cada pan y cuántos hay».",
            "Antes de la prueba se fijaron cuatro condiciones para darla por buena, entre ellas que ningún texto escrito con el archivo se sustituya por una pregunta o una nota. En español se cumplen las cuatro.",
        ],
        "none": "ninguno", "request": "La petición", "without": "Sin el archivo", "with": "Con el archivo",
        "tasks": {"page": "El párrafo de la web", "instagram": "Un texto para Instagram", "reply": "Una respuesta a un cliente molesto",
                  "newsletter": "La apertura de un boletín", "linkedin": "Una publicación de LinkedIn"},
        "licence": "Gratis, con licencia MIT.",
    },
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{background:var(--c1);color:var(--c2);font-family:var(--f-body);font-size:16px;line-height:1.6;
  font-variant-numeric:tabular-nums;font-synthesis:none;-webkit-font-smoothing:antialiased;overflow-wrap:break-word}
.band{color:var(--fg);background:var(--bg)}
.s1{--bg:var(--c1);--fg:var(--c2)} .s3{--bg:var(--c3);--fg:var(--c2)} .s4{--bg:var(--c4);--fg:var(--c2)}
.s7{--bg:var(--c7);--fg:var(--c2)} .s6{--bg:var(--c6);--fg:var(--c1)}
.wrap{max-width:1280px;margin:0 auto;padding:clamp(64px,10vw,120px) clamp(20px,5vw,64px)}
.top{display:flex;justify-content:space-between;align-items:baseline;gap:24px}
h1,h2,h3{font-family:var(--f-head);font-weight:700;text-transform:uppercase;letter-spacing:var(--head-track)}
h1{color:var(--c5);font-size:clamp(72px,17vw,119px);line-height:.88}
h2{font-size:clamp(40px,8vw,79px);line-height:.92;margin:0 0 clamp(32px,5vw,56px);max-width:16ch;overflow-wrap:anywhere}
h3{font-size:clamp(24px,4vw,35px);line-height:1;margin:clamp(48px,6vw,64px) 0 24px;max-width:26ch}
.lede{font-size:clamp(18px,2.4vw,22px);line-height:1.55;max-width:40ch;margin-top:clamp(40px,6vw,64px)}
p{max-width:52ch;margin:0 0 16px}
p.before{opacity:.6}
.meta{font-size:14px;opacity:.75;margin:0}
.note{font-size:14px;opacity:.75;max-width:52ch;margin-top:24px}
.lang{display:flex;gap:4px}
.lang button,.copy{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
.lang button{font-size:14px;letter-spacing:.08em;padding:8px 10px;opacity:.55;transition:opacity .2s}
.lang button[aria-pressed=true]{opacity:1}
.lang button:hover{opacity:.85}
button:focus-visible{outline:2px solid currentColor;outline-offset:3px}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:16px 24px;margin:0 0 24px}
.copy{background:var(--c2);color:var(--c3);padding:12px 20px;font-size:16px;font-weight:500;transition:opacity .2s}
.copy:hover{opacity:.7}
.text{font-family:var(--f-body);font-size:14px;line-height:1.6;white-space:pre-wrap;overflow-wrap:anywhere;
  background:var(--c1);color:var(--c2);padding:clamp(20px,3vw,32px);max-width:72ch}
.scroll{max-height:30rem;overflow:auto}
h2.sub{font-size:clamp(24px,4vw,35px);line-height:1;margin:clamp(48px,6vw,64px) 0 24px;max-width:26ch}
.groups{margin-top:clamp(48px,6vw,64px)}
.group{break-inside:avoid;padding-bottom:clamp(40px,5vw,56px)}
.group h3{margin-top:0}
@media (min-width:1100px){.tells .groups{columns:2;column-gap:96px}}
.pairs{display:grid;gap:clamp(48px,6vw,96px);margin-top:clamp(64px,8vw,96px)}
.pair h3{margin-top:0}
.ask{font-size:14px;opacity:.75;max-width:72ch}
.two{display:grid;grid-template-columns:1fr;gap:32px;margin-top:24px}
.two .label{font-size:14px;opacity:.75;margin:0 0 8px}
.two .said{white-space:pre-wrap;overflow-wrap:anywhere;max-width:52ch}
@media (min-width:860px){.two{grid-template-columns:1fr 1fr;gap:48px}
  .two>div+div{border-left:1px solid color-mix(in srgb,currentColor 14%,transparent);padding-left:48px}}
footer .wrap{padding-top:64px;padding-bottom:64px}
footer p{font-size:14px;margin:0}
"""

JS = """
const langs=['fr','en','es'];
function show(l){
  document.querySelectorAll('[data-lang]').forEach(s=>s.hidden=s.dataset.lang!==l);
  document.querySelectorAll('.lang button').forEach(b=>b.setAttribute('aria-pressed',b.value===l));
  document.documentElement.lang=l;
  history.replaceState(null,'','#'+l);
}
document.querySelectorAll('.lang button').forEach(b=>b.addEventListener('click',()=>show(b.value)));
const want=location.hash.slice(1), nav=(navigator.language||'').slice(0,2);
show(langs.includes(want)?want:langs.includes(nav)?nav:'en');
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{
  const text=document.getElementById(b.dataset.target).textContent;
  try{await navigator.clipboard.writeText(text)}
  catch(e){const r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.target));
    const s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy')}
  b.textContent=b.dataset.done;setTimeout(()=>b.textContent=b.dataset.label,2000);
}));
"""


def esc(s):
    return html.escape(s, quote=False)


def typo(s, lang):
    # French spacing on the page only, so a line never breaks before ":" or inside « » or 1 500.
    if lang != "fr":
        return s
    s = re.sub(r"(\d) (\d{3})\b", "\\1\u202f\\2", s)
    s = s.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
    return re.sub(r" ([:;?!])", "\u00a0\\1", s)


def md(path, lang, dashes_ok=False):
    # The kit's Markdown is headings and one paragraph per line, nothing else.
    # Each "##" part becomes a group, so a long list can sit in columns without splitting one.
    out, groups = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s == UNREVIEWED:
            continue
        if s.startswith("## "):
            groups.append([])
        dest = groups[-1] if groups else out
        if DASH.search(s):
            assert dashes_ok, f"{path}: dash outside the tells specimens: {s[:60]}"
            dest.append("<!-- brand-check: ok dash specimen from the tells list -->")
        t = esc(typo(s, lang))
        if s.startswith("## "):
            dest.append(f"<h3>{t[3:]}</h3>")
        elif s.startswith("# "):
            dest.append(f"<h2>{t[2:]}</h2>")
        else:
            dest.append(f"<p{' class=\"before\"' if BEFORE.match(s) else ''}>{t}</p>")
    return "\n".join(out + ['<div class="groups">'] + [f'<div class="group">\n{chr(10).join(g)}\n</div>' for g in groups] + ["</div>"])


def number(n, lang):
    return f"{n:,}".replace(",", {"en": ",", "fr": "\u202f", "es": ""}[lang] if n >= 10000 or lang != "es" else "")


def tasks():
    # tasks.py imports the API client; the requests are read from its source instead.
    tree = ast.parse((ROOT / "test" / "tasks.py").read_text(encoding="utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == "TASKS")
    return ast.literal_eval(node.value)


def figures(lang, c):
    total = {}
    for cond in ("without", "with"):
        texts = [(ROOT / "test" / "tasks" / lang / f"{t}-{cond}.txt").read_text(encoding="utf-8").strip() for t in scan.TASKS]
        total[cond] = sum(sum(scan.counts(lang, x).values()) for x in texts)
    return {"without": total["without"], "with": total["with"] or c["none"]}


def proof(lang, c, req):
    fig, pairs = figures(lang, c), []
    for t in scan.TASKS:
        said = {cond: (ROOT / "test" / "tasks" / lang / f"{t}-{cond}.txt").read_text(encoding="utf-8").strip()
                for cond in ("without", "with")}
        for x in said.values():
            assert not DASH.search(x), f"dash in a Levain text ({lang} {t})"
        r = req[lang]
        pairs.append(
            f'<div class="pair">\n<h3>{esc(c["tasks"][t])}</h3>\n'
            f'<p class="ask">{esc(c["request"])}{typo(" : " if lang == "fr" else ": ", lang)}{esc(typo(r["intro"] + r[t] + r["tail"], lang))}</p>\n'
            f'<div class="two">\n'
            + "".join(f'<div><p class="label">{esc(c[cond])}</p><p class="said">{esc(said[cond])}</p></div>\n' for cond in ("without", "with"))
            + "</div>\n</div>")
    paras = "\n".join(f"<p>{esc(typo(p.format(**fig), lang))}</p>" for p in c["proof_p"])
    return paras + '\n<div class="pairs">\n' + "\n".join(pairs) + "\n</div>"


def section(lang, req):
    c, kit = COPY[lang], ROOT / "kit" / lang
    prompt = (kit / "interview.txt").read_text(encoding="utf-8")
    assert not prompt.startswith("\n"), "a leading newline after <pre> is dropped by the parser"
    t = lambda s: esc(typo(s, lang))
    note = f'<p class="note">{esc(UNREVIEWED)}</p>\n' if lang == "es" else ""
    return f"""<div data-lang="{lang}" lang="{lang}"{"" if lang == "en" else " hidden"}>
<section class="band s1"><div class="wrap" style="padding-top:0">
<p class="lede">{t(c["lede"])}</p>
{note}<h2 class="sub">{t(c["how"])}</h2>
{"".join(f"<p>{t(p)}</p>" + chr(10) for p in c["method"])}</div></section>
<section class="band s3"><div class="wrap">
<h2>{t(c["prompt"])}</h2>
<div class="bar"><button class="copy" type="button" data-target="prompt-{lang}" data-label="{t(c["copy"])}" data-done="{t(c["done"])}">{t(c["copy"])}</button>
<p class="meta" aria-live="polite">{t(c["chars"].format(n=number(size(prompt), lang)))}</p></div>
<pre class="text scroll" id="prompt-{lang}" tabindex="0">{esc(prompt)}</pre>
<h3>{t(c["templates"])}</h3>
<p>{t(c["templates_p"])}</p>
<h3>{t(c["short"])}</h3>
<pre class="text">{esc((kit / "voice-short.txt").read_text(encoding="utf-8"))}</pre>
<h3>{t(c["full"])}</h3>
<pre class="text">{esc((kit / "voice-full.txt").read_text(encoding="utf-8"))}</pre>
</div></section>
<section class="band s4 tells"><div class="wrap">
{md(kit / "tells.md", lang, dashes_ok=True)}
</div></section>
<section class="band s7"><div class="wrap">
{md(kit / "where-to-paste.md", lang)}
</div></section>
<section class="band s6"><div class="wrap">
<h2>{t(c["proof"])}</h2>
{proof(lang, c, req)}
</div></section>
<section class="band s1"><div class="wrap" style="padding-bottom:0"><p class="meta">{t(c["licence"])}</p></div></section>
</div>"""


def tokens_css():
    # tokens.css as written, minus the faces this page does not ship, with font paths beside the page.
    css = (BRAND / "design" / "tokens.css").read_text(encoding="utf-8")
    faces = re.findall(r"@font-face\s*\{[^}]*\}", css)
    keep = [f for f in faces if any(name in f for name in FONTS)]
    assert len(keep) == len(FONTS), "a shipped face is missing from tokens.css"
    for f in faces:
        css = css.replace(f, f if f in keep else "")
    return re.sub(r"url\('\.\./fonts/web/", "url('fonts/", css)


def main():
    (SITE / "fonts").mkdir(exist_ok=True)
    for f in FONTS:
        shutil.copyfile(BRAND / "fonts" / "web" / f, SITE / "fonts" / f)
    for f in LICENCES:
        shutil.copyfile(BRAND / "fonts" / f, SITE / "fonts" / f)
    req = tasks()
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tonal</title>
<meta name="description" content="A free kit that turns a brand's own texts into a voice file for ChatGPT, Claude or Gemini, in French, English and Spanish.">
<meta name="color-scheme" content="dark">
<style>
{tokens_css()}
{CSS}</style>
</head>
<body>
<header class="band s1"><div class="wrap" style="padding-bottom:0">
<div class="top"><h1>Tonal</h1>
<nav class="lang" aria-label="Language">{"".join(f'<button type="button" value="{l}" lang="{l}" aria-pressed="{str(l == "en").lower()}">{l.upper()}</button>' for l in LANGS)}</nav></div>
</div></header>
<main>
{chr(10).join(section(l, req) for l in LANGS)}
</main>
<footer class="band s1"><div class="wrap"><p>Pierre Tran, Taykon Studio</p></div></footer>
<script>{JS}</script>
</body>
</html>
"""
    (SITE / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print(f"site/index.html, {len(page.encode('utf-8')):,} bytes")


if __name__ == "__main__":
    main()
