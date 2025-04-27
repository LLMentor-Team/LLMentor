import streamlit as st
from llm_agent import fai_domanda

st.set_page_config(page_title="LLMentor", layout="wide")

st.sidebar.title("LLMentor")
pagina = st.sidebar.radio("Vai a:", ["Home", "Carica File", "Genera Quiz", "Riassunto/Spiegazione", "Info Progetto"])

if pagina == "Home":
    st.title("👩‍🏫 LLMentor – AI Tutor Universitario")
    st.write("Benvenuto nella piattaforma intelligente per supportare lo studio universitario.")

elif pagina == "Carica File":
    st.title("Carica i tuoi materiali di studio")
    st.write("Syllabus, appunti o testi da cui generare quiz o riassunti.")
    st.file_uploader("Carica un file", type=["pdf", "docx", "txt"])

elif pagina == "Genera Quiz":
    st.title("Genera Quiz Interattivi")
    st.write("Dopo aver caricato un file, puoi generare quiz per esercitarti.")

elif pagina == "Riassunto/Spiegazione":
    st.title("Ottieni Riassunti e Spiegazioni")
    st.write("L'AI ti aiuta a comprendere meglio i concetti chiave.")

    domanda_utente = st.text_input("Scrivi qui la tua domanda o un concetto che vuoi approfondire:")

    if st.button("Invia"):
        if domanda_utente:
            with st.spinner("Sto elaborando la risposta..."):
                risposta = fai_domanda(domanda_utente)
            st.success("Ecco la spiegazione:")
            st.markdown(f"> {risposta}")
        else:
            st.warning("Inserisci una domanda prima di cliccare.")

elif pagina == "Info Progetto":
    st.title("Info Progetto")
    st.markdown("""
    **LLMentor** è una Web App creata durante il Bootcamp AI di Edgemony.  
    Permette di caricare materiali, generare quiz e ricevere tutoring automatico.  
    Sviluppato dal team LLMentor.
    """)
