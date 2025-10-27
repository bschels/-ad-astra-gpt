# AdAstraGPT - Architektur & Zuständigkeiten

## 🏗️ System-Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                     AdAstraGPT Backend                       │
│                     (Python/FastAPI)                        │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐│
│  │ Trading Engine  │  │ Tax Optimizer   │  │ Coinbase API││
│  │                 │  │                 │  │             ││
│  │ - Live Prices   │  │ - FIFO          │  │ - Auth      ││
│  │ - Top 100       │  │ - 1-Jahr Regel  │  │ - Sync      ││
│  │ - Gold          │  │ - Tax-Status    │  │ - Portfolio  ││
│  │ - Signals       │  │ - Recommendations│  │             ││
│  └─────────────────┘  └─────────────────┘  └─────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  REST API Endpoints                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│              ChatGPT / GPT Actions                         │
│                                                             │
│  - Strategische Beratung                                   │
│  - Trading-Entscheidungen                                  │
│  - Portfolio-Interpretation                               │
│  - Marktanalyse & Insights                                 │
│  - Steueroptimierte Empfehlungen                           │
│                                                             │
│  ↕ Nutzt API-Endpoints ↕                                   │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Zuständigkeiten

### 🔧 Backend (Python/FastAPI) - WAS

#### 1. Daten & Storage
- ✅ **Trade History** - Jede Transaktion mit Datum/Price/Amount
- ✅ **Portfolio State** - Aktuelle Holdings
- ✅ **Haltefrist-Tracking** - 1 Jahr ab Kauf → steuerfrei
- ✅ **FIFO-Logik** - Welche Coins beim Verkauf besteuert werden
- ✅ **Cost Basis** - Durchschnittskosten pro Asset

#### 2. Live-Daten Integration
- ✅ **Top 100 Market Data** - Von CoinGecko
- ✅ **Gold Price** - Live API
- ✅ **Coinbase Sync** - Automatischer Import
- ✅ **Portfolio Abfrage** - Live Balances von Coinbase

#### 3. Berechnung & Logic
- ✅ **Tax-Free Calculator** - Welche Coins steuerfrei sind
- ✅ **FIFO für Verkäufe** - Tax-optimized sell recommendations
- ✅ **Portfolio Valuation** - Aktueller Wert
- ✅ **P&L Calculation** - Profit/Loss
- ✅ **Rebalancing Logic** - Asset allocation math

#### 4. API & Endpoints
- ✅ **GET `/tax/holdings/{asset}`** - Tax Status für Asset
- ✅ **GET `/tax/soon`** - Coins die bald steuerfrei werden
- ✅ **GET `/tax/recommend/{asset}`** - Welche Coins verkaufen
- ✅ **POST `/coinbase/sync`** - Sync von Coinbase
- ✅ **GET `/coinbase/portfolio`** - Portfolio von Coinbase
- ✅ **POST `/transactions/add`** - Transaktion hinzufügen

### 🧠 GPT/Actions - WIE & WARUM

#### 1. Strategische Beratung
- 🎯 **"Welche Coins kaufen?"** - Based on market analysis
- 🎯 **"Wann verkaufen?"** - Timing recommendations
- 🎯 **"Wie rebalancen?"** - Portfolio allocation advice
- 🎯 **"Risk assessment"** - Portfolio risk evaluation

#### 2. Tax-Optimierung
- 🎯 **"Steuerfrei verkaufen"** - Nutzt Tax-Free Status
- 🎯 **"Warten bis steuerfrei"** - Timing based on 1-Jahr Regel
- 🎯 **"Steuerbelastung minimieren"** - FIFO recommendations
- 🎯 **"Welche Transaktionen planen"** - Proactive advice

#### 3. Interpretation & Insights
- 🎯 **"Warum diese Empfehlung?"** - Erklärung der Signals
- 🎯 **"Market context"** - Warum Preis steigt/fällt
- 🎯 **"Portfolio health"** - Performance Interpretation
- 🎯 **"Risk factors"** - Gewarnte Risiken

#### 4. Decision Making
- 🎯 **"Buy/Sell/Hold"** - Konkrete Entscheidungen
- 🎯 **"Portfolio strategy"** - Langfristige Planung
- 🎯 **"Asset selection"** - Welche Assets ins Portfolio
- 🎯 **"Exit strategy"** - Wie aussteigen

### 🔄 Zusammenarbeit Backend ↔ GPT

#### GPT fragt Backend:
1. **"GET /portfolio/live"** → "Was habe ich aktuell?"
2. **"GET /tax/holdings/{asset}"** → "Welche Coins sind steuerfrei?"
3. **"GET /tax/recommend/BTC"** → "Welche BTC soll ich verkaufen?"
4. **"GET /markets/overview"** → "Wie sieht der Markt aus?"
5. **"POST /coinbase/sync"** → "Sync Daten von Coinbase"

#### Backend liefert Daten:
- Portfolio-Werte
- Tax-Status
- Rebalancing-Empfehlungen
- Trading-Signale
- Markt-Metriken

#### GPT interpretiert & entscheidet:
- "OK, diese Coins sind steuerfrei, die verkaufen wir"
- "Markt sieht gut aus, wir warten noch 20 Tage bis BTC steuerfrei ist"
- "Rebalancing nötig: +5% BTC, -5% SOL"
- "Risk zu hoch, Cash erhöhen"

## 🎯 Workflow-Beispiele

### Beispiel 1: Steueroptimiertes Verkaufen

```
1. User fragt GPT: "Soll ich 2 BTC verkaufen?"
   
2. GPT fragt Backend:
   - GET /tax/holdings/BTC → "1.5 BTC steuerfrei, 0.5 BTC steuerpflichtig"
   - GET /tax/recommend/BTC?amount=2 → "Verkaufe zuerst die steuerfreien!"

3. Backend antwortet:
   {
     "recommendation": [
       {"sell_amount": 1.5, "is_tax_free": true, "tax_saved": 0},
       {"sell_amount": 0.5, "is_tax_free": false, "tax_saved": 7150}
     ]
   }

4. GPT interpretiert:
   "Ja, verkaufen! Verwende FIFO: zuerst die steuerfreien (1.5), 
    dann wenn nötig die neueren (0.5). So sparst du ~7150€ Steuern."
```

### Beispiel 2: Coinbase Auto-Sync

```
1. User fragt GPT: "Sync mein Coinbase Portfolio"

2. GPT ruft auf:
   POST /coinbase/sync
   Headers: {API_KEY, CB_API_KEY, CB_API_SECRET}

3. Backend:
   - Hole Portfolio von Coinbase
   - Parse alle Transaktionen
   - Füge zu Tax Optimizer hinzu
   - Berechne Haltefristen

4. GPT interpretiert:
   "Portfolio gesynct! Du hast:
    - 0.5 BTC (steuerfrei in 30 Tagen)
    - 2.0 ETH (steuerfrei)
    - 1000 USDC
    Portfolio Wert: $28,500"
```

### Beispiel 3: Strategische Beratung

```
1. User fragt GPT: "Wie soll ich mein Portfolio strukturieren?"

2. GPT holt Daten:
   - GET /portfolio/live
   - GET /markets/overview
   - GET /tax/holdings/*

3. GPT analysiert:
   "Markt analysiert. Empfehlung:
    - Aktuell: 40% BTC, 30% ETH, 20% SOL, 10% Cash
    - Optimal: 30% BTC, 25% ETH, 20% SOL, 15% Gold, 10% Cash
    - Rebalancing: -5% BTC, -5% ETH, +15% Gold
    - Tax-optimiert: Warte 20 Tage bis BTC steuerfrei wird"

4. GPT zieht Schlüsse:
   "Verkaufe jetzt ETH (steuerfrei), kaufe Gold. 
    Warte mit BTC-Verkauf bis steuerfrei."
```

## 🔐 Security & Access

### Backend Security
- ✅ API Key Authentication (x-api-key)
- ✅ Coinbase OAuth (separate credentials)
- ✅ Keine Secrets im Code
- ✅ Environment Variables (Fly.io Secrets)

### GPT Actions Security
- ✅ Actions nur via Backend-API
- ✅ Keine direkten Exchange-Calls
- ✅ Protected Endpoints für writes
- ✅ Read-only für Analysis

## 📊 Daten-Flow

```
User Request
    ↓
GPT (Strategie)
    ↓
Backend API (Daten)
    ↓
Trading Engine / Tax Optimizer / Coinbase
    ↓
Daten → GPT
    ↓
Interpreation → User
```

## 🎯 Use Cases

### 1. "Wie viel ist mein Portfolio wert?"
GPT → Backend → GET /portfolio/live → "€28,500"

### 2. "Soll ich Bitcoin verkaufen?"
GPT → Backend → GET /tax/recommend/BTC → "Ja, steuerfrei verkaufen möglich"

### 3. "Welche Coins sind bald steuerfrei?"
GPT → Backend → GET /tax/soon → "BTC in 30 Tagen, ETH in 20 Tagen"

### 4. "Sync Coinbase"
GPT → Backend → POST /coinbase/sync → "Done, 15 Transaktionen importiert"

### 5. "Rebalance mein Portfolio"
GPT → Backend → GET /portfolio/analyze → "Verkaufe 5% ETH, kaufe 5% Gold"

## ✅ Implementiert

- ✅ Backend mit FastAPI
- ✅ Tax Optimizer mit FIFO + 1-Jahr Regel
- ✅ Coinbase API Integration
- ✅ Alle Endpoints für GPT-Integration
- ✅ Portfolio Management
- ✅ Live Price Feeds (Top 100 + Gold)

## 🚀 Next Steps

1. **GPT Actions konfigurieren** - Endpoints registrieren
2. **Testing** - API testen
3. **Deployment** - Auf Fly.io deployen
4. **API Key** - Für Coinbase setzen
5. **Integration** - GPT Actions connecten

