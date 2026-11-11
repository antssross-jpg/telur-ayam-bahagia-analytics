# Dashboard Power BI — petunjuk membangun (Telur Ayam Bahagia)

File .pbix tidak disertakan (dibuat di Power BI Desktop). Ikuti langkah ini:

## 1. Sambungkan data
- Get Data → Text/CSV → pilih `data/produksi.csv`, `data/penjualan.csv`, `data/biaya.csv`.
- Pastikan kolom `tanggal` bertipe Date dan `bulan` di biaya bertipe Date (format yyyy-MM).

## 2. Model (relasi)
- `produksi[tanggal]` → `penjualan[tanggal]` (relasi tanggal, many-to-many tidak perlu — cukup pakai tabel kalender dari `tanggal` produksi).
- Buat tabel kalender dari kolom `tanggal` bila perlu (bulan, kuartal).

## 3. Measures (DAX)
```dax
Total Telur (butir) = SUM(produksi[telur_butir])

Hen-day % = DIVIDE(SUM(produksi[telur_butir]), SUM(produksi[populasi_awal])) * 100

FCR = DIVIDE(SUM(produksi[pakan_kg]), SUM(produksi[telur_kg]))

Mortalitas % = DIVIDE(SUM(produksi[mati]), 6000) * 100

Total Biaya = SUM(biaya[total_biaya])

HPP per Butir = DIVIDE([Total Biaya], SUM(produksi[telur_butir]) - SUM(produksi[telur_retak]) - SUM(produksi[telur_afkir]))

Total Omzet = SUM(penjualan[omzet])

Margin % = DIVIDE([Total Omzet] - [Total Biaya], [Total Omzet]) * 100
```

## 4. Halaman 1 — Ringkasan KPI
- Kartu KPI: Total Telur (1.743.333 butir), Hen-day 81,4%, FCR 2,33, Mortalitas 5,13%, HPP Rp1.402/butir, Margin 22,4%.
- Line chart: hen-day % bulanan per kandang (sorot Kandang B paling rendah, 79,9%).
- Line chart: FCR bulanan (naik dari 2,2 ke 2,4 seiring umur ayam; Nov 2025 3,1 karena masa awal bertelur).
- Bar chart: omzet per grade (A Rp1,79 M, B Rp1,05 M, C Rp0,26 M).
- Slicer: kandang, periode.

## 5. Halaman 2 — Biaya, Gangguan & Grade
- Bar chart: komposisi biaya (pakan 73,6%, amortisasi pullet 18,7%, sisanya operasional).
- Tabel: hen-day & mati Kandang C 8–21 Sep 2026 vs 2 minggu sebelumnya (55,8% vs 78,4%; 29 vs 4 ekor mati).
- Tabel: telur retak (21.012 butir, 1,2%) dan afkir (8.661 butir, 0,5%) per kandang.
- Tulis 3 kalimat insight di bawah dashboard (lihat `docs/executive-summary.md`).

## 6. Selesai
- Publish ke Power BI Service → atur Scheduled Refresh (mis. tiap Senin 06:00).
- Simpan file .pbix ke folder ini (`powerbi/dashboard-telur-ayam-bahagia.pbix`) dan upload ke repo.
