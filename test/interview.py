"""Run the kit's interview against a scripted founder and keep everything.

    python test/interview.py claude en fr es
    python test/interview.py codex en

The interviewer gets kit/<lang>/interview.txt as its first message, with no
system prompt, exactly as a founder would paste it. The founder is
claude-haiku-5-5 playing Sam from test/levain/<lang>.md, a fictional bakery.
The run stops when the interviewer writes the full voice file; nobody edits
anything in between. Output: test/interview/<who>-<lang>.md and .json.
"""
import concurrent.futures as cf, json, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import api

INTERVIEWER, FOUNDER = "claude-sonnet-5-5", "claude-haiku-5-5"
HEADER = {"en": "VOICE FILE FOR", "fr": "FICHIER DE VOIX DE", "es": "ARCHIVO DE VOZ DE"}
MAX_TURNS = 30
OUT = HERE / "interview"
# test/brand.py points these at another founder sheet and output folder.
FIXTURE, TAG = HERE / "levain", ""


def as_messages(turns):
    return [{"role": "user" if i % 2 == 0 else "assistant", "content": t} for i, t in enumerate(turns)]


def founder(lang, turns):
    # The founder sees the interviewer as the user: drop the pasted prompt, roles flip.
    sheet = (FIXTURE / f"{lang}.md").read_text(encoding="utf-8")
    return api.call(FOUNDER, as_messages(turns[1:]), system=sheet, max_tokens=4000, effort="low", tag=f"{TAG}founder-{lang}")


def claude(lang, turns, state):
    # The last turn writes both files after thinking them through: 8,000 tokens ran out,
    # then 16,000 on Grave Water's third run.
    return api.call(INTERVIEWER, as_messages(turns), max_tokens=32000, tag=f"{TAG}interview-{lang}")


def codex(lang, turns, state):
    # ChatGPT stand-in. Pierre's global ~/.codex/AGENTS.md loads regardless (operating
    # rules, no style rules); the events log is checked for anything but messages.
    work = state.setdefault("dir", tempfile.mkdtemp(prefix="tonal-codex-"))
    out = pathlib.Path(work) / "last.txt"
    exe = shutil.which("codex")
    if "thread" not in state:
        cmd = [exe, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "-C", work, "--json", "-o", str(out), "-"]
        prompt = "Do not run any command or read any file. Answer this request directly.\n\n" + turns[0]
    else:
        cmd = [exe, "exec", "resume", "--skip-git-repo-check", "--json", "-o", str(out), state["thread"], "-"]
        prompt = turns[-1]
    p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=900, cwd=work)
    state.setdefault("events", []).append(p.stdout)
    for line in p.stdout.splitlines():
        if line.startswith("{"):
            e = json.loads(line)
            if e.get("type") == "thread.started":
                state["thread"] = e["thread_id"]
    if p.returncode or not out.exists():
        raise RuntimeError(f"codex {lang}: exit {p.returncode} {p.stderr[-300:]}")
    text = out.read_text(encoding="utf-8").strip()
    out.unlink()
    return text


def save(who, lang, turns, state):
    OUT.mkdir(exist_ok=True)
    stem = OUT / f"{who}-{lang}"
    stem.with_suffix(".json").write_text(json.dumps(turns, ensure_ascii=False, indent=1), encoding="utf-8")
    roles = ["Founder (pastes the prompt)"] + ["Interviewer", "Founder"] * MAX_TURNS
    md = "\n\n".join(f"## {r}\n\n{t}" for r, t in zip(roles, turns))
    stem.with_suffix(".md").write_text(f"# Interview, {who}, {lang}\n\n{md}\n", encoding="utf-8")
    if state.get("events"):
        (OUT / f"{who}-{lang}.events.jsonl").write_text("".join(state["events"]), encoding="utf-8")


def run(who, lang):
    # A run cut by an API error resumes from its saved transcript: the failed call is
    # sent again unchanged, nothing in the conversation is edited.
    saved = OUT / f"{who}-{lang}.json"
    turns = json.loads(saved.read_text(encoding="utf-8")) if saved.exists() and who == "claude" else \
        [(ROOT / "kit" / lang / "interview.txt").read_text(encoding="utf-8")]
    ask, state = {"claude": claude, "codex": codex}[who], {}
    # Codex wrote the header in sentence case, "Voice file for Levain": any case, at a line start.
    done = re.compile(r"(?im)^" + re.escape(HEADER[lang]) + r" (?!\[)")
    if len(turns) % 2 == 0:  # ends on the interviewer
        if done.search(turns[-1]):
            return f"{who}-{lang}: already finished"
        turns.append(founder(lang, turns))
    for n in range((len(turns) + 1) // 2, MAX_TURNS + 1):
        turns.append(ask(lang, turns, state))
        save(who, lang, turns, state)
        print(f"{who}-{lang}: interviewer turn {n}", flush=True)
        if done.search(turns[-1]):
            return f"{who}-{lang}: voice file after {n} interviewer turns"
        turns.append(founder(lang, turns))
        save(who, lang, turns, state)
    raise RuntimeError(f"{who}-{lang}: no voice file after {MAX_TURNS} turns")


if __name__ == "__main__":
    who, langs = sys.argv[1], sys.argv[2:]
    with cf.ThreadPoolExecutor(len(langs)) as ex:
        for f in cf.as_completed([ex.submit(run, who, lang) for lang in langs]):
            print(f.result())
    print(f"spent ${api.spent():.4f}")
