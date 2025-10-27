# 🚀 AdAstraGPT - Deploy Anleitung

## Schritt 1: Fly.io Account erstellen

Falls noch nicht vorhanden:
1. Gehe zu https://fly.io
2. Signup mit GitHub (kostenlos)
3. Install Fly CLI (falls nicht da)

```bash
# Windows PowerShell
# Download: https://fly.io/docs/getting-started/installing-flyctl/
```

---

## Schritt 2: Project zum Mac/deinem PC pushen

**Option A: Git Repository (empfohlen)**
```bash
git init
git add .
git commit -m "Initial commit - AdAstraGPT"
git remote add origin <dein-repo>
git push -u origin main
```

**Option B: Alle Dateien kopieren**
- Alles in .zip packen
- Auf deinen Mac/crypto-PC kopieren
- Dort deployen

---

## Schritt 3: Auf Fly.io deployen

```bash
# 1. Login
fly auth login

# 2. App erstellen
fly apps create ad-astra-gpt

# 3. Volume für Daten erstellen
fly volumes create adastra_data_vol --size 1 --region fra

# 4. Secrets setzen
fly secrets set API_KEY=dein-super-geheimer-key-2024

# 5. Deploy
fly deploy
```

---

## Schritt 4: Testen

Nach dem Deploy:

```bash
# Health Check
curl https://ad-astra-gpt.fly.dev/health

# Status
curl https://ad-astra-gpt.fly.dev/goal/status

# Markets
curl https://ad-astra-gpt.fly.dev/markets/overview
```

---

## Schritt 5: GPT konfigurieren

1. Öffne ChatGPT/Custom GPT
2. Kopiere `GPT_PROMPT.md` als System Prompt
3. Füge Actions hinzu:
   - GET /goal/status
   - GET /portfolio/live
   - GET /tax/recommend/{asset}
   - POST /state/update
   - GET /markets/overview

4. Backend URL: `https://ad-astra-gpt.fly.dev`

---

## Schritt 6: Loslegen! 🎯

**Frage dein GPT:**
- "Wie steht's?"
- "Bin ich auf Kurs?"
- "Was sollte ich ändern?"
- "Soll ich Gold verkaufen?"

---

## Probleme? Debugging

```bash
# Logs ansehen
fly logs

# SSH in Container
fly ssh console

# App neu starten
fly apps restart ad-astra-gpt
```

