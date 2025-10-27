# 🚀 GitHub Actions Auto-Deploy Setup

## Was zu tun ist (5 Minuten)

### 1. Fly.io API Token holen

```bash
# Auf deinem Mac (wo Fly CLI installiert ist):
fly auth token
```

Das gibt dir einen Token wie: `flyv1_dR7x...`

### 2. Token in GitHub Secrets eintragen

1. Gehe zu: https://github.com/bschels/-ad-astra-gpt/settings/secrets/actions
2. Click "New repository secret"
3. Name: `FLY_API_TOKEN`
4. Value: Den Token von Step 1 einfügen
5. Click "Add secret"

### 3. Workflow manuell triggern

1. Gehe zu: https://github.com/bschels/-ad-astra-gpt/actions
2. Click auf "Deploy AdAstraGPT to Fly.io"
3. Click "Run workflow" (Dropdown rechts oben)
4. Click "Run workflow" (Button)

**FERTIG!** Deployment läuft automatisch.

---

## Alternativ: Direkt auf Mac deployen

```bash
# Clone
git clone https://github.com/bschels/-ad-astra-gpt.git
cd -ad-astra-gpt

# Auth
fly auth login

# Deploy
fly deploy
fly secrets set API_KEY=dein-key
```

---

**Wähle eine Option - GitHub Actions oder manuell auf Mac!**

