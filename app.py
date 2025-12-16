import streamlit as st
import pandas as pd
from google import genai 
from google.genai import types
import os 
import json 
import time

# --- KONTEKS BISNIS UTAMA UNTUK PROMPT AI ---
BUSINESS_CONTEXT = """
Perusahaan Group Holding, terdiri dari:
1. Manufaktur Skincare & Kosmetik (R&D, Produksi, Quality Control).
2. Distributor Kosmetik & Skincare (Logistik, Sales, Marketing).
3. Retail Kebutuhan Sehari-hari (Operasional Toko, Merchandising).
4. Jasa IT (Pengembangan Software, Infrastruktur, Support).
5. Peternakan Ayam Petelur (Produksi Telur, Pakan, Kesehatan Hewan).

Definisi harus: profesional, ringkas, lengkap, dan relevan dengan industri di atas.
"""

# --- FUNGSI FALLBACK/MOCK-UP AI LOKAL ---
def fuzzier_ai_mock(competency_list, context):
    """
    Simulasi AI menggunakan logika Python sederhana (tanpa model AI eksternal).
    Digunakan saat kuota atau API Key gagal/habis.
    """
    st.info("⚠️ Menggunakan Simulasi AI Lokal. Kualitas definisi mungkin tidak seakurat Gemini.")
    time.sleep(1) # Tambahkan sedikit delay untuk visual
    
    results = []
    
    # Logika sederhana untuk membuat definisi berdasarkan kata kunci dan konteks multi-industri
    for comp in competency_list:
        
        # 1. Ekstrak detail dalam kurung
        detail = ""
        comp_name = comp.strip()
        if '(' in comp and ')' in comp:
            try:
                detail = comp.split('(')[-1].split(')')[0].strip()
                comp_name = comp.split('(')[0].strip()
            except:
                pass # Jika parsing gagal, gunakan nama kompetensi asli
        
        # 2. Tentukan Fokus Konteks
        fokus = "prosedur standar operasional (SOP) yang relevan dan terbaik."
        if "IT" in comp_name or "Kode" in comp_name or "Sistem" in comp_name:
            fokus = "metodologi pengembangan perangkat lunak, infrastruktur jaringan, dan keamanan siber."
        elif "Skincare" in comp_name or "Kosmetik" in comp_name or "Formulasi" in comp_name or "Organoleptik" in comp_name:
            fokus = "standar Good Manufacturing Practice (GMP), Quality Control (QC), dan riset formulasi produk kecantikan."
        elif "Pakan" in comp_name or "Ayam" in comp_name or "Peternakan" in comp_name:
            fokus = "praktik peternakan modern, manajemen pakan, kesehatan hewan, dan biosekuriti."
        elif "Retail" in comp_name or "Distribusi" in comp_name or "Vendor" in comp_name:
            fokus = "manajemen rantai pasok, kepuasan pelanggan, dan operasional toko yang efisien."

        # 3. Bangun Definisi
        definisi = f"Kemampuan untuk menguasai dan menerapkan {comp_name.lower()} di lingkungan multi-industri. Meliputi pemahaman mendalam tentang {fokus}"
        
        if detail:
            definisi += f" Fokus pada detail teknis/objek seperti: {detail.replace(',', ', ')}."
        
        results.append((comp, definisi.capitalize()))
        
    df = pd.DataFrame(results, columns=['Nama Kompetensi', 'Definisi'])
    df.index = df.index + 1
    df.index.name = 'No.'
    return df
# ----------------------------------------------------------------------


def generate_definition_with_ai(competency_list):
    """
    Fungsi ini memanggil Gemini API (dengan fallback ke simulasi lokal).
    """
    
    # 1. Ambil API Key dari environment variable
    api_key = os.environ.get("AIzaSyBW3XamS_Smay4wOUdFQpzxgBq75ZDvB5Q") 
    
    if not api_key:
        # Jika kunci tidak ditemukan, langsung fallback
        return fuzzier_ai_mock(competency_list, BUSINESS_CONTEXT)
    
    try:
        client = genai.Client(api_key=api_key)
        model = 'gemini-2.5-flash' 
        
        # 2. Siapkan System Prompt (Sama seperti sebelumnya)
        system_prompt = f"""
        Anda adalah ahli HR dan Technical Writer. Tugas Anda adalah membuat DEFINISI KOMPETENSI TEKNIS yang akurat.
        KONTEKS PERUSAHAAN: {BUSINESS_CONTEXT}
        ATURAN DEFINISI: ... (Aturan 1-4 Anda)
        FORMAT OUTPUT JSON: [...]
        """
        
        # 3. Siapkan User Prompt
        competency_input_str = "\n".join([f"- {c}" for c in competency_list])
        user_prompt = f"""Tolong buatkan definisi kompetensi untuk daftar berikut: {competency_input_str}"""
        
        # 4. Panggil API Gemini
        st.info(f"⏳ Mengirim {len(competency_list)} kompetensi ke Gemini API untuk digenerate...")
        
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json"
        )
        
        response = client.models.generate_content(
            model=model,
            contents=user_prompt,
            config=config
        )
        
        # 5. Parsing Hasil JSON
        json_data = json.loads(response.text)
        results = [(item['kompetensi'], item['definisi']) for item in json_data]
        
        df = pd.DataFrame(results, columns=['Nama Kompetensi', 'Definisi'])
        df.index = df.index + 1
        df.index.name = 'No.'
        
        return df

    except Exception as e:
        # Jika terjadi error API (misalnya Kuota Habis, Key Invalid)
        st.error(f"Terjadi kesalahan API (Kemungkinan Kuota Habis/Kunci Invalid): {e}. Beralih ke Simulasi Lokal.")
        return fuzzier_ai_mock(competency_list, BUSINESS_CONTEXT)


# --- FUNGSI UTAMA STREAMLIT (design st.page) ---
def main():
    st.set_page_config(layout="wide")
    st.title("🤖 Generator Definisi Kompetensi Teknis (AI-Powered)")
    st.subheader("Dilengkapi Fallback Otomatis Saat Kuota API Habis")
    st.markdown("---")

    # Input Area di Sidebar
    st.sidebar.header("⚙️ Input Kompetensi")
    st.sidebar.markdown("**Masukkan setiap kompetensi dalam baris terpisah (minimal 5 hingga 30 poin).**")
    
    # Contoh input
    default_input = """Administrasi dan Pengarsipan Dokumen (Penguasaan Filling Document)
Desain Komunikasi Visual dan Grafis (Adobe Illustrator, Photoshop, InDesign)
Manajemen & Evaluasi Vendor (Follow-up, Komunikasi, Perjanjian Kerjasama, Lead Time, Payment, Delivery, MOQ, Database Vendor, & Retur)
E-Faktur, E-Bupot (CORETAX)
Evaluasi Parameter Organoleptik (Warna, Bau, Tekstur, Dan Kritikal)
Sistem Manajemen Kualitas ISO 9001 (Audit Internal)
Manajemen Rantai Pasok (Supply Chain Management)
Penulisan Kode Program (Python, Go, Node.js)
Formulasi Kosmetik (Skincare)
Penanganan Pakan Ayam (Nutrisi dan Komposisi)
"""
    
    # Text area untuk input kompetensi
    competency_input = st.sidebar.text_area(
        "Daftar Kompetensi Teknis:", 
        value=default_input, 
        height=350
    )
    
    # Tombol Generate
    if st.sidebar.button("Generate Definisi Kompetensi"):
        if not competency_input.strip():
            st.error("Mohon masukkan setidaknya satu poin kompetensi.")
            return

        # Proses input menjadi list bersih
        competency_list = [
            item.strip() for item in competency_input.split('\n') if item.strip()
        ]

        if competency_list:
            df_generated = generate_definition_with_ai(competency_list)

            if not df_generated.empty:
                st.success("✅ Proses Generate Selesai.")
                
                # Tampilkan Hasil
                st.header("Hasil Definisi Kompetensi")
                st.dataframe(df_generated, use_container_width=True, height=500)

                # Download Button
                csv = df_generated.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="Unduh Data (.CSV)",
                    data=csv,
                    file_name='Definisi_Kompetensi_Teknis.csv',
                    mime='text/csv',
                    help="Unduh tabel hasil generate AI sebagai file CSV."
                )

# Jalankan Aplikasi
if __name__ == "__main__":
    main()