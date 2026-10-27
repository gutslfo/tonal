"""Liquid Death, renamed Grave Water: does the voice file bring a real brand's voice closer?

    python test/brand.py interview [dir]  # the kit's interview; the founder answers only from four real texts
    python test/brand.py write       # six held-out requests, four ways each
    python test/brand.py judge [runs]  # GPT judge through Codex, plus a style distance script; runs 1 2 by default
    python test/brand.py blind       # Pierre's blind sheet

The ways: none (the request alone), line (the founder's own one-sentence
description of the voice), samples (the four real texts pasted as examples),
file (the full voice file the interview wrote), kit (the file plus the four
texts, the way where-to-paste.md sets up a ChatGPT or Claude project). Each is
a fresh claude-sonnet-5-5 call; everything but "none" goes in the system
prompt, where a project's instructions are read. Runs 1 and 2 judged the first
four; kit came after. file-2 and kit-2 use the file from interview-2, written
by the kit whose shape rules yield to the founder's texts; kit-3 adds a facts
rule that asks only for what the text cannot do without (interview-3). Sources and cuts: test/liquid-death/SOURCES.md.
"""
import collections, concurrent.futures as cf, json, math, pathlib, random, re, shutil, string, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
DIR = HERE / "liquid-death"
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import api, extract, interview

BRAND = "Grave Water"
CONDS = ["none", "line", "samples", "file", "kit", "file-2", "kit-2", "kit-3"]
# A new judge key draws from this pool; runs 1 to 6 drew from earlier ones, kept in their keys.
JUDGED = ["samples", "file", "kit", "kit-2", "kit-3"]
WORDS = {4: "four", 5: "five", 6: "six"}
DATA = json.loads((DIR / "heldout.json").read_text(encoding="utf-8"))
SHEET = (DIR / "en.md").read_text(encoding="utf-8")
SAMPLES = SHEET[SHEET.index("TEXT 1,"):].strip()
rng = random.SystemRandom()


def read(p):
    return p.read_text(encoding="utf-8").strip()


def write_text(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def do_interview(args=("interview",)):
    # interview-2 is the kit whose shape rules yield to the founder's texts (26.10).
    out = args[0]
    interview.FIXTURE, interview.OUT = DIR, DIR / out
    interview.TAG = "ld-" if out == "interview" else f"ld-{out}-"
    print(interview.run("claude", "en"))
    extract.OUT, extract.BRAND = DIR / out, BRAND
    extract.extract("claude-en")
    print(f"spent ${api.spent():.4f}")


def oneline():
    # The founder's own words, asked the way a founder would brief a chatbot in one go.
    out = DIR / "oneline.txt"
    if not out.exists():
        q = f"In one sentence, how would you describe {BRAND}'s voice to ChatGPT, so that it writes like your team?"
        write_text(out, api.call(interview.FOUNDER, [{"role": "user", "content": q}], system=SHEET,
                                 max_tokens=300, effort="low", tag="ld-founder-oneline"))
    return read(out)


def systems():
    return {"none": None, "line": oneline(),
            "samples": "Texts our team wrote. Write in the same voice.\n\n" + SAMPLES,
            "file": read(DIR / "interview" / "claude-en-full.txt"),
            "kit": read(DIR / "interview" / "claude-en-full.txt") + "\n\nPROJECT FILE: our-texts.txt\n\n" + SAMPLES,
            "file-2": read(DIR / "interview-2" / "claude-en-full.txt"),
            "kit-2": read(DIR / "interview-2" / "claude-en-full.txt") + "\n\nPROJECT FILE: our-texts.txt\n\n" + SAMPLES,
            "kit-3": read(DIR / "interview-3" / "claude-en-full.txt") + "\n\nPROJECT FILE: our-texts.txt\n\n" + SAMPLES}


def do_write():
    missing = sum(not (DIR / "tasks" / f"{i['id']}-{c}.txt").exists() for i in DATA["items"] for c in CONDS)
    if api.spent() + 0.02 * missing > api.CAP_USD:  # ponytail: $0.02 a call, the most any task call cost so far
        sys.exit(f"spent ${api.spent():.2f}: {missing} calls could cross the ${api.CAP_USD:.0f} cap, nothing sent")
    sysp = systems()

    def one(item, cond):
        out = DIR / "tasks" / f"{item['id']}-{cond}.txt"
        if not out.exists():
            ask = DATA["intro"] + item["request"] + DATA["tail"]
            write_text(out, api.call("claude-sonnet-5-5", [{"role": "user", "content": ask}], system=sysp[cond],
                                     max_tokens=8000, tag=f"ld-task-{item['id']}-{cond}"))

    with cf.ThreadPoolExecutor(6) as ex:
        for f in cf.as_completed([ex.submit(one, i, c) for i in DATA["items"] for c in CONDS]):
            f.result()
    # The writing model must not know which brand this is: any mention of the real name voids that.
    leaks = [p.name for p in (DIR / "tasks").glob("*.txt") if re.search(r"liquid\s*death", read(p), re.I)]
    print(f"{len(DATA['items']) * len(CONDS)} texts, real name in {leaks or 'none'}, spent ${api.spent():.4f}")


def texts(item):
    t = {c: read(DIR / "tasks" / f"{item['id']}-{c}.txt") for c in CONDS}
    t["real"] = item["real"]
    return t


def codex(prompt):
    # Same call as interview.codex: read-only sandbox, nothing run, answer only.
    work = tempfile.mkdtemp(prefix="tonal-judge-")
    out = pathlib.Path(work) / "last.txt"
    cmd = [shutil.which("codex"), "exec", "--skip-git-repo-check", "--sandbox", "read-only", "-C", work, "-o", str(out), "-"]
    p = subprocess.run(cmd, input="Do not run any command or read any file. Answer this request directly.\n\n" + prompt,
                       capture_output=True, text=True, encoding="utf-8", timeout=900, cwd=work)
    if p.returncode or not out.exists():
        raise RuntimeError(f"codex: exit {p.returncode} {p.stderr[-300:]}")
    return out.read_text(encoding="utf-8").strip()


CLOSE = ("You are judging brand copy. For each of six products below you get the brand's real product description "
         "(REFERENCE) and {count} other descriptions of the same product, {labels}, written by different processes. Rank them "
         "from closest to farthest from the REFERENCE in voice: the kind of joke, what the text chooses to say and to leave "
         "out, sentence shapes, length, register and punctuation. Do not reward matching facts or copied words for their "
         "own sake. Answer with JSON only, no prose, one list per product id, closest first, like {example}.\n\n")
SPOT = ("Below are texts written by a brand's own team (BRAND TEXTS). Then, for six products, {count} descriptions each, "
        "{labels}. For each product, one was written by the brand's team and {ai} were written by AI from a short list of "
        "facts. Rank the {count} from most to least likely to be the team's own text. Answer with JSON only, no prose, one "
        "list per product id, most likely first, like {example}.\n\nBRAND TEXTS\n\n" + SAMPLES + "\n\n")


def judge_prompts(run):
    # One shuffle per item and run, kept in key.json so a re-run judges the same order.
    keyf = DIR / "judge" / f"key-{run}.json"
    if keyf.exists():
        key = json.loads(read(keyf))
    else:
        key = {"close": {}, "spot": {}}
        for item in DATA["items"]:
            for kind, pool in (("close", JUDGED), ("spot", JUDGED + ["real"])):
                order = pool[:]
                rng.shuffle(order)
                key[kind][item["id"]] = dict(zip(string.ascii_uppercase, order))
        write_text(keyf, json.dumps(key, indent=1))
    prompts = {}
    for kind, head in (("close", CLOSE), ("spot", SPOT)):
        ls = list(key[kind][DATA["items"][0]["id"]])  # the key's own labels: runs 1 and 2 had four conditions
        labels, example = ", ".join(ls[:-1]) + " and " + ls[-1], json.dumps({"mug": ls})
        body = head.format(labels=labels, example=example, count=WORDS[len(ls)], ai=WORDS.get(len(ls) - 1))
        for item in DATA["items"]:
            t = texts(item)
            body += f"=== {item['id']}\n\n"
            if kind == "close":
                body += f"REFERENCE\n{t['real']}\n\n"
            body += "".join(f"{l}\n{t[c]}\n\n" for l, c in key[kind][item["id"]].items())
        prompts[kind] = body
    return key, prompts


def parse(answer):
    return json.loads(re.search(r"\{.*\}", answer, re.S).group(0))


def stylometry(item):
    # Character trigrams and length against the real text: crude, but nobody's judgement.
    def grams(s):
        s = re.sub(r"\s+", " ", s.lower())
        return collections.Counter(s[i:i + 3] for i in range(len(s) - 2))

    def cos(a, b):
        return sum(a[k] * b[k] for k in a) / math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))

    def words(s):
        return len(re.findall(r"[\w'’$]+", s))

    t = texts(item)
    g = grams(t["real"])
    return {c: (cos(grams(t[c]), g), words(t[c]) / words(t["real"])) for c in CONDS}


def do_judge(runs=("1", "2")):
    # Each judge prompt runs twice, shuffled afresh: one order alone carries position bias.
    jdir = DIR / "judge"
    scores = {"close": collections.defaultdict(list), "spot": collections.defaultdict(list)}
    for run in runs:
        key, prompts = judge_prompts(run)
        for kind in ("close", "spot"):
            raw = jdir / f"{kind}-{run}.txt"
            if not raw.exists():
                write_text(jdir / f"{kind}-{run}-prompt.txt", prompts[kind])
                write_text(raw, codex(prompts[kind]))
            ranks = parse(read(raw))
            for item in DATA["items"]:
                order = ranks[item["id"]]
                assert sorted(order) == sorted(key[kind][item["id"]]), f"{kind}-{run} {item['id']}: {order}"
                for pos, label in enumerate(order, 1):
                    scores[kind][key[kind][item["id"]][label]].append(pos)
    style = [stylometry(i) for i in DATA["items"]]
    n = len(DATA["items"]) * len(runs)
    lines = [f"| | close: mean rank of {len(scores['close'])} | close: ranked first | spot: mean rank of "
             f"{len(scores['spot'])} | spot: taken for the real one | trigram cosine to real | words vs real |",
             "|---|---|---|---|---|---|---|"]
    for c in [c for c in CONDS + ["real"] if c in scores["spot"]]:
        cl = scores["close"].get(c)
        sp = scores["spot"][c]
        st = [s[c] for s in style] if c != "real" else None
        lines.append(f"| {c} | {sum(cl) / n:.2f} | {cl.count(1)} of {n} | " if cl else f"| {c} | | | ")
        lines[-1] += f"{sum(sp) / n:.2f} | {sp.count(1)} of {n} | "
        lines[-1] += (f"{sum(x for x, _ in st) / len(st):.3f} | {sorted(r for _, r in st)[len(st) // 2]:.1f}x |"
                      if st else "1.000 | 1.0x |")
    table = "\n".join(lines)
    name = "scores.md" if list(runs) == ["1", "2"] else f"scores-{'-'.join(runs)}.md"
    write_text(jdir / name, f"# Judge and style scores, {len(runs)} runs of six items\n\n{table}\n\n"
               "Per item: " + json.dumps({k: dict(v) for k, v in scores.items()}))
    print(table)


def do_blind():
    out = DIR / "blind"
    if (out / "key.json").exists():
        sys.exit("test/liquid-death/blind/key.json exists: the texts are already shuffled.")
    key, parts = {}, []
    for item in DATA["items"]:
        t = texts(item)
        order = CONDS + ["real"]
        rng.shuffle(order)
        key[item["id"]] = dict(zip(string.ascii_uppercase, order))
        parts.append(f"## {item['id']}\n\nThe request: {DATA['intro']}{item['request']}{DATA['tail']}\n\n"
                     + "".join(f"{l}\n\n```text\n{t[c]}\n```\n\n" for l, c in key[item["id"]].items()))
    write_text(out / "texts.md",
               "# Blind picks, Grave Water\n\nGrave Water is Liquid Death under another name. Its own texts, the ones the "
               f"interview started from, are in test/liquid-death/en.md. For each product, one of the {WORDS[len(order)]} "
               f"texts is the brand's own and {WORDS[len(order) - 1]} were written by AI. In picks.md, write the letter you think the brand wrote, and the "
               "letter you would publish if it were your brand. Open key.json, scores.md and RESULTS.md only after all six "
               "lines are written.\n\n" + "".join(parts))
    write_text(out / "picks.md", "# Picks\n\nBrand's own, then the one I would publish.\n\n"
               + "".join(f"{i['id']}: \n" for i in DATA["items"]))
    write_text(out / "key.json", json.dumps(key, indent=1))
    print(f"{len(key)} items shuffled")


if __name__ == "__main__":
    step, args = sys.argv[1], sys.argv[2:]
    {"interview": do_interview, "write": do_write, "judge": do_judge, "blind": do_blind}[step](*([args] if args else []))
