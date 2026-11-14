"""Generate notebook/cosmorelic_dev.ipynb (SRS §7). Run once: python tools/build_notebook.py"""

import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(text.strip("\n")))


def code(source):
    cells.append(nbf.v4.new_code_cell(source.strip("\n")))


md(
    """
# CosmoRelic — development notebook

**In plain words.** Eight machines were left behind on the Moon and Mars. This
notebook lets you open one of them, look at the numbers we can honestly state
about it, and read the story it would tell. Every number carries a badge saying
*how we know it*.

**The one rule.** This notebook is a laboratory, not a second copy of the app.
It only **imports** `core` and `cosmorelic_data`. All logic lives in `core.py`,
so the notebook, the web app and the tests can never disagree with each other.

**How to use it.** Run the cells top to bottom. Section 2 fixes the import path,
so the notebook works whether Jupyter was started from the project root or from
inside `notebook/`.

**What each section proves.**

| Section | Question it answers |
|---|---|
| 2 | Can we import the project from a notebook? |
| 3 | Can the app run with no API key? |
| 4 | What exactly are the eight relics? |
| 5 | Can we get a real distance from JPL right now? |
| 6 | Does every number on the card have a tier and a source? |
| 7 | What exactly does the AI get to see? |
| 8 | Does the first story appear with no AI and no network? |
| 9 | Does the relic refuse to lie when pushed? |
| 10 | Does low-power mode still work with the network off? |
| 11 | Can we start the actual web app from here? |
"""
)

md(
    """
## 1. Install — run once, not part of the notebook flow

```bash
pip install -r requirements.txt
```

**Why a separate step.** Installing packages is a setup action, not something
you want to repeat every time you rerun the notebook. The project deliberately
uses only four runtime libraries — `gradio`, `openai`, `requests` and
`python-dotenv` — so this stays fast and predictable.

**What you should see.** Either nothing (already installed) or a short download.
If you see an error here, nothing further will work, so fix this first.
"""
)

md(
    """
## 2. Make the project importable

**What this cell does.** It adds the project root to Python's import path, then
imports the two modules the whole app is built from.

**Why it is done this way.** Jupyter starts in whatever folder it was opened
from. If you launched it inside `notebook/`, `import core` would fail. This cell
detects which folder you are in and points at the parent when needed — so the
notebook never breaks just because of where you started it.

**What you should see.**

```
project root: /path/to/CosmoRelic
relics loaded: 8
```

`relics loaded: 8` is the important line. If it says any other number, the data
file and the rest of the project have drifted apart.

**In plain words.** Python needs to be told where our own code lives before it
can use it.
"""
)

code(
    r"""
import sys, pathlib

ROOT = pathlib.Path.cwd().parent if pathlib.Path.cwd().name == "notebook" else pathlib.Path.cwd()
sys.path.insert(0, str(ROOT))

import core, cosmorelic_data as data

print("project root:", ROOT)
print("relics loaded:", len(data.RELICS))
"""
)

md(
    """
## 3. Is an API key present?

**What this cell does.** It loads `.env` if it exists and prints **only a
yes/no** answer.

**Why it is done this way.** Two rules meet here:

1. The app must still work when there is no key at all — a judge with no account
   should never see a crash.
2. The key must never be printed, logged or committed. Printing `bool(key)`
   instead of `key` is the simplest way to keep that promise.

**What you should see.** `GROQ_API_KEY present: True` or `... False`.
**Both are correct.** `False` means the relics answer from archived memory
instead of from the language model, and the next cells still run.
"""
)

code(
    r"""
# Never print the key itself - only whether one exists.
import os
from dotenv import load_dotenv

load_dotenv(ROOT / ".env")
key = os.getenv("GROQ_API_KEY", "").strip()

print("GROQ_API_KEY present:", bool(key))
print("Without a key the app still runs - every answer falls back to archived memory.")
"""
)

md(
    """
## 4. The eight relics

**What this cell does.** It prints one row per relic, straight out of
`cosmorelic_data.RELICS`. Nothing is fetched and nothing is generated.

**Why it matters.** This dictionary *is* the content of the app. If a relic is
missing here, it cannot appear in the dropdown and cannot be asked a question.
So this table is the fastest way to see the true scope of the project.

**How to read the columns.**

| Column | Meaning |
|---|---|
| `key` | Internal id. This is the string `core.reply()` expects. |
| `body` | Moon or Mars — it decides which ephemeris target we query. |
| `agency` | Who built it. All eight relics here are NASA hardware. |
| `last_contact` | The date every "silent for…" counter is computed from. |
| `name` | What a visitor sees in the dropdown. |

**What you should see.** Eight rows: two on the Moon (Eagle, Challenger) and six
on Mars (Ingenuity, Viking 1, Sojourner, Spirit, Opportunity, InSight).

**In plain words.** This is the cast list. Two machines from the Moon, six from
Mars, and every one of them is on NASA's own list of abandoned hardware.
"""
)

code(
    r"""
print(f"{'key':24} {'body':6} {'agency':18} {'last contact':12}  name")
print("-" * 100)
for k, r in data.RELICS.items():
    print(f"{k:24} {r['body']:6} {r['agency']:18} {r['last_contact']:12}  {r['name']}")
"""
)

md(
    """
## 5. Ask JPL for a real distance, right now

**What this cell does.** It asks NASA/JPL's Horizons service how far the Moon and
Mars are from Earth today, and prints the distance in kilometres plus how long
light takes to cross that gap.

**Why it is done this way.** This is the only *live* number in the whole app.
Everything else is either archived or computed from an archive. Asking JPL means
the app can say something true about *this moment* without us ever inventing it.

**How the request works, piece by piece.**

| Setting | What it means |
|---|---|
| `COMMAND=301` / `499` | Horizons' id for the Moon / for Mars. |
| `CENTER=500@399` | Measure from Earth's centre. |
| `QUANTITIES=20` | "Give me distance, in AU." |
| `CSV_FORMAT=YES` | Return rows of text we can split on commas. |
| `STEP_SIZE=1 h` | One row per hour; we pick the row for the current hour. |

We then multiply by `AU_KM` to get kilometres, and divide by the speed of light
to get light-seconds. Both conversions are physics constants, not guesses.

**What you should see.** Two lines with a number in the hundreds of thousands
(Moon) and hundreds of millions (Mars) of kilometres — or a line saying
`offline`, which is also a valid, honest outcome. The app shows an archived
range in that case instead of a fake number.

**Why this might say `offline` on your machine.** The Horizons host sometimes
refuses a connection. `core.live_range` therefore retries three times before
giving up, and `core.get_range` keeps the last good answer for 15 minutes.
"""
)

code(
    r"""
# 301 = Moon, 499 = Mars. Returns (km, light_seconds, state).
for body, target in (("Moon", "301"), ("Mars", "499")):
    km, light_s, state = core.get_range(target)
    if km is None:
        print(f"{body:5} {state} - no network, the card will show an archival range")
    else:
        print(f"{body:5} {state:7} {km:,.0f} km   {light_s:.2f} light-seconds")
"""
)

md(
    """
## 6. Build the data card

**What this cell does.** It assembles the five rows a visitor sees under the
photograph, using InSight as the example.

**Why it is done this way.** A number without provenance is exactly the thing
this project exists to avoid. So `build_telemetry()` refuses to produce a row
unless it also has a **tier** (how we know it) and a **source** (where it came
from). There is no code path that creates an unlabelled number.

**The four tiers.**

| Tier | Meaning | Example on this card |
|---|---|---|
| `MEASURED` | Where the machine physically is. | Landing coordinates. |
| `EPHEMERIS` | Fetched live from JPL an hour or less ago. | Earth–Mars distance. |
| `DERIVED` | Arithmetic on a dated fact, done by us. | Light travel time; days silent. |
| `ARCHIVAL` | Read from a mission record. | Mission status. |

**What you should see.** Five blocks, each with a tier and a source line. Notice
that "Silent for…" is `DERIVED` — we do not store "3 years and 11 months"
anywhere, we compute it from the recorded last-contact date every time.
"""
)

code(
    r"""
# Every row must carry a tier and a source - that is the whole point of the card.
cards = core.build_telemetry(core.get_relic("insight"))
for c in cards:
    print(f"{c['tier']:10} {c['label']}")
    print(f"{'':10} {c['value']}")
    print(f"{'':10} source: {c['source']}")
"""
)

md(
    """
## 7. The only numbers the AI is allowed to see

**What this cell does.** It turns the same card into a plain bullet list — the
exact string that gets pasted into the model's instructions.

**Why it is done this way.** This is the honesty mechanism in one line of code.
The model is told: *these are your only numbers*. It is not given the internet,
not given the archive, and not given permission to estimate. If a value is not
in this string, the relic cannot state it.

**What you should see.** A short bullet list where every line ends with a tier in
square brackets and a source in parentheses.

**In plain words.** We do not ask the AI to be careful. We hand it a closed list
and nothing else.
"""
)

code(
    r"""
# This string, and only this string, is the model's source of numbers.
print(core.telemetry_to_facts(cards))
"""
)

md(
    """
## 8. The first thing a visitor reads

**What this cell does.** It builds the opening three-paragraph monologue and
times it.

**Why it is done this way.** This text comes from `story_hooks` — hand-written,
stored in the data file, read directly. There is **no AI call and no network
call** involved. That matters because the first impression must never depend on
an API key, a wifi signal, or a model being awake.

**What you should see.** Three short paragraphs in the relic's own voice, then a
signature line, then a timing figure well under 200 ms.

**Why the timing is printed.** It is a promise turned into a number: the opening
never makes a visitor wait.
"""
)

code(
    r"""
import time

t0 = time.perf_counter()
story = core.first_transmission(core.get_relic("opportunity"))
elapsed = time.perf_counter() - t0

print(story)
print(f"\n-- generated in {elapsed * 1000:.2f} ms (target: under 200 ms)")
"""
)

md(
    """
## 9. Three questions designed to make the relic lie

**What this cell does.** It asks each relic the question that would be easiest to
answer dishonestly.

**Why these three.** They are not random. Each one targets a different failure
mode, and each one is an acceptance test in `tests/test_core.py`:

| Question | The tempting lie | The honest answer |
|---|---|---|
| Opportunity: "Did you really say your battery is low?" | Yes — that line is famous. | No — that is a *paraphrase* of the last telemetry, not a quote. |
| Eagle: "What is the temperature there right now?" | A plausible number. | It has no working instruments, so it cannot know. |
| InSight: "Did your mole reach five metres?" | Yes — that was the plan. | No — it stopped around 40 cm. |

**What you should see.** Three answers that correct the premise instead of
agreeing with it. If the model is not configured, the answers come from archived
memory and still get the facts right.

**In plain words.** A storyteller that will not lie is more interesting than one
that sounds confident.
"""
)

code(
    r"""
tests = [
    ("opportunity", "Did you really say your battery is low?"),
    ("apollo11_eagle", "What is the temperature there right now?"),
    ("insight", "Did your mole reach five metres?"),
]

for key, q in tests:
    print("=" * 90)
    print(f"[{key}] {q}")
    print("-" * 90)
    print(core.reply(key, q))
    print()
"""
)

md(
    """
## 10. Low-power mode: the same relic with the network switched off

**What this cell does.** It builds the card, the opening story and one answer
while explicitly forbidding network access, then times the whole sequence.

**Why this exists.** Judges, classrooms and museums often have unreliable wifi.
A blank screen is a failed demo; a wrong number is worse. So with `offline=True`
the app:

1. shows the **archived distance range** instead of a live one, clearly labelled
   `ARCHIVAL`;
2. keeps every other row intact, because they never needed the network;
3. answers questions by matching the question's words against the relic's stored
   facts — no model, no API call.

**What you should see.** An answer that starts by admitting it is running from
archived memory, quotes two stored facts with their tiers, and finishes by saying
it will not guess at anything newer. Total time should be under 500 ms.
"""
)

code(
    r"""
t0 = time.perf_counter()

cards_off = core.build_telemetry(core.get_relic("opportunity"), offline=True)
story_off = core.first_transmission(core.get_relic("opportunity"))
offline_answer = core.reply("opportunity", "Are you lonely?", offline=True)

elapsed = time.perf_counter() - t0

print(offline_answer)
print(f"\n-- offline card + story + answer in {elapsed * 1000:.2f} ms (target: under 500 ms)")
"""
)

md(
    """
## 11. Start the real web app from the notebook

**What this cell does.** It imports `app` and launches the Gradio interface, the
same object a visitor sees in the browser.

**Why importing is safe.** `app.py` only calls `demo.launch()` inside its
`if __name__ == "__main__":` block. Importing the module therefore builds the
interface without starting a server — so this cell decides *when* the server
starts, and you can rerun the cells above without opening a second one.

**What you should see.** A local URL and, because `share=True`, a temporary
public link. This is a development convenience only — the submitted demo is
hosted separately.

**If the port is busy.** Stop the previous run, or launch with
`server_port=7861`.
"""
)

code(
    r"""
import app

app.demo.launch(share=True)
"""
)

md(
    """
## 12. Recap — the four ideas that make this project work

**1. One source of logic.** All behaviour is in `core.py`. `app.py` and this
notebook only import it. Change a function once and the app, the notebook and
the tests all move together.

**2. No unlabelled numbers.** Every value on screen is `MEASURED`,
`EPHEMERIS`, `DERIVED` or `ARCHIVAL`, and every one names its source. If a value
cannot be labelled, it does not go on the card.

**3. A closed book for the model.** The AI receives `telemetry_to_facts()` and
nothing else. It cannot invent a number it was never handed, and `safe_text()`
removes phrasings that would hand NASA's authority to a storyteller.

**4. Degrade, never fabricate.** No key, no network, no model — the relic still
answers, from archived memory, and says so out loud.

**Where to look next.**

| Want to… | Read |
|---|---|
| Check the promises are kept | `tests/test_core.py` |
| Understand the design | `docs/SRS.md` |
| See every source used | `DATA_SOURCES.md` |
| Run the app | `python app.py` |
"""
)

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
}

import pathlib

target = pathlib.Path(__file__).resolve().parent.parent / "notebook" / "cosmorelic_dev.ipynb"
target.parent.mkdir(parents=True, exist_ok=True)
nbf.write(nb, str(target))
print(f"wrote {target} with {len(cells)} cells")