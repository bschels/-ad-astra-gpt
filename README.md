# AdAstraGPT Backend

**Dein persönlicher Weg zur Million bis 2030!**

Ein intelligentes, steueroptimiertes Portfolio-System mit:
- 🎯 Ziel-Tracking (1M bis 2030)
- 💰 Tax-Optimierung (1-Jahr Regel, FIFO)
- 📊 Live Markets (Top 100 + Gold)
- 🔄 Coinbase Integration
- 📈 Performance-Analyse

## 🚀 Dein Aktuelles Portfolio

```
Gold:    8.04 oz  → €32,087
ETH:     2.10 ETH  → €8,716
SOL:     15.02 SOL → €2,990
ONDO:    12,250    → €8,230
FET:     2,450     → €657
USDC:    770       → €770
───────────────────────────
TOTAL:   ≈€53,450  (15.2% von 1M)
```

## 🚀 Features

- **FastAPI** Minimal-Setup (< 100 MB)
- **SQLite** lokale Datenbank
- **API-Key Auth** via `x-api-key` Header
- **Fly.io Ready** für kostenlose Deployments

## 📁 Struktur

```
AdAstraGPT/
├── main.py           # FastAPI App
├── requirements.txt  # Dependencies
├── Dockerfile       # Container
├── fly.toml         # Fly.io Config
└── README.md
```

## 🧩 Endpoints

| Route               | Methode | Beschreibung                    |
| ------------------- | ------- | ------------------------------- |
| `/health`           | GET     | Status-Check                     |
| `/portfolio/live`   | GET     | Aktuelles Portfolio (JSON)      |
| `/portfolio/update` | POST    | Portfolio updaten                |
| `/state/update`     | POST    | Strategie speichern              |
| `/logs/decision`    | POST    | Analyse-Logs entgegennehmen      |
| `/backup/dump`      | GET     | Komprimirter Daten-Dump          |
| `/logs/recent`      | GET     | Letzte Logs                      |
| `/strategies/current` | GET  | Aktuelle Strategie               |

## 📊 Datenstrukturen

### Portfolio
```json
{
  "assets": [
    {"symbol": "BTC", "quantity": 0.5, "avg_buy": 28000},
    {"symbol": "ETH", "quantity": 2.0, "avg_buy": 1600}
  ],
  "cash_eur": 2000,
  "timestamp": "2025-10-25T12:00:00Z"
}
```

### Strategy
```json
{
  "target": {"gold": 0.6, "crypto": 0.4},
  "cash_buffer": 0.05,
  "mode": "review"
}
```

### Decision Log
```json
{
  "timestamp": "2025-10-25T12:30:00Z",
  "summary": "Rebalance empfohlen",
  "actions": [
    {"type": "buy", "asset": "BTC", "amount": 0.1}
  ]
}
```

## 🔐 Setup

### Lokal testen

```bash
pip install -r requirements.txt
python main.py
```

### Auf Fly.io deployen

```bash
# Fly.io Login
fly auth login

# App erstellen
fly apps create ad-astra-gpt

# Secret setzen (wichtig!)
fly secrets set API_KEY=dein-sicherer-api-key

# Deploy
fly deploy
```

## ⚙️ Konfiguration

**API Key setzen:**
```bash
fly secrets set API_KEY=your-secret-api-key-here
```

**API verwenden:**
```bash
curl -H "x-api-key: your-secret-api-key-here" https://ad-astra-gpt.fly.dev/portfolio/live
```

## 📦 Ressourcen

- **Memory**: 512 MB (Free Tier)
- **Storage**: Persistent Volume `/data`
- **CPU**: 1 Shared CPU
- **Idle Timeout**: 60+ seconds

## 🧪 Testing

```bash
# Health check
curl https://ad-astra-gpt.fly.dev/health

# Get portfolio
curl https://ad-astra-gpt.fly.dev/portfolio/live

# Update strategy (mit API Key)
curl -X POST https://ad-astra-gpt.fly.dev/state/update \
  -H "x-api-key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"target":{"gold":0.6,"crypto":0.4},"cash_buffer":0.05,"mode":"active"}'
```

## 📝 Notes

- Alle Daten werden in `/data` persistent gespeichert
- Auth via `x-api-key` Header
- Endpoints mit `/state/update`, `/logs/decision`, `/backup/dump` benötigen API Key
- GET-Endpoints sind öffentlich (außer `/backup/dump`)
