import streamlit as st
from modules.data_loader import carica_syllabus
from modules.piano_studio import genera_piano_studio, esporta_piano_pdf
from modules.quiz_module import esegui_quiz
from llm_agent import fai_domanda
import os

st.set_page_config(page_title="LLMentor", layout="wide")

st.sidebar.title("LLMentor")
pagina = st.sidebar.radio("Vai a:", ["Home", "Carica File", "Piano di Studio", "Genera Quiz", "Riassunto/Spiegazione", "Info Progetto"])

if pagina == "Home":
    st.title("👩‍🏫 LLMentor – AI Tutor Universitario")
    st.write("Benvenuto nella piattaforma intelligente per supportare lo studio universitario.")

elif pagina == "Carica File": 
    st.title("Carica i tuoi materiali di studio") 
    st.write("Syllabus, appunti o testi da cui generare quiz o riassunti.") 
    file = st.file_uploader("Carica un file", type=["pdf", "docx", "txt", "csv"]) 
    if file: 
        st.session_state.file_name = file.name 
        st.session_state.file_bytes = file.getvalue() 
        st.success(f"File {file.name} caricato correttamente!")

elif pagina == "Genera Quiz": 
    from modules.quiz_module import esegui_quiz 
    esegui_quiz()

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

elif pagina == "Piano di Studio":
    st.title("Crea il tuo Piano di Studio")

    files = ["economia_politica.csv", "economia_gestione_imprese.csv"]
    selected = st.selectbox("Scegli un file:", files)

    df = carica_syllabus(selected)
    if not df.empty:
        st.dataframe(df)

        settimane = st.number_input("In quante settimane vuoi prepararti?", min_value=1, max_value=20, value=4)

        if st.button("Genera Piano di Studio"):
            df.columns = df.columns.str.strip().str.lower()
            genera_piano_studio(df, settimane)

            pdf_path = esporta_piano_pdf(df, settimane)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Scarica il piano di studio in PDF",
                    data=f.read(),
                    file_name="piano_di_studio.pdf",
                    mime="application/pdf"
                )

elif pagina == "Info Progetto":
    st.title("Info Progetto")
    st.markdown("""
    **LLMentor** è una Web App creata durante il Bootcamp AI di Edgemony.  
    Permette di caricare materiali, generare quiz e ricevere tutoring automatico.  
    Sviluppato dal team LLMentor.
    """)
