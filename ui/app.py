import streamlit as st
import pandas as pd

st.title("📊 Análisis de Reclamos - SUSALUD")
st.sidebar.header("Opciones")

df = pd.read_csv("data/processed/reclamos_clean.csv")
st.write("Vista previa de los datos", df.head())

if st.button("Mostrar Distribución de Reclamos"):
    st.bar_chart(df["AÑO"].value_counts())