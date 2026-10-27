"""Assemble each language's interview prompt from its head and the two templates.

    python kit/build.py

The prompt carries the templates verbatim, so editing a template means running
this again; check.py fails if a prompt is out of date.
"""
import pathlib

KIT = pathlib.Path(__file__).parent
LANGS = {
    "en": ("THE FULL TEMPLATE", "Start now: ask me for my texts."),
    "fr": ("LE MODÈLE COMPLET", "Commence maintenant : demande-moi mes textes."),
    "es": ("LA PLANTILLA COMPLETA", "Empieza ahora: pídeme mis textos."),
}


def assemble(lang):
    full_label, start = LANGS[lang]
    d = KIT / lang
    read = lambda n: (d / n).read_text(encoding="utf-8")
    return read("interview-head.txt") + read("voice-short.txt") + f"\n{full_label}\n\n" + read("voice-full.txt") + f"\n{start}\n"


if __name__ == "__main__":
    for lang in LANGS:
        if (KIT / lang / "interview-head.txt").exists():
            (KIT / lang / "interview.txt").write_text(assemble(lang), encoding="utf-8", newline="\n")
            print(lang, len(assemble(lang)), "characters")
