# 🚀 Deployment Guide für AdAstraGPT

## Vorbereitung

### 1. Fly.io Account erstellen
```bash
# Falls noch nicht installiert
curl -L https://fly.io/install.sh | sh

# Login
fly auth login
```

### 2. App erstellen
```bash
cd ad-astra-gpt
fly apps create ad-astra-gpt
```

### 3. API Key setzen
```bash
fly secrets set API_KEY=dein-super-sicherer-api-key-hier
```

### 4. Volume erstellen (für persistente Daten)
```bash
fly volumes create adastra_data_vol --size 1 --region fra
```

### 5. Deployen
```bash
fly deploy
```

## Nach dem Deployment

### Health Check
```bash
curl https://ad-astra-gpt.fly.dev/health
```

### Portfolio abrufen
```bash
curl https://ad-astra-gpt.fly.dev/portfolio/live
```

### Strategie updaten
```bash
curl -X POST https://ad-astra-gpt.fly.dev/state/update \
  -H "x-api-key: dein-super-sicherer-api-key-hier" \
  -H "Content-Type: application/json" \
  -d '{
    "target": {"gold": 0.6, "crypto": 0.4},
    "cash_buffer": 0.05,
    "mode": "active"
  }'
```

### Logs ansehen
```bash
fly logs
```

## Wichtige Befehle

```bash
# SSH in die App
fly ssh console

# App Status
fly status

# Secrets ändern
fly secrets set API_KEY=neuer-key

# App neu starten
fly apps restart ad-astra-gpt
```

## Monitoring

- Health Endpoint: `/health`
- Logs: `fly logs`
- Metrics: Fly.io Dashboard


