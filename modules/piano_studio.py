
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, date
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os

def genera_piano_studio(df, settimane):
    df.columns = df.columns.str.strip().str.lower()

    if "argomento" not in df.columns:
        st.error("Il file selezionato non contiene una colonna 'argomento'.")
        return

    argomenti = df["argomento"].dropna().tolist()
    totale = len(argomenti)

    if totale == 0:
        st.warning("Nessun argomento disponibile da distribuire.")
        return

        # Distribuzione argomenti per settimana
    per_settimana = totale // settimane
    distribuzione = [per_settimana] * settimane
    for i in range(totale % settimane):
        distribuzione[i] += 1

    # Timeline con date
    piano = []
    start_date = datetime.today()
    inizio = 0

    for i, num in enumerate(distribuzione):
        settimana = i + 1
        fine = inizio + num
        subset = argomenti[inizio:fine]
        data_inizio = start_date + timedelta(weeks=i)
        data_fine = data_inizio + timedelta(days=6)
        titolo = f"Settimana {settimana}"
        descrizione = "\n".join(subset)
        piano.append({
            "Settimana": titolo,
            "Argomenti": descrizione,
            "Inizio": data_inizio,
            "Fine": data_fine
        })
        inizio = fine

    df_timeline = pd.DataFrame(piano)

    st.subheader("Piano settimanale con argomenti")
    for riga in piano:
        st.markdown(f"**{riga['Settimana']}**:  \n{riga['Argomenti']}")

    st.subheader("Timeline visuale (con date)")
    fig = px.timeline(
        df_timeline,
        x_start="Inizio",
        x_end="Fine",
        y="Settimana",
        color="Settimana",
        hover_data=["Argomenti"]
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def esporta_piano_pdf(df, settimane, nome_file=""):
    df.columns = df.columns.str.strip().str.lower()
    argomenti = df["argomento"].dropna().tolist()
    totale = len(argomenti)

    if totale == 0:
        return None

    per_settimana = totale // settimane
    distribuzione = [per_settimana] * settimane
    for i in range(totale % settimane):
        distribuzione[i] += 1

    temp_path = tempfile.mktemp(suffix=".pdf")
    c = canvas.Canvas(temp_path, pagesize=A4)
    width, height = A4
    margin = 50

    # --- COVER PAGE ---
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "📘 Piano di Studio Personalizzato")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 140, f"Corso: {nome_file.replace('_', ' ').replace('.csv', '').title()}")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 180, f"Data di generazione: {date.today().isoformat()}")

    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(width / 2, height - 240, "Studia con costanza, supera ogni ostacolo!")

    c.showPage()  # nuova pagina per il piano di studio

    # --- CONTENUTO ---
    y = height - 50
    index = 0
    c.setFont("Helvetica", 12)
    for settimana, num in enumerate(distribuzione, start=1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, f"Settimana {settimana}")
        y -= 20
        c.setFont("Helvetica", 11)
        for i in range(num):
            c.drawString(margin + 20, y, f"- {argomenti[index]}")
            index += 1
            y -= 18

            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)

        y -= 10

    c.save()
    return temp_path