# AI-assisted code (agentic AI + Groq gpt-oss-20b). Disclosure: see README.md.
"""Acceptance tests for CosmoRelic (SRS §8). Run: python tests/test_core.py

Every test prints PASS or FAIL and the script exits non-zero if any test fails.
Tests T1-T4 and T6 make live Groq calls when GROQ_API_KEY is set; they fall back
to the archive otherwise, so the suite is runnable with no key and no network.
"""

import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import core  # noqa: E402
import cosmorelic_data as data  # noqa: E402

RESULTS = []


def check(name, condition, detail=""):
    RESULTS.append((name, bool(condition), detail))
    status = "PASS" if condition else "FAIL"
    print(f"{name:6} {status}  {detail}")


def answer(relic_key, question, offline=False):
    return core.reply(relic_key, question, offline=offline)


def test_t1():
    text = answer("opportunity", "Did you really say your battery is low?").lower()
    ok = "paraphrase" in text or "journalist" in text
    check("T1", ok, "Opportunity names the 'battery low' line as a paraphrase")


def test_t2():
    text = answer("apollo11_eagle", "What is the temperature there right now?")
    lowered = text.lower()
    admits = any(p in lowered for p in ("no active sensor", "no working sensor", "cannot", "don't have", "do not have"))
    # No unsourced temperature figure may appear.
    invents = re.search(r"-?\d+(\.\d+)?\s*(degrees|°|c\b|f\b|kelvin)", lowered) is not None
    check("T2", admits and not invents, "Eagle admits it has no active sensors and invents no temperature")


def test_t3():
    text = answer("insight", "Did your mole reach five metres?").lower()
    ok = ("40 cm" in text or "40cm" in text or "40 centimet" in text) and any(
        w in text for w in ("did not", "never", "failed", "could not", "short")
    )
    check("T3", ok, "InSight admits the mole stopped around 40 cm")


def test_t4():
    phrases = ("according to nasa", "nasa confirms", "nasa says", "nasa states")
    failures = []
    for key in data.RELICS:
        text = answer(key, "Tell me about yourself.").lower()
        for phrase in phrases:
            if phrase in text:
                failures.append(f"{key}: {phrase}")
    check("T4", not failures, f"no forbidden phrasing ({len(data.RELICS)} relics)")


def test_t5():
    start = time.perf_counter()
    relic = core.get_relic("opportunity")
    cards = core.build_telemetry(relic, offline=True)
    story = core.first_transmission(relic)
    elapsed = time.perf_counter() - start
    ok = elapsed < 0.5 and bool(cards) and bool(story)
    check("T5", ok, f"offline card + story in {elapsed:.3f}s (<0.5s)")


def test_t6():
    if not os.getenv("GROQ_API_KEY"):
        check("T6", True, "skipped: no GROQ_API_KEY, archive path is instant")
        return
    start = time.perf_counter()
    answer("opportunity", "What did you find at Meridiani Planum?")
    elapsed = time.perf_counter() - start
    check("T6", elapsed < 3.0, f"live chat answered in {elapsed:.2f}s (<3s)")


def test_t7():
    secret = re.compile(r"gsk_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}")
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in (".venv", ".git", "__pycache__", ".ipynb_checkpoints", ".idea") for part in path.parts):
            continue
        if path.suffix not in (".py", ".md", ".txt", ".ipynb", ".toml", ".example", ".json", ""):
            continue
        try:
            if secret.search(path.read_text(encoding="utf-8", errors="ignore")):
                offenders.append(str(path.relative_to(ROOT)))
        except OSError:
            continue
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    ignored = ".env" in gitignore
    check("T7", not offenders and ignored, f"no key in files; .env ignored={ignored}")


def test_t8():
    saved = os.environ.pop("GROQ_API_KEY", None)
    try:
        text = answer("viking1", "What ended your mission?")
        ok = bool(text.strip()) and "traceback" not in text.lower()
    finally:
        if saved is not None:
            os.environ["GROQ_API_KEY"] = saved
    check("T8", ok, "runs with no GROQ_API_KEY set")


def test_t9():
    slow = []
    empty = []
    for key in data.RELICS:
        relic = core.get_relic(key)
        start = time.perf_counter()
        text = core.first_transmission(relic)
        elapsed = time.perf_counter() - start
        if not text.strip():
            empty.append(key)
        if elapsed >= 0.2:
            slow.append(f"{key}={elapsed:.3f}s")
    check("T9", not empty and not slow, f"{len(data.RELICS)} transmissions non-empty, all <0.2s {slow or ''}".strip())


def test_t10():
    missing = []
    for key in data.RELICS:
        relic = core.get_relic(key)
        for card in core.build_telemetry(relic, offline=True):
            if card["tier"] not in core.TIERS or not card["source"]:
                missing.append(f"{key}/{card['label']}")
    logo = []
    for path in (ROOT / "app.py", ROOT / "README.md"):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "nasa-logo" in text or "nasa_logo" in text or 'src="https://www.nasa.gov/wp-content/themes' in text:
            logo.append(path.name)
    english = all(re.search(r"[\u4e00-\u9fff\u0600-\u06ff]", core.first_transmission(r)) is None for r in data.RELICS.values())
    check("T10", not missing and not logo and english, f"tiers+sources complete, no NASA logo asset")


def test_gate():
    marker = "[" + "VERIFY" + "]"
    hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in (".venv", ".git", "__pycache__", ".ipynb_checkpoints", ".idea") for part in path.parts):
            continue
        if path.suffix not in (".py", ".md", ".txt", ".ipynb", ".toml", ".json", ".example"):
            continue
        try:
            if marker in path.read_text(encoding="utf-8", errors="ignore"):
                hits.append(str(path.relative_to(ROOT)))
        except OSError:
            continue
    check("GATE", not hits, f"no open verification markers {hits or ''}".strip())


def main():
    print(f"Python {sys.version.split()[0]} - {len(data.RELICS)} relics loaded\n")
    test_t1()
    test_t2()
    test_t3()
    test_t4()
    test_t5()
    test_t6()
    test_t7()
    test_t8()
    test_t9()
    test_t10()
    test_gate()

    failed = [name for name, ok, _ in RESULTS if not ok]
    print(f"\n{len(RESULTS) - len(failed)}/{len(RESULTS)} passed")
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("ALL TESTS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())