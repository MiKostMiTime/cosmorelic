# PDW-APP.md — Plan-Do-Work (Aplikasi)

## 0. Aturan main
Deadline submission: **Minggu 15 Nov 2026, 23:59 waktu lokal event**.
Anggaran: ±12 jam kerja + 8 jam tidur. Tidur tetap wajib.
Mentok 45 menit → potong pakai cut-line §2. Satu sesi lolos checkpoint dulu, baru lanjut.
Boleh minta bantuan agent/mentor.

**Dua gate tidak bisa dinegosiasi** (kalau gagal, diskualifikasi / skor jatuh):
- G1 COPYRIGHT: 0 materi berhak cipta di repo & References.
- G2 DECK: 7 slide ada, English, tanpa logo NASA.

## 1. Sesi

| Sesi | Durasi | Plan | Do | Check |
|---|---|---|---|---|
| S0 | 45m | Proyek siap | Kamu: PyCharm+venv, pip install, .env isi key. Agent: SRS §9.1 | C0: import gradio & openai sukses |
| S1 | 1,5j | Data 8 artefak + URL foto | Agent: SRS §9.2 (pakai tabel §4.2 apa adanya). Kamu: buka 8 URL foto di browser | C1: penanda verifikasi terbuka = 0 **dan 8/8 foto balas 200** |
| S2 | 1,5j | Telemetri | Agent: §9.3. Kamu: lihat angka live, matikan internet, tes lagi | C2: T5 PASS |
| S3 | 2j | Cerita + chat + mitos | Agent: §9.4. Kamu: jalankan T1–T4, T6, T8, T9 | C3: mitos terkoreksi, First Transmission muncul |
| 😴 | 8j | Tidur | Tidur | — |
| S4 | 2j | UI + accordion | Agent: §9.5. Kamu: Run ▶, coba di HP | C4: alur buka→cerita→kartu→chat mulus |
| S5 | 1j | Notebook | Agent: §9.6. Kamu: jupyter lab → Run All | C5: semua sel jalan |
| S6 | 1j | Tes + README + DATA_SOURCES | Agent: §9.7–9.8. Kamu: baca README, cek git status | C6: 11 tes PASS, .env tidak ter-commit | ✅ SELESAI |
| S7 | 1,5j | **DECK 7 SLIDE (wajib)** | Agent: §9.9. Kamu: isi nama tim + link demo | **G2: 7 slide, English, no NASA logo** — ✅ file jadi & terverifikasi visual; sisa: isi 2 placeholder + host link publik |
| S8 | 45m | References + submit | Kamu: salin §11 SRS ke form. Agent: cek ulang repo | **G1: 0 materi berhak cipta. Submit.** |

Total ±12 jam. Kalau jam dinding sudah menunjukkan 6 jam sebelum deadline dan S7 belum mulai → **kerjakan S7 dulu**, S5/S6 boleh disusutkan.

## 2. Cut-lines
Horizons rewel >45m → kartu [ARCHIVAL] + counter ·
foto 403 → ganti ke `~small.jpg`/`~thumb.jpg` versi PIA (lihat §3) ·
UI mepet → satu kolom · notebook mepet → 6 sel inti ·
kuota habis → low-power mode adalah fitur · persona 8 belum dalam → 3 flagship cukup ·
**deck mepet → tetap 7 slide, isi dipadatkan; JANGAN kurang dari 7** ·
references mepet → §11 SRS sudah final, tinggal salin.

## 3. Troubleshooting
ModuleNotFoundError → interpreter harus .venv, pip install ulang ·
401 → cek .env (bukan .env.txt), tanpa kutip/spasi ·
404 model → fallback chain otomatis; manual: ganti GROQ_MODEL di .env (id valid: `curl https://api.groq.com/openai/v1/models`) ·
429 → tunggu / low-power mode ·
notebook "No module named core" → pakai sel 3 ·
port sibuk → server_port=7861 ·
**foto 403 → JANGAN pakai template `~medium.jpg` untuk semua. Aturan sudah diverifikasi:**
- `PIA12909`, `PIA00381`, `PIA00621` → **hanya** `~small.jpg` atau `~thumb.jpg`
- `S72-55421`, `PIA16442`, `PIA22222`, `PIA25287`, `PIA24542` → `~medium.jpg` OK
- Ambil URL final dari SRS §4.2, jangan dikarang.

## 4. Perintah
Windows: `.venv\Scripts\activate` | Mac/Linux: `source .venv/bin/activate`
`pip install -r requirements.txt` · `python app.py` · `jupyter lab` ·
`python tests/test_core.py` · `git status`

## 5. Checklist submit (isi di halaman Project)
- [x] Challenge dipilih: **01 — Abandoned but not Forgotten**
- [ ] Deskripsi project English
- [x] 7 slide di `deck/cosmorelic_deck.pptx` — **G2 LULUS** (tepat 7, English, tanpa logo NASA)
- [ ] Nama tim + anggota diisi di slide 1 (placeholder `TEAM NAME ...`)
- [ ] Link demo publik ditempel di slide 5 dan 7 (placeholder `LIVE DEMO ...`)
- [ ] Deck di-host publik tanpa login (juri butuh link, bukan file)
- [ ] References field = SRS §11 (NASA + OSS saja) — G1
- [ ] Checkbox "no copyrighted materials" dicentang dengan sadar
- [ ] Semua anggota terdaftar di Local Event yang sama (maks 6 orang)
- [ ] Submit sebelum 23:59 lokal
