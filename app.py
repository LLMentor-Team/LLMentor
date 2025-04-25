import streamlit as st
from modules.data_loader import carica_syllabus
from modules.piano_studio import genera_piano_studio
import os

st.set_page_config(page_title="LLMentor", layout="wide")
st.title("LLMentor - Timeline Studio")

st.header("Scegli il syllabus")
files = ["economia_politica.csv", "economia_gestione_imprese.csv"]
selected = st.selectbox("Scegli un file:", files)

df = carica_syllabus(selected)
if not df.empty:
    st.dataframe(df)

    st.header("Crea un piano di studio personalizzato")
    settimane = st.number_input("In quante settimane vuoi prepararti?", min_value=1, max_value=20, value=4)
    if st.button("Genera piano"):
        genera_piano_studio(df, settimane)
