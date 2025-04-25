import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

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
