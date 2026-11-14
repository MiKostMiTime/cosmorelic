# PRD.md — CosmoRelic (Application Only)

## 1. Satu kalimat
Web app gratis yang mengubah 8 artefak yang ditinggalkan di Bulan & Mars menjadi
pencerita orang pertama: buka artefak → ia langsung bercerita → lihat kartu data
live berlabel kejujuran → tanya apa saja → ia mengoreksi mitosnya sendiri.

## 2. Tantangan resmi (bukan pilihan bebas)
**NASA Space Apps Challenge 2026 — Challenge 01**
"Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on
the Moon and Mars."

Kalimat kunci dari pernyataan resmi: *"tell the story of some or all of this
equipment that introduces school-age space enthusiasts to the hardware and the
science it made possible."* → Sasaran audiens **school-age** adalah perintah
challenge, bukan asumsi kita.

Pernyataan resmi juga menuntut: *"Accuracy is important throughout!"* →
kartu ber-badge + mitos terkoreksi adalah jawaban langsung, bukan hiasan.

**14 sumber daya resmi yang disebut challenge:** NSSDCA · Apollo Lunar Modules ·
Lunar Roving Vehicles · ALSEP · Surveyor 3 · Sojourner · Spirit & Opportunity ·
Viking 1 & 2 · Phoenix & InSight · Dawn · NEAR Shoemaker · Pioneer 10 & 11 ·
Ingenuity · Kepler.

**Cakupan kita: 8 dari 8 artefak berasal dari daftar itu** (Apollo LM ×2 + LRV,
Viking 1, Sojourner, Spirit, Opportunity, InSight, Ingenuity). Tidak ada artefak
di luar daftar resmi.

## 3. Masalah (dua lapis, ini yang menaikkan nilai Impact)
- Lapis 1: cerita hardware yang ditinggalkan NASA terkubur di arsip teknis kering.
- Lapis 2: pelajar hari ini menerima jawaban AI mentah-mentah, tanpa tahu mana
  angka terukur dan mana tebakan.
Solusi: cerita orang pertama yang emosional, TAPI setiap angka berlabel sumber &
tingkat validitas, dan AI-nya berani berkata "aku tidak tahu".

## 4. Pengguna
Pelajar sekolah & guru (utama, sesuai challenge), juri hackathon (pembukti),
portofolio saya (kedua).

## 5. Lingkungan kerja
PyCharm (proyek Python lokal) + Jupyter Notebook (.ipynb) + opsional Colab/HF
Spaces. Biaya Rp 0, tanpa GPU, tanpa training.

## 6. Scope

### P0 — wajib (setiap item memetakan ke kriteria juri 2026)
1. Dropdown 8 artefak + tombol Load. [Relevance]
2. **Setiap artefak terpetakan ke sumber daya resmi challenge 01.** [Relevance]
3. FIRST TRANSMISSION: begitu artefak dibuka, ia otomatis bercerita 3 paragraf
   pendek (dari story_hooks, tanpa AI → instan & offline-safe). [Relevance:
   ini "storytelling", bukan sekadar chatbot] [Creativity] [Presentation]
4. Kartu data ber-badge: foto NASA + kredit + judul foto · koordinat [MEASURED] ·
   jarak Bumi–benda live, label "center-to-center" [EPHEMERIS] · jeda cahaya
   [DERIVED] · waktu di permukaan / kesunyian [DERIVED] · status [ARCHIVAL] ·
   link Moon Trek / Mars Trek. [Validity]
5. Chat persona orang pertama + 3 pertanyaan pemantik + label "AI-generated".
   3 persona dalam: Opportunity, Eagle, InSight. [Creativity]
6. MYTH CORRECTION: artefak mengoreksi legendanya sendiri — "battery low"
   Opportunity = parafrase jurnalis; mole InSight gagal (~40 cm, target 3–5 m);
   Viking 1 berakhir karena perintah software keliru, bukan badai debu;
   Ingenuity tidak hancur — rotor rusak saat mendarat, tapi masih tegak.
   [Validity] [Creativity]
7. LOW-POWER MODE: saat offline/kuota habis, artefak bicara dari memorinya —
   didesain sebagai metafora nasib nyata Opportunity, bukan sekadar error.
   [Creativity] [Impact: sekolah berinternet lemah]
8. Accordion "Data & Sources": legenda 4 tier + daftar sumber. [Validity]
9. Accordion "For Teachers": aktivitas kelas 5 menit + 3 pertanyaan diskusi.
   [Impact]
10. **DECK 7 SLIDE** (English, tanpa logo NASA) — syarat eligibilitas, lihat §7.
    [Presentation]
11. Footer disclaimer + README + DATA_SOURCES + LICENSE + NOTICE. [eligibility]

### P1 — kalau sempat
Persona dalam untuk 6 artefak sisanya; tombol Clear chat; rentang suhu
literatur [ARCHIVAL]; kartu tambahan Surveyor / ALSEP / Phoenix / Dawn /
NEAR Shoemaker / Pioneer (memperluas cakupan keluarga hardware resmi).

### P2 — DILARANG sekarang
Model termal, sub-solar, fajar lunar, cuaca Mars live, LLM fallback kedua,
deep-link Trek, pencarian foto runtime, database, login, multilingual,
TTS/suara, video AI.

## 7. Deliverable presentasi — DECK 7 SLIDE (wajib)
Submission 2026 menuntut **7-slide deck ATAU video 30 detik**. Kita pilih deck
(risiko lebih rendah). Struktur baku:

| # | Slide | Isi wajib |
|---|---|---|
| 1 | Title | "CosmoRelic — Abandoned, but not forgotten." + challenge 01 + 1 kalimat |
| 2 | Problem | Dua lapis §3 + siapa yang dirugikan (sekolah bandwidth rendah) |
| 3 | The eight relics | 8 nama + status 1 baris; tiap baris menyebut sumber daya resmi yang mendasarinya |
| 4 | The honesty system | 4 tier + contoh nyata satu angka per tier |
| 5 | Live demo | Screenshot app: kartu ber-badge + chat + mitos terkoreksi |
| 6 | Low-power mode | "Works at 0 kbps" + alasan desain (metafora Opportunity) |
| 7 | Impact & sources | Guru/kelas + daftar sumber NASA + link repo |

Aturan deck: English, tanpa logo/patch/bendera NASA, tanpa foto orang, tanpa
gambar hasil AI, setiap gambar arsip diberi kredit di slide.

## 8. Aturan produk (tidak boleh dilanggar)
- **G1 — Nol materi berhak cipta.** Tidak ada paper jurnal, artikel berita,
  kutipan Wikipedia, musik, atau gambar pihak ketiga di repo maupun di field
  References. Semua klaim bersumber ke halaman **NASA public domain** atau
  perangkat lunak open-source. Field References hanya berisi daftar SRS §11.
- Semua teks UI & materi submission: ENGLISH.
- Tanpa logo NASA / mission patch / bendera NASA di UI maupun slide.
- Chat berlabel "AI-generated"; kode hasil AI diakui di header file + README.
- Tidak ada gambar/video hasil generate AI. Hanya foto arsip NASA berkredit +
  screenshot sendiri.
- Tidak ada gambar orang di UI, README, maupun slide (foto Apollo yang dipakai
  adalah citra orbital LRO atau bingkai TV tanpa manusia).
- Saya di bawah 18: tidak ada wajah, suara, atau nama yang mengenali saya di
  demo/screenshot. Identitas anggota cukup di halaman Project.
- AI dilarang mengarang angka dan dilarang berkata "according to NASA".
- API key hanya di .env / environment, tidak pernah di file yang di-commit.

## 9. Keselarasan kriteria juri 2026 (skala 1–5, semua fase)
| Kriteria | Definisi skor 5 (dari guide resmi) | Posisi kita | Celah yang ditutup |
|---|---|---|---|
| Impact | Masalah signifikan, jangkauan luas | Sekolah bandwidth rendah, low-power mode | Angka "0 kbps" ditampilkan di slide 6 |
| Creativity | Belum pernah dicoba | Artefak mengoreksi mitosnya sendiri | Demo koreksi mitos live, bukan teks |
| Validity | Layak, **fully developed**, usable | 4 tier + Horizons + fallback offline | **0 penanda verifikasi terbuka** di seluruh repo |
| Relevance | Data NASA **integral**, bukan tempelan | Horizons menghasilkan angka inti; 8/8 artefak dari daftar resmi | Tambah keluarga resmi lain jika waktu memungkinkan |
| Presentation | Storytelling menarik, terstruktur | Deck 7 slide + demo | Deck dikerjakan di sesi terlindungi |

Guide resmi memperingatkan presentation paling sering diabaikan → deck bukan
opsional.

**Target award yang realistis:** Best Storytelling · Most Inspirational ·
Best Use of Data · Best Use of Science. Pitch spine: *Most Inspirational*.

## 10. Definisi sukses
- [ ] `python app.py` jalan di PyCharm; notebook Run All tanpa error.
- [ ] 10 tes di SRS §8 PASS, dan tidak ada penanda verifikasi terbuka tersisa.
- [ ] Internet mati → app tetap jalan (low-power mode).
- [ ] Tanpa API key → app tetap jalan, tidak crash.
- [ ] 8/8 URL foto balas HTTP 200 saat diperiksa.
- [ ] Deck 7 slide lengkap, English, tanpa logo NASA.
- [ ] Juri baru bisa paham produk dalam <60 detik tanpa penjelasan saya.
