import streamlit as st
import os
import pandas as pd
from modules.data_viewer import processa_pdf_adattivo, salva_output

def carica_pdf_e_converti():
    st.header("Carica Syllabus in PDF")

    uploaded_file = st.file_uploader("Carica un file PDF", type=["pdf"])

    if uploaded_file:
        # Salva temporaneamente il PDF
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open('file.txt', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File caricato: {uploaded_file.name}")

        # Elabora il PDF
        st.info("Analisi del syllabus in corso...")
        df = processa_pdf_adattivo(temp_path)

        if not df.empty:
            st.success("Syllabus elaborato con successo!")
            st.dataframe(df, use_container_width=True)

            # Salva anche nella cartella 'data'
            salva_output(df, temp_path)

            # Download CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Scarica CSV",
                data=csv,
                file_name=uploaded_file.name.replace(".pdf", ".csv"),
                mime="text/csv"
            )
        else:
            st.warning("Non è stato possibile estrarre contenuti utili dal PDF.")
