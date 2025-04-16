import streamlit as st

st.set_page_config(page_title="LLMentor", layout="wide")

st.sidebar.title("UniCoach")
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

elif pagina == "Info Progetto":
    st.title("Info Progetto")
    st.markdown("""
    **UniCoach** è una Web App creata durante il Bootcamp AI.  
    Permette di caricare materiali, generare quiz e ricevere tutoring automatico.  
    Sviluppato dal team LLMentor.
    """)
