Project: Kalkulasi Magnitudo (ML, MS, MB) - Demo
------------------------------------------------
Instruksi:
1. Buat virtualenv dan install dependensi:
   python -m venv venv
   source venv/bin/activate   (Windows: venv\Scripts\activate)
   pip install -r requirements.txt

2. Struktur file seperti di atas. Jalankan:
   python main.py

3. Siapkan CSV sederhana dengan 2 kolom: 'time' dan 'amp'.
   - time: detik relatif (0, 0.01, 0.02, ...) atau timestamps ISO
   - amp: amplitudo (unit yang konsisten — contoh: mm)

4. Klik "Load CSV", kemudian "Compute". Sesuaikan parameter model di kode (MLParams, dll) berdasarkan kalibrasi/rumus yang kamu gunakan.

Catatan penting:
- Default coefficient hanyalah contoh. Untuk hasil nyata, pakai kurva/koefisien lokal dari literatur.
- Fitur yang bisa ditambahkan: pick otomatis (STA/LTA), baca format SAC/MSEED, smoothing, export PDF laporan, batch processing.
