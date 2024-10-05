import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from streamlit_folium import folium_static

# Memuat data yang telah dibersihkan
cleaned_df = pd.read_csv('dashboard/cleaned_data.csv')

# Judul proyek
st.title("Proyek Analisis Data: Air-quality-dataset")

# Menampilkan identitas diri
st.write("### Identitas Diri")
st.write("- **Nama:** Arya Setia Pratama")
st.write("- **Email:** aryasetia30@gmail.com")
st.write("- **ID Dicoding:** aryasetia30")

# Menampilkan 10 baris pertama dari data
st.write("### 10 Baris Pertama dari Air Quality Dataset yang telah dibersihkan")
st.dataframe(cleaned_df.head(10))

# Exploratory Data Analysis (EDA)
st.write("## Exploratory Data Analysis (EDA)")

# Menghitung parameter statistik dasar
statistics_summary = cleaned_df.describe()
st.write("### Parameter Statistik dari Data")
st.write(statistics_summary)

# Visualisasi distribusi dengan histogram
st.subheader("Distribusi Polutan")
numeric_columns = cleaned_df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Membuat figure untuk histogram
num_plots = len(numeric_columns)
n_cols = 4
n_rows = (num_plots + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, n_rows * 3))

# Rata-rata subplot untuk menghindari akses ke subplot yang tidak ada
for i, column in enumerate(numeric_columns):
    ax = axes[i // n_cols, i % n_cols] if n_rows > 1 else axes[i % n_cols]
    sns.histplot(cleaned_df[column], kde=True, ax=ax)
    ax.set_title(f'Distribusi {column}')
    ax.set_xlabel(column)
    ax.set_ylabel('Frekuensi')

plt.tight_layout()
st.pyplot(fig)

# Menghitung dan menampilkan matriks korelasi
correlation_matrix = cleaned_df[numeric_columns].corr()
st.subheader('Matriks Korelasi')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True, ax=ax)
plt.title('Matriks Korelasi')
st.pyplot(fig)

# Pengelompokan Data
st.write("### Pengelompokan Data:")
grouped_by_station = cleaned_df.groupby('station')[numeric_columns].mean()
st.subheader("Rata-rata Polutan per Stasiun")
st.dataframe(grouped_by_station)

# Visualisasi rata-rata polutan per stasiun
st.subheader('Visualisasi Rata-rata Polutan per Stasiun')
fig, ax = plt.subplots(figsize=(12, 6))
grouped_by_station.plot(kind='bar', ax=ax)
ax.set_title('Rata-rata Polutan per Stasiun')
ax.set_xlabel('Stasiun')
ax.set_ylabel('Rata-rata Polutan')
ax.set_xticklabels(grouped_by_station.index, rotation=45)
ax.legend(title='Polutan')
st.pyplot(fig)

# Insight
st.write("### Insight")

# Insight tentang Korelasi
st.write("#### Korelasi Antara Variabel Meteorologi dan Polutan")
st.write(
    "Terdapat beberapa korelasi signifikan antara variabel meteorologi dan polutan. "
    "Salah satu yang paling mencolok adalah korelasi positif yang kuat antara suhu (TEMP) "
    "dan O3, dengan nilai 0.6, serta antara kelembapan (DEWP) dan O3, yang mencapai 0.31. "
    "Temuan ini menunjukkan bahwa peningkatan suhu dan kelembapan dapat berkontribusi terhadap "
    "peningkatan konsentrasi O3 di udara. Pengetahuan ini berpotensi dimanfaatkan untuk memprediksi "
    "kualitas udara berdasarkan data meteorologi, serta dapat mendukung perencanaan langkah-langkah "
    "mitigasi yang lebih efektif untuk mengurangi polusi udara pada kondisi cuaca tertentu."
)

# Insight tentang Variasi Kualitas Udara
st.write("#### Variasi Kualitas Udara Berdasarkan Stasiun")
st.write(
    "Dari analisis pola polutan, terlihat bahwa stasiun Dongsi memiliki tingkat polutan tertinggi "
    "untuk beberapa variabel, termasuk PM2.5 dan SO2. Sebaliknya, stasiun Dingling menunjukkan "
    "rata-rata polutan terendah untuk PM2.5, PM10, SO2, dan CO. Hal ini menandakan adanya perbedaan "
    "signifikan dalam kualitas udara antar lokasi, yang mungkin dipengaruhi oleh faktor-faktor lokal "
    "seperti aktivitas industri, kepadatan penduduk, atau kondisi geografis. Data ini sangat berharga "
    "untuk merencanakan intervensi dan kebijakan pengendalian polusi yang lebih tepat di daerah-daerah "
    "yang paling terpengaruh."
)

# Visualization & Explanatory Analysis
st.write("## Visualization & Explanatory Analysis")

# Pertanyaan 1
st.write("### Pertanyaan 1")
st.write("Bagaimana tren kualitas udara (PM2.5 dan PM10) di berbagai lokasi dari tahun 2013 hingga 2017?")

# Mengonversi kolom 'year', 'month', dan 'day' menjadi datetime
cleaned_df['date'] = pd.to_datetime(cleaned_df[['year', 'month', 'day']])

# Mengelompokkan data berdasarkan stasiun dan tahun
trends_df = cleaned_df.groupby(['station', cleaned_df['date'].dt.year])[['PM2.5', 'PM10']].mean().reset_index()

# Membuat grafik tren
st.subheader('Tren Kualitas Udara (PM2.5 dan PM10) di Berbagai Lokasi (2013-2017)')

plt.figure(figsize=(14, 8))

# Plot PM2.5 dengan marker
sns.lineplot(data=trends_df, x='date', y='PM2.5', hue='station', marker='o', palette='Set1', linestyle='-')
# Plot PM10 dengan marker dan gaya garis putus-putus
sns.lineplot(data=trends_df, x='date', y='PM10', hue='station', marker='x', palette='Set2', linestyle='--')

# Menambahkan elemen tambahan
plt.title('Tren Kualitas Udara (PM2.5 dan PM10)')
plt.xlabel('Tahun')
plt.ylabel('Konsentrasi (µg/m³)')
plt.legend(title='Stasiun')
plt.grid()

# Menampilkan grafik di Streamlit
st.pyplot(plt)

# Pertanyaan 2
st.write("### Pertanyaan 2")
st.write("Faktor meteorologi apa yang paling mempengaruhi konsentrasi polutan di berbagai kota?")

# Membuat heatmap untuk menunjukkan korelasi antara variabel meteorologi dan polutan
st.subheader('Korelasi antara Variabel Meteorologi dan Polutan')

correlation_matrix = cleaned_df[numeric_columns].corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Korelasi antara Variabel Meteorologi dan Polutan')

# Menampilkan heatmap di Streamlit
st.pyplot(plt)

# Pertanyaan 3
st.write("### Pertanyaan 3")
st.write("Apakah ada perbedaan signifikan dalam kualitas udara antara lokasi yang berbeda pada waktu-waktu tertentu?")

# Membuat boxplot untuk perbandingan kualitas udara berdasarkan lokasi
st.subheader('Distribusi Kualitas Udara PM2.5 Berdasarkan Bulan dan Lokasi')

plt.figure(figsize=(14, 8))
sns.boxplot(x='month', y='PM2.5', data=cleaned_df, hue='station')
plt.title('Distribusi Kualitas Udara PM2.5 Berdasarkan Bulan dan Lokasi')
plt.xlabel('Bulan')
plt.ylabel('Konsentrasi PM2.5 (µg/m³)')
plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid()

# Menampilkan boxplot di Streamlit
st.pyplot(plt)

# Judul insight
st.title("Insight Analisis Kualitas Udara")

# Insight 1
st.header("1. Tren Kualitas Udara (PM2.5 dan PM10) di Berbagai Lokasi (2013-2017)")
st.write(
    "Secara umum, kualitas udara di wilayah tersebut mengalami fluktuasi yang signifikan selama periode 2013 hingga 2017. "
    "Beberapa stasiun menunjukkan peningkatan konsentrasi partikulat, yang mengindikasikan penurunan kualitas udara. "
    "Namun, terdapat juga stasiun yang menunjukkan tren penurunan, menandakan adanya perbaikan kualitas udara."
)
st.write("Faktor-faktor yang mempengaruhi fluktuasi kualitas udara dapat berupa:")
st.markdown("- **Aktivitas Industri**")
st.markdown("- **Transportasi**")
st.markdown("- **Kondisi Meteorologi**")
st.markdown("- **Pembakaran Biomassa**")
st.markdown("- **Kebijakan Pemerintah**")

# Insight 2
st.header("2. Faktor Meteorologi yang Mempengaruhi Konsentrasi Polutan")
st.write(
    "Berdasarkan analisis, beberapa faktor meteorologi yang paling berpengaruh terhadap konsentrasi polutan di berbagai kota adalah:"
)
st.markdown("- **Suhu (TEMP)**  : Terdapat korelasi positif yang kuat antara suhu dan beberapa polutan seperti NO2 dan CO. Hal ini menunjukkan bahwa peningkatan suhu cenderung meningkatkan konsentrasi polutan tersebut.")
st.markdown("- **Tekanan (PRES)**  : Korelasi antara tekanan dan polutan bervariasi. Namun, terdapat korelasi negatif yang kuat antara tekanan dan konsentrasi O3, yang menunjukkan bahwa penurunan tekanan sering dikaitkan dengan peningkatan konsentrasi O3.")
st.markdown("- **Kelembaban (DEWP)**  : Kelembaban menunjukkan korelasi yang cukup kuat dengan polutan, terutama NO2 dan CO. Peningkatan kelembaban cenderung meningkatkan konsentrasi polutan tersebut.")
st.markdown("- **Kecepatan Angin (WSPM)**  : Secara umum, kecepatan angin memiliki korelasi negatif dengan sebagian besar polutan. Semakin tinggi kecepatan angin, semakin rendah konsentrasi polutan di udara, karena angin yang kencang membantu mendispersikan polutan.")

# Insight 3
st.header("3. Perbedaan Kualitas Udara antara Lokasi yang Berbeda pada Waktu Tertentu")
st.write(
    "Berdasarkan visualisasi boxplot, dapat disimpulkan bahwa terdapat perbedaan signifikan dalam kualitas udara antara berbagai lokasi pada waktu-waktu tertentu."
)
st.write("**Indikasi Perbedaan Signifikan:**")
st.markdown("- **Jangkauan Nilai** : Beberapa stasiun memiliki jangkauan nilai konsentrasi PM2.5 yang jauh lebih besar dibandingkan stasiun lainnya, menunjukkan adanya variasi yang signifikan dalam kualitas udara.")
st.markdown("- **Median yang Berbeda** : Median konsentrasi PM2.5 untuk setiap stasiun pada bulan yang sama sering kali berbeda secara signifikan, mengindikasikan bahwa tingkat polusi rata-rata di setiap lokasi tidak sama.")

# Analisis Lanjutan | Geospatial Analysis
st.write("## Analisis Lanjutan | Geospatial Analysis")

# Membuat DataFrame untuk koordinat stasiun
station_coordinates = {
    'station': [
        'Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
        'Gucheng', 'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan',
        'Wanliu', 'Wanshouxigong'
    ],
    'latitude': [
        39.973, 39.981, 39.965, 39.938, 39.913,
        39.911, 40.064, 39.879, 40.131, 39.883,
        39.964, 39.935
    ],
    'longitude': [
        116.413, 116.205, 116.239, 116.420, 116.274,
        116.318, 116.267, 116.329, 116.675, 116.471,
        116.329, 116.511
    ]
}

coordinates_df = pd.DataFrame(station_coordinates)

# Menghitung rata-rata polutan untuk setiap stasiun
average_pollutants = cleaned_df.groupby('station')[['PM2.5', 'PM10']].mean().reset_index()

# Menggabungkan dengan koordinat
combined_df = pd.merge(coordinates_df, average_pollutants, on='station')

# Membuat peta dengan pusat di lokasi rata-rata
map_center = [combined_df['latitude'].mean(), combined_df['longitude'].mean()]
map = folium.Map(location=map_center, zoom_start=10)

# Menambahkan marker untuk setiap stasiun
for index, row in combined_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=(f"<strong>{row['station']}</strong><br>"
               f"PM2.5: {row['PM2.5']:.2f} µg/m³<br>"
               f"PM10: {row['PM10']:.2f} µg/m³"),
        icon=folium.Icon(color='blue')
    ).add_to(map)

# Menampilkan peta di Streamlit
st.title("Peta Rata-rata Kualitas Udara di Berbagai Stasiun")
folium_static(map, width=700, height=500)

st.write("## Kesimpulan Analisis Kualitas Udara")

# Temuan Utama
st.write("### Temuan Utama")
st.write("#### 1. Rata-Rata Kualitas Udara:")
st.markdown("""
- Rata-rata konsentrasi PM2.5 dan PM10 menunjukkan variasi signifikan antar stasiun, dengan beberapa lokasi mengalami pencemaran yang lebih tinggi dibandingkan yang lain.
- Stasiun yang terletak di area perkotaan yang padat seperti **Dongsi** dan **Guanyuan** menunjukkan tingkat polusi udara yang lebih tinggi, dibandingkan dengan stasiun yang berada di area lebih terbuka seperti **Huairou** dan **Changping**.
""")

st.write("#### 2. Pengaruh Faktor Meteorologi:")
st.markdown("""
- Analisis menunjukkan bahwa kondisi meteorologi seperti suhu, kelembapan, dan curah hujan memiliki dampak signifikan terhadap konsentrasi polutan. Sebagai contoh, peningkatan suhu cenderung berhubungan dengan peningkatan konsentrasi PM2.5, menunjukkan potensi pembentukan ozon yang lebih tinggi di kondisi panas.
""")

st.write("#### 3. Perubahan Musiman:")
st.markdown("""
- Data menunjukkan pola musiman yang jelas dalam konsentrasi polutan, dengan tingkat polusi tertinggi terjadi selama musim dingin, kemungkinan disebabkan oleh peningkatan penggunaan pemanas yang mengeluarkan emisi polutan.
""")

st.write("#### 4. Jam Puncak Penggunaan:")
st.markdown("""
- Penggunaan kendaraan bermotor dan aktivitas industri memuncak pada jam tertentu, yang berkorelasi dengan peningkatan tingkat polusi di waktu-waktu tersebut, terutama pada pagi dan sore hari.
""")

# Interpretasi
st.write("### Interpretasi")
st.markdown("""
Temuan ini menunjukkan bahwa kualitas udara dipengaruhi oleh berbagai faktor yang saling terkait, termasuk aktivitas manusia dan kondisi lingkungan. Tingginya konsentrasi polutan di daerah perkotaan dapat dihubungkan dengan kepadatan lalu lintas dan aktivitas industri, sedangkan faktor meteorologi memberikan konteks yang penting untuk memahami fluktuasi dalam data kualitas udara.
""")

# Rekomendasi
st.write("### Rekomendasi")
st.write("#### 1. Kebijakan Pengendalian Polusi:")
st.markdown("""
- Diperlukan kebijakan yang lebih ketat untuk mengendalikan emisi dari kendaraan bermotor dan industri, terutama di daerah yang teridentifikasi dengan tingkat polusi tinggi.
- Penetapan zona rendah emisi di area perkotaan dapat membantu mengurangi paparan polutan bagi penduduk.
""")

st.write("#### 2. Program Kesadaran Lingkungan:")
st.markdown("""
- Meluncurkan program kesadaran publik mengenai pentingnya menjaga kualitas udara dan cara mengurangi emisi, seperti menggunakan transportasi umum atau kendaraan ramah lingkungan.
""")

st.write("#### 3. Penggunaan Teknologi untuk Pemantauan:")
st.markdown("""
- Meningkatkan pemantauan kualitas udara dengan teknologi sensor yang lebih canggih di lokasi-lokasi yang kritis untuk memberikan data real-time kepada masyarakat dan pemerintah.
""")

st.write("#### 4. Riset Lanjutan:")
st.markdown("""
- Melakukan penelitian lebih lanjut mengenai dampak kesehatan dari paparan jangka panjang terhadap polutan tertentu, untuk mendukung pengembangan kebijakan berbasis bukti.
""")

# Kesimpulan Akhir
st.write("### Kesimpulan Akhir")
st.markdown("""
Secara keseluruhan, analisis ini memberikan wawasan yang berharga mengenai pola kualitas udara di berbagai lokasi, serta faktor-faktor yang mempengaruhinya. Dengan menerapkan rekomendasi yang dihasilkan dari analisis ini, diharapkan kualitas udara dapat diperbaiki, yang pada akhirnya akan meningkatkan kesehatan masyarakat dan kualitas hidup secara keseluruhan.
""")
