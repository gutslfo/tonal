"""Measure voice files against their limits. Exits 1 if any file is over.

    python check.py                      # the kit itself, every language
    python check.py short my-short.txt   # a short voice file you wrote
    python check.py full my-full.txt     # a full voice file you wrote

Characters are counted the way a browser text field counts them (UTF-16
units), so an emoji counts as two. That is the stricter count.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "kit"))
from build import LANGS, assemble

LIMITS = {"short": 1500, "full": 8000}


def size(text):
    return len(text.encode("utf-16-le")) // 2


def measure(kind, path):
    text = pathlib.Path(path).read_text(encoding="utf-8").strip()
    n, limit = size(text), LIMITS[kind]
    ok = n <= limit
    print(f"{'ok  ' if ok else 'OVER'} {kind:5} {n:5} / {limit} characters, {len(text.split()):4} words  {path}")
    return ok


def check_kit():
    ok = True
    for lang in LANGS:
        d = ROOT / "kit" / lang
        ok &= measure("short", d / "voice-short.txt")
        ok &= measure("full", d / "voice-full.txt")
        prompt = d / "interview.txt"
        current = prompt.exists() and prompt.read_text(encoding="utf-8") == assemble(lang)
        print(f"{'ok  ' if current else 'OLD '} the interview carries both templates verbatim  {prompt}")
        ok &= current
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        ok = check_kit()
    elif len(args) == 2 and args[0] in LIMITS:
        ok = measure(*args)
    else:
        sys.exit(__doc__)
    sys.exit(0 if ok else 1)
