# Proyek Analisis Data Air Quality Dataset

## Struktur Direktori

```bash
submission/
│
├── dashboard/
│   ├── air_quality_map.html         # Peta kualitas udara berbasis folium
│   ├── cleaned_data.csv             # Data yang sudah dibersihkan untuk keperluan analisis
│   ├── dashboard.py                 # Aplikasi Streamlit
│   ├── main_data.csv                # Data utama untuk analisis
│
├── data/
│   ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
│   ├── PRSA_Data_Changping_20130301-20170228.csv
│   ├── PRSA_Data_Dingling_20130301-20170228.csv
│   ├── PRSA_Data_Dongsi_20130301-20170228.csv
│   ├── PRSA_Data_Guanyuan_20130301-20170228.csv
│   ├── PRSA_Data_Gucheng_20130301-20170228.csv
│   ├── PRSA_Data_Huairou_20130301-20170228.csv
│   ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
│   ├── PRSA_Data_Shunyi_20130301-20170228.csv
│   ├── PRSA_Data_Tiantan_20130301-20170228.csv
│   ├── PRSA_Data_Wanliu_20130301-20170228.csv
│   ├── PRSA_Data_Wanshouxigong_20130301-20170228.csv
│
├── Air-quality-dataset.zip            # Data mentah (terkompres)
├── Proyek_Analisis_Data.ipynb         # Notebook untuk EDA
├── README.md                          # Dokumentasi proyek
├── requirements.txt                   # Daftar library yang digunakan
├── url.txt                            # Daftar URL referensi yang digunakan

```

## Persiapan Environtment

1. Membuat Virtual Environment <br>
   Sebelum menjalankan proyek, pastikan Python 3.7+ sudah terinstal di sistem. Untuk menjaga agar dependensi tetap terisolasi, disarankan membuat virtual environment.

   Menggunakan venv:

   ```bash
   python -m venv env
   source env/bin/activate   # Di Mac/Linux
   .\env\Scripts\activate    # Di Windows
   ```

   Menggunakan conda:

   ```bash
   conda create --name air-quality-analysis python=3.8
   conda activate air-quality-analysis
   ```

2. Menginstal Dependensi <br>
   Setelah virtual environment aktif, instal semua dependensi dengan menjalankan perintah berikut:

   ```bash
   pip install -r requirements.txt
   ```

   Jika Anda tidak memiliki file requirements.txt, Anda dapat membuatnya sendiri dengan mencantumkan library berikut:

   ```bash
   pandas
   matplotlib
   seaborn
   folium
   streamlit
   streamlit-folium
   ```

   Atau

   ```bash
   pip install pandas matplotlib seaborn folium streamlit streamlit-folium
   ```

   Anda juga bisa membuat file requirements.txt secara otomatis dengan perintah:

   ```bash
   pip freeze > requirements.txt
   ```

3. Menjalankan Aplikasi <br>
   Untuk menjalankan aplikasi Streamlit, ikuti langkah berikut:
   - Pastikan Anda berada di direktori proyek.
   - Jalankan perintah berikut untuk menjalankan aplikasi:
     ```bash
     streamlit run submission/dashboard/dashboard.py
     ```
     atau
     ```bash
     python -m streamlit run submission/dashboard/dashboard.py
     ```
     Aplikasi akan berjalan di browser pada alamat http://localhost:8501.

## Data yang Digunakan

Proyek ini menggunakan data kualitas udara, data mencakup beberapa parameter polusi seperti PM2.5, PM10, SO2, NO2, CO, O3, dan variabel meteorologi lainnya seperti suhu, kelembapan, dan tekanan udara.

### Fitur Proyek

- Exploratory Data Analysis (EDA):
  Menyajikan analisis statistik deskriptif dan visualisasi distribusi polutan.
- Analisis Tren Polusi:
  Menganalisis dan memvisualisasikan tren PM2.5 dan PM10 di berbagai stasiun pengamatan dari tahun 2013 hingga 2017.
- Korelasi Faktor Meteorologi:
  Menganalisis hubungan antara variabel meteorologi (suhu, kelembapan, tekanan udara) dengan polusi udara.
- Analisis Geospasial:
  Menyajikan peta kualitas udara dari berbagai stasiun pengamatan menggunakan library Folium.
- Interaksi Dinamis dengan Streamlit:
  Aplikasi berbasis Streamlit yang interaktif, memungkinkan pengguna untuk mengeksplorasi data, visualisasi, dan hasil analisis secara langsung.

### Kontak

Jika ada pertanyaan atau masukan, silakan hubungi:

- Nama: Arya Setia Pratama
- Email: aryasetia30@gmail.com
- ID Dicoding: aryasetia30
