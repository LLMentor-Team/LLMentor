import pandas as pd

def carica_syllabus(nome_file):
    try:
        return pd.read_csv(f"data/{nome_file}")
    except Exception as e:
        print("Errore nel caricamento:", e)
        return pd.DataFrame()
