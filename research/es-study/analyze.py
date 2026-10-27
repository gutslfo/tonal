"""Compare the machine Spanish samples against pre-LLM human Spanish.

Human reference: the human half of AuTexTification 2023 (Spanish), domains news,
reviews, wiki and tweets; legal is left out as a register no brand writes in.
The texts predate 2023. Data is CC BY-NC-SA 4.0 and is not committed: see
data/README.md for the source.

    python -I analyze.py > results-raw.md
"""
import collections
import csv
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from generate import BUSINESSES, GENRES, TAIL  # noqa: E402

WORD = re.compile(r"[a-záéíóúüñ]+")
HUMAN_DOMAINS = ("news", "reviews", "wiki", "tweets")

# Published Spanish lists, checked here rather than trusted (grade C).
PUBLISHED = {
    "borjagiron.com 2026-08-12": ["en primer lugar", "adicionalmente", "en resumen", "en conclusión",
                                  "en última instancia", "es importante destacar", "vale la pena señalar",
                                  "por otro lado", "sumérgete", "desbloquear", "profundizar en", "elevar",
                                  "desatar", "revolucionar", "fomentar", "sin duda", "ciertamente", "magia",
                                  "brújula", "faro", "sinfonía", "tejido"],
    "elandroidefeliz.com 2024-07-02": ["asimismo", "de hecho", "esencialmente", "notablemente",
                                       "cuando se trata de", "en el ámbito de", "embárcate", "ahondar en",
                                       "en la era digital", "meticuloso", "vanguardia", "tapiz", "bullicioso",
                                       "paisaje", "testimonio", "vibrante", "crucial", "esencial", "vital",
                                       "laberinto", "enigma", "indeleble", "cambio de juego", "viaje",
                                       "resonar", "emprender"],
}

# Hypotheses written in Spanish from the brand-copy reflexes the humanizer lists
# for English (patterns 1, 4, 7, 9, 20) and French (37): what a Spanish model
# might reach for, to be confirmed or dropped by the counts, never assumed.
HYPOTHESES = ["en el corazón de", "el corazón de", "auténtic", "únic", "experiencia", "pasión", "cariño",
              "mimo", "artesan", "hecho a mano", "hechas a mano", "con amor", "cada detalle", "cada pieza",
              "rincón", "esencia", "alma", "tradición", "comunidad", "más que un", "detrás de", "historia",
              "calidez", "acogedor", "no dudes en", "te esperamos", "estamos aquí", "lamentamos", "lamento",
              "sin prisa", "dedicación", "compromiso", "descubre", "disfruta", "déjate", "ideal para",
              "perfecto para", "imprescindible", "a medida", "porque creemos", "creemos que", "sabemos que",
              "gracias por", "a quienes", "merece", "cuidado"]

# AuTexTification strips every quote mark from its texts (counted: zero " “ ” and
# no closing », human and generated alike), so quotes are not compared here.
STRUCT = {
    "raya (—), any": r"—",
    "en dash (–) not in a number range": r"(?<!\d)\s?–\s?(?!\d)",
    "no es X, es Y": r"\bno (?:es|son|era|fue|se trata de)\b[^.!?\n]{1,80}?[,;:.—–]\s*(?:es|son|era|fue|se trata de)\b",
    "no solo X sino Y": r"\bno (?:solo|sólo|solamente|únicamente)\b[^.!?\n]{1,80}?\bsino\b",
    "Sin X. Sin Y. chain": r"\b[Ss]in [^.!?\n]{1,30}\.\s+[Ss]in\b",
    "gerund after a comma": r",\s+[a-záéíóú]+(?:ando|iendo|yendo)\b",
    "X, Y y Z (one-word items)": r"\b[a-záéíóúñ]+, [a-záéíóúñ]+ y [a-záéíóúñ]+\b",
    "opening ¡": r"¡",
    "emoji": r"[\U0001F300-\U0001FAFF☀-➿]",
    "markdown bold **": r"\*\*",
}


def human_texts():
    csv.field_size_limit(10**9)
    by_domain = collections.defaultdict(list)
    for f in ("autext-es-train.tsv", "autext-es-test.tsv"):
        with open(HERE / "data" / f, encoding="utf-8") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if r["label"] == "human" and r["domain"] in HUMAN_DOMAINS:
                    by_domain[r["domain"]].append(r["text"])
    return by_domain


def machine_texts(who):
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted((HERE / "samples" / who).glob("*.txt"))}


def words(t):
    return WORD.findall(t.lower())


def ngrams(ws, n):
    return [" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def per10k(n, total):
    return 1e4 * n / total if total else 0.0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    human = human_texts()
    hall = [t for ts in human.values() for t in ts]
    mach = {w: machine_texts(w) for w in ("claude", "codex")}
    mall = {f"{w}:{k}": t for w, d in mach.items() for k, t in d.items()}

    prompt_words = set(words(" ".join(t.format(**d) for d in BUSINESSES.values() for t in GENRES.values()) + TAIL))

    hw = [words(t) for t in hall]
    mw = {k: words(t) for k, t in mall.items()}
    nh = sum(map(len, hw))
    nm = sum(map(len, mw.values()))

    print("# Spanish tells study, raw output\n")
    print(f"Human reference: {len(hall)} texts, {nh:,} words "
          f"({', '.join(f'{d} {len(v)}' for d, v in human.items())}).")
    print(f"Machine sample: {len(mall)} texts, {nm:,} words "
          f"(claude-sonnet-5-5 {len(mach['claude'])}, codex {len(mach['codex'])}).\n")

    for n, label in ((1, "Words"), (2, "Two-word phrases")):
        hc = collections.Counter(g for ws in hw for g in ngrams(ws, n))
        mc = collections.Counter(g for ws in mw.values() for g in ngrams(ws, n))
        df = collections.defaultdict(collections.Counter)
        biz = collections.defaultdict(set)
        for k, ws in mw.items():
            for g in set(ngrams(ws, n)):
                df[g][k.split(":")[0]] += 1
                biz[g].add(k.split(":")[1].rsplit("-", 1)[0])
        nh_n, nm_n = sum(hc.values()), sum(mc.values())
        rows = []
        for g, m in mc.items():
            # three businesses at least, so one shop's own vocabulary does not count as a tell
            if m < 4 or len(biz[g]) < 3 or set(g.split()) <= prompt_words:
                continue
            ratio = ((m + 0.5) / nm_n) / ((hc[g] + 0.5) / nh_n)
            if ratio >= 5:
                rows.append((ratio, g, m, hc[g], df[g]["claude"], df[g]["codex"], len(biz[g])))
        rows.sort(reverse=True)
        print(f"## {label} over-used by the models (count >= 4, in >= 3 businesses, ratio >= 5)\n")
        print("| phrase | machine count | human count | ratio | texts, claude | texts, codex | businesses |")
        print("|---|---|---|---|---|---|---|")
        for ratio, g, m, h, dc, dx, nb in rows[:70]:
            print(f"| {g} | {m} | {h} | {ratio:.0f} | {dc} | {dx} | {nb} |")
        print()

    hjoin = "\n".join(hall).lower()
    mjoin = "\n".join(mall.values()).lower()
    print("## Published Spanish lists, checked against both corpora (per 10k words)\n")
    print("| source | phrase | machine | human | machine texts |")
    print("|---|---|---|---|---|")
    for src, items in PUBLISHED.items():
        for p in items:
            rx = re.compile(r"\b" + re.escape(p) + r"\w*")
            m, h = len(rx.findall(mjoin)), len(rx.findall(hjoin))
            dfm = sum(1 for t in mall.values() if rx.search(t.lower()))
            print(f"| {src} | {p} | {per10k(m, nm):.1f} | {per10k(h, nh):.1f} | {dfm} |")
    print()

    print("## Spanish hypotheses from the humanizer's English and French patterns (per 10k words)\n")
    print("| phrase | machine | human | ratio | texts, claude | texts, codex |")
    print("|---|---|---|---|---|---|")
    for p in HYPOTHESES:
        rx = re.compile(r"\b" + re.escape(p) + r"\w*")
        m, h = len(rx.findall(mjoin)), len(rx.findall(hjoin))
        dc = sum(1 for t in mach["claude"].values() if rx.search(t.lower()))
        dx = sum(1 for t in mach["codex"].values() if rx.search(t.lower()))
        ratio = ((m + 0.5) / nm) / ((h + 0.5) / nh)
        print(f"| {p} | {per10k(m, nm):.1f} | {per10k(h, nh):.1f} | {ratio:.0f} | {dc} | {dx} |")
    print()

    print("## Structural counts (per 10k words)\n")
    cols = [("claude", list(mach["claude"].values())), ("codex", list(mach["codex"].values()))] + \
           [(f"human {d}", v) for d, v in human.items()]
    print("| pattern | " + " | ".join(c for c, _ in cols) + " |")
    print("|---|" + "---|" * len(cols))
    sizes = {c: sum(len(words(t)) for t in ts) for c, ts in cols}
    for name, rx in STRUCT.items():
        r = re.compile(rx)
        print(f"| {name} | " + " | ".join(f"{per10k(sum(len(r.findall(t)) for t in ts), sizes[c]):.1f}"
                                          for c, ts in cols) + " |")
    print()

    print("## Per text, machine only\n")
    print("| check | claude | codex |")
    print("|---|---|---|")
    proper = set(re.findall(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", " ".join(
        t.format(**d) for d in BUSINESSES.values() for t in GENRES.values())))
    checks = {
        "a single raya in a sentence (English-style pivot)":
            lambda t: any(s.count("—") == 1 for s in re.split(r"(?<=[.!?])\s+|\n", t)),
        "ends on a question": lambda t: t.rstrip().rstrip("🙂😊☕📚🚲").rstrip().endswith("?"),
        # a heading-like line (short, one sentence, no hashtag) with two capitalised
        # words after the first that are not proper nouns from the prompts
        "a line in Title Case": lambda t: any(
            "#" not in l and len(l.split()) <= 10 and not re.search(r"[.!?]\s", l) and
            sum(w[0].isupper() and w not in proper for w in
                re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{4,}", l)[1:]) >= 2 for l in t.splitlines()),
        "markdown bold **": lambda t: "**" in t,
        "hashtags": lambda t: bool(re.search(r"#\w", t)),
        "emoji": lambda t: bool(re.search(STRUCT["emoji"], t)),
    }
    for name, fn in checks.items():
        print(f"| {name} | " + " | ".join(f"{sum(map(fn, mach[w].values()))} of {len(mach[w])}"
                                          for w in ("claude", "codex")) + " |")
    print(f"\nMean length in words: claude {sum(len(words(t)) for t in mach['claude'].values()) / max(1, len(mach['claude'])):.0f}, "
          f"codex {sum(len(words(t)) for t in mach['codex'].values()) / max(1, len(mach['codex'])):.0f}.")


if __name__ == "__main__":
    main()
