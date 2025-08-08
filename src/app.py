# File: src/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import logging
import os
from typing import Dict, Any
import uvicorn
# Importa l'instrumentator
from prometheus_fastapi_instrumentator import Instrumentator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")


Instrumentator().instrument(app).expose(app)

# Global variable per il modello
model = None

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    sentiment: str
    confidence: float

def load_model():
    """Carica il modello di sentiment analysis"""
    global model
    model_path = "src/sentiment_analysis_model.pkl"
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modello non trovato: {model_path}")
        file_size = os.path.getsize(model_path)
        logger.info(f"Caricamento modello da {model_path} (dimensione: {file_size} bytes)")
        if file_size == 0:
            raise ValueError("Il file del modello è vuoto")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info("✅ Modello caricato con successo")
        if hasattr(model, 'predict'):
            test_prediction = model.predict(["test"])
            logger.info(f"Test modello: {test_prediction}")
        return True
    except Exception as e:
        logger.error(f"❌ Errore nel caricamento del modello: {e}")
        model = None
        return False

@app.on_event("startup")
async def startup_event():
    """All'avvio, carica solo il modello. Il monitoraggio è già attivo."""
    logger.info("🚀 Avvio applicazione Sentiment Analysis")
    load_model()

@app.get("/")
async def root():
    """Endpoint root"""
    return {"message": "Sentiment Analysis API", "version": "1.0.0", "status": "running", "model_loaded": model is not None}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None, "timestamp": "2025-08-06T11:00:00Z"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_sentiment(request: TextRequest):
    """Predice il sentiment di un testo"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modello non disponibile.")
    
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Testo vuoto.")
    
    try:
        prediction = model.predict([text])
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba([text])[0]
            confidence = float(max(probabilities))
        else:
            confidence = 0.8
        sentiment = str(prediction[0])
        logger.info(f"Predizione completata: {sentiment} (confidenza: {confidence:.2f})")
        return PredictionResponse(sentiment=sentiment, confidence=confidence)
    except Exception as e:
        logger.error(f"Errore INASPETTATO nella predizione: {e}")
        raise HTTPException(status_code=500, detail=f"Errore interno del server: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Informazioni sul modello"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modello non caricato")
    
    info = {"model_type": str(type(model).__name__), "model_loaded": True}
    if hasattr(model, 'classes_'):
        info["classes"] = model.classes_.tolist()
    return info

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
