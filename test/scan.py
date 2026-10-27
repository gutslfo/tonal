"""Count the AI tells a script can see in the before and after texts.

    python test/scan.py > test/scan.md

Per language, summed over the five tasks, without the voice file against with
it. A script sees words, punctuation and shapes, not meaning: "rich" counts
even when it is literal, and a text can be generic with zero hits. The brand's
own list is read from the "Ours" line of the Levain voice file.
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).parent
TASKS = ["page", "instagram", "reply", "newsletter", "linkedin"]

WORDS = {
    "en": r"nestled|in the heart of|vibrant|rich|boasts?|stunning|must-visit|delv(?:e|es|ed|ing)|tapestry|landscape|crucial|pivotal"
          r"|enhanc(?:e|es|ed|ing)|foster(?:s|ed|ing)?|showcas(?:e|es|ed|ing)|testament",
    "fr": r"au cœur d[eu]|nich[ée]e?s?|véritables?|incontournables?|authentiques?|chaleureu(?:x|se|ses)|convivia(?:l|le|les|ux)|univers"
          r"|expériences?|alli(?:er|ant|e)|point d'honneur|permettant|offrant|garantissant",
    "es": r"en el corazón de|artesan(?:o|a|os|as|al|ales|ía)|con mimo|con pasión|lament(?:o|amos)|entiendo que|estimad[oa]s?"
          r"|cordial saludo|porque creemos|creemos (?:en|que)|sabemos que|(?:te|os) esperamos|nos vemos",
}
CONNECTORS = {"en": r"Additionally|Moreover|Furthermore", "fr": r"De plus|Par ailleurs|En outre|Enfin|En conclusion",
              "es": r"Además|Asimismo|Por otro lado|En definitiva"}
NOT_X_Y = {
    "en": [r"\b(?:not|isn't|wasn't|aren't)\s+(?:just|only|merely|simply)\b", r"\bnot\b[^.!?\n]{1,60}?,\s*(?:it's|it is)\b"],
    "fr": [r"\bce n['’]est pas\b[^.!?\n]{1,80}?,\s*c['’]est\b", r"\bnon seulement\b", r"\bpas (?:seulement|simplement|juste)\b"],
    "es": [r"\bno (?:es|son|fue|era)\b[^.!?\n]{1,80}?,\s*(?:es|son|fue|era)\b", r"\bNo (?:es|fue|son)\b[^.!?\n]{1,60}\.\s+(?:Es|Fue|Son)\b",
           r"\bno solo\b[^.!?\n]{1,80}?\bsino\b"],
}
STOCK = {
    "en": r"here's|here is|i hope this helps|let me know|feel free|thank you so much|sincerely apologi[sz]e|any inconvenience"
          r"|can't wait|exciting times|big news|exciting news|we're (?:thrilled|excited|delighted)|honestly\?|here's the thing",
    "fr": r"voici|n'hésitez pas|au plaisir|sincèrement désolée?s?|gêne occasionnée|nous sommes ravie?s|bonne nouvelle|grande nouvelle"
          r"|chers clients|à très vite|à bientôt",
    "es": r"aquí tienes|buenas noticias|gran noticia|nos complace|nos alegra|disculpa(?:s|d)? las molestias|las molestias"
          r"|¡hola|será un placer|¡no te lo pierdas",
}
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿]")


def ours(lang):
    full = (HERE / "interview" / f"claude-{lang}-full.txt").read_text(encoding="utf-8")
    line = next(l for l in full.splitlines() if re.match(r"(Ours|Les nôtres|Las nuestras)\s*:", l))
    # The model quotes some lists and ends the Spanish one on "y cualquier adjetivo de elogio": words only.
    # The 27.10 runs add a sentence after the list ("Chez nous, l'heure sert d'invitation."): the list ends at the first full stop.
    words = [re.sub(r"[«»\"“”]", "", w).strip(" .") for w in re.split(r"[.»]\s+(?=[A-ZÀ-Ý«])", line.split(":", 1)[1])[0].split(",")]
    return "|".join(re.escape(w) for w in words if w and not re.match(r"(and|et|y) ", w))


def counts(lang, text):
    ci = re.IGNORECASE
    return {
        "kit word list": len(re.findall(rf"\b(?:{WORDS[lang]})\b", text, ci)),
        "brand's own list": len(re.findall(rf"\b(?:{ours(lang)})\b", text, ci)),
        "connector ladder": len(re.findall(rf"(?:^|[.!?]\s+)(?:{CONNECTORS[lang]})\b", text, re.M)),
        "not X, it's Y": sum(len(re.findall(p, text, ci)) for p in NOT_X_Y[lang]),
        "stock phrases": len(re.findall(rf"(?:{STOCK[lang]})", text, ci)),
        "em or en dash": len(re.findall("[—–]", text)),
        "emoji": len(EMOJI.findall(text)),
        "hashtags": len(re.findall(r"(?<![\w&])#\w+", text)),
        "bold (**)": text.count("**") // 2,
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("# Tells a script can see, before and after\n")
    print("Five Levain tasks per language, one fresh call each, claude-sonnet-5-5. Counts are summed over the five texts; "
          "the figure in brackets is how many of the five texts have at least one. A phrase on two lists counts twice. "
          "Raw output of `test/scan.py`.\n")
    for lang in ("en", "fr", "es"):
        rows = {}
        words = {}
        for cond in ("without", "with"):
            per = [counts(lang, (HERE / "tasks" / lang / f"{t}-{cond}.txt").read_text(encoding="utf-8")) for t in TASKS]
            words[cond] = sum(len((HERE / "tasks" / lang / f"{t}-{cond}.txt").read_text(encoding="utf-8").split()) for t in TASKS)
            for k in per[0]:
                rows.setdefault(k, {})[cond] = (sum(p[k] for p in per), sum(1 for p in per if p[k]))
        print(f"## {lang}\n\n| | without the file | with the file |\n|---|---|---|")
        for k, v in rows.items():
            print(f"| {k} | {v['without'][0]} ({v['without'][1]}) | {v['with'][0]} ({v['with'][1]}) |")
        total = {c: sum(v[c][0] for v in rows.values()) for c in ("without", "with")}
        print(f"| **all tells** | {total['without']} | {total['with']} |")
        print(f"| words in the five texts | {words['without']} | {words['with']} |\n")


if __name__ == "__main__":
    main()
