# 🚀 AdAstraGPT - Quick Start

## Dein System ist bereit!

### ✅ Was du hast:
- **Portfolio**: €53,450 (Gold, ETH, SOL, ONDO, FET, USDC)
- **Ziel**: €1 Million bis 2030
- **Start**: Jetzt (5.3% vom Ziel)
- **Zeit**: 4.2 Jahre
- **System**: Backend + GPT + API Integration

---

## 🎯 Jetzt loslegen

### 1. Backend starten (lokal testen)

```bash
# Dependencies installieren
pip install -r requirements.txt

# Backend starten
python main.py
```

Backend läuft auf: `http://localhost:8080`

### 2. Status abfragen

```bash
# Fortschritt checken
curl http://localhost:8080/goal/status

# Portfolio ansehen
curl http://localhost:8080/portfolio/live

# Tax-Status prüfen
curl http://localhost:8080/tax/holdings/BTC
```

### 3. GPT konfigurieren

Use die Datei **`GPT_PROMPT.md`** als System-Prompt für dein GPT.

Die GPT Actions sind:
- `GET /goal/status` - Fortschritt abfragen
- `GET /portfolio/live` - Portfolio sehen
- `GET /tax/recommend/{asset}` - Tax-Optimiert verkaufen
- `POST /state/update` - Strategie ändern
- `GET /markets/overview` - Markt-Daten

### 4. Deploy auf Fly.io (optional)

```bash
# Auth
fly auth login

# Deploy
fly deploy

# Secrets setzen
fly secrets set API_KEY=dein-sicherer-key
fly secrets set COINBASE_API_KEY=...
fly secrets set COINBASE_API_SECRET=...
```

---

## 📊 Dein aktueller Status

```
Portfolio:     €53,450
Ziel:          €1,000,000
Fortschritt:   5.35%
Zeit:          4.2 Jahre
Benötigt:      ~33% p.a. (sehr ambitioniert!)

Alternativen:
- +€1,500/Monat bei 10% Return
- +€800/Monat bei 15% Return  
- +€300/Monat bei 20% Return
```

---

## 💡 Erste Schritte

### 1. Status Report
Frage dein GPT: **"Wie steht's?"**

Es wird: `/goal/status` aufrufen und dir sagen:
- Progress %
- On-Track Status
- Health Score
- Empfehlungen

### 2. Portfolio Optimieren
Frage: **"Soll ich mehr Risiko gehen?"**

GPT analysiert:
- Aktuelle Allokation (60% Gold!)
- Empfohlen: Mehr Crypto für höheren Return
- Risiko vs. Chance Trade-off

### 3. Tax-Optimierung
Frage: **"Soll ich [Asset] verkaufen?"**

GPT checkt `/tax/recommend/{asset}`:
- Welche Coins sind steuerfrei?
- FIFO Optimierung
- Steuer-Ersparnis berechnen

### 4. Strategie anpassen
"**Ich will 20% mehr Risiko**"

GPT:
- Neue Allokation berechnen
- POST `/state/update` mit neuer Strategie
- Konsequenzen erklären

---

## 🎯 Realistische Szenarien

### Szenario 1: Konservativ
- **Return**: 10% p.a.
- **Benötigt**: +€1,500/Monat
- **Ergebnis**: ~€1M bis 2030
- **Risk**: Niedrig

### Szenario 2: Moderat
- **Return**: 15% p.a.
- **Benötigt**: +€800/Monat
- **Ergebnis**: ~€1M bis 2030
- **Risk**: Medium
- **Empfehlung**: ✅ Diese Balance!

### Szenario 3: Aggressiv
- **Return**: 20% p.a.
- **Benötigt**: +€300/Monat
- **Ergebnis**: ~€1M bis 2030
- **Risk**: Hoch
- **Warnung**: Sehr viel Risiko für ~€53k Start

---

## 📈 Health Score Details

Der Health Score (0-100) misst:

- **Progress**: Wie weit bist du? (25%)
- **Timing**: Bist du auf Kurs? (25%)
- **Momentum**: Entwickelst du dich gut? (50%)

**Interpretation**:
- 🟢 80-100: Exzellent
- 🟡 60-80: Auf Kurs
- 🟠 40-60: Leicht zurück
- 🔴 <40: Schwierig

---

## 🔄 Workflow-Beispiele

### Täglich
```
User: "Wie steht's?"
→ GPT: [interpretiert /goal/status]
→ Response: "🟢 Auf Kurs! 5.4% Progress..."
```

### Verkauf
```
User: "Soll ich Gold verkaufen?"
→ GPT: [checkt /tax/recommend/GOLD]
→ Response: "Ja, aber verkaufe erst nächste Woche wenn steuerfrei..."
```

### Strategie
```
User: "Ich will mehr Crypto"
→ GPT: [berechnet neue Allokation]
→ POST /state/update
→ Response: "Strategie angepasst! 40% Gold, 60% Crypto..."
```

---

## 🚀 System ready!

**Dein Backend ist fertig!**
- Portfolio geladen
- Ziel konfiguriert
- APIs ready
- Tax-Optimierung aktiv

**Nächster Schritt:**
1. Backend starten: `python main.py`
2. GPT mit `GPT_PROMPT.md` konfigurieren
3. Loss fragen: "Wie steht's?" 🎯

---

**Viel Erfolg zur Million! 💰**


