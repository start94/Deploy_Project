import requests
import sys
import os

# L'URL originale delle specifiche, che funziona 
MODEL_URL = "https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentiment_analysis_model.pkl"

# definisce il percorso di output direttamente nello script
# Il modello verrà salvato in 'src/sentimentanalysismodel.pkl'
output_path = "src/sentiment_analysis_model.pkl"

# Crea la directory di destinazione se non esiste
output_dir = os.path.dirname(output_path)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)

print(f"Downloading model from: {MODEL_URL}")
try:
    response = requests.get(MODEL_URL, timeout=30)
    response.raise_for_status()  # Lancia un errore per status code 4xx/5xx

    with open(output_path, 'wb') as f:
        f.write(response.content)

    print(f"Model downloaded successfully to {output_path}")

except requests.exceptions.RequestException as e:
    print(f"Error during download: {e}")
    sys.exit(1) # Esce con un codice di errore per far fallire la pipeline