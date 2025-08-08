FROM python:3.9-slim-bookworm

WORKDIR /app

# Installa curl per health checks
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements e installa dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# per test
COPY tests/ /app/tests/

# Copia tutto il codice
COPY . .

# Esponi porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando di avvio
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]