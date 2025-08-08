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

