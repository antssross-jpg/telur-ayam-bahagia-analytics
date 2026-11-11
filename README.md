# Farm Analytics — Telur Ayam Bahagia

Analisis end-to-end untuk menjawab pertanyaan manajemen:

> "Produksi telur per kandang sudah efisien belum — dan di mana pakan paling boros?"

Telur Ayam Bahagia adalah peternakan ayam petelur (3 kandang, 6.000 ekor awal, strain Lohmann Brown & Isa Brown) yang memasok telur ke Agrolestari Mart. Periode analisis 12 bulan, Nov 2025–Okt 2026.

## Data

Data contoh (sintetis, dibuat untuk latihan) — 12 bulan, Nov 2025–Okt 2026. **Harga jual adalah harga farm-gate peternakan** (Grade A Rp1.900/butir), bukan harga retail Rp2.900/butir di Agrolestari Mart — selisihnya adalah margin ritel. Umur ayam, populasi awal, dan harga jual per grade adalah asumsi yang dimodelkan dan dilabeli sebagai asumsi:

| File | Isi | Baris |
|---|---|---|
| `data/produksi.csv` | Produksi harian per kandang: populasi, telur butir & kg, retak, afkir, mati, pakan kg | 1.095 |
| `data/penjualan.csv` | Penjualan harian per grade (A/B/C) + harga farm-gate & omzet | 1.095 |
| `data/biaya.csv` | Biaya bulanan: pakan, obat/vaksin, tenaga kerja, amortisasi pullet, penyusutan kandang, listrik/air, lain-lain | 12 |

## Metode

1. **SQL** (`sql/analisis.sql`) — hen-day per kandang per bulan, FCR per kandang, mortalitas, HPP per butir & margin per grade, mix grade, dampak gangguan Kandang C, komposisi biaya, tren bulanan.
2. **Python/pandas** (`python/analisis.py`) — cleaning, hen-day, FCR, mortalitas, biaya per butir, bukti gangguan, tren bulanan.
3. **Power BI** (`powerbi/`) — dashboard 2 halaman (lihat petunjuk di foldernya).
4. **Ringkasan eksekutif** (`docs/executive-summary.md`) — temuan → dampak → rekomendasi.

## Temuan utama

1. **Produksi 1.743.333 butir (105.548 kg) setahun, hen-day rata-rata 81,4%.** Puncak Jan 2026 (89,5%), lalu turun perlahan seiring umur ayam menjadi 75,4% di Okt 2026.
2. **FCR 2,33 — di atas patokan 2,0–2,2.** Kandang B paling boros (2,4) sekaligus hen-day paling rendah (79,9% vs 83,4% di Kandang A). FCR memburuk dari 2,2 (Jan–Jun) menjadi 2,4 (Sep–Okt) seiring umur ayam.
3. **Gangguan Kandang C, 8–21 Sep 2026.** Hen-day jatuh ke 55,8% (vs 78,4% dua minggu sebelumnya), 29 ekor mati (vs 4), kehilangan ~4.653 butir ≈ Rp8,4 juta omzet. Inilah penyebab utama mortalitas Kandang C tertinggi (6,5%).
4. **HPP Rp1.402/butir; omzet Rp3,10 miliar, laba Rp693 juta, margin 22,4%.** Pakan mendominasi biaya (73,6%), disusul amortisasi pullet/ayam dara (18,7%).
5. **Grade A 55% dari volume, 57,8% dari omzet** (Rp1,79 miliar). Telur retak 21.012 butir (1,2%) dan afkir 8.661 butir (0,5%) — keduanya langsung mengurangi telur layak jual.
6. **Mortalitas setahun 5,13% (308 ekor)** — masih dalam batas wajar, tapi terkonsentrasi di Kandang C pada September.

## Rekomendasi

1. Audit Kandang B dulu: hen-day terendah + FCR tertinggi — cek pakan, air minum, ventilasi, dan pencahayaan dibanding Kandang A.
2. Buat protokol respons cepat untuk gangguan kesehatan (deteksi dini + isolasi), karena 2 minggu gangguan di Kandang C menghilangkan ~4.653 butir.
3. Rencanakan pergantian flock (replacement) sebelum hen-day jatuh di bawah 75% dan FCR menembus 2,4 — tren Okt 2026 sudah mengarah ke sana.
4. Turunkan telur retak (1,2%): cek handling saat panen dan kondisi litter/tempat bertelur.
5. Dashboard mingguan: hen-day per kandang, FCR, mati harian, dan stok pakan — supaya gangguan ketahuan dalam hitungan hari, bukan minggu.

## Tools

SQL • Python (pandas) • Power BI • Excel

## Cara menjalankan

```bash
# Python
cd python
pip install pandas
python analisis.py

# SQL: import ketiga CSV ke database (SQLite/PostgreSQL/dll),
# lalu jalankan sql/analisis.sql
```

## Struktur repo

```
├── data/          # dataset contoh (CSV)
├── sql/           # query analisis
├── python/        # script pandas
├── powerbi/       # petunjuk membangun dashboard + mockup
├── docs/          # executive summary 1 halaman
└── README.md
```

*Data dalam repo ini sintetis dan dibuat untuk keperluan belajar/portofolio, bukan data perusahaan nyata. Harga jual adalah harga farm-gate peternakan; HPP, volume harian, dan biaya adalah asumsi yang dimodelkan. Hubungannya dengan portofolio Agrolestari Mart: telur yang sama dijual Rp1.900/butir di peternakan dan Rp2.900/butir di retail.*
