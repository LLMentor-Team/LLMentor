
import streamlit as st

def genera_piano_studio(df, settimane):
    st.write("Funzionalità di creazione piano di studio qui.")

def esporta_piano_pdf(df, settimane, file_name):
    pdf_path = "piano_di_studio.pdf"
    with open(pdf_path, "w") as f:
        f.write("Piano di studio per il file " + file_name)
    return pdf_path
