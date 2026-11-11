"""Analisis Peternakan Ayam Petelur — Telur Ayam Bahagia (data contoh).

Menjawab pertanyaan manajemen:
"Produksi telur per kandang sudah efisien belum — dan di mana pakan paling boros?"

Jalankan:  python analisis.py
Butuh:    pandas (pip install pandas)
"""
import pandas as pd

prod = pd.read_csv('../data/produksi.csv', parse_dates=['tanggal'])
jual = pd.read_csv('../data/penjualan.csv', parse_dates=['tanggal'])
biaya = pd.read_csv('../data/biaya.csv')

prod['hen_day_%'] = (prod['telur_butir'] / prod['populasi_awal'] * 100)
prod['bulan'] = prod['tanggal'].dt.to_period('M')

# 1. Ringkasan 12 bulan (Nov 2025-Okt 2026)
butir = prod['telur_butir'].sum()
telur_kg = prod['telur_kg'].sum()
pakan_kg = prod['pakan_kg'].sum()
mati = prod['mati'].sum()
pop_awal = 6000
print('== Ringkasan 12 bulan (Nov 2025-Okt 2026) ==')
print(f'Total telur diproduksi : {butir:,} butir ({telur_kg:,.0f} kg)')
print(f'Total pakan dipakai    : {pakan_kg:,.0f} kg')
print(f'FCR (kg pakan/kg telur): {pakan_kg / telur_kg:.2f}')
print(f'Mortalitas setahun     : {mati:,} ekor ({mati / pop_awal * 100:.2f}% dari populasi awal)')
print(f'Hen-day rata-rata      : {prod["hen_day_%"].mean():.1f}%')
print()

# 2. Per kandang: hen-day, mortalitas, FCR
k = prod.groupby('kandang').agg(
    butir=('telur_butir', 'sum'), telur_kg=('telur_kg', 'sum'),
    pakan_kg=('pakan_kg', 'sum'), mati=('mati', 'sum'),
    hen_day=('hen_day_%', 'mean'), populasi_awal=('populasi_awal', 'first'))
k['fcr'] = (k['pakan_kg'] / k['telur_kg']).round(2)
k['mortalitas_%'] = (k['mati'] / k['populasi_awal'] * 100).round(2)
print('== Per kandang ==')
print(k[['butir', 'hen_day', 'fcr', 'mati', 'mortalitas_%']].round(1).to_string())
print()

# 3. Biaya & laba: biaya per butir, harga jual vs HPP
total_biaya = biaya['total_biaya'].sum()
layak = butir - prod['telur_retak'].sum() - prod['telur_afkir'].sum()
omzet = jual['omzet'].sum()
hpp_per_butir = total_biaya / layak
print('== Biaya & laba ==')
print(f'Total biaya setahun     : Rp{total_biaya:,.0f}')
print(f'  di antaranya pakan    : Rp{biaya["biaya_pakan"].sum():,.0f} ({biaya["biaya_pakan"].sum() / total_biaya * 100:.1f}%)')
print(f'  amortisasi pullet     : Rp{biaya["biaya_pullet"].sum():,.0f} ({biaya["biaya_pullet"].sum() / total_biaya * 100:.1f}%)')
print(f'Telur layak jual        : {layak:,} butir (retak {prod["telur_retak"].sum():,}, afkir {prod["telur_afkir"].sum():,})')
print(f'HPP per butir           : Rp{hpp_per_butir:,.0f}')
print(f'Omzet penjualan telur   : Rp{omzet:,.0f}')
print(f'Laba kotor (omzet-biaya): Rp{omzet - total_biaya:,.0f}')
print(f'Margin                  : {(omzet - total_biaya) / omzet * 100:.1f}%')
print()

# 4. Grade: mix & omzet per grade
g = jual.groupby('grade').agg(qty=('qty_butir', 'sum'), omzet=('omzet', 'sum'),
                              harga=('harga_jual', 'first'))
g['share_qty_%'] = (g['qty'] / g['qty'].sum() * 100).round(1)
print('== Penjualan per grade ==')
print(g.to_string())
print()

# 5. Gangguan Kandang C, 8-21 Sep 2026 vs 2 minggu sebelumnya
c = prod[prod['kandang'] == 'C'].copy()
event = c[(c['tanggal'] >= '2026-09-08') & (c['tanggal'] <= '2026-09-21')]
sebelum = c[(c['tanggal'] >= '2026-08-25') & (c['tanggal'] <= '2026-09-07')]
print('== Gangguan Kandang C (8-21 Sep 2026) ==')
print(f"  Hen-day saat gangguan : {event['hen_day_%'].mean():.1f}% (vs {sebelum['hen_day_%'].mean():.1f}% sebelumnya)")
print(f"  Mati saat gangguan    : {int(event['mati'].sum())} ekor (vs {int(sebelum['mati'].sum())} sebelumnya)")
print(f"  Telur hilang (estimasi): {int(sebelum['telur_butir'].mean() * 14 - event['telur_butir'].sum()):,} butir")
print()

# 6. Tren bulanan: hen-day & FCR (FCR memburuk seiring umur ayam?)
bul = prod.groupby('bulan').agg(butir=('telur_butir', 'sum'),
                                 telur_kg=('telur_kg', 'sum'),
                                 pakan_kg=('pakan_kg', 'sum'),
                                 hen_day=('hen_day_%', 'mean'))
bul['fcr'] = (bul['pakan_kg'] / bul['telur_kg']).round(2)
print('== Tren bulanan ==')
print(bul.round(1).to_string())
print()

# 7. Biaya per bulan (pakan mendominasi?)
print('== Biaya per bulan ==')
print(biaya.to_string(index=False))
