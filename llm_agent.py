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