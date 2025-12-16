# 🤖 Generator Definisi Kompetensi Teknis (AI-Powered)

!

Aplikasi berbasis [Streamlit](https://streamlit.io/) dan Gemini API (Google GenAI) untuk menghasilkan definisi kompetensi teknis secara otomatis, profesional, dan kontekstual. Proyek ini dirancang untuk tim Learning & Development (L&D) dan HR dalam menyusun katalog kompetensi teknis dengan cepat dan akurat.

## 🏭 Konteks Bisnis

Generator ini secara spesifik dilatih (melalui prompt engineering) untuk menyesuaikan definisi dengan konteks multi-industri dari Group Holding, yang meliputi:
* Manufaktur Skincare & Kosmetik (R&D, QC)
* Distributor Kosmetik & Skincare (Logistik, Sales)
* Retail Kebutuhan Sehari-hari
* Jasa IT (Software Development, Infrastruktur)
* Peternakan Ayam Petelur

## ✨ Fitur Utama

* **Generasi AI Cerdas:** Memanfaatkan Gemini 2.5 Flash untuk definisi yang detail.
* **Penanganan Detail Teknis:** Mampu mengintegrasikan detail dalam kurung (misalnya, `CORETAX` atau `Warna, Bau, Tekstur`) ke dalam deskripsi kompetensi.
* **Fallback Lokal (Fuzzier AI):** Dilengkapi dengan logika Python lokal sebagai *fallback* otomatis. Jika kuota API habis atau kunci tidak valid, aplikasi tetap berjalan dan memberikan output berupa *draft* definisi.
* **Ekspor Data:** Hasil definisi dapat diunduh langsung dalam format CSV (`Definisi_Kompetensi_Teknis.csv`).

## ⚙️ Cara Menjalankan Aplikasi

### 1. Prasyarat

Pastikan Anda telah menginstal **Python (Versi 3.8+)**.

### 2. Instalasi Pustaka (Dependencies)

Buat *virtual environment* dan instal dependensi yang tercantum dalam `requirements.txt`:

```bash
# Instal pustaka yang dibutuhkan
pip install -r requirements.txt

### 3. Konfigurasi API Gemini

$env:GEMINI_API_KEY="[PASTE_KUNCI_API_LENGKAP_ANDA_DI_SINI]"

### 4. Jalankan Aplikasi
python -m streamlit run app.py
