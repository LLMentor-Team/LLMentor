import os 
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    openai_api_key = "dummy_key"

if openai_api_key != "dummy_key":
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)

   
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

    risposta = chain.run({"domanda": domanda})
    return risposta

if __name__ == "__main__":
    domanda_esempio = "Cos'è una rete neurale?"
    risposta = fai_domanda(domanda_esempio)
    print(risposta)
