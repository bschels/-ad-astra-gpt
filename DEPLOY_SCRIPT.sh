#!/bin/bash
# AdAstraGPT Deployment Script

echo "🚀 AdAstraGPT - Deployment Script"
echo "=================================="
echo ""

# Check if flyctl is installed
if ! command -v fly &> /dev/null
then
    echo "❌ Fly CLI nicht installiert!"
    echo "Installiere mit: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

echo "✅ Fly CLI gefunden"

# Login check
echo ""
echo "1. Login zu Fly.io..."
fly auth whoami

# Create app if not exists
echo ""
echo "2. App erstellen..."
fly apps create ad-astra-gpt || echo "App existiert bereits"

# Create volume for data
echo ""
echo "3. Volume erstellen..."
fly volumes create adastra_data_vol --size 1 --region fra || echo "Volume existiert bereits"

# Set secrets
echo ""
echo "4. Secrets setzen..."
read -s -p "API Key eingeben: " api_key
echo ""
fly secrets set "API_KEY=$api_key"

echo ""
echo "✅ Secrets gesetzt"

# Deploy
echo ""
echo "5. Deploy..."
fly deploy

echo ""
echo "🎉 Deployment abgeschlossen!"
echo ""
echo "Teste mit:"
echo "  curl https://ad-astra-gpt.fly.dev/health"
echo "  curl https://ad-astra-gpt.fly.dev/goal/status"
echo ""


