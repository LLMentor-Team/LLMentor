import streamlit as st
import os
import pandas as pd
from data_viewer import processa_pdf_adattivo, salva_output



def carica_pdf_e_converti():
    st.header("Carica un syllabus")

    # Caricamento del file: supporta sia PDF che CSV
    uploaded_file = st.file_uploader("Carica un file PDF o CSV", type=["pdf", "csv"])

    if uploaded_file:
        # Salvataggio temporaneo del file
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File caricato: {uploaded_file.name}")

        # Elaborazione del file caricato
        st.info("Elaborando il file...")
        df = carica_syllabus(temp_path)

        if not df.empty:
            st.success("File elaborato con successo!")
            st.dataframe(df, use_container_width=True)

            # Download dei dati come CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Scarica il CSV elaborato",
                data=csv,
                file_name=uploaded_file.name.replace('.pdf', '.csv'),
                mime="text/csv",
            )
        else:
            st.error("Il file non è stato elaborato correttamente. Verifica il formato o il contenuto.")
