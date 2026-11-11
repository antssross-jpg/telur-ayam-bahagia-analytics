-- Analisis Peternakan Ayam Petelur — Telur Ayam Bahagia (data contoh)
-- Tabel: produksi(tanggal, kandang, strain, umur_minggu, populasi_awal, telur_butir,
--                 telur_kg, telur_retak, telur_afkir, mati, pakan_kg)
--        penjualan(tanggal, grade, qty_butir, harga_jual, omzet)
--        biaya(bulan, pakan_kg, biaya_pakan, biaya_obat_vaksin, biaya_tenaga_kerja,
--              biaya_pullet, biaya_penyusutan_kandang, biaya_listrik_air, biaya_lain, total_biaya)

-- 1. Hen-day % dan produksi per kandang per bulan
SELECT kandang, DATE_TRUNC('month', tanggal) AS bulan,
       SUM(telur_butir) AS total_butir,
       AVG(telur_butir * 1.0 / populasi_awal * 100) AS hen_day_pct
FROM produksi
GROUP BY kandang, bulan
ORDER BY bulan, kandang;

-- 2. FCR (kg pakan / kg telur) per kandang — makin kecil makin efisien
SELECT kandang,
       SUM(pakan_kg) AS total_pakan_kg,
       SUM(telur_kg) AS total_telur_kg,
       SUM(pakan_kg) * 1.0 / SUM(telur_kg) AS fcr
FROM produksi
GROUP BY kandang
ORDER BY fcr;

-- 3. Mortalitas per kandang (ekor & % dari populasi awal)
SELECT kandang,
       MAX(populasi_awal) AS populasi_awal,
       SUM(mati) AS total_mati,
       SUM(mati) * 100.0 / MAX(populasi_awal) AS mortalitas_pct
FROM produksi
GROUP BY kandang
ORDER BY mortalitas_pct DESC;

-- 4. HPP per butir dan margin per grade
--    (total biaya setahun dibagi telur layak jual; harga jual = harga farm-gate)
SELECT grade, SUM(qty_butir) AS qty,
       SUM(omzet) AS omzet,
       AVG(harga_jual) AS harga_jual,
       SUM(qty_butir) * 1402 AS hpp_total,
       SUM(omzet) - SUM(qty_butir) * 1402 AS laba_kotor
FROM penjualan
GROUP BY grade
ORDER BY omzet DESC;

-- 5. Mix grade: berapa % telur yang masuk Grade A (paling mahal)?
SELECT grade, SUM(qty_butir) AS qty,
       SUM(qty_butir) * 100.0 / (SELECT SUM(qty_butir) FROM penjualan) AS share_pct
FROM penjualan
GROUP BY grade
ORDER BY grade;

-- 6. Gangguan Kandang C, 8-21 Sep 2026 vs 2 minggu sebelumnya
SELECT CASE WHEN tanggal BETWEEN '2026-09-08' AND '2026-09-21' THEN 'gangguan'
            ELSE 'sebelum' END AS periode,
       AVG(telur_butir * 1.0 / populasi_awal * 100) AS hen_day_pct,
       SUM(mati) AS total_mati,
       SUM(telur_butir) AS total_butir
FROM produksi
WHERE kandang = 'C'
  AND tanggal BETWEEN '2026-08-25' AND '2026-09-21'
GROUP BY periode;

-- 7. Komposisi biaya: pakan vs amortisasi pullet vs operasional
SELECT 'pakan' AS komponen, SUM(biaya_pakan) AS nilai FROM biaya
UNION ALL SELECT 'pullet (amortisasi)', SUM(biaya_pullet) FROM biaya
UNION ALL SELECT 'tenaga kerja', SUM(biaya_tenaga_kerja) FROM biaya
UNION ALL SELECT 'obat & vaksin', SUM(biaya_obat_vaksin) FROM biaya
UNION ALL SELECT 'penyusutan kandang', SUM(biaya_penyusutan_kandang) FROM biaya
UNION ALL SELECT 'listrik & air', SUM(biaya_listrik_air) FROM biaya
UNION ALL SELECT 'lain-lain', SUM(biaya_lain) FROM biaya
ORDER BY nilai DESC;

-- 8. Tren bulanan: hen-day turun dan FCR naik seiring umur ayam?
SELECT DATE_TRUNC('month', tanggal) AS bulan,
       AVG(telur_butir * 1.0 / populasi_awal * 100) AS hen_day_pct,
       SUM(pakan_kg) * 1.0 / SUM(telur_kg) AS fcr
FROM produksi
GROUP BY bulan
ORDER BY bulan;
