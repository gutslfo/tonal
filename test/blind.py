"""Shuffle the five English pairs into A and B for a blind pick.

    python test/blind.py

Writes test/blind/pairs.md (the request and both texts, as written) and
test/blind/key.json (which letter had the voice file). Refuses to run twice:
a second shuffle would void picks already made against the first.
"""
import json, pathlib, random, sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "blind"
sys.path.insert(0, str(HERE))
from tasks import TASKS, NAMES

if (OUT / "key.json").exists():
    sys.exit("test/blind/key.json exists: the pairs are already shuffled.")
rng, key, parts = random.SystemRandom(), {}, []
en = TASKS["en"]
for task in NAMES:
    order = ["with", "without"]
    rng.shuffle(order)
    key[task] = dict(zip("AB", order))
    texts = [(HERE / "tasks" / "en" / f"{task}-{c}.txt").read_text(encoding="utf-8").strip() for c in order]
    parts.append(f"## {task}\n\nThe request: {en['intro']}{en[task]}{en['tail']}\n\n"
                 f"A\n\n```text\n{texts[0]}\n```\n\nB\n\n```text\n{texts[1]}\n```\n")
OUT.mkdir(exist_ok=True)
(OUT / "pairs.md").write_text(
    "# Blind pairs, English\n\n"
    "Five requests for Levain, a fictional bakery. Each was sent twice to the same model, once with the voice file "
    "and once without. A and B are in random order. For each pair, write in picks.md the one that sounds like Levain, "
    "and why in a line if you like. Levain's own texts, the ones the interview started from, are in "
    "test/levain/en.md. Do not open key.json, test/RESULTS.md, the page or the PDF until all five picks are written: they all show which is which.\n\n"
    + "\n".join(parts), encoding="utf-8", newline="\n")
(OUT / "picks.md").write_text(
    "# Picks\n\nWritten before key.json was opened.\n\n" + "".join(f"{t}: \n" for t in NAMES),
    encoding="utf-8", newline="\n")
(OUT / "key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8", newline="\n")
print("5 pairs shuffled")
