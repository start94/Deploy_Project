
# 🚀 Piattaforma di Sentiment Analysis | CI/CD & Monitoraggio Avanzato

Un sistema end-to-end per il deploy e il monitoraggio di un modello di Sentiment Analysis, costruito con un approccio DevOps moderno. Questo progetto implementa un'API REST basata su FastAPI, containerizzata con Docker e orchestrata tramite Docker Compose. L'intero ciclo di vita, dal push del codice al deploy in produzione, è automatizzato da una pipeline Jenkins che esegue test rigorosi e rilascia uno stack completo che include monitoraggio in tempo reale con Prometheus, Grafana e cAdvisor.

---

## Autore

**Raffaele Diomaiuto**

- GitHub: [start94](https://github.com/start94)
- LinkedIn: [Raffaele Diomaiuto](https://www.linkedin.com/in/raffaele-diomaiuto/)

---

## 📋 Indice

- [Architettura del Sistema](#-architettura-del-sistema)  
- [Stack Tecnologico](#-stack-tecnologico)  
- [Funzionalità Principali](#-funzionalità-principali)  
- [Come Funziona: La Pipeline CI/CD](#-come-funziona-la-pipeline-cicd)  
- [Avvio e Utilizzo](#-avvio-e-utilizzo)  
- [Utilizzo dell'API](#-utilizzo-dellapi)  
- [Accesso allo Stack di Monitoraggio](#-accesso-allo-stack-di-monitoraggio)  
- [Struttura del Progetto](#-struttura-del-progetto)  

---

## 🏗️ Architettura del Sistema

Il flusso di lavoro è completamente automatizzato: uno sviluppatore effettua un git push su GitHub, che innesca un webhook. Jenkins riceve la notifica, esegue la pipeline per testare e costruire gli artefatti Docker, e infine deploya l'intero stack di servizi.

```mermaid
graph TD
    A[👨‍💻 Sviluppatore<br>git push] --> B{🐙 GitHub Repo}
    B -->|Webhook| C[🌶️ Jenkins Server]
    subgraph "Pipeline CI/CD in Jenkins"
        C --> D{1. Setup<br>Pulizia Ambiente}
        D --> E{2. Download & Verify<br>Scarica Modello .pkl}
        E --> F{3. Build<br>Crea Immagine API}
        F --> G{4. Test<br>Test Unitari e Integrazione<br>in un container isolato}
        G --> H{5. Deploy<br>docker-compose up --build}
    end
    subgraph "🐳 Stack Applicativo in Esecuzione"
        H --> I[🚀 Sentiment API<br>Porta: 8081]
        H --> J[🔥 Prometheus<br>Porta: 9090]
        H --> K[📊 Grafana<br>Porta: 3000]
        H --> L[📈 cAdvisor<br>Porta: 8082]
    end
    J --> K
    I --> J
    L --> J
````

---

## 🛠️ Stack Tecnologico

| Categoria          | Tecnologia                    | Scopo                                                    |
| ------------------ | ----------------------------- | -------------------------------------------------------- |
| Backend            | Python 3.9, FastAPI, Uvicorn  | Creazione di un'API REST asincrona e performante.        |
| Machine Learning   | Scikit-learn                  | Utilizzo del modello di sentiment analysis.              |
| CI/CD              | Jenkins                       | Automazione del ciclo di build, test e deploy.           |
| Container          | Docker, Docker Compose        | Containerizzazione dei servizi e orchestrazione locale.  |
| Monitoraggio       | Prometheus, Grafana, cAdvisor | Raccolta e visualizzazione di metriche di app e sistema. |
| Testing            | unittest (standard library)   | Esecuzione di test unitari e di integrazione.            |
| Controllo Versione | Git, GitHub                   | Gestione del codice sorgente e trigger per la pipeline.  |

---

## ✨ Funzionalità Principali

* **Pipeline CI/CD Completamente Automatizzata**: Ogni push sul branch `main` scatena l'intero processo di deploy.
* **Download Dinamico del Modello**: Il modello ML non è archiviato nel repo, ma scaricato durante la pipeline per garantire la versione aggiornata.
* **Test Containerizzati**: I test avvengono in un container temporaneo isolato per massima affidabilità.
* **Deploy Atomico dello Stack**: L'intero ambiente (API, Prometheus, Grafana, cAdvisor) viene deployato con un unico comando.
* **Monitoraggio Chiavi in Mano**: Dashboard pre-configurate in Grafana per osservabilità immediata di performance e risorse.

---

## ⚙️ Come Funziona: La Pipeline CI/CD

Il cuore del progetto è il `Jenkinsfile`, che orchestra ogni passo. Ecco le fasi principali:

1. **Checkout SCM**: Jenkins clona il codice dal repo GitHub su webhook.
2. **Setup Environment**: Pulizia ambiente Docker rimuovendo container e immagini non usate.
3. **Download Model**: Esegue `scripts/download_model.py` per scaricare il file `sentiment_analysis_model.pkl`.
4. **Verify Model**: Controlla l'esistenza e integrità del modello.
5. **Build**: Costruisce l’immagine Docker dell’API (`sentiment-api:latest`).
6. **Test**: Avvia un container temporaneo per test unitari e di integrazione.
7. **Deploy Full Stack**: Se i test passano, avvia lo stack completo tramite:

   ```bash
   docker-compose -f docker-compose-app.yml up -d --build
   ```

---

## 🚀 Avvio e Utilizzo

Il progetto è eseguito interamente in Docker, senza bisogno di ambienti Python locali.

### Prerequisiti

* Git
* Docker
* Docker Compose

### Procedura di Avvio

```bash
git clone https://github.com/start94/Deploy_Project.git
cd Deploy_Project
docker-compose -f docker-compose-app.yml up -d --build
docker ps
```

Dovresti vedere quattro container attivi: `sentiment-api-prod`, `prometheus-server`, `grafana-server`, `cadvisor`.

---

## 🔌 Utilizzo dell'API

L'API è disponibile su `http://localhost:8081`.

### Endpoint Principali

* **POST /predict**
  Input JSON:

  ```json
  {
    "text": "Questo prodotto è fantastico!"
  }
  ```

  Output: sentiment e punteggio di confidenza.

* **GET /health**
  Stato di salute dell'app e del modello.

### Esempi con cURL

```bash
curl -X POST "http://localhost:8081/predict" \
-H "Content-Type: application/json" \
-d '{
  "text": "This product is amazing! I really love it and would recommend it to everyone."
}'
```

```bash
curl http://localhost:8081/health
```

---

## 📊 Accesso allo Stack di Monitoraggio

* **Grafana**: [http://localhost:3000](http://localhost:3000)
  Credenziali: admin / admin
  Dashboard preconfigurate per metriche API e sistema.

* **Prometheus**: [http://localhost:9090](http://localhost:9090)
  Esplora metriche grezze e stato target.

* **cAdvisor**: [http://localhost:8082](http://localhost:8082)
  Monitoraggio in tempo reale risorse container.

---

## 📁 Struttura del Progetto

```
.
├── .dockerignore              # Ignora file durante il build Docker
├── Dockerfile                 # Dockerfile per l'API FastAPI
├── Dockerfile.jenkins         # Dockerfile per immagine Jenkins
├── Jenkinsfile                # Pipeline CI/CD Jenkins
├── docker-compose-app.yml     # Stack produzione (API + monitoraggio)
├── docker-compose.jenkins.yml # Servizio Jenkins
├── docker-compose.yml         # Base Docker Compose per Jenkins
├── docs/                      # Documentazione
│   └── architecture.md
├── grafana/                   # Configurazione Grafana
│   └── provisioning/
│       ├── dashboards/
│       └── datasources/
├── monitoring/                # Configurazioni monitoraggio
│   ├── Dockerfile.prometheus  # Immagine Prometheus custom
│   └── prometheus.yml         # Configurazione Prometheus
├── payload.json               # Esempio payload API
├── README.md                  # Questo file
├── requirements.txt           # Dipendenze Python
├── scripts/                   # Script di utilità
│   └── download_model.py      # Scarica modello
├── src/                       # Codice sorgente FastAPI
│   └── app.py                 
└── tests/                     # Test unitari e integrazione
    ├── test_api.py
    └── test_model.py
```

---

⭐ Se questo progetto ti è stato utile, considera di lasciare una stella al repository GitHub! ⭐
