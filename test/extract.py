"""Cut the two voice files out of the interviewer's last message, unedited.

    python test/extract.py claude-en claude-fr claude-es

The short file starts at the first line beginning with the brand's name, the
full file at its header; each ends at the first marker the interviewer put
after it (a line of = or -, a code fence, FIN, or its own length line). Writes
test/interview/<run>-short.txt and -full.txt.
"""
import json, pathlib, re, sys

OUT = pathlib.Path(__file__).parent / "interview"
HEADER = re.compile(r"^(VOICE FILE FOR|FICHIER DE VOIX DE|ARCHIVO DE VOZ DE) (?!\[)", re.I)
# The 27.10 French and Spanish runs closed each file with a code fence or "----- fin -----".
END = re.compile(r"^(=+$|```|-{3,}|FIN\b|Length|Longueur|Extensión)")
BRAND = "Levain"  # test/brand.py sets its own


def block(lines, start):
    end = next((i for i in range(start + 1, len(lines)) if END.match(lines[i]) or HEADER.match(lines[i])), len(lines))
    return "\n".join(lines[start:end]).strip() + "\n"


def extract(run):
    # The first interviewer message holding the file: codex-en ran on past it, unnoticed.
    turns = json.loads((OUT / f"{run}.json").read_text(encoding="utf-8"))
    lines = next(t for t in turns[1::2] if any(HEADER.match(l) for l in t.splitlines())).splitlines()
    short = next(i for i, l in enumerate(lines) if l.startswith(BRAND))
    full = next(i for i, l in enumerate(lines) if HEADER.match(l))
    assert short < full, f"{run}: short file not before the full one"
    for kind, start in (("short", short), ("full", full)):
        (OUT / f"{run}-{kind}.txt").write_text(block(lines, start), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    for run in sys.argv[1:]:
        extract(run)
        print(run, "extracted")
