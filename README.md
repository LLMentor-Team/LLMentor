# LLMentor 🧠🎓
Progetto finale Bootcamp AI – Team LLMentor


**LLMentor** è una web app AI-powered progettata per supportare lo studio universitario in modo personalizzato e interattivo.  
Sviluppata come progetto finale del Bootcamp AI da un team di 5 studenti, integra moduli didattici, generazione di quiz e un tutor LLM conversazionale.

---

## 🚀 Funzionalità principali

- 📚 Visualizzazione appunti e syllabus (dataset simulato)
- 🧠 Generazione quiz a scelta multipla con feedback
- 💬 Agente LLM per spiegazioni e supporto personalizzato
- 📊 Dashboard per il tracciamento dei progressi
- 🔍 Ricerca e filtri per argomento, corso, settimana

---

## 👥 Team

- Cristina – UX/UI
- Noemi – Dataset e contenuti
- Martina – Quiz
- Maria – Integrazione LLM
- Domenico – Dashboard e Deploy

---

## 🔧 Configurazione dell'API Key

Per utilizzare correttamente il progetto LLMentor, è necessario configurare una chiave API di OpenAI.
1. Creazione del file `.env`
Nella root del progetto, crea un file chiamato `.env` (puoi duplicare il file `.env.example`).
Aggiungi al suo interno la tua **OpenAI API Key** come segue:
```bash
OPENAI_API_KEY="la_tua_chiave_api"
