import json
import streamlit as st
import os


def esegui_quiz():
    st.title("Genera Quiz Interattivi")

    if "file_name" not in st.session_state:
        st.warning("⚠️ Nessun file caricato. Torna alla sezione 'Carica File'.")
        return

    nome_file = st.session_state.file_name.lower()

    if "gestione" in nome_file:
        categoria_file = "economia_gestione_imprese"
    elif "politica" in nome_file:
        categoria_file = "economia_politica"
    else:
        st.error("❌ File non riconosciuto.")
        return

    base_dir = os.path.dirname(os.path.dirname(__file__))
    percorso_dataset = os.path.join(base_dir, "assets", "quiz_dataset.json")

    try:
        with open(percorso_dataset, "r", encoding="utf-8") as f:
            dataset_quiz = json.load(f)

        argomenti_disponibili = [
            argomento for argomento, contenuto in dataset_quiz.items()
            if contenuto["categoria_file"] == categoria_file
        ]

        if not argomenti_disponibili:
            st.error("Nessun argomento disponibile per questo file.")
            return

        argomento_scelto = st.selectbox("� Seleziona un argomento:", argomenti_disponibili)

        if argomento_scelto:
            domande = dataset_quiz[argomento_scelto]["domande"]

            if (
                "quiz_domande" not in st.session_state
                or st.session_state.get("quiz_argomento") != argomento_scelto
            ):
                st.session_state.quiz_domande = domande
                st.session_state.quiz_argomento = argomento_scelto
                st.session_state.indice_domanda = 0
                st.session_state.punteggio = 0
                st.session_state.risposte = []

            indice = st.session_state.indice_domanda

            if indice < len(domande):
                domanda_corrente = domande[indice]
                st.markdown(f"### Domanda {indice + 1} di {len(domande)}")
                st.markdown(domanda_corrente["domanda"])

                risposta_utente = st.radio(
                    "Scegli una risposta:",
                    domanda_corrente["opzioni"],
                    key=f"risposta_{indice}"
                )

                if st.button("Conferma", key=f"conferma_{indice}"):
                    corretta = risposta_utente == domanda_corrente["corretta"]
                    feedback = domanda_corrente.get("feedback", {}).get(
                        "corretta" if corretta else "errata", ""
                    )
                    esito = "✔️ Corretta" if corretta else "❌ Errata"

                    st.session_state.risposte.append({
                        "domanda": domanda_corrente["domanda"],
                        "scelta": risposta_utente,
                        "corretta": domanda_corrente["corretta"],
                        "feedback": feedback,
                        "esito": esito
                    })

                    if corretta:
                        st.session_state.punteggio += 1

                    st.session_state.indice_domanda += 1
                    st.rerun()

            else:
                st.success("� Quiz completato!")
                st.write(f"� Punteggio finale: {st.session_state.punteggio} / {len(domande)}")

                with st.expander("� Rivedi le tue risposte"):
                    for i, r in enumerate(st.session_state.risposte):
                        st.markdown(f"""
                        {i+1}. {r['domanda']}  
                        <span style='color: yellow;'>� Tua risposta:</span> _{r['scelta']}_ → **{r['esito']}**  
                        {f"<span style='color: #32CD32;'>� Risposta corretta:</span> {r['corretta']}" if r['esito'] == "❌ Errata" else ""}
                        """, unsafe_allow_html=True)


                if st.button("� Ricomincia quiz"):
                    del st.session_state.quiz_domande
                    del st.session_state.quiz_argomento
                    del st.session_state.indice_domanda
                    del st.session_state.punteggio
                    del st.session_state.risposte
                    st.rerun()

    except Exception as e:
        st.error(f"❌ Errore durante il caricamento dei quiz: {e}")
