import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera la chiave API da .env
openai_api_key = os.getenv("OPENAI_API_KEY")

# Usa una chiave API di fallback se non è impostata nel .env
if not openai_api_key:
    openai_api_key = "dummy_key"

# Inizializza il modello solo se la chiave è valida
chain = None  # Impostiamo chain a None di default

if openai_api_key != "dummy_key":
    # Inizializza il modello GPT solo se la chiave API è valida
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)

    # Crea un prompt template iniziale
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
    if openai_api_key == "dummy_key":
        return "⚡️ Al momento il tutor AI non è disponibile. Inserisci una OpenAI API key nel file .env."
    
    # Verifica che chain sia stato creato prima di usarlo
    if chain:
        risposta = chain.run({"domanda": domanda})
        return risposta
    else:
        return "⚠️ Errore: la chiave API non è valida o non è stata configurata correttamente."

# Test rapido del tuo agente
if __name__ == "__main__":
    domanda_esempio = "Cos'è una rete neurale?"
    risposta = fai_domanda(domanda_esempio)
    print(risposta)
