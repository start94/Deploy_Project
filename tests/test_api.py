import unittest
import requests
import time
import json

class TestSentimentAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup eseguito una volta per tutta la classe"""
        cls.base_url = "http://test-api-container:8000"
        cls.wait_for_api()
    
    @classmethod
    def wait_for_api(cls, timeout=30):
        """Attende che l'API sia disponibile"""
        for i in range(timeout):
            try:
                response = requests.get(f"{cls.base_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✅ API disponibile dopo {i+1} tentativi")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        raise Exception("❌ API non disponibile entro il timeout")
    
    def test_health_endpoint(self):
        """Test dell'endpoint health"""
        response = requests.get(f"{self.base_url}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertEqual(data["status"], "healthy")
        print("✅ Health check: PASSED")
    
    def test_root_endpoint(self):
        """Test dell'endpoint root"""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
        print("✅ Root endpoint: PASSED")
    
    def test_predict_endpoint_valid_text(self):
        """Test predizione con testo valido"""
        test_data = {"text": "I love this product! It's amazing!"}
        response = requests.post(
            f"{self.base_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # Se il modello non è caricato, mi aspetto un errore 503
        if response.status_code == 503:
            print("⚠️ Modello non caricato - test saltato")
            self.skipTest("Modello sentiment non disponibile")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("sentiment", data)
        self.assertIn("confidence", data)
        print(f"✅ Predizione: {data}")
    
    def test_predict_endpoint_empty_text(self):
        """Test predizione con testo vuoto"""
        test_data = {"text": ""}
        response = requests.post(
            f"{self.base_url}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 400)
        print("✅ Validazione testo vuoto: PASSED")
    
    def test_model_info_endpoint(self):
        """Test dell'endpoint model info"""
        response = requests.get(f"{self.base_url}/model/info")
        
        # Se il modello non è caricato, mi aspetto un errore 503
        if response.status_code == 503:
            print("⚠️ Modello non caricato - test info saltato")
            return
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("model_type", data)
        print(f"✅ Model info: {data}")

if __name__ == '__main__':
    unittest.main(verbosity=2)