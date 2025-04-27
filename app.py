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
    st.file_uploader("Carica un file", type=["pdf", "docx", "txt"])

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
import streamlit as st
from modules.data_loader import carica_syllabus
from modules.piano_studio import genera_piano_studio, esporta_piano_pdf
import os


st.set_page_config(page_title="LLMentor", layout="wide")
st.title("LLMentor - Timeline Studio")

st.header("Scegli il syllabus")
files = ["economia_politica.csv", "economia_gestione_imprese.csv"]
selected = st.selectbox("Scegli un file:", files)

df = carica_syllabus(selected)
if not df.empty:
    st.dataframe(df)

    st.header("Crea un piano di studio personalizzato")
    settimane = st.number_input("In quante settimane vuoi prepararti?", min_value=1, max_value=20, value=4)

    if st.button("Genera piano"):
        # Pulisce i nomi delle colonne (in minuscolo)
        df.columns = df.columns.str.strip().str.lower()

        # Mostra la timeline
        genera_piano_studio(df, settimane)

        # Esporta il piano come PDF
        pdf_path = esporta_piano_pdf(df, settimane, selected)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Scarica piano di studio in PDF",
                data=f.read(),
                file_name="piano_di_studio.pdf",
                mime="application/pdf"
            )

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
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# Carica la tua chiave API
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Inizializza il modello GPT
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Crea un prompt template iniziale (semplice)
prompt_template = ChatPromptTemplate.from_template("""
Sei LLMentor, un assistente virtuale universitario che aiuta gli studenti a capire argomenti complessi. 
Fornisci spiegazioni chiare e usa esempi semplici quando possibile.

Domanda dello studente: {domanda}
Risposta dettagliata, utile e chiara:
""")

# Crea la catena LLM (Prompt → LLM → Risposta)
chain = LLMChain(llm=llm, prompt=prompt_template)

# Funzione per fare domande al modello GPT
def fai_domanda(domanda):
    risposta = chain.run(domanda=domanda)
    return risposta

# Test rapido del tuo agente
if __name__ == "__main__":
    domanda_esempio = "Cos'è una rete neurale?"
    risposta = fai_domanda(domanda_esempio)
    print(risposta)
