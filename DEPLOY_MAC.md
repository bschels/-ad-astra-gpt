# 🍎 AdAstraGPT - Deploy auf Mac

## Was du jetzt hast

**Alle Dateien sind im Ordner:** `C:\Users\kruckoy\Downloads\Nodus`

**Für Mac Deployment:**
1. Folder auf Mac kopieren (via USB, iCloud, oder Git)
2. `cd` in den Folder
3. `fly deploy` ausführen

---

## 🚀 Schnell-Deploy auf Mac (2 Minuten)

### 1. Dateien auf Mac holen

**Option A: iCloud**
- Kopiere gesamten `Nodus` Folder nach iCloud Drive
- Öffne auf Mac

**Option B: Git (empfohlen)**
```bash
# Auf Windows-PC (Cursor):
git init
git add .
git commit -m "Initial AdAstraGPT"
git remote add origin <dein-repo-url>
git push

# Auf Mac:
git clone <dein-repo-url>
cd Nodus
```

**Option C: USB/Manuell**
- Zip erstellen auf Windows
- Auf Mac entpacken

---

### 2. Auf Mac: Terminal öffnen

```bash
# In den Nodus Folder
cd ~/Downloads/Nodus  # oder wo dein Folder ist

# Fly CLI installieren (falls nicht da)
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Volume erstellen
fly volumes create adastra_data_vol --size 1 --region fra

# API Key setzen
fly secrets set API_KEY=dein-super-sicherer-key-2024

# DEPLOY!
fly deploy
```

---

### 3. Testen

Nach Deploy:
```bash
# Browser öffnen:
https://ad-astra-gpt.fly.dev/health
https://ad-astra-gpt.fly.dev/goal/status

# Oder Terminal:
curl https://ad-astra-gpt.fly.dev/health
```

---

### 4. GPT konfigurieren

1. Öffne ChatGPT/Custom GPT
2. System Prompt einfügen (aus `GPT_PROMPT.md`)
3. Actions hinzufügen:
   - URL: `https://ad-astra-gpt.fly.dev`
   - Endpoints: `/goal/status`, `/portfolio/live`, etc.

---

## ✅ Fertig!

**Dann kannst du fragen:**
- "Wie steht's?"
- "Bin ich auf Kurs?"
- "Was sollte ich ändern?"

---

## 📝 Quick Commands

```bash
# Deploy
fly deploy

# Logs ansehen
fly logs

# SSH ins System
fly ssh console

# Secrets ändern
fly secrets set API_KEY=neuer-key

# Restart
fly apps restart ad-astra-gpt
```

**Los geht's! 🚀**


