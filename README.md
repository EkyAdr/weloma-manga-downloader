# 📚 Manga Downloader (Weloma.art)

Script ini digunakan untuk mengunduh seluruh gambar dari sebuah chapter manga di situs [weloma.art](https://weloma.art), termasuk gambar yang dimuat secara **lazyload** (baru muncul setelah discroll).

Program ini dibuat menggunakan **Python + Playwright** dan **BeautifulSoup**, serta akan menyimpan hasil unduhan ke dalam folder lokal sesuai dengan judul chapter.

---

## ⚙️ Persyaratan Sistem

Pastikan sudah menginstal:
- **Python 3.10+**
- **pip (Python package manager)**
- **Google Chrome** *(untuk Playwright Chromium)*

---

## 🚀 Langkah Instalasi

1. **Clone atau download** project ini ke komputer kamu  
   ```bash
   git clone https://github.com/username/manga-downloader.git
   cd "Manga Downloader"

## Buat virtual environment (opsional tapi disarankan)

python -m venv venv
venv\Scripts\activate

## Instal semua dependensi yang dibutuhkan

- pip install playwright bs4 rich httpx

- Instal browser Chromium untuk Playwright

- playwright install chromium

## 🧩 Cara Menjalankan

Jalankan program:

- python main.py

- Masukkan URL chapter manga, contoh:

- https://weloma.art/5574/223669/


Program akan:

- Membuka halaman tersebut dengan Chromium.
- Scroll otomatis sampai semua gambar muncul.
- Mengunduh semua gambar ke folder downloads/<nama_chapter>/.
- Setelah selesai, kamu akan melihat folder berisi semua halaman manga.

## 💡 Catatan

Jika muncul error ModuleNotFoundError, pastikan kamu menjalankan perintah pip install di atas.

Kalau gambar tidak terdeteksi, pastikan halaman benar-benar memuat semua gambar sebelum menutup browser.

Kamu juga bisa ubah headless=False ke headless=True agar browser tidak tampil saat proses unduh.

## 🛠️ Teknologi yang Digunakan

- Playwright
- BeautifulSoup4
- Rich
- HTTPX

👨‍💻 Dibuat oleh: Zero Speed
📅 Terakhir diperbarui: November 2025
