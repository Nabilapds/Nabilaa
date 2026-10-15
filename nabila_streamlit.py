import pandas as pd
import streamlit as st

st.title("Dashboard Saya")

# Membaca data dari file CSV terpisah
df = pd.read_csv("data.csv")

# Menampilkan data ke Streamlit
st.dataframe(df)
