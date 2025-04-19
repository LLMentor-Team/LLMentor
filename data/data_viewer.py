import streamlit as st
import pandas as pd
import os
import fitz  # PyMuPDF per leggere i PDF


# Funzione per processare i PDF e convertirli in DataFrame
def processa_pdf_adattivo(percorso_pdf):
    """
    Estrae contenuto da un PDF e lo converte in DataFrame.
    """
    try:
        doc = fitz.open(percorso_pdf)
        testo_completo = ""
        for page in doc:
            testo_completo += page.get_text()

        # Esempio: dividerlo riga per riga
        righe = testo_completo.split("\n")
        data = {"Righe": righe}
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Errore nella lettura del PDF {percorso_pdf}: {e}")
        return pd.DataFrame()  # Restituisce un DataFrame vuoto in caso di errore
# Funzione per salvare i DataFrame come file CSV
def salva_output(df, percorso_output):
    """
    Salva un DataFrame in un file CSV specificato.
    """
    try:
        os.makedirs(os.path.dirname(percorso_output), exist_ok=True)
        df.to_csv(percorso_output, index=False)
        st.success(f"File salvato con successo in: {percorso_output}")
    except Exception as e:
        st.error(f"Errore durante il salvataggio del file CSV in {percorso_output}: {e}")


# Funzione per caricare i CSV dalla directory "data"
@st.cache_data
def carica_syllabi():
    """
    Carica tutti i file CSV nella directory 'data'.
    """
    syllabi = {}
    for filename in os.listdir("data"):
        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join("data", filename))
                syllabi[filename] = df
            except Exception as e:
                st.warning(f"Errore nel caricamento di {filename}: {e}")
    return syllabi


# Funzione principale per il visualizzatore
def mostra_syllabus():
    st.header("Visualizzatore Syllabus")

    # Funzione di caricamento PDF
    st.markdown("## 1. Carica un file PDF")
    uploaded_file = st.file_uploader("Seleziona un file PDF per processarlo", type=["pdf"])

    if uploaded_file is not None:
        # Salva il file PDF caricato nella directory 'data'
        percorso_pdf = os.path.join("data", uploaded_file.name)
        with open(percorso_pdf, "wb") as f:
            f.write(uploaded_file.read())

        # Processa il PDF e visualizza i dati estratti
        st.info("Processando il file PDF... potrebbe richiedere qualche secondo.")
        df = processa_pdf_adattivo(percorso_pdf)

        if not df.empty:
            st.success("Il PDF è stato processato correttamente!")
            st.write("Anteprima dei dati estratti:")
            st.dataframe(df)

            # Salva il risultato in formato CSV
            output_csv = os.path.join("data", uploaded_file.name.replace(".pdf", ".csv"))
            salva_output(df, output_csv)
        else:
            st.error("Non è stato possibile estrarre i dati dal PDF. Riprova con un altro file.")

    # Carica i file CSV disponibili per la visualizzazione
    st.markdown("## 2. Visualizza i file CSV disponibili")
    syllabi = carica_syllabi()

    if not syllabi:
        st.warning("Nessun file CSV trovato nella cartella 'data'. Carica e processa un PDF per iniziare.")
    else:
        file_selezionato = st.selectbox("Scegli un syllabus da visualizzare:", list(syllabi.keys()))
        df = syllabi[file_selezionato]

        st.success(f"Visualizzazione del file: {file_selezionato}")

        # Filtra per modulo, se la colonna esiste
        if "Modulo" in df.columns:
            moduli = df["Modulo"].dropna().unique()
            modulo_scelto = st.selectbox("Filtra per modulo:", ["Tutti"] + list(moduli))
            if modulo_scelto != "Tutti":
                df = df[df["Modulo"] == modulo_scelto]

        st.dataframe(df, use_container_width=True)

        # Statistiche descrittive
        st.markdown("### Dettagli statistici")
        st.write(df.describe(include="all"))

        # Download del CSV filtrato
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Scarica CSV filtrato",
            data=csv,
            file_name=f"{file_selezionato.replace('.csv', '')}_filtrato.csv",
            mime="text/csv",
        )


# Esegui la funzione principale
mostra_syllabus()
