"""
Quick API Tests für AdAstraGPT Backend
"""

import requests
import json

BASE_URL = "http://localhost:8080"

def test_health():
    """Test /health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_portfolio():
    """Test /portfolio/live endpoint"""
    response = requests.get(f"{BASE_URL}/portfolio/live")
    print(f"\nPortfolio: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_update_strategy(api_key: str):
    """Test strategy update"""
    data = {
        "target": {"gold": 0.6, "crypto": 0.4},
        "cash_buffer": 0.05,
        "mode": "active"
    }
    response = requests.post(
        f"{BASE_URL}/state/update",
        json=data,
        headers={"x-api-key": api_key}
    )
    print(f"\nStrategy Update: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_log_decision(api_key: str):
    """Test decision logging"""
    data = {
        "timestamp": "2025-10-27T12:00:00Z",
        "summary": "Rebalance empfohlen",
        "actions": [
            {"type": "buy", "asset": "BTC", "amount": 0.1},
            {"type": "sell", "asset": "FET", "amount": 2000}
        ]
    }
    response = requests.post(
        f"{BASE_URL}/logs/decision",
        json=data,
        headers={"x-api-key": api_key}
    )
    print(f"\nDecision Log: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_backup(api_key: str):
    """Test backup dump"""
    response = requests.get(
        f"{BASE_URL}/backup/dump",
        headers={"x-api-key": api_key}
    )
    print(f"\nBackup: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("🧪 AdAstraGPT API Tests")
    print("=" * 50)
    
    # Health check (kein API Key benötigt)
    test_health()
    
    # Portfolio (kein API Key)
    test_portfolio()
    
    # Strategy update (benötigt API Key)
    API_KEY = input("\nAPI Key eingeben (oder Enter für 'dev-key-change-me-in-production'): ").strip()
    if not API_KEY:
        API_KEY = "dev-key-change-me-in-production"
    
    test_update_strategy(API_KEY)
    test_log_decision(API_KEY)
    test_backup(API_KEY)
    
    print("\n✅ Tests abgeschlossen!")


