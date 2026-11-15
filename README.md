# CosmoRelic

**Abandoned, but not forgotten.**

Eight machines were left behind on the Moon and Mars. CosmoRelic lets a student
open one, hear it tell its own story in the first person, and see a live data
card where **every number is labelled by how we know it** - measured, computed
from a live ephemeris, derived from one of those, or read from the mission
archive. When the relic does not know something, it says so.

Built for **NASA Space Apps Challenge 2026, Challenge 01: "Abandoned but not
Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars."**

---

## The honesty problem this project takes seriously

The challenge statement says *"Accuracy is important throughout!"* Most
storytelling tools blur the line between what a mission actually measured and
what a narrator invented. CosmoRelic makes that line visible:

| Badge | Meaning |
|---|---|
| **MEASURED** | Recorded by an instrument or a published survey (e.g. landing coordinates). |
| **EPHEMERIS** | A live position or distance computed by JPL Horizons right now. |
| **DERIVED** | Arithmetic performed on a measured or ephemeris value (e.g. light travel time). |
| **ARCHIVAL** | A fact from the mission record - not a live measurement. |

The AI never sees a number that is not in the data card, and it is instructed to
correct myths about its own mission rather than repeat them.

### Myths the relics correct about themselves

- **Opportunity** - *"My battery is low and it's getting dark"* is a journalist's
  paraphrase of the final telemetry, **not** the rover's literal words.
- **InSight** - its heat probe (the "mole") never reached the 3-5 m target;
  it stopped at roughly **40 cm**, about its own length.
- **Viking 1** - ended because of a **faulty software command**, not a dust storm.
- **Ingenuity** - not destroyed. A rotor blade was damaged during its final
  landing, so it can no longer fly; NASA reports it stayed upright and in contact.
- **Eagle** - the fate of its ascent stage is genuinely **unknown**; the app
  refuses to state a guess as fact.

---

## Quick start

```bash
# 1. Create and activate a virtual environment (Python 3.11+)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Optional: add a free Groq API key for live chat
cp .env.example .env
# then paste your key after GROQ_API_KEY=   (https://console.groq.com/keys)

# 4. Run
python app.py                    # opens the web UI
python tests/test_core.py        # runs the acceptance tests
jupyter lab                      # then open notebook/cosmorelic_dev.ipynb
```

**No key? No internet?** Both are supported. Without a key the app still runs
and every answer comes from the archived memory. Without a network the data card
shows an honest archival range instead of a fabricated live number. This is a
feature, not a degraded mode - see *Low-power mode* below.

---

## Architecture

```
cosmorelic_data.py   static data: 8 relics, coordinates, facts, credits, TEACHER_BOX
core.py              ALL logic: telemetry, tiers, prompts, myth-safe answers
app.py               Gradio UI (imports core; contains no logic)
notebook/            development notebook (imports core; re-implements nothing)
tests/test_core.py   the acceptance suite
tools/               build-time only: build_deck.py, build_notebook.py, shot.py
docs/                PRD.md, SRS.md, PDW.md - the full specification set
```

**One source of logic.** `app.py` and the notebook only import from `core.py`.
This keeps the UI, the notebook and the tests provably in agreement.

### Low-power mode

When the network is unavailable or the API rate limit is hit, the relic
answers from its archived memory. This is designed as a metaphor for the real
fate of Opportunity - a machine that kept talking until it could not - rather
than presented as an error state. It also makes the app usable in classrooms
with weak or no connectivity.

---

## For Teachers

A five-minute classroom activity and three discussion questions are built into
the app under the **For Teachers** accordion. The core exercise: read a relic's
story, then ask *"which numbers on this card were measured, and which were
derived from a measurement?"* and *"why did the AI say it did not know?"*

---

## Data and credits

Full source list: **[DATA_SOURCES.md](DATA_SOURCES.md)**.

- Live distances come from the **JPL Horizons System** (no key required).
- Mission records and coordinates come from **NSSDCA** and **NASA GISS**.
- All photographs are **NASA archival imagery** and are credited individually in
  the UI and in `DATA_SOURCES.md`. No NASA logo, flag or mission patch is used.
- All eight relics are drawn from the **14 resources named in challenge 01**:
  Apollo Lunar Modules and Lunar Roving Vehicles (Eagle, Challenger),
  Viking 1, Sojourner, Spirit and Opportunity, Phoenix and InSight, and the
  Ingenuity Helicopter.

---

## AI disclosure (Super Intelligence)

In the spirit of the Space Apps SI disclosure requirement, and because this
project is *about* AI honesty:

- **Code.** Written with agentic AI assistance (an AI coding agent plus an
  LLM). Every Python file states this in its first line,
  and this section is the descriptive acknowledgement.
- **Runtime model.** Persona chat uses an open-weight LLM served by Groq
  (default `llama-3.1-8b-instant`, OpenAI-compatible endpoint), with an
  automatic fallback chain to `openai/gpt-oss-120b` and `allam-2-7b` if the
  primary model is unavailable to the key. Responses are labelled
  **"AI-generated"** in the UI. The model receives only the numbers from the
  data card and is forbidden from inventing others.
- **Images.** **No AI-generated images are used anywhere.** Every photograph is
  credited NASA archival imagery. There is therefore no SI watermark to apply to
  any image, and none is claimed.
- **Text.** Story hooks, persona descriptions and myth corrections were drafted
  with AI assistance and then checked line by line against the NASA sources in
  `DATA_SOURCES.md`.

---

## Limitations (stated honestly)

- CosmoRelic covers **8 relics** spanning 7 of the 14 resource families named in
  challenge 01. Surveyor, ALSEP, Phoenix, Dawn, NEAR Shoemaker, Pioneer 10/11
  and Kepler are not yet included.
- The relic is an **AI storyteller, not the real spacecraft**. It says so if
  asked.
- Live distance is a *center-to-center* figure between Earth and the body, not
  the distance to the specific relic on the surface.
- No image, video or audio likeness of any person appears in this project.

---

## Deploy CosmoRelic to Hugging Face Spaces

CosmoRelic runs on any Python environment with `gradio` and the `openai` SDK (used as a client for Groq's OpenAI-compatible endpoint). To deploy:

1. **Push this repo to GitHub** (or upload it directly to a Space repo).
2. **Create a new Hugging Face Space** — select **Gradio SDK** and connect the repo.
3. Go to **Settings → Variables and secrets** and add a secret `GROQ_API_KEY` with your free key from [console.groq.com/keys](https://console.groq.com/keys). The key is **never** stored in the repo — `.env` is gitignored.
4. Ensure `requirements.txt` lists `gradio`, `openai`, `requests`, `python-dotenv`.

The app exposes a Gradio Chat Interface and starts listening on port 7860 by default, which HF Spaces expects. No model downloads — inference runs on Groq's cloud API; if the free-tier rate limit is hit or the key is missing the conversation falls back gracefully to locally stored archival data (zero latency).

---

## License

Apache-2.0 (see `LICENSE`). NASA data and imagery are used under the
[NASA Media Usage Guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/).
See `NOTICE` for the non-endorsement statement.

*Not affiliated with or endorsed by NASA.*
