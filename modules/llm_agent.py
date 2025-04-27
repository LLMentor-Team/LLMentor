import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Carica variabili ambiente
load_dotenv()

# Crea il prompt template una volta sola
prompt_template = ChatPromptTemplate.from_template("""
Sei LLMentor, un assistente virtuale universitario che aiuta gli studenti a capire argomenti complessi.
Fornisci spiegazioni chiare e usa esempi semplici quando possibile.

Domanda dello studente: {domanda}
Risposta dettagliata, utile e chiara:
""")

# Funzione per fare domande al modello
def fai_domanda(domanda: str) -> str:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Chiave OpenAI non trovata. Assicurati che il file .env contenga OPENAI_API_KEY.")
    
    # Inizializza il modello GPT dentro la funzione
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    if not domanda:
        return "Per favore, inserisci una domanda valida."
    
    risposta = chain.run({"domanda": domanda})
    return risposta

# Test rapido
if __name__ == "__main__":
    domanda_esempio = "Cos'è una rete neurale?"
    risposta = fai_domanda(domanda_esempio)
    print(risposta)
