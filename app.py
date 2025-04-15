import streamlit as st
from modules.data_loader import carica_syllabus, filtra_per_modulo

st.set_page_config(page_title="LLMentor", layout="wide")

st.title("📘 LLMentor – Visualizzatore Syllabus")

df = carica_syllabus()

if df.empty:
    st.warning("⚠️ Nessun dato trovato.")
else:
    modulo = st.selectbox("Filtra per modulo", ["Tutti", "Microeconomia", "Macroeconomia"])
    if modulo != "Tutti":
        df = filtra_per_modulo(df, modulo)
    st.dataframe(df)
