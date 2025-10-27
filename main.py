"""
AdAstraGPT Backend - Lightweight FastAPI Server
Designed for Fly.io Free Tier
"""

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import json
import os
import gzip
from trading_engine import TradingEngine
from tax_optimizer import TaxOptimizer, Transaction
from coinbase_integration import CoinbaseAPI
from goal_tracker import GoalTracker

app = FastAPI(title="AdAstraGPT Backend", version="1.0.0")

# Data directory (works locally and in Docker)
DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.getcwd(), "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize Trading Engine, Tax Optimizer & Goal Tracker
trading_engine = TradingEngine()
tax_optimizer = TaxOptimizer()
goal_tracker = GoalTracker()

# Setup default million goal with user's current portfolio
portfolio_path = os.path.join(DATA_DIR, "portfolio.json")
starting_amount = 0

# Try to load current portfolio value
if os.path.exists(portfolio_path):
    with open(portfolio_path, "r") as f:
        portfolio = json.load(f)
        # Rough estimate from current holdings
        starting_amount = 53450  # User's reported value

# Initialize goal with persistence
goal_tracker.set_million_goal(target_year=2030, starting_amount=starting_amount)

# Load historical transactions if they exist
transactions_file = os.path.join(DATA_DIR, "transactions.json")
if os.path.exists(transactions_file):
    with open(transactions_file, "r") as f:
        transactions = json.load(f)
        for tx_data in transactions:
            tx = Transaction(**tx_data)
            tax_optimizer.add_transaction(tx)

# API Key Authentication
API_KEY_NAME = "x-api-key"
api_key_value = os.getenv("API_KEY", "dev-key-change-me-in-production")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != api_key_value:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# Pydantic Models
class Asset(BaseModel):
    symbol: str
    quantity: float
    avg_buy: Optional[float] = None

class Portfolio(BaseModel):
    assets: List[Asset]
    cash_eur: Optional[float] = 0
    gold_oz: Optional[float] = 0  # Gold holdings in ounces
    timestamp: str

class Strategy(BaseModel):
    target: dict
    cash_buffer: float
    mode: str

class DecisionLog(BaseModel):
    timestamp: str
    summary: str
    actions: List[dict]

# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    return {"service": "AdAstraGPT Backend", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/markets/overview")
async def get_market_overview():
    """Get overall market overview with all metrics"""
    # Fetch top 100 markets
    markets = trading_engine.get_top_100_markets()
    
    # Fetch gold price
    gold = trading_engine.get_gold_price()
    
    # Calculate market metrics
    total_market_cap = sum(m.get("market_cap", 0) for m in markets if m.get("market_cap"))
    total_volume = sum(m.get("volume_24h", 0) for m in markets if m.get("volume_24h"))
    
    # Top gainers/losers
    top_gainers = sorted(markets, key=lambda x: x.get("price_change_24h", 0), reverse=True)[:10]
    top_losers = sorted(markets, key=lambda x: x.get("price_change_24h", 0))[:10]
    
    return {
        "total_market_cap_usd": total_market_cap,
        "total_volume_24h_usd": total_volume,
        "gold": gold,
        "top_10_coins": markets[:10],
        "top_gainers_24h": top_gainers,
        "top_losers_24h": top_losers,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/portfolio/live")
async def get_portfolio_live():
    """Get current portfolio with LIVE prices and analysis"""
    # Load or generate top 100 cache first
    trading_engine.get_top_100_markets()
    
    file_path = os.path.join(DATA_DIR, "portfolio.json")
    
    if not os.path.exists(file_path):
        # Return mock data
        portfolio = {
            "assets": [
                {"symbol": "BTC", "quantity": 0.5, "avg_buy": 28000},
                {"symbol": "ETH", "quantity": 2.0, "avg_buy": 1600}
            ],
            "cash_eur": 2000,
            "gold_oz": 8.04,
            "timestamp": datetime.now().isoformat()
        }
    else:
        with open(file_path, "r") as f:
            portfolio = json.load(f)
    
    # Get symbols for live prices
    symbols = [asset["symbol"] for asset in portfolio.get("assets", [])]
    
    # Fetch LIVE prices (with enhanced data)
    prices = trading_engine.get_live_prices(symbols)
    
    # Fetch gold price if gold is held
    gold_price = None
    if portfolio.get("gold_oz", 0) > 0:
        gold_price = trading_engine.get_gold_price()
    
    # Calculate portfolio value and analysis
    analysis = trading_engine.calculate_portfolio_value(portfolio, prices, gold_price)
    
    return {
        "portfolio": portfolio,
        "analysis": analysis,
        "prices": prices,
        "gold_price": gold_price
    }

@app.post("/state/update")
async def update_state(
    strategy: Strategy,
    x_api_key: str = Depends(verify_api_key)
):
    """Save strategy or state JSON"""
    file_path = os.path.join(DATA_DIR, "strategy.json")
    
    data = strategy.model_dump()
    data["updated_at"] = datetime.now().isoformat()
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    return {"status": "updated", "timestamp": data["updated_at"]}

@app.post("/portfolio/update")
async def update_portfolio(
    portfolio: Portfolio,
    x_api_key: str = Depends(verify_api_key)
):
    """Update portfolio data"""
    file_path = os.path.join(DATA_DIR, "portfolio.json")
    
    data = portfolio.model_dump()
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    
    return {"status": "updated", "portfolio": data}

@app.post("/logs/decision")
async def log_decision(
    log: DecisionLog,
    x_api_key: str = Depends(verify_api_key)
):
    """Receive analysis logs"""
    file_path = os.path.join(DATA_DIR, "decisions.jsonl")
    
    log_entry = log.model_dump()
    
    # Append to JSONL file
    with open(file_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return {"status": "logged", "timestamp": log_entry["timestamp"]}

@app.get("/backup/dump")
async def backup_dump(x_api_key: str = Depends(verify_api_key)):
    """Get compressed JSON dump of all data"""
    backup = {
        "timestamp": datetime.now().isoformat(),
        "data": {}
    }
    
    # Collect all JSON files
    for filename in ["portfolio.json", "strategy.json"]:
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                backup["data"][filename.replace(".json", "")] = json.load(f)
    
    # Read decisions
    decisions_path = os.path.join(DATA_DIR, "decisions.jsonl")
    if os.path.exists(decisions_path):
        decisions = []
        with open(decisions_path, "r") as f:
            for line in f:
                if line.strip():
                    decisions.append(json.loads(line))
        backup["data"]["decisions"] = decisions[-100:]  # Last 100
    
    return JSONResponse(content=backup)

@app.get("/logs/recent")
async def get_recent_logs(limit: int = 10):
    """Get recent decision logs"""
    decisions_path = os.path.join(DATA_DIR, "decisions.jsonl")
    
    if not os.path.exists(decisions_path):
        return {"logs": []}
    
    decisions = []
    with open(decisions_path, "r") as f:
        lines = f.readlines()[-limit:]
        for line in lines:
            if line.strip():
                decisions.append(json.loads(line))
    
    return {"logs": decisions}

@app.get("/portfolio/analyze")
async def analyze_portfolio():
    """Get deep portfolio analysis with rebalancing suggestions"""
    # Load portfolio
    portfolio_path = os.path.join(DATA_DIR, "portfolio.json")
    if not os.path.exists(portfolio_path):
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    with open(portfolio_path, "r") as f:
        portfolio = json.load(f)
    
    # Load strategy
    strategy_path = os.path.join(DATA_DIR, "strategy.json")
    strategy = {}
    if os.path.exists(strategy_path):
        with open(strategy_path, "r") as f:
            strategy = json.load(f)
    else:
        strategy = {
            "target": {"BTC": 0.4, "ETH": 0.4, "CASH": 0.2},
            "cash_buffer": 0.1,
            "mode": "active"
        }
    
    # Get live prices
    symbols = [asset["symbol"] for asset in portfolio.get("assets", [])]
    prices = trading_engine.get_live_prices(symbols)
    
    # Fetch gold price if applicable
    gold_price = None
    if portfolio.get("gold_oz", 0) > 0:
        gold_price = trading_engine.get_gold_price()
    
    # Full analysis (with gold support)
    analysis = trading_engine.analyze_portfolio(portfolio, prices, strategy, gold_price)
    
    # Add trading signals
    asset_values = analysis.get("assets", [])
    signals = trading_engine.generate_trading_signals(asset_values)
    
    # Risk checks
    risk_checks = trading_engine.check_risk_limits(portfolio, prices)
    
    return {
        "analysis": analysis,
        "signals": signals,
        "risk_checks": risk_checks,
        "recommendations": [
            s for s in analysis.get("suggestions", []) 
            if abs(s.get("diff_pct", 0)) > 5
        ]
    }

@app.get("/strategies/current")
async def get_current_strategy():
    """Get current strategy"""
    file_path = os.path.join(DATA_DIR, "strategy.json")
    
    if not os.path.exists(file_path):
        return {
            "target": {"gold": 0.6, "crypto": 0.4},
            "cash_buffer": 0.05,
            "mode": "review"
        }
    
    with open(file_path, "r") as f:
        return json.load(f)

@app.get("/markets/top100")
async def get_top_100_markets():
    """Get top 100 cryptocurrencies with complete metrics"""
    markets = trading_engine.get_top_100_markets()
    return {
        "markets": markets,
        "count": len(markets),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/markets/gold")
async def get_gold_price():
    """Get live gold price"""
    gold = trading_engine.get_gold_price()
    return {
        "gold": gold,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/prices/live/{symbols}")
async def get_live_prices(symbols: str):
    """Get live prices for comma-separated symbols"""
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    prices = trading_engine.get_live_prices(symbol_list)
    return {"prices": prices, "timestamp": datetime.now().isoformat()}

@app.get("/tax/holdings/{asset}")
async def get_tax_status(asset: str):
    """Get tax status for asset holdings (German 1-year rule)"""
    status = tax_optimizer.get_current_tax_status(asset)
    return status

@app.get("/tax/soon")
async def get_tax_free_soon(days: int = 30):
    """Get assets that will become tax-free soon"""
    soon = tax_optimizer.get_tax_free_soon(days)
    return {"upcoming_tax_free": soon, "days_ahead": days}

@app.get("/tax/recommend/{asset}")
async def get_tax_recommendation(asset: str, amount: float):
    """Get tax-optimized sell recommendation"""
    recommendation = tax_optimizer.recommend_tax_optimized_sell(asset, amount)
    return recommendation

@app.post("/coinbase/sync")
async def sync_coinbase(
    api_key: str,
    api_secret: str,
    x_api_key: str = Depends(verify_api_key)
):
    """Sync data from Coinbase"""
    try:
        cb = CoinbaseAPI(api_key, api_secret)
        sync_data = cb.sync_transactions()
        
        # Process transactions into tax optimizer
        for tx in sync_data.get("transactions", []):
            transaction = Transaction(
                date=tx["date"],
                asset=tx["asset"],
                t_type=tx["type"],
                amount=tx["quantity"],
                price=tx["price"],
                total=tx["total"]
            )
            tax_optimizer.add_transaction(transaction)
        
        return {
            "status": "synced",
            "transactions": len(sync_data.get("transactions", [])),
            "portfolio": sync_data.get("portfolio"),
            "synced_at": sync_data.get("synced_at")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/coinbase/portfolio")
async def get_coinbase_portfolio(
    api_key: str,
    api_secret: str,
    x_api_key: str = Depends(verify_api_key)
):
    """Get current portfolio from Coinbase"""
    try:
        cb = CoinbaseAPI(api_key, api_secret)
        portfolio = cb.get_portfolio_balances()
        return portfolio
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions/add")
async def add_transaction(
    asset: str,
    t_type: str,
    amount: float,
    price: float,
    date: str,
    x_api_key: str = Depends(verify_api_key)
):
    """Manually add a transaction"""
    try:
        total = amount * price
        tx = Transaction(date=date, asset=asset, t_type=t_type, amount=amount, price=price, total=total)
        tax_optimizer.add_transaction(tx)
        return {"status": "added", "transaction": tx.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/goal/status")
async def get_goal_status():
    """Get current status towards million goal"""
    return goal_tracker.get_status_report()

@app.post("/goal/update")
async def update_goal(
    current_value: float,
    contributions: float = 0,
    min_monthly: float = 200,
    x_api_key: str = Depends(verify_api_key)
):
    """Update goal progress"""
    result = goal_tracker.update_progress(current_value, contributions, min_monthly)
    return result

@app.get("/goal/simulate")
async def simulate_goal_scenarios():
    """Simulate different scenarios to reach goal"""
    # Get current portfolio value
    portfolio_path = os.path.join(DATA_DIR, "portfolio.json")
    current_value = 0
    
    if os.path.exists(portfolio_path):
        with open(portfolio_path, "r") as f:
            portfolio = json.load(f)
        
        # Get live prices and calculate value
        symbols = [asset["symbol"] for asset in portfolio.get("assets", [])]
        prices = trading_engine.get_live_prices(symbols)
        
        # Quick value calculation
        for asset in portfolio.get("assets", []):
            symbol = asset["symbol"]
            quantity = asset["quantity"]
            price = prices.get(symbol, {}).get("price", 0) if isinstance(prices.get(symbol), dict) else 0
            current_value += quantity * price
        
        current_value += portfolio.get("cash_eur", 0)
        
        # Add gold if present
        if portfolio.get("gold_oz", 0) > 0:
            gold_price = trading_engine.get_gold_price()
            if gold_price:
                current_value += portfolio["gold_oz"] * gold_price.get("price_per_oz", 0)
    
    scenarios = goal_tracker.simulate_scenarios(current_value)
    return {"current_value": current_value, "scenarios": scenarios}

@app.get("/goal/report")
async def get_full_report():
    """Get comprehensive progress report"""
    status = goal_tracker.get_status_report()
    
    # Add portfolio info
    portfolio_path = os.path.join(DATA_DIR, "portfolio.json")
    portfolio_info = {}
    
    if os.path.exists(portfolio_path):
        with open(portfolio_path, "r") as f:
            portfolio_info = json.load(f)
    
    return {
        "goal_status": status,
        "portfolio": portfolio_info,
        "message": _generate_status_message(status)
    }

def _generate_status_message(status: Dict) -> str:
    """Generate human-readable status message"""
    emoji = status["status_emoji"]
    text = status["status_text"]
    progress = status["progress_pct"]
    current = status["current"]
    target = status["target"]
    
    message = f"{emoji} {text}\n"
    message += f"Fortschritt: {progress:.1f}% (€{current:,.0f} von €{target:,.0f})\n"
    
    if not status["on_track"]:
        message += f"⚠️ Abweichung: {status['deviation_pct']:.1f}%\n"
        message += f"Benötigt: €{status['additional_monthly_needed']:.0f}/Monat zusätzlich"
    else:
        message += "✅ Auf Kurs!"
    
    return message

@app.get("/signals/generate")
async def generate_signals():
    """Generate trading signals for current portfolio"""
    portfolio_path = os.path.join(DATA_DIR, "portfolio.json")
    if not os.path.exists(portfolio_path):
        return {"signals": [], "message": "No portfolio found"}
    
    with open(portfolio_path, "r") as f:
        portfolio = json.load(f)
    
    symbols = [asset["symbol"] for asset in portfolio.get("assets", [])]
    prices = trading_engine.get_live_prices(symbols)
    
    # Calculate values
    analysis = trading_engine.calculate_portfolio_value(portfolio, prices)
    
    # Generate signals
    signals = trading_engine.generate_trading_signals(analysis.get("assets", []))
    
    return {
        "signals": signals,
        "portfolio_analysis": {
            "total_value": analysis["total_value_usd"],
            "total_pnl": analysis["total_pnl"],
            "roi_pct": analysis["roi_pct"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, workers=1, threads=2)
