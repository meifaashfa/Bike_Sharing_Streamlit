import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set up for better display
sns.set_style("whitegrid")

# Load dataset
df = pd.read_csv("main_data.csv", parse_dates=['dteday'])

# ========== SIDEBAR ==========
st.sidebar.title("Dashboard Peminjaman Sepeda")
st.sidebar.markdown("""
    Aplikasi ini untuk menganalisis pengaruh **Musim**, **Cuaca**, dan **Waktu** terhadap *Peminjaman Sepeda*.
""")

# Filter Tanggal
st.sidebar.title("Filter Data")
min_date = df['dteday'].min()
max_date = df['dteday'].max()
start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Terapkan filter tanggal ke dataframe
filtered_df = df[
    (df['dteday'] >= pd.to_datetime(start_date)) &
    (df['dteday'] <= pd.to_datetime(end_date))
]

# Pilihan Analisis
menu = st.sidebar.selectbox("Pilih Analisis", ["Distribusi Peminjaman", "Musim & Cuaca", "Jam Sibuk", "Clustering (Binning)"])

# ========== VISUALISASI ==========
st.title("Analisis Peminjaman Sepeda Berdasarkan Musim, Cuaca, dan Waktu")

if menu == "Distribusi Peminjaman":
    st.write("### Distribusi Jumlah Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10,5))
    sns.histplot(filtered_df["cnt"], bins=30, kde=True, color="blue", ax=ax)
    ax.set_title("Distribusi Peminjaman Sepeda")
    ax.set_xlabel("Jumlah Peminjaman")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)

elif menu == "Musim & Cuaca":
    # Musim
    st.write("### Pengaruh Musim terhadap Peminjaman Sepeda")
    seasonal_count = filtered_df.groupby("season")["cnt"].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=seasonal_count, x="season", y="cnt", palette="coolwarm", ax=ax, errorbar=None)
    ax.set_title(f"Total Peminjaman Sepeda Berdasarkan Musim ({start_date} hingga {end_date})")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Peminjaman")
    st.pyplot(fig)

    # Cuaca
    st.write("### Pengaruh Cuaca terhadap Peminjaman Sepeda")
    weather_count = filtered_df.groupby("weathersit")["cnt"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=weather_count, x="weathersit", y="cnt", palette="Blues", ax=ax, errorbar=None)
    ax.set_title("Total Peminjaman Sepeda Berdasarkan Cuaca")
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Total Peminjaman")
    st.pyplot(fig)

elif menu == "Jam Sibuk":
    st.write("### Tren Peminjaman Sepeda Berdasarkan Jam")
    hourly_count = filtered_df.groupby("hr")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=hourly_count, x="hr", y="cnt", marker="o", color="red", ax=ax)
    ax.set_title("Tren Peminjaman Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Peminjaman")
    st.pyplot(fig)

elif menu == "Clustering (Binning)":
    st.write("### Binning data numerik ke dalam interval kategori")

    # Fungsi binning
    def binning(col, bins, labels):
        return pd.cut(col, bins=bins, labels=labels, include_lowest=True)

    # Binning untuk 'hr'
    filtered_df['hr_bin'] = binning(filtered_df['hr'], bins=[0, 5, 11, 17, 23], labels=['Malam', 'Pagi', 'Siang', 'Sore/Malam'])

    # Binning untuk 'temp'
    filtered_df['temp_bin'] = binning(filtered_df['temp'], bins=[-float('inf'), 10, 20, float('inf')], labels=['Dingin', 'Sedang', 'Hangat'])

    # Binning untuk 'hum'
    filtered_df['hum_bin'] = binning(filtered_df['hum'], bins=[-float('inf'), 50, 75, float('inf')], labels=['Rendah', 'Sedang', 'Tinggi'])

    # Binning untuk 'windspeed'
    filtered_df['windspeed_bin'] = binning(filtered_df['windspeed'], bins=[-float('inf'), 5, 15, float('inf')], labels=['Tenang', 'Sedang', 'Kencang'])

    # Binning untuk 'cnt'
    filtered_df['cnt_bin'] = binning(filtered_df['cnt'], bins=[-float('inf'), 10, 30, float('inf')], labels=['Rendah', 'Sedang', 'Tinggi'])

    # Tampilkan hasil
    st.write("#### Hasil Binning (5 Baris Pertama)")
    st.dataframe(filtered_df[['hr', 'hr_bin', 'temp', 'temp_bin', 'hum', 'hum_bin', 
                              'windspeed', 'windspeed_bin', 'cnt', 'cnt_bin']].head())
    
    # Visualisasi distribusi bin
    st.write("#### Distribusi Binning")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Distribusi Jam**")
        st.bar_chart(filtered_df['hr_bin'].value_counts())
        
        st.write("**Distribusi Suhu**")
        st.bar_chart(filtered_df['temp_bin'].value_counts())
    
    with col2:
        st.write("**Distribusi Kelembapan**")
        st.bar_chart(filtered_df['hum_bin'].value_counts())
        
        st.write("**Distribusi Rental**")
        st.bar_chart(filtered_df['cnt_bin'].value_counts())
    
    with col3:
        st.write("**Distribusi Kecepatan Angin**")
        st.bar_chart(filtered_df['windspeed_bin'].value_counts())