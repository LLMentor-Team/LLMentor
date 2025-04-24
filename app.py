import streamlit as st

st.set_page_config(page_title="LLMentor", layout="wide")

st.sidebar.title("LLMentor")
pagina = st.sidebar.radio("Vai a:", ["Home", "Carica File", "Genera Quiz", "Riassunto/Spiegazione", "Info Progetto"])

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

elif pagina == "Info Progetto":
    st.title("Info Progetto")
    st.markdown("""
    **LLMentor** è una Web App creata durante il Bootcamp AI di Edgemony.  
    Permette di caricare materiali, generare quiz e ricevere tutoring automatico.  
    Sviluppato dal team LLMentor.
    """)
