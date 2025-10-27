# 🚀 Push AdAstraGPT auf GitHub - Anleitung

## 📦 Was du jetzt hast

**Local Repository erstellt:**
```
✓ Git init
✓ 31 Dateien committed
✓ Ready to push
```

---

## 🚀 Push auf GitHub (3 Möglichkeiten)

### Option 1: GitHub CLI (Einfach)

```bash
# GitHub CLI installieren (falls nicht da)
winget install GitHub.cli

# Login
gh auth login

# Repo erstellen + pushen
gh repo create ad-astra-gpt --public --source=. --remote=origin --push
```

### Option 2: GitHub Website + Git Push (Manuell)

**Schritt 1: GitHub Repo erstellen**
1. Gehe zu https://github.com/new
2. Name: `ad-astra-gpt`
3. Public oder Private
4. **KEINE** README, .gitignore etc. (haben wir schon)
5. Click "Create repository"

**Schritt 2: Push**
```bash
git remote add origin https://github.com/bschels/ad-astra-gpt.git
git branch -M main
git push -u origin main
```

### Option 3: Auf deinem Mac (Empfohlen)

Da auf Windows Git-Installation kompliziert ist:

1. **Folder auf Mac kopieren**
   - Via iCloud/USB/Git
   
2. **Auf Mac:**
```bash
cd ~/Downloads/AdAstraGPT  # oder wo der Folder ist

# GitHub erstellen (fals noch nicht)
gh repo create ad-astra-gpt --public

# Oder manuell auf github.com/new

# Dann pushen
git remote add origin https://github.com/bschels/ad-astra-gpt.git
git push -u origin main
```

---

## ✅ Nach dem Push

**Dein Code ist online auf:**
```
https://github.com/bschels/ad-astra-gpt
```

**Dann kannst du:**
- Von überall darauf zugreifen
- Deployen von jedem PC
- Collaborator hinzufügen
- Weiter entwickeln

---

## 🎯 Schnellste Option

**Auf deinem Mac (2 Min):**
```bash
cd ~/Downloads/Nodus  # Folder name auf Mac ändern zu AdAstraGPT wenn du willst

# GitHub CLI verwenden
gh repo create ad-astra-gpt --public --source=. --remote=origin --push
```

**Done!** Dann ist alles online.

---

**Code ist lokal committed, bereit zum pushen! 📦**


