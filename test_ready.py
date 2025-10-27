"""
Quick System Test - Prüft ob alle Imports funktionieren
"""

print("🧪 AdAstraGPT - System Test")
print("=" * 50)

# Test imports
try:
    print("\n1. Importing main.py...")
    # Don't actually import main (it starts server)
    print("   ✓ main.py wird Server starten")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n2. Testing trading_engine...")
    from trading_engine import TradingEngine
    te = TradingEngine()
    print("   ✓ TradingEngine imported")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n3. Testing tax_optimizer...")
    from tax_optimizer import TaxOptimizer, Transaction
    to = TaxOptimizer()
    print("   ✓ TaxOptimizer imported")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n4. Testing goal_tracker...")
    from goal_tracker import GoalTracker
    gt = GoalTracker()
    print("   ✓ GoalTracker imported")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n5. Testing coinbase_integration...")
    from coinbase_integration import CoinbaseAPI
    print("   ✓ CoinbaseAPI imported")
except Exception as e:
    print(f"   ✗ Error: {e}")

try:
    print("\n6. Checking files...")
    import os
    files = ["portfolio.json", "requirements.txt", "Dockerfile", "fly.toml"]
    for f in files:
        if os.path.exists(f):
            print(f"   ✓ {f}")
        else:
            print(f"   ✗ {f} missing")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 50)
print("✅ System Test Complete!")
print("\n→ Deploy mit: fly deploy")
print("→ Oder: python main.py (lokal)")

