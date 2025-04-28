
import streamlit as st
from modules.data_loader import carica_syllabus
from modules.piano_studio import genera_piano_studio, esporta_piano_pdf
from modules.quiz_module import esegui_quiz
from modules.llm_agent import fai_domanda
import os

# Configurazione iniziale della pagina
st.set_page_config(page_title="LLMentor", layout="wide")

# Sidebar di navigazione
st.sidebar.title("LLMentor")
pagina = st.sidebar.radio("Vai a:", ["Home", "Carica File", "Genera Quiz", "Riassunto/Spiegazione", "Info Progetto"])

# Contenuto principale in base alla selezione
if pagina == "Home":
    st.title("👩‍🏫 LLMentor – AI Tutor Universitario")
    st.write(
        "Benvenuto in LLMentor, la piattaforma intelligente per supportare lo studio universitario."
    )

elif pagina == "Carica File":
    st.title("Carica i tuoi materiali di studio")
    st.write("Carica un file CSV con il syllabus o i dati di studio.")

    uploaded_file = st.file_uploader("Carica un file CSV", type=["csv"])

    if uploaded_file is not None:
        # Salva il file caricato nella cartella 'data'
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Carica il file salvato usando carica_syllabus
        df = carica_syllabus(uploaded_file.name)
        
        if not df.empty:
            st.session_state["syllabus_df"] = df
            st.success(f"File **{uploaded_file.name}** caricato e letto con successo!")
            st.dataframe(df)  # Mostra una preview dei dati caricati
        else:
            st.error("Errore nel caricamento del file. Assicurati che sia un file CSV valido.")

elif pagina == "Genera Quiz":
    st.title("Genera Quiz")
    esegui_quiz()

elif pagina == "Riassunto/Spiegazione":
    st.title("Ottieni Riassunti e Spiegazioni")

    domanda = st.text_input("Fai una domanda all'AI:")
    if domanda:
        try:
            risposta = fai_domanda(domanda)
            st.success(risposta)
        except Exception as e:
            st.error(f"Errore durante la generazione della risposta: {e}")

elif pagina == "Info Progetto":
    st.title("Info Progetto")
    st.markdown("""
    **LLMentor** è una Web App creata durante il Bootcamp AI di Edgemony.
    
    Permette di:
    - Caricare materiali di studio
    - Generare quiz automatici
    - Ricevere riassunti e spiegazioni tramite AI

    **Team di sviluppo:** LLMentor.
    """)
