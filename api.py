"""One Claude call, logged to ledger.jsonl, refused once the spend passes the cap.

The brief capped the test budget at $4 (approved estimate under $2); Pierre raised
it for the Grave Water reruns and the French and Spanish rerun. The cap is a guard, not a warning: a call that
would start above it raises before it is sent.
"""
import json
import pathlib
import threading
import time

import anthropic

ROOT = pathlib.Path(__file__).parent
LEDGER = ROOT / "ledger.jsonl"
CAP_USD = 8.25  # raised from 4.00 to 5.00 and 5.50 by Pierre on 26.10, to 5.75 on 27.10 for the Grave Water reruns, to 8.25 on 27.10 for the French and Spanish rerun
# $ per million tokens (input, output), claude-api skill table cached 2026-10-06.
PRICES = {"claude-sonnet-5-5": (2.00, 10.00), "claude-haiku-5-5": (0.10, 0.50)}

_client = anthropic.Anthropic()
_lock = threading.Lock()


def spent():
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l)["usd"] for l in LEDGER.read_text(encoding="utf-8").splitlines() if l)


def call(model, messages, system=None, max_tokens=8000, effort="medium", tag=""):
    if spent() >= CAP_USD:
        raise SystemExit(f"budget cap reached: ${spent():.2f} of ${CAP_USD:.2f}, nothing sent")
    kw = {"system": system} if system else {}
    # Streamed: the SDK refuses a plain request whose max_tokens could run past ten minutes.
    with _client.messages.stream(model=model, max_tokens=max_tokens, messages=messages,
                                 output_config={"effort": effort}, **kw) as s:
        r = s.get_final_message()
    pin, pout = PRICES[model]
    u = r.usage
    usd = (u.input_tokens * pin + u.output_tokens * pout) / 1e6
    # Logged before the stop check: a call cut at max_tokens is still paid for.
    with _lock, LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "tag": tag, "model": model,
                            "in": u.input_tokens, "out": u.output_tokens, "usd": round(usd, 5),
                            "stop": r.stop_reason}) + "\n")
    if r.stop_reason not in ("end_turn", "stop_sequence"):
        raise RuntimeError(f"{tag}: stop_reason {r.stop_reason}")
    return "".join(b.text for b in r.content if b.type == "text").strip()


if __name__ == "__main__":
    print(f"spent ${spent():.4f} of ${CAP_USD:.2f}")
