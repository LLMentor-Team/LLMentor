import streamlit as st
import os
from data_loader import carica_syllabus, filtra_per_modulo


def mostra_syllabus():
    st.header("Visualizzatore Syllabus")

    # Selezione del syllabus da visualizzare
    st.markdown("## 1. Carica un file PDF o CSV")
    uploaded_file = st.file_uploader("Seleziona un file per visualizzare il syllabus:", type=["pdf", "csv"])

    if uploaded_file:
        # Salvataggio temporaneo del file caricato
        temp_path = os.path.join("temp_viewer", uploaded_file.name)
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Caricamento e visualizzazione del file
        st.info("Elaborando il file...")
        df = carica_syllabus(temp_path)

        if not df.empty:
            st.success("Syllabus elaborato e caricato con successo!")
            st.dataframe(df, use_container_width=True)

            # Filtro opzionale per il modulo, se la colonna 'modulo' è presente
            if "modulo" in df.columns:
                moduli = df["modulo"].dropna().unique()
                modulo_scelto = st.selectbox("Filtra per modulo:", ["Tutti"] + list(moduli))
                if modulo_scelto != "Tutti":
                    df = filtra_per_modulo(df, modulo_scelto)

            # Informazioni statistiche
            st.markdown("### Dettagli statistici")
            st.write(df.describe(include="all"))

            # Download del CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Scarica il syllabus filtrato",
                data=csv,
                file_name=f"{uploaded_file.name.replace('.pdf', '')}_filtrato.csv",
                mime="text/csv",
            )
        else:
            st.error("Non è stato possibile elaborare il file. Assicurati che sia formattato correttamente.")

