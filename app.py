elif pagina == "Carica File":
    st.title("Carica i tuoi materiali di studio")
    st.write("Carica syllabus, appunti o testi da cui generare quiz o riassunti.")
    
    uploaded_file = st.file_uploader("Carica un file", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        st.session_state["file_name"] = uploaded_file.name
        st.success(f"File **{uploaded_file.name}** caricato con successo!")

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
