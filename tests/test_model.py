# tests/test_model.py
import unittest
import pickle
import os
from pathlib import Path # Importa la classe Path

class TestSentimentModel(unittest.TestCase):
    
    def setUp(self):
        # Percorso del file corrente
        current_dir = Path(__file__).parent
        
        # Costruisci il percorso del modello in modo robusto
        # '..' si sposta alla directory genitore (da /app/tests a /app)
        # '/' unisce i percorsi
        model_path = current_dir.parent / 'src' / 'sentiment_analysis_model.pkl'

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            self.pipeline = pickle.load(f)
            
    def test_positive_prediction(self):
        text_to_predict = ["This product is amazing, I highly recommend it!"]
        predicted_sentiment = self.pipeline.predict(text_to_predict)[0]
        self.assertEqual(predicted_sentiment, "positive")

    def test_negative_prediction(self):
        text_to_predict = ["The service was terrible and I will never use it again."]
        predicted_sentiment = self.pipeline.predict(text_to_predict)[0]
        self.assertEqual(predicted_sentiment, "negative")
        
    def test_confidence(self):
        # Questo test potrebbe fallire se il modello non ha il metodo 'predict_proba'
        # Lo metto in un blocco try-except per sicurezza
        try:
            text_to_predict = ["This product is fine."]
            prediction_probabilities = self.pipeline.predict_proba(text_to_predict)[0]
            confidence = max(prediction_probabilities)
            self.assertIsInstance(confidence, float)
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)
        except AttributeError:
            self.skipTest("Il modello non supporta 'predict_proba'")


if __name__ == '__main__':
    unittest.main()
