import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Mengatur gaya seaborn
sns.set(style='dark')

def create_daily_usage_df(df):
    daily_usage_df = df.resample(rule='D', on='dteday').agg({
        "cnt_x": "sum"  # Menggunakan 'cnt_x' sesuai dengan data Anda
    })
    daily_usage_df = daily_usage_df.reset_index()
    daily_usage_df.rename(columns={"cnt_x": "total_rentals"}, inplace=True)
    return daily_usage_df

def create_by_weather_df(df):
    by_weather_df = df.groupby(by="weathersit_x").cnt_x.sum().reset_index()  # Menggunakan 'weathersit_x' dan 'cnt_x'
    by_weather_df.rename(columns={"cnt_x": "total_rentals"}, inplace=True)
    return by_weather_df

def create_by_month_df(df):
    by_month_df = df.groupby(by="mnth_x").cnt_x.sum().reset_index()  # Menggunakan 'mnth_x' dan 'cnt_x'
    by_month_df.rename(columns={"cnt_x": "total_rentals"}, inplace=True)
    return by_month_df

def create_by_weekday_df(df):
    by_weekday_df = df.groupby(by="weekday_x").cnt_x.sum().reset_index()  # Menggunakan 'weekday_x' dan 'cnt_x'
    by_weekday_df.rename(columns={"cnt_x": "total_rentals"}, inplace=True)
    return by_weekday_df

# Membaca data dari CSV
all_df = pd.read_csv("dashboard/all_data.csv")

# Mengonversi kolom tanggal menjadi datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Mengambil rentang tanggal minimum dan maksimum
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("assets/images.jpeg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Mengfilter data berdasarkan rentang waktu
main_df = all_df[(all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))]

# Membuat DataFrame berdasarkan analisis
daily_usage_df = create_daily_usage_df(main_df)
by_weather_df = create_by_weather_df(main_df)
by_month_df = create_by_month_df(main_df)
by_weekday_df = create_by_weekday_df(main_df)

# Judul Dashboard
st.header('Bike Sharing :sparkles:')

# Total Rentals
col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_usage_df.total_rentals.sum()
    st.metric("Total Rentals", value=total_rentals)

# Visualisasi Penggunaan Harian
with col2:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily_usage_df["dteday"], daily_usage_df["total_rentals"], marker='o', color="#90CAF9")
    ax.set_title('Total Penggunaan Sepeda Harian', fontsize=20)
    ax.set_xlabel('Tanggal', fontsize=15)
    ax.set_ylabel('Jumlah Pengguna', fontsize=15)
    st.pyplot(fig)

# Visualisasi berdasarkan cuaca
st.subheader("Penggunaan Sepeda Berdasarkan Kondisi Cuaca")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weathersit_x", y="total_rentals", data=by_weather_df, ax=ax)
ax.set_title('Jumlah Pengguna Berdasarkan Cuaca', fontsize=20)
ax.set_xlabel('Kondisi Cuaca (1 = Clear, 2 = Mist, 3 = Light Snow/Rain)', fontsize=15)
ax.set_ylabel('Jumlah Pengguna', fontsize=15)
st.pyplot(fig)

# Visualisasi berdasarkan bulan
st.subheader("Penggunaan Sepeda Berdasarkan Bulan")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="mnth_x", y="total_rentals", data=by_month_df, ax=ax)
ax.set_title('Jumlah Pengguna Berdasarkan Bulan', fontsize=20)
ax.set_xlabel('Bulan', fontsize=15)
ax.set_ylabel('Jumlah Pengguna', fontsize=15)
st.pyplot(fig)

# Visualisasi berdasarkan hari dalam seminggu
st.subheader("Penggunaan Sepeda Berdasarkan Hari dalam Minggu")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weekday_x", y="total_rentals", data=by_weekday_df, ax=ax)
ax.set_title('Jumlah Pengguna Berdasarkan Hari dalam Minggu', fontsize=20)
ax.set_xlabel('Hari dalam Minggu', fontsize=15)
ax.set_ylabel('Jumlah Pengguna', fontsize=15)
st.pyplot(fig)

st.caption('Copyright (c) 2024')
