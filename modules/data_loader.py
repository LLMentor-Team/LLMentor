import pandas as pd

def carica_syllabus(path='data/syllabus_economia.csv'):
    """
    Carica il syllabus del corso da file CSV.
    """
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print("❌ File non trovato. Verifica il percorso.")
        return pd.DataFrame()

def filtra_per_modulo(df, modulo):
    """
    Ritorna solo le righe del modulo indicato (Micro o Macro).
    """
    return df[df['modulo'].str.lower() == modulo.lower()]
