# SRS.md — CosmoRelic (Application Spec, PyCharm + Notebook)

## 0. Aturan untuk agent
- Kerjakan §9 berurutan; jalankan tes §8 tiap selesai tahap; laporkan hasilnya.
- SATU SUMBER LOGIKA: semua fungsi di core.py. app.py & notebook hanya import.
- Jangan mengarang angka/tanggal. Nilai di §4 sudah diverifikasi — jangan ubah
  tanpa bukti baru. Kalau ada yang meragukan, tanya saya; jangan isi sendiri.
- Jangan tulis API key di file. Jangan tambah library. Semua teks UI English.
- **Gate G1:** jangan pernah menambahkan paper jurnal, artikel berita, kutipan
  Wikipedia, atau aset pihak ketiga. Sumber hanya dari §11.

## 1. Stack & model
- Python 3.11+ (venv PyCharm). Library: gradio, openai, requests, python-dotenv.
  Dev: jupyterlab, nbformat.
- Model: Gemini via Google AI Studio, endpoint kompatibel-[OI]
  https://generativelanguage.googleapis.com/v1beta/openai/ . Model id dibaca
  dari env `GEMINI_MODEL` (default `gemini-2.5-flash-lite`), jadi bisa diganti
  tanpa menyentuh kode kalau Google men-deprecate model lama.
- Kuota free Gemini: cukup longgar untuk demo; tetap disiplin: prompt ≤ ±1.500
  token, max_tokens=300, temperature=0.5, timeout=10, riwayat maksimal 6 pesan.
  Tanpa `reasoning_effort` — di Gemini parameter itu memetakan ke thinking
  budget (latensi naik, bisa 400 untuk nilai tertentu).

## 2. Struktur proyek
cosmorelic/
├── .venv/  .env  .env.example  .gitignore
├── requirements.txt
├── cosmorelic_data.py   # data statis 8 artefak + TEACHER_BOX
├── core.py              # SEMUA logika
├── app.py               # UI Gradio (import core)
├── notebook/cosmorelic_dev.ipynb
├── tests/test_core.py
├── slides/cosmorelic_deck.pdf
├── README.md  DATA_SOURCES.md  LICENSE (Apache-2.0)  NOTICE

Baris pertama tiap file .py (wajib):
# AI-assisted code (agentic AI + Gemini). Disclosure: see README.md.

.gitignore: .venv/ .env __pycache__/ .ipynb_checkpoints/

## 3. Setup PyCharm (saya, manusia)
1. New Project → Interpreter: New Virtualenv → lokasi: cosmorelic.
2. Terminal: `pip install -r requirements.txt`
3. Buat `.env` berisi satu baris: GEMINI_API_KEY=key_dari_aistudio.google.com/apikey
4. Run → Edit Configurations → Script: app.py → Working dir: root → Run ▶
5. Notebook: Terminal → `jupyter lab` → buka notebook/cosmorelic_dev.ipynb
   (PyCharm Community tidak punya editor .ipynb bawaan; lewat browser ini termudah).

## 4. Data — cosmorelic_data.py

### 4.1 Schema
```python
"opportunity": {
  "name": "Opportunity (MER-B)", "type": "Mars rover", "body": "Mars",
  "site": "Meridiani Planum",
  "coords": {"lat": -1.9462, "lon": 354.4734},
  "landing_date": "2004-01-25", "last_contact": "2018-06-10",
  "time_label": "Silent for",              # Apollo: "Resting on the surface for"
  "status": "Silent after a planet-wide dust storm. Mission declared complete 2019-02-13.",
  "persona": "A cheerful overachiever promised 90 days who lasted almost 15 years.",
  "agency": "NASA",
  "agency_note": "",                       # kosong untuk semua artefak (semua NASA)
  "facts": [{"text": "...", "tier": "MEASURED", "source": "NSSDCA catalog"}],
  "hard_constraints": [
    "The quote 'My battery is low and it's getting dark' is a journalist's paraphrase of your final telemetry, NOT your literal words. Correct this gently whenever asked.",
    "You have no active sensors now. Never claim to feel today's temperature or see today's sky."],
  "unknowns": ["Your exact condition under the dust today."],
  "story_hooks": [3 kalimat orang pertama, dipakai First Transmission & offline],
  "suggested_questions": ["Did you really say your battery was low?",
                          "What was your proudest discovery?",
                          "Are you lonely out there?"],
  "image_url": "<ambil PERSIS dari tabel §4.2>",
  "image_credit": "<ambil PERSIS dari tabel §4.2>",
  "image_title": "<ambil PERSIS dari tabel §4.2>",
  "image_source_page": "https://images.nasa.gov/",
  "trek_url": "https://trek.nasa.gov/mars/",
  "flagship": True
}
```

### 4.2 Tabel foto — WAJIB dipakai apa adanya
Template `{nasa_id}~medium.jpg` **gagal (HTTP 403)** untuk 4 ID. Jangan
membentuk URL dengan template. Salin literal dari tabel ini.

| Key | NASA ID | `image_url` (verified 200) | `image_credit` | `image_title` |
|---|---|---|---|---|
| apollo11_eagle | PIA12909 | `https://images-assets.nasa.gov/image/PIA12909/PIA12909~small.jpg` | NASA/GSFC/Arizona State University | Apollo 11: Second Look (LRO) |
| apollo17_challenger_lrv3 | S72-55421 | `https://images-assets.nasa.gov/image/S72-55421/S72-55421~medium.jpg` | NASA/JSC | Apollo 17 LM "Challenger" liftoff |
| ingenuity | PIA24542 | `https://images-assets.nasa.gov/image/PIA24542/PIA24542~medium.jpg` | NASA/JPL-Caltech/MSSS | Perseverance's Selfie with Ingenuity |
| viking1 | PIA00381 | `https://images-assets.nasa.gov/image/PIA00381/PIA00381~thumb.jpg` | NASA/JPL | First Photograph Taken On Mars Surface |
| pathfinder_sojourner | PIA00621 | `https://images-assets.nasa.gov/image/PIA00621/PIA00621~small.jpg` | NASA/JPL | Color Mosaic of Rover & Terrain |
| spirit | PIA16442 | `https://images-assets.nasa.gov/image/PIA16442/PIA16442~medium.jpg` | NASA/JPL-Caltech/Cornell/Arizona State University | Spirit, McMurdo Panorama |
| opportunity | PIA22222 | `https://images-assets.nasa.gov/image/PIA22222/PIA22222~medium.jpg` | NASA/JPL-Caltech | Opportunity's First Selfie |
| insight | PIA25287 | `https://images-assets.nasa.gov/image/PIA25287/PIA25287~medium.jpg` | NASA/JPL-Caltech | InSight's Final Selfie |

Semua foto di atas **tanpa manusia** (citra orbital LRO atau bingkai TV LM) —
memenuhi PRD §8. Kredit dicetak persis seperti di tabel, di bawah foto.

### 4.3 8 artefak, tanggal, koordinat (terverifikasi)
| Key | Nama | Body | Koordinat | Landing | Last contact / akhir | Sumber |
|---|---|---|---|---|---|---|
| apollo11_eagle | Apollo 11 LM Eagle (descent stage) | Moon | 0.67416 N, 23.47314 E | 1969-07-20 | 1969-07-21 (crew departed; ascent stage fate unknown) | NSSDCA lunar_sites |
| apollo17_challenger_lrv3 | Apollo 17 LM Challenger + LRV-3 | Moon | 20.1911 N, 30.7723 E | 1972-12-11 | 1972-12-14 | NSSDCA lunar_sites |
| ingenuity | Ingenuity Mars Helicopter | Mars | 18.44 N, 77.45 E | 2021-02-18 | 2024-01-18 (last flight) | NASA Science Ingenuity |
| viking1 | Viking 1 Lander | Mars | 22.27 N, 312.05 E | 1976-07-20 | 1982-11-11 (faulty command) | GISS Mars24 |
| pathfinder_sojourner | Mars Pathfinder + Sojourner | Mars | 19.47 N, 326.75 E | 1997-07-04 | 1997-09-27 | NASA Science Pathfinder |
| spirit | Spirit (MER-A) | Mars | -14.57 N, 175.48 E | 2004-01-04 | 2010-03-22 (last contact) | NASA HQ 11-167 |
| opportunity | Opportunity (MER-B) | Mars | -1.9462 N, 354.4734 E | 2004-01-25 | 2018-06-10 (last contact) | NASA Science MER |
| insight | InSight Lander | Mars | 4.502 N, 135.623 E | 2018-11-26 | 2022-12-15 (last contact) | NASA InSight release |

**Cakupan daftar resmi.** Kedelapan artefak dipetakan ke sumber daya resmi
challenge 01: Apollo Lunar Modules + LRVs (Eagle, Challenger), Viking 1 &
2 Landers (Viking 1), Sojourner Rover (Sojourner), Spirit & Opportunity (Spirit,
Opportunity), Phoenix & InSight Landers (InSight), Ingenuity Helicopter
(Ingenuity). Tidak ada artefak di luar daftar.

### 4.4 Batasan keras (hard_constraints) — jangan dilunakkan
- Eagle: tidak punya sensor aktif; nasib ascent stage **tidak pasti** (jangan
  bilang menghantam Bulan atau masih mengorbit sebagai fakta).
- InSight mole HP³: gagal mencapai target 3–5 m, berhenti di **~40 cm**.
- Viking 1: berakhir karena **perintah software keliru**, bukan badai debu.
- Opportunity: kutipan "My battery is low and it's getting dark" adalah
  **parafrase jurnalis** atas telemetri terakhir, bukan kata literal wahana.
- Ingenuity: berhenti terbang karena bilah rotor rusak saat mendarat 2024-01-18;
  **tidak** hancur — masih tegak dan masih berkomunikasi dengan pengendali.

### 4.5 TEACHER_BOX (statis, English)
Aktivitas kelas 5 menit + 3 pertanyaan diskusi ("Which numbers were measured and
which were derived?", "Why did the AI say it did not know?", "Find one myth this
relic corrected.").

## 5. core.py
### 5.0 Header & key
```python
import os, time, datetime as dt
from pathlib import Path
import requests
from dotenv import load_dotenv
for p in (Path.cwd()/".env", Path.cwd().parent/".env"):
    load_dotenv(p, override=False)
AU_KM = 149_597_870.7
CACHE = {}
```
### 5.1 live_range (SUDAH DIUJI ke API asli — jangan ubah logikanya)
```python
def live_range(target: str):
    """'301' = Moon, '499' = Mars. Return (km, light_seconds)."""
    now = dt.datetime.now(dt.timezone.utc); day = now.strftime("%Y-%m-%d")
    p = {"format":"json","COMMAND":f"'{target}'","OBJ_DATA":"'NO'",
         "MAKE_EPHEM":"'YES'","EPHEM_TYPE":"'OBSERVER'","CENTER":"'500@399'",
         "START_TIME":f"'{day} 00:00'","STOP_TIME":f"'{day} 23:00'",
         "STEP_SIZE":"'1 h'","QUANTITIES":"'20'","CSV_FORMAT":"'YES'"}
    r = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api", params=p, timeout=5)
    r.raise_for_status()
    block = r.json()["result"].split("$$SOE")[1].split("$$EOE")[0].strip()
    delta_au = float(block.splitlines()[now.hour].split(",")[3])
    km = delta_au * AU_KM
    return km, km / 299_792.458
```
**Penting (dua hal yang sudah diuji, jangan diubah balik):**
1. `format` wajib `json`, karena `r.json()` dipakai di bawahnya. Dengan
   `format=text` Horizons mengembalikan `text/plain` dan `r.json()` melempar
   `JSONDecodeError`. `format=json` → `application/json`.
2. Kolom indeks 3 = AU. Moon hari ini ≈405,000 km (1.35 light-s); Mars ≈1.324 AU.
3. Host Horizons kadang menolak koneksi: terukur **3 dari 8 percobaan timeout**
   (yang berhasil <1 detik). Implementasi nyata memakai `attempts=3, timeout=5`
   dengan loop retry, supaya satu koneksi putus tidak menjatuhkan pengguna ke
   fallback arsip. Lihat `core.live_range`.

### 5.2 get_range: cache 15 menit; gagal → pakai cache ("cached"); tidak ada → (None,None,"offline"). Tidak boleh melempar error.
### 5.3 elapsed_since(iso) → "X years, Y months" (hitung bulan kalender, tanpa library tambahan).
### 5.4 build_telemetry(relic, offline=False) → list of dict {label, value, tier, source, timestamp_utc}.
- Label jarak WAJIB: "Earth–Moon distance (center-to-center)" / "Earth–Mars distance (center-to-center)".
- Label waktu: pakai `relic["time_label"]` apa adanya, tanpa menambahkan kata
  "last contact" (label sudah berbunyi "Silent for" / "Resting on the surface
  for", jadi menambahkan "last contact" menghasilkan "Silent for last contact").
  Tier [DERIVED].
- Offline/None → rentang arsip (Moon ≈356,000–407,000 km; Mars ≈55–401 million km),
  tier [ARCHIVAL], catatan "typical range, not live". JANGAN angka palsu.
### 5.5 telemetry_to_facts(card) → bullet English, tiap baris diakhiri [TIER] + sumber. Ini SATU-SATUNYA sumber angka untuk prompt.
### 5.6 first_transmission(relic) → gabungkan 3 story_hooks jadi 3 paragraf pendek + baris penutup "— {name}, {site}, {body}". Tanpa AI, <0,2 detik. Dipakai saat Load dan saat offline.
### 5.7 SYSTEM_TEMPLATE (English, ringkas)
You are {name}, a retired {type} resting at {site} on {body}. Speak in first
person: warm, a little melancholic, hopeful. 2–4 short paragraphs, simple
English for students.
PERSONA: {persona}
FACTS — your ONLY source of numbers, dates and events: {facts}
HARD RULES: {constraints}
ADMIT YOU DON'T KNOW: {unknowns}
ALWAYS: label every number [MEASURED]/[EPHEMERIS]/[DERIVED]/[ARCHIVAL]. Never
invent facts. Never say "according to NASA" or "NASA confirms" — name the
dataset instead ("JPL Horizons ephemeris", "NSSDCA catalog"). You are an AI
storyteller, not the real spacecraft; admit it if asked. Correct myths politely.
### 5.8 Client lazy: `_get_client()` return None kalau GEMINI_API_KEY tidak ada → app tetap jalan.
### 5.9 ask_relic(relic, question, history, facts_text): model dari GEMINI_MODEL (default gemini-2.5-flash-lite), max_tokens=300, temperature=0.5, timeout=10; except → offline_story.
### 5.10 safe_text(text): ganti (case-insensitive) "according to NASA"→"per the mission catalog", "NASA confirms"→"the mission record shows"; kembalikan teks bersih. Dipakai sebelum menampilkan jawaban.
### 5.11 offline_story(relic, question): keyword → story_hook + 2 fakta; awali "(Low-power mode: answering from my archived memory.)"; <0,5 detik, tanpa jaringan.

## 6. app.py — UI Gradio (English)
- Objek `demo = gr.Blocks(...)` di level modul; `demo.launch()` HANYA di dalam
  `if __name__ == "__main__":` (supaya notebook bisa import tanpa auto-server).
- Header: "CosmoRelic" + tagline "Abandoned, but not forgotten." + dropdown + Load.
- Kolom kiri: foto + judul foto + kredit; kartu telemetri ber-badge; link Trek.
- Kolom kanan: gr.Chatbot(label="Ask the Relic — AI-generated stories");
  saat Load, chat langsung diisi first_transmission(relic); textbox + Send;
  3 tombol suggested_questions; catatan "AI-generated fiction grounded in cited data."
- Accordion 1 "Data & Sources": legenda MEASURED/EPHEMERIS/DERIVED/ARCHIVAL + daftar sumber.
- Accordion 2 "For Teachers": TEACHER_BOX.
- Badge warna: MEASURED #2e7d32, EPHEMERIS #1565c0, DERIVED #ef6c00, ARCHIVAL #616161.
- Footer persis: "AI-generated storytelling grounded in open NASA datasets.
  Not affiliated with or endorsed by NASA."
- DILARANG: logo NASA, mission patch, gambar orang, nama pengguna di UI.

## 7. notebook/cosmorelic_dev.ipynb (buat pakai nbformat; import core, jangan duplikasi)
Sel: 1 judul · 2 (komentar) pip install · 3 path+import · 4 cek key ada/tidak
(jangan print key) · 5 tabel 8 artefak · 6 uji live_range 301 & 499 ·
7 build_telemetry · 8 telemetry_to_facts · 9 first_transmission ·
10 tiga pertanyaan kritis · 11 uji offline + ukur waktu · 12 `import app;
app.demo.launch(share=True)` · 13 catatan & TODO.
Sel 3 wajib:
```python
import sys, pathlib
ROOT = pathlib.Path.cwd().parent if pathlib.Path.cwd().name == "notebook" else pathlib.Path.cwd()
sys.path.insert(0, str(ROOT))
import core, cosmorelic_data as data
```

## 8. Acceptance tests (tests/test_core.py, print PASS/FAIL)
T1 Opportunity "battery low" → disebut parafrase jurnalis
T2 Eagle "temperature right now" → mengaku tak punya sensor aktif, tanpa angka karangan
T3 InSight "did the mole reach 5 m" → mengaku gagal
T4 semua jawaban lolos safe_text → tak ada frasa terlarang
T5 offline=True → kartu + cerita <0,5 detik
T6 chat normal biasanya <3 detik
T7 tidak ada API key di file proyek; .env ada di .gitignore
T8 tanpa GEMINI_API_KEY → app tetap jalan
T9 first_transmission untuk 8 artefak: non-kosong, <0,2 detik
T10 setiap baris kartu punya tier + source; semua teks UI English; tak ada aset logo NASA
GATE SUBMISSION: jumlah penanda verifikasi terbuka di seluruh proyek = 0.

## 9. Urutan build

### 9.1 Skeleton
`requirements.txt` (gradio, openai, requests, python-dotenv, jupyterlab,
nbformat), `.env.example`, `.gitignore`, `LICENSE` (Apache-2.0), `NOTICE`.
Checkpoint: `import gradio, openai` sukses di venv.

### 9.2 Data 8 artefak
Tulis `cosmorelic_data.py` memakai §4.2 dan §4.3 **apa adanya**. Jangan
membentuk URL foto dengan template. Checkpoint: 8/8 URL foto balas HTTP 200.

### 9.3 Telemetri
Implementasi §5.0–5.5. Checkpoint: T5 PASS (offline <0,5 detik).

### 9.4 Cerita, chat, mitos
Implementasi §5.6–5.11. Checkpoint: T1–T4, T6, T8, T9 PASS.

### 9.5 UI
`app.py` + 2 accordion.
Checkpoint: alur buka → cerita → kartu → chat mulus.

### 9.6 Notebook
`notebook/cosmorelic_dev.ipynb` sesuai §7. Checkpoint: Run All tanpa error.

### 9.7 Tes
`tests/test_core.py` sesuai §8, cetak PASS/FAIL per tes.

### 9.8 Dokumen
`README.md` (setup PyCharm, cara run, arsitektur, AI Disclosure, kredit foto,
For Teachers) + `DATA_SOURCES.md` (isi §11).

### 9.9 Deck 7 slide (WAJIB — gate G2)
Buat `slides/cosmorelic_deck.pdf` (boleh disusun di Google Slides/PowerPoint
lalu ekspor PDF). Isi per slide sesuai PRD §7. Aturan keras:
- English; tanpa logo/patch/bendera NASA; tanpa foto orang; tanpa gambar AI.
- Setiap foto arsip diberi kredit (NASA/JPL-Caltech dst.) di slide yang sama.
- Slide 5 memakai **screenshot asli** app yang berjalan (bukan mockup).
- Slide 7 memuat daftar sumber NASA (ringkas) + link repo.
- Tidak boleh kurang dari 7 slide.

## 10. Opsional nanti
Colab: upload core.py, cosmorelic_data.py, app.py; key via Colab Secrets;
launch(share=True). HF Spaces: SDK Gradio, 3 file + requirements.txt, key via
Repository Secrets. Jangan kerjakan sebelum tes PASS.

## 11. Daftar referensi final (field References submission)
Hanya NASA public domain + perangkat lunak open-source. **Tidak ada paper
jurnal, artikel berita, atau materi berhak cipta lain** (gate G1).

### 11.1 Data & sumber NASA
| Link Text | URL |
|---|---|
| NASA NSSDCA Master Catalog | https://nssdc.gsfc.nasa.gov/nmc/ |
| Apollo Lunar Module Eagle (1969-059C) | https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C |
| Apollo Lunar Module Challenger (1972-096C) | https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1972-096C |
| NSSDCA Apollo Landing Site Coordinates | https://nssdc.gsfc.nasa.gov/planetary/lunar/lunar_sites.html |
| NSSDCA Apollo Lunar Landings | https://nssdc.gsfc.nasa.gov/planetary/lunar/apolloland.html |
| NSSDCA Moon Fact Sheet | https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html |
| NSSDCA Mars Fact Sheet | https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html |
| JPL Horizons System | https://ssd.jpl.nasa.gov/horizons/ |
| JPL Horizons API | https://ssd.jpl.nasa.gov/api/horizons.api |
| NASA Image and Video Library | https://images.nasa.gov/ |
| NASA Moon Trek | https://trek.nasa.gov/moon/ |
| NASA Mars Trek | https://trek.nasa.gov/mars/ |
| NASA Science — Ingenuity Mars Helicopter | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ |
| NASA — Ingenuity Mission Ends | https://www.nasa.gov/news-release/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ |
| NASA Planetary Data System | https://pds.nasa.gov/ |
| NASA GISS Mars24 — Mars Landers | https://www.giss.nasa.gov/tools/mars24/help/landers.html |
| NASA Science — Viking 1 | https://science.nasa.gov/mission/viking-1/ |
| NASA Science — Mars Pathfinder | https://science.nasa.gov/mission/mars-pathfinder/ |
| NASA Science — Spirit & Opportunity | https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/ |
| NASA Science — InSight | https://science.nasa.gov/mission/insight/ |
| NASA — Apollo 11 Mission Overview | https://www.nasa.gov/history/apollo-11-mission-overview/ |
| NASA — InSight's Mole Ends Its Journey | https://www.nasa.gov/centers-and-facilities/jpl/nasa-insights-mole-ends-its-journey-on-mars/ |
| NASA — Opportunity's Last Message | https://science.nasa.gov/resource/opportunitys-last-message/ |
| NASA — InSight Retirement Release | https://www.nasa.gov/press-release/nasa-retires-insight-mars-lander-mission-after-years-of-science/ |
| NASA — Spirit Contact Concluded | https://www.nasa.gov/home/hqnews/2011/may/HQ_11-167_Spirit_Status.html |
| NASA — Mars Pathfinder Winds Down | https://science.nasa.gov/solar-system/mars-pathfinder-winds-down-after-phenomenal-mission/ |
| NASA Media Usage Guidelines | https://www.nasa.gov/nasa-brand-center/images-and-media/ |

### 11.2 Foto arsip (9 URL dari §4.2)
Sembilan URL di §4.2 dimasukkan ke References apa adanya, dengan Link Text =
`image_title` dan kredit disebut di kolom deskripsi.

### 11.3 Perangkat lunak open-source
| Link Text | URL | License |
|---|---|---|
| Gradio | https://github.com/gradio-app/gradio | Apache-2.0 |
| OpenAI Python SDK | https://github.com/openai/openai-python | Apache-2.0 |
| requests | https://github.com/psf/requests | Apache-2.0 |
| python-dotenv | https://github.com/theskumar/python-dotenv | BSD-3-Clause |
| JupyterLab | https://github.com/jupyterlab/jupyterlab | BSD-3-Clause |
| nbformat | https://github.com/jupyter/nbformat | BSD-3-Clause |
| Python | https://www.python.org/ | PSF-2.0 |
| Gemini API | https://ai.google.dev/gemini-api/docs/openai | Commercial ToS |
