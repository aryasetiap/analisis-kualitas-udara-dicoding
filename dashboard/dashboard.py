import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import numpy as np
import streamlit as st
from streamlit_folium import folium_static

# Judul aplikasi
st.title("Air Quality Dataset")

# Data diri
st.write("**=================================**")
st.write("**Nama:** Arya Setia Pratama")
st.write("**Email:** aryasetia30@gmail.com")
st.write("**ID Dicoding:** aryasetia30")
st.write("**=================================**")

# Path ke folder data
path = 'data/'  # Path ke folder data
all_files = glob.glob(path + "*.csv")  # Mengambil semua file CSV dalam folder

# List untuk menyimpan DataFrame
dataframes = []

for filename in all_files:
    # Membaca file CSV
    df = pd.read_csv(filename)
    dataframes.append(df)

# Menggabungkan semua DataFrame menjadi satu
combined_data = pd.concat(dataframes, ignore_index=True)

# Mendefinisikan kolom yang akan digunakan untuk analisis
columns_to_use = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO',
                  'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

# Menyimpan hasil gabungan ke dalam file CSV
combined_data.to_csv('dashboard/main_data.csv', index=False)
st.write("Data berhasil digabungkan dan disimpan ke main_data.csv")

# Menampilkan beberapa baris awal dari dataset yang baru dibentuk
st.write("Beberapa baris awal dari main_data.csv:")
st.dataframe(combined_data.head())  # Menampilkan 5 baris pertama

# Assessing Missing Value
missing_values_count = combined_data.isnull().sum()
missing_values_percentage = (missing_values_count / len(combined_data)) * 100
missing_values_df = pd.DataFrame({
    'Jumlah Missing Values': missing_values_count,
    'Persentase Missing Values (%)': missing_values_percentage
})
st.write("Analisis Missing Values:")
st.dataframe(missing_values_df)

# Assessing invalid values pada kolom polutan
invalid_counts = {}
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
for pollutant in pollutants:
    invalid_counts[pollutant] = combined_data[pollutant] < 0

# Assessing invalid values pada kolom (TEMP) dan kelembapan (DEWP)
invalid_counts['TEMP'] = (combined_data['TEMP'] < -
                          50) | (combined_data['TEMP'] > 50)
invalid_counts['DEWP'] = (combined_data['DEWP'] < -
                          50) | (combined_data['DEWP'] > 100)

# Hitung jumlah invalid values per kolom
invalid_values_count = {key: value.sum()
                        for key, value in invalid_counts.items()}
invalid_values_df = pd.DataFrame(
    {'Jumlah Invalid Values': invalid_values_count})
st.write("Analisis Invalid Values:")
st.dataframe(invalid_values_df)

# Cek baris duplikat
duplicate_rows = combined_data[combined_data.duplicated()]
st.write(f"Jumlah baris duplikat: {duplicate_rows.shape[0]}")
if not duplicate_rows.empty:
    st.write("Contoh baris duplikat:")
    st.dataframe(duplicate_rows.head())

# Deteksi outlier dengan metode IQR
columns_to_check = ['PM2.5', 'PM10', 'SO2', 'NO2',
                    'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
outliers_count = {}
for column in columns_to_check:
    Q1 = combined_data[column].quantile(0.25)
    Q3 = combined_data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = combined_data[(combined_data[column] < lower_bound) | (
        combined_data[column] > upper_bound)]
    outliers_count[column] = outliers.shape[0]

outliers_df = pd.DataFrame(list(outliers_count.items()), columns=[
                           'Kolom', 'Jumlah Outlier'])
st.write("Jumlah Outlier per Kolom (Metode IQR):")
st.dataframe(outliers_df)

# Imputasi nilai missing values
combined_data['PM2.5'].fillna(combined_data['PM2.5'].median(), inplace=True)
combined_data['PM10'].fillna(combined_data['PM10'].median(), inplace=True)
combined_data['SO2'].fillna(combined_data['SO2'].median(), inplace=True)
combined_data['NO2'].fillna(combined_data['NO2'].median(), inplace=True)
combined_data['CO'].fillna(combined_data['CO'].median(), inplace=True)
combined_data['O3'].fillna(combined_data['O3'].median(), inplace=True)
combined_data['TEMP'].fillna(combined_data['TEMP'].mean(), inplace=True)
combined_data['PRES'].fillna(combined_data['PRES'].mean(), inplace=True)
combined_data['DEWP'].fillna(combined_data['DEWP'].mean(), inplace=True)
combined_data['RAIN'].fillna(0, inplace=True)
combined_data['wd'].fillna(combined_data['wd'].mode()[0], inplace=True)
combined_data['WSPM'].fillna(combined_data['WSPM'].median(), inplace=True)

st.write("Informasi dataset setelah imputasi missing values:")
st.write(combined_data.info())

# Capping outlier berdasarkan persentil 5 dan 95


def cap_outliers(df, column):
    batas_bawah = df[column].quantile(0.05)
    batas_atas = df[column].quantile(0.95)
    df[column] = df[column].clip(lower=batas_bawah, upper=batas_atas)
    return batas_bawah, batas_atas


kolom_yang_dicheck = ['PM2.5', 'PM10', 'SO2', 'NO2',
                      'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
for kolom in kolom_yang_dicheck:
    cap_outliers(combined_data, kolom)

st.write("Outlier telah di-capping:")
st.write(combined_data.describe())

# Visualisasi histogram untuk setiap kolom
st.subheader("Histogram untuk Setiap Kolom")
fig, ax = plt.subplots(figsize=(15, 10))
combined_data.hist(bins=30, ax=ax)
st.pyplot(fig)

# Boxplot untuk kolom polutan dan data meteorologi
st.subheader("Boxplot Polutan dan Data Meteorologi")
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=combined_data[['PM2.5', 'PM10', 'SO2', 'NO2',
            'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']], ax=ax)
plt.xticks(rotation=45)
plt.title('Boxplot Polutan dan Data Meteorologi')
st.pyplot(fig)

# Visualisasi matriks korelasi
st.subheader("Matriks Korelasi")
correlation_matrix = combined_data[columns_to_use].corr()
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
plt.title('Matriks Korelasi')
st.pyplot(fig)

# Analisis tren kualitas udara berdasarkan waktu
combined_data['date'] = pd.to_datetime(
    combined_data[['year', 'month', 'day', 'hour']])
trend_pm25 = combined_data.groupby(
    'date')['PM2.5'].mean().reset_index()  # Add this line
trend_pm10 = combined_data.groupby('date')['PM10'].mean().reset_index()
trend_so2 = combined_data.groupby('date')['SO2'].mean().reset_index()
trend_no2 = combined_data.groupby('date')['NO2'].mean().reset_index()
trend_co = combined_data.groupby('date')['CO'].mean().reset_index()
trend_o3 = combined_data.groupby('date')['O3'].mean().reset_index()

st.subheader("Tren Kualitas Udara dari Waktu ke Waktu")
fig, axs = plt.subplots(3, 2, figsize=(14, 10))
axs[0, 0].plot(trend_pm25['date'], trend_pm25['PM2.5'],
               color='blue')  # Add this line
axs[0, 0].set_title('Tren PM2.5 dari Waktu ke Waktu')  # Add this line
axs[0, 0].grid()

axs[0, 1].plot(trend_pm10['date'], trend_pm10['PM10'], color='orange')
axs[0, 1].set_title('Tren PM10 dari Waktu ke Waktu')
axs[0, 1].grid()

axs[1, 0].plot(trend_so2['date'], trend_so2['SO2'], color='red')
axs[1, 0].set_title('Tren SO2 dari Waktu ke Waktu')
axs[1, 0].grid()

axs[1, 1].plot(trend_no2['date'], trend_no2['NO2'], color='green')
axs[1, 1].set_title('Tren NO2 dari Waktu ke Waktu')
axs[1, 1].grid()

axs[2, 0].plot(trend_co['date'], trend_co['CO'], color='blue')
axs[2, 0].set_title('Tren CO dari Waktu ke Waktu')
axs[2, 0].grid()

axs[2, 1].plot(trend_o3['date'], trend_o3['O3'], color='purple')
axs[2, 1].set_title('Tren O3 dari Waktu ke Waktu')
axs[2, 1].grid()

plt.tight_layout()
st.pyplot(fig)

# Visualisasi perbandingan kualitas udara antar lokasi
st.subheader("Distribusi Kualitas Udara Antar Lokasi")
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

sns.boxplot(x='station', y='PM10', data=combined_data, ax=axs[0])
axs[0].set_title('Distribusi PM10 per Lokasi')
axs[0].tick_params(axis='x', rotation=45)

sns.boxplot(x='station', y='NO2', data=combined_data, ax=axs[1])
axs[1].set_title('Distribusi NO2 per Lokasi')
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

# Visualisasi peta kualitas udara
st.subheader("Peta Kualitas Udara")

# Data koordinat stasiun
station_coords = {
    'Aotizhongxin': {'lat': 39.978, 'lon': 116.407},
    'Changping': {'lat': 40.217, 'lon': 116.235},
    'Dingling': {'lat': 40.292, 'lon': 116.227},
    'Dongsi': {'lat': 39.93, 'lon': 116.42},
    'Guanyuan': {'lat': 39.929, 'lon': 116.344},
    'Gucheng': {'lat': 39.914, 'lon': 116.184},
    'Huairou': {'lat': 40.375, 'lon': 116.628},
    'Nongzhanguan': {'lat': 39.934, 'lon': 116.455},
    'Shunyi': {'lat': 40.127, 'lon': 116.655},
    'Tiantan': {'lat': 39.886, 'lon': 116.414},
    'Wanliu': {'lat': 39.997, 'lon': 116.304},
    'Wanshouxigong': {'lat': 39.878, 'lon': 116.339},
}

# Buat peta
m = folium.Map(location=[39.9042, 116.4074], zoom_start=10)

# Menambahkan marker untuk setiap stasiun
for station, coords in station_coords.items():
    # Menghitung rata-rata PM2.5 untuk setiap stasiun
    avg_pm25 = combined_data[combined_data['station']
                             == station]['PM2.5'].mean()

    # Menentukan warna marker berdasarkan tingkat PM2.5
    if avg_pm25 < 50:
        color = 'green'
    elif avg_pm25 < 100:
        color = 'yellow'
    elif avg_pm25 < 150:
        color = 'orange'
    else:
        color = 'red'

    # Menambahkan marker ke peta
    folium.Marker(
        [coords['lat'], coords['lon']],
        popup=f"{station}: {avg_pm25:.2f} µg/m³",
        icon=folium.Icon(color=color)
    ).add_to(m)

# Menampilkan peta di Streamlit
folium_static(m)

# Kesimpulan
st.header("Kesimpulan")

st.write("**=================================**")
# Pertanyaan 1
st.write("**Kesimpulan Pertanyaan 1:**")
st.write("Kualitas udara di berbagai lokasi mengalami fluktuasi "
         "signifikan dari waktu ke waktu. Pola musiman terlihat jelas, "
         "dengan peningkatan konsentrasi polutan pada musim tertentu, "
         "seperti musim kemarau. Beberapa lokasi menunjukkan tren "
         "peningkatan konsentrasi polutan dari tahun ke tahun, yang "
         "mungkin disebabkan oleh peningkatan aktivitas yang "
         "menghasilkan polusi.")
st.write("**=================================**")
# Pertanyaan 2
st.write("**Kesimpulan Pertanyaan 2:**")
st.write("Hubungan antara konsentrasi PM2.5 dan PM10 dengan faktor "
         "meteorologi seperti suhu, kelembapan, dan curah hujan tidak "
         "bersifat linear atau sederhana. Faktor meteorologi hanya satu "
         "dari banyak faktor yang memengaruhi kualitas udara, dengan "
         "emisi dari aktivitas manusia juga memainkan peran penting. "
         "Terbatasnya data pada kondisi tertentu (seperti cuaca kering) "
         "membuat sulit untuk menyimpulkan hubungan yang kuat antara "
         "variabel-variabel ini.")
st.write("**=================================**")
# Pertanyaan 3
st.write("**Kesimpulan Pertanyaan 3:**")
st.write("Kualitas udara bervariasi secara signifikan antar lokasi, "
         "dipengaruhi oleh faktor-faktor lokal seperti aktivitas "
         "industri, kepadatan penduduk, dan kondisi geografis. Adanya "
         "nilai outlier mengindikasikan adanya kejadian khusus yang "
         "menyebabkan lonjakan konsentrasi polutan di beberapa lokasi.")
st.write("**=================================**")
