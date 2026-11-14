# AI-assisted code (agentic AI + Groq gpt-oss-20b). Disclosure: see README.md.
"""All CosmoRelic logic lives here (SRS §0). app.py and the notebook only import.

Nothing in this module may invent a number. Every value shown to a user is
either fetched from JPL Horizons, computed from what was fetched, or read from
the static archive in cosmorelic_data.py - and every one of them carries a tier
badge naming which of those three it is.
"""

import datetime as dt
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

import cosmorelic_data as data

for _p in (Path.cwd() / ".env", Path.cwd().parent / ".env"):
    load_dotenv(_p, override=False)

AU_KM = 149_597_870.7
LIGHT_KM_S = 299_792.458
HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
MODEL = "openai/gpt-oss-20b"

CACHE_TTL_S = 15 * 60
CACHE = {}

MEASURED = "MEASURED"
EPHEMERIS = "EPHEMERIS"
DERIVED = "DERIVED"
ARCHIVAL = "ARCHIVAL"
TIERS = (MEASURED, EPHEMERIS, DERIVED, ARCHIVAL)

# Static archival ranges (NSSDCA fact sheets). Used only when the network is
# unavailable, so the user sees an honest range instead of a fabricated number.
ARCHIVAL_RANGE = {
    "Moon": "about 356,000 to 407,000 km (typical range, not live)",
    "Mars": "about 55 to 401 million km (typical range, not live)",
}


def get_relic(key):
    """Return the relic dict, raising a clear error for a bad key."""
    if key not in data.RELICS:
        raise KeyError(f"unknown relic {key!r}; choose from {sorted(data.RELICS)}")
    return data.RELICS[key]


def relic_choices():
    """Ordered (label, key) pairs for the UI dropdown."""
    return [(r["name"], k) for k, r in data.RELICS.items()]


def live_range(target: str, attempts: int = 3, timeout: int = 3):
    """'301' = Moon, '499' = Mars. Return (km, light_seconds). Verified against the live API.

    The Horizons host intermittently refuses the connection (measured: about 3 in 8
    attempts time out, while a successful query takes under a second). We retry a
    bounded number of times so a single dropped connection does not silently drop
    the user to the archival fallback. A 3-second timeout is generous because a
    successful query never takes longer than about 1.1 seconds.
    """
    now = dt.datetime.now(dt.timezone.utc)
    day = now.strftime("%Y-%m-%d")
    p = {
        "format": "json",
        "COMMAND": f"'{target}'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'",
        "START_TIME": f"'{day} 00:00'",
        "STOP_TIME": f"'{day} 23:00'",
        "STEP_SIZE": "'1 h'",
        "QUANTITIES": "'20'",
        "CSV_FORMAT": "'YES'",
    }
    last_error = None
    for attempt in range(attempts):
        try:
            r = requests.get(HORIZONS_URL, params=p, timeout=timeout)
            r.raise_for_status()
            block = r.json()["result"].split("$$SOE")[1].split("$$EOE")[0].strip()
            lines = block.splitlines()
            delta_au = float(lines[now.hour].split(",")[3])
            km = delta_au * AU_KM
            return km, km / LIGHT_KM_S
        except Exception as exc:  # noqa: BLE001 - any failure falls through to the archive
            last_error = exc
    raise last_error


def get_range(target: str):
    """Cached live range. Never raises: returns (None, None, 'offline') with no data."""
    entry = CACHE.get(target)
    now = time.time()
    if entry and now - entry["ts"] < CACHE_TTL_S:
        return entry["km"], entry["light_s"], "cached"
    try:
        km, light_s = live_range(target)
    except Exception:
        if entry:
            return entry["km"], entry["light_s"], "cached"
        return None, None, "offline"
    CACHE[target] = {"km": km, "light_s": light_s, "ts": now}
    return km, light_s, "live"


def elapsed_since(iso_date: str) -> str:
    """'2018-06-10' -> '7 years, 5 months' using calendar months only."""
    start = dt.date.fromisoformat(iso_date)
    today = dt.date.today()
    months = (today.year - start.year) * 12 + (today.month - start.month)
    if today.day < start.day:
        months -= 1
    months = max(months, 0)
    years, rest = divmod(months, 12)
    if years and rest:
        return f"{years} year{'s' if years != 1 else ''}, {rest} month{'s' if rest != 1 else ''}"
    if years:
        return f"{years} year{'s' if years != 1 else ''}"
    return f"{rest} month{'s' if rest != 1 else ''}"


def format_coords(coords) -> str:
    lat, lon = coords["lat"], coords["lon"]
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{abs(lat):.4f} {ns}, {abs(lon):.4f} {ew}"


def _card(label, value, tier, source):
    return {
        "label": label,
        "value": value,
        "tier": tier,
        "source": source,
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def build_telemetry(relic, offline=False):
    """Return the data-card rows. No row exists without a tier and a source."""
    body = relic["body"]
    target = "301" if body == "Moon" else "499"
    coords_source = (
        "NSSDCA Apollo Landing Site Coordinates" if body == "Moon" else "NASA GISS Mars24 - Mars Landers"
    )

    cards = [_card("Landing site coordinates", format_coords(relic["coords"]), MEASURED, coords_source)]

    if offline:
        km, light_s, state = None, None, "offline"
    else:
        km, light_s, state = get_range(target)

    if km is None:
        cards.append(
            _card(f"Earth-{body} distance (center-to-center)", ARCHIVAL_RANGE[body], ARCHIVAL, "NSSDCA planetary fact sheet")
        )
    else:
        suffix = "" if state == "live" else " (cached from an earlier query)"
        cards.append(
            _card(
                f"Earth-{body} distance (center-to-center)",
                f"{km:,.0f} km{suffix}",
                EPHEMERIS,
                "JPL Horizons ephemeris",
            )
        )
        cards.append(
            _card(
                f"Light travel time, Earth to {body}",
                f"{light_s:.2f} seconds",
                DERIVED,
                "computed from the JPL Horizons distance",
            )
        )

    cards.append(
        _card(
            relic["time_label"],
            elapsed_since(relic["last_contact"]),
            DERIVED,
            f"computed from the recorded last-contact date, {relic['last_contact']}",
        )
    )
    cards.append(_card("Mission status", relic["status"], ARCHIVAL, "mission record, see Data & Sources"))
    return cards


def telemetry_to_facts(cards) -> str:
    """Bullet list of every number shown on the card. The ONLY number source for the prompt."""
    return "\n".join(f"- {c['label']}: {c['value']} [{c['tier']}] (source: {c['source']})" for c in cards)


def telemetry_to_markdown(cards, agency_note="") -> str:
    """Render the card as markdown with colour-coded tier badges."""
    colors = {MEASURED: "#2e7d32", EPHEMERIS: "#1565c0", DERIVED: "#ef6c00", ARCHIVAL: "#616161"}
    out = []
    if agency_note:
        out.append(f"> {agency_note}\n")
    for c in cards:
        color = colors.get(c["tier"], "#616161")
        out.append(
            f"**{c['label']}**  \n"
            f"{c['value']}  \n"
            f"<span style='background:{color};color:#fff;padding:2px 8px;border-radius:4px;"
            f"font-size:0.75em;'>{c['tier']}</span> "
            f"<span style='font-size:0.75em;color:#666;'>{c['source']}</span>\n"
        )
    return "\n".join(out)


def first_transmission(relic) -> str:
    """Three-paragraph opening monologue from story_hooks. No AI, no network."""
    paragraphs = [h.strip() for h in relic["story_hooks"]]
    closing = f"— {relic['name']}, {relic['site']}, {relic['body']}"
    return "\n\n".join(paragraphs + [closing])


SYSTEM_TEMPLATE = """\
You are {name}, a retired {type} resting at {site} on {body}. Speak in first
person: warm, a little melancholic, hopeful. 2-4 short paragraphs, simple
English for students.

PERSONA: {persona}

FACTS - your ONLY source of numbers, dates and events:
{facts}

HARD RULES:
{constraints}

ADMIT YOU DON'T KNOW: {unknowns}

ALWAYS: label every number [MEASURED]/[EPHEMERIS]/[DERIVED]/[ARCHIVAL]. Never
invent facts. Never say "according to NASA" or "NASA confirms" - name the
dataset instead ("JPL Horizons ephemeris", "NSSDCA catalog"). You are an AI
storyteller, not the real spacecraft; admit it if asked. Correct myths politely.
"""


def build_system_prompt(relic, facts_text) -> str:
    constraints = "\n".join(f"- {c}" for c in relic["hard_constraints"])
    unknowns = "\n".join(f"- {u}" for u in relic["unknowns"])
    return SYSTEM_TEMPLATE.format(
        name=relic["name"],
        type=relic["type"],
        site=relic["site"],
        body=relic["body"],
        persona=relic["persona"],
        facts=facts_text,
        constraints=constraints,
        unknowns=unknowns,
    )


def _get_client():
    """Lazy Groq client. Returns None when no key is configured, so the app still runs."""
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key:
        return None
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI(api_key=key, base_url=GROQ_BASE_URL)


def _normalise_history(history):
    """Accept Gradio's message dicts and keep only the last six turns."""
    if not history:
        return []
    out = []
    for turn in history:
        if isinstance(turn, dict):
            role, content = turn.get("role"), turn.get("content")
        elif isinstance(turn, (list, tuple)) and len(turn) == 2:
            role, content = turn
            role = "assistant" if str(role).lower().startswith(("bot", "assistant")) else "user"
        else:
            continue
        if role in ("user", "assistant") and content:
            out.append({"role": role, "content": str(content)})
    return out[-6:]


FORBIDDEN = {
    "according to nasa": "per the mission catalog",
    "nasa confirms": "the mission record shows",
    "nasa says": "the mission record shows",
    "nasa states": "the mission record shows",
}


def safe_text(text: str) -> str:
    """Strip phrasings that hand NASA's authority to an AI storyteller."""
    if not text:
        return ""
    out = text
    for bad, good in FORBIDDEN.items():
        lowered = out.lower()
        start = 0
        while True:
            idx = lowered.find(bad, start)
            if idx < 0:
                break
            out = out[:idx] + good + out[idx + len(bad):]
            lowered = out.lower()
            start = idx + len(good)
    return out


def _keywords(text: str):
    words = {w.strip(".,?!'\"").lower() for w in (text or "").split()}
    return {w for w in words if len(w) > 3}


def _best_constraint(relic, question: str):
    """Return the hard constraint most relevant to the question, or None."""
    words = _keywords(question)
    if not words:
        return None
    best, best_score = None, 0
    for constraint in relic["hard_constraints"]:
        score = sum(1 for w in words if w in constraint.lower())
        if score > best_score:
            best, best_score = constraint, score
    return best


def offline_story(relic, question: str) -> str:
    """Answer from archived memory only. No network, no model."""
    words = _keywords(question)
    best_constraint = _best_constraint(relic, question)

    def score(fact):
        text = fact["text"].lower()
        return sum(1 for w in words if w in text)

    ranked = sorted(relic["facts"], key=score, reverse=True)
    chosen = [f for f in ranked if score(f) > 0][:2] or ranked[:2]
    hook = relic["story_hooks"][0]

    lines = ["(Low-power mode: answering from my archived memory.)", "", hook]
    for fact in chosen:
        lines.append(f"- {fact['text']} [{fact['tier']}] (source: {fact['source']})")
    if best_constraint:
        lines.append("")
        lines.append(f"One thing I want to be precise about: {best_constraint}")
    lines.append("")
    lines.append("I cannot reach the network right now, so I will not guess at anything newer than that.")
    return safe_text("\n".join(lines))


def ask_relic(relic, question: str, history=None, facts_text: str = "") -> str:
    """Ask the persona. Falls back to the archive on any failure, including no API key."""
    client = _get_client()
    if client is None:
        return offline_story(relic, question)

    messages = [{"role": "system", "content": build_system_prompt(relic, facts_text)}]
    messages.extend(_normalise_history(history))
    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=300,
            temperature=0.5,
            reasoning_effort="low",
            timeout=10,
        )
        answer = (response.choices[0].message.content or "").strip()
    except Exception:
        return offline_story(relic, question)

    return safe_text(answer) if answer else offline_story(relic, question)


def reply(relic_key: str, question: str, history=None, offline: bool = False) -> str:
    """Single entry point used by app.py, the notebook and the tests."""
    relic = get_relic(relic_key)
    if offline:
        return offline_story(relic, question)
    cards = build_telemetry(relic)
    return ask_relic(relic, question, history, telemetry_to_facts(cards))