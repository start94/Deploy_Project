# 🚀 Sentiment Analysis API con CI/CD e Monitoraggio

## 📋 Descrizione del Progetto

Sistema automatizzato per l'analisi del sentiment di recensioni e-commerce con pipeline CI/CD completa e monitoraggio in tempo reale. Il progetto implementa un'API REST per analizzare il sentiment (positivo, negativo, neutro) di recensioni di prodotti utilizzando un modello di Machine Learning pre-addestrato.

## 🎯 Obiettivi

- ✅ Deploy automatizzato di un modello di Sentiment Analysis
- ✅ Pipeline CI/CD con Jenkins
- ✅ Monitoraggio con Prometheus e Grafana
- ✅ API REST scalabile e performante
- ✅ Containerizzazione con Docker
- ✅ Test automatizzati e quality assurance

## 🏗️ Architettura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│   Jenkins CI/CD │───▶│  Production API │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Docker Images  │    │   Prometheus    │
                       └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │     Grafana     │
                                              └─────────────────┘
```

## 🛠️ Stack Tecnologico

- **Backend**: Python 3.9, Flask
- **ML Framework**: Scikit-learn
- **CI/CD**: Jenkins
- **Containerizzazione**: Docker, Docker Compose
- **Monitoraggio**: Prometheus, Grafana
- **Testing**: Pytest
- **Version Control**: Git, GitHub

## 📦 Installazione e Setup

### Prerequisiti
- Python 3.9+
- Docker e Docker Compose
- Jenkins (per CI/CD)
- Git

### 1. Clone del Repository
```bash
git clone https://github.com/your-username/sentiment-analysis-devops.git
cd sentiment-analysis-devops
```

### 2. Setup dell'Ambiente di Sviluppo
```bash
# Crea virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### 3. Download del Modello Pre-addestrato
```bash
wget -O sentimentanalysismodel.pkl \
  "https://github.com/Profession-AI/progetti-devops/raw/refs/heads/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentimentanalysismodel.pkl"
```

### 4. Avvio in Modalità Sviluppo
```bash
python app.py
```

L'API sarà disponibile su `http://localhost:5000`

## 🐳 Deploy con Docker

### Build dell'immagine
```bash
docker build -t sentiment-analysis-api .
```

### Avvio con Docker Compose
```bash
# Ambiente di sviluppo
docker-compose up -d

# Ambiente di produzione
docker-compose -f docker-compose.prod.yml up -d
```

## 🔌 Utilizzo dell'API

### Endpoint Principali

#### POST /predict
Analizza il sentiment di una recensione

**Request:**
```json
{
  "review": "This product is amazing! I love it."
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95
}
```

#### GET /health
Verifica lo stato di salute dell'API

**Response:**
```json
{
  "status": "healthy"
}
```

#### GET /metrics
Metriche per Prometheus (formato OpenMetrics)

### Esempi con cURL

```bash
# Test di predizione
curl -X POST \
  http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"review": "Great product, highly recommended!"}'

# Health check
curl http://localhost:5000/health

# Metriche
curl http://localhost:5000/metrics
```

## 🧪 Testing

### Esecuzione dei Test
```bash
# Tutti i test
pytest

# Test specifici
pytest tests/test_model.py -v
pytest tests/test_api.py -v

# Con coverage
pytest --cov=app tests/
```

### Tipi di Test Implementati
- **Unit Tests**: Test delle funzioni del modello
- **Integration Tests**: Test dell'API end-to-end
- **Performance Tests**: Test dei tempi di risposta

## 🔄 Pipeline CI/CD

### Trigger Automatici
La pipeline Jenkins si attiva automaticamente su:
- Push sul branch `main` o `develop`
- Apertura/aggiornamento di Pull Request
- Tag di release

### Stages della Pipeline
1. **Checkout**: Clone del codice dal repository
2. **Setup Environment**: Installazione dipendenze e download modello
3. **Unit Tests**: Esecuzione test unitari
4. **Integration Tests**: Test dell'API completa
5. **Build Docker Image**: Creazione immagine container
6. **Deploy Staging**: Deploy su ambiente di test
7. **Deploy Production**: Deploy su ambiente di produzione (solo branch main)

### Configurazione Jenkins
Il file `Jenkinsfile` contiene la configurazione completa della pipeline. Assicurati di configurare:
- GitHub webhook: `http://your-jenkins:8080/github-webhook/`
- Credenziali Docker Hub (se necessario)
- Notifiche email per success/failure

## 📊 Monitoraggio e Metriche

### Prometheus Metrics
L'API espone le seguenti metriche:
- `flask_http_request_duration_seconds`: Tempo di risposta delle richieste
- `flask_http_request_total`: Numero totale di richieste
- `flask_http_request_exceptions_total`: Numero di errori
- Metriche di sistema (CPU, memoria, etc.)

### Dashboard Grafana
Dashboard pre-configurata con visualizzazioni per:
- Tempo di risposta medio
- Throughput (richieste/secondo)
- Tasso di errore
- Utilizzo risorse sistema
- Distribuzione dei sentiment predetti

### Accesso ai Dashboard
- Grafana: `http://localhost:3000` (admin/admin)
- Prometheus: `http://localhost:9090`

## 📁 Struttura del Progetto

```
sentiment-analysis-project/
├── app.py                          # API Flask principale
├── model.py                        # Wrapper del modello ML
├── requirements.txt                # Dipendenze Python
├── Dockerfile                      # Container dell'applicazione
├── docker-compose.yml             # Orchestrazione sviluppo
├── docker-compose.prod.yml        # Orchestrazione produzione
├── Jenkinsfile                     # Pipeline CI/CD
├── prometheus.yml                  # Configurazione Prometheus
├── grafana/                        # Dashboard e config Grafana
│   └── dashboards/
│       └── sentiment-dashboard.json
├── tests/                          # Test automatizzati
│   ├── test_model.py
│   ├── test_api.py
│   └── conftest.py
├── scripts/                        # Script di utilità
│   ├── setup.sh
│   └── deploy.sh
└── docs/                          # Documentazione aggiuntiva
    ├── api.md
    └── deployment.md
```

## 🚀 Deployment in Produzione

### Variabili d'Ambiente
```env
FLASK_ENV=production
MODEL_PATH=/app/sentimentanalysismodel.pkl
PROMETHEUS_PORT=8080
LOG_LEVEL=INFO
```

### Kubernetes (Opzionale)
Manifesti Kubernetes disponibili nella cartella `k8s/` per deployment su cluster.

```bash
kubectl apply -f k8s/
```

## 🔧 Troubleshooting

### Problemi Comuni

**1. Modello non trovato**
```bash
# Verifica che il modello sia stato scaricato
ls -la *.pkl

# Re-download se necessario
wget -O sentimentanalysismodel.pkl [MODEL_URL]
```

**2. Errori di connessione Jenkins**
- Verifica che il webhook GitHub sia configurato correttamente
- Controlla i log Jenkins: `/var/log/jenkins/jenkins.log`
- Verifica firewall e porte aperte

**3. Prometheus non raccoglie metriche**
- Controlla la configurazione `prometheus.yml`
- Verifica che l'endpoint `/metrics` risponda
- Controlla i target in Prometheus UI

## 📈 Metriche di Performance

### Benchmark di Riferimento
- **Tempo di risposta medio**: < 200ms
- **Throughput**: > 100 richieste/secondo
- **Accuracy del modello**: > 85%
- **Uptime**: > 99.9%

## 🤝 Contribuzione

1. Fork del repository
2. Crea un branch feature (`git checkout -b feature/amazing-feature`)
3. Commit delle modifiche (`git commit -m 'Add amazing feature'`)
4. Push sul branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

### Coding Standards
- Segui PEP8 per Python
- Aggiungi test per nuove funzionalità
- Documenta le API changes
- Mantieni coverage test > 80%

## 📝 Changelog

### v1.0.0 (2025-01-XX)
- ✅ Prima release stabile
- ✅ API REST completa
- ✅ Pipeline CI/CD Jenkins
- ✅ Monitoraggio Prometheus/Grafana
- ✅ Containerizzazione Docker
- ✅ Test suite completa

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.



## 🆘 Supporto

Per supporto tecnico o segnalazione di bug:
- 📧 Email: support@yourcompany.com
- 🐛 Issues: [GitHub Issues](https://github.com/start94/sentiment-analysis-devops/issues)
- 📚 Wiki: [Project Wiki](https://github.com/your-username/sentiment-analysis-devops/wiki)

---

**🎯 Obiettivo del progetto**: Dimostrare competenze DevOps attraverso un caso d'uso reale di ML in produzione con focus su automazione, scalabilità e monitoraggio.

⭐ **Se questo progetto ti è stato utile, lascia una star!** ⭐