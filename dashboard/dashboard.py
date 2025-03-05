import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    file_path = "dashboard/all_clean_data.csv"
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df[["year", "month", "day", "hour"]].astype(str).agg('-'.join, axis=1), format="%Y-%m-%d-%H")
    return df

df = load_data()

# Clustering manual berdasarkan kuartil
df["pollution_category"] = pd.qcut(df["combined_pollution"], q=3, labels=["Baik", "Sedang", "Buruk"], duplicates='drop')

# Sidebar
st.sidebar.title("Dashboard Kualitas Udara")
selected_page = st.sidebar.radio("Pilih Halaman", ["Rata-rata Polusi per Jam", "Rata-rata Polusi per Lokasi"])

if selected_page == "Rata-rata Polusi per Jam":
    selected_station = st.sidebar.selectbox("Pilih Lokasi", df["station"].unique())
    min_date, max_date = df["date"].min().date(), df["date"].max().date()
    start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)
    
    df_filtered = df[(df["station"] == selected_station) & (df["date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))]
    
    st.title("Analisis Kualitas Udara")
    st.subheader("Rata-rata Polusi Gabungan per Jam")
    avg_pollution_by_hour = df_filtered.groupby(df_filtered["date"].dt.hour)["combined_pollution"].mean()
    
    fig, ax = plt.subplots()
    sns.lineplot(x=avg_pollution_by_hour.index, y=avg_pollution_by_hour.values, marker="o", color="red", ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Polusi Gabungan")
    st.pyplot(fig)

elif selected_page == "Rata-rata Polusi per Lokasi":
    st.title("Rata-rata Polusi Gabungan per Lokasi")
    avg_pollution_by_station = df.groupby("station")["combined_pollution"].mean().sort_values()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=avg_pollution_by_station.index, x=avg_pollution_by_station.values, palette="coolwarm", ax=ax)
    ax.set_xlabel("Polusi Gabungan")
    st.pyplot(fig)
