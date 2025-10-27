"""
AdAstraGPT Trading Engine
Live Crypto Prices, Portfolio Analysis & Trading Logic
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime
import json

class TradingEngine:
    """Core Trading Logic for AdAstraGPT"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.price_cache = {}
        self.market_data_cache = {}
        
    def get_top_100_markets(self) -> List[Dict]:
        """Fetch top 100 cryptocurrencies with all metrics"""
        try:
            url = f"{self.base_url}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h,24h,7d,30d,1y"
            
            response = requests.get(url, timeout=15)
            data = response.json()
            
            markets = []
            for coin in data:
                markets.append({
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "id": coin["id"],
                    "price": coin["current_price"],
                    "market_cap": coin["market_cap"],
                    "volume_24h": coin["total_volume"],
                    "market_cap_rank": coin["market_cap_rank"],
                    "price_change_1h": coin.get("price_change_percentage_1h_in_currency", 0),
                    "price_change_24h": coin.get("price_change_percentage_24h_in_currency", 0),
                    "price_change_7d": coin.get("price_change_percentage_7d_in_currency", 0),
                    "price_change_30d": coin.get("price_change_percentage_30d_in_currency", 0),
                    "price_change_1y": coin.get("price_change_percentage_1y_in_currency", 0),
                    "high_24h": coin["high_24h"],
                    "low_24h": coin["low_24h"],
                    "circulating_supply": coin["circulating_supply"],
                    "total_supply": coin.get("total_supply"),
                    "ath": coin["ath"],
                    "ath_change_percentage": coin["ath_change_percentage"],
                    "from_ath_pct": coin["ath_change_percentage"]
                })
            
            self.market_data_cache = {m["symbol"]: m for m in markets}
            return markets
            
        except Exception as e:
            print(f"⚠️ Markets fetch error: {e}")
            return []
    
    def get_gold_price(self) -> Dict:
        """Fetch gold price in USD (using PAXG as proxy)"""
        try:
            url = f"{self.base_url}/simple/price?ids=pax-gold&vs_currencies=usd&include_24hr_change=true"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if "pax-gold" in data:
                return {
                    "price_per_oz": data["pax-gold"]["usd"],
                    "change_24h": data["pax-gold"].get("usd_24h_change", 0),
                    "symbol": "XAU",
                    "name": "Gold",
                    "unit": "USD per troy ounce"
                }
            return {}
            
        except Exception as e:
            print(f"⚠️ Gold price error: {e}")
            return {}
    
    def get_live_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Fetch live crypto prices from CoinGecko (enhanced with more data)"""
        try:
            # Use top 100 cache if available
            if self.market_data_cache:
                prices = {}
                for symbol in symbols:
                    symbol_upper = symbol.upper()
                    if symbol_upper in self.market_data_cache:
                        coin = self.market_data_cache[symbol_upper]
                        prices[symbol] = {
                            "price": coin["price"],
                            "change_24h": coin["price_change_24h"],
                            "change_7d": coin["price_change_7d"],
                            "change_30d": coin["price_change_30d"],
                            "market_cap": coin["market_cap"],
                            "volume_24h": coin["volume_24h"],
                            "market_cap_rank": coin["market_cap_rank"],
                            "from_ath_pct": coin["from_ath_pct"]
                        }
                return prices
            
            # Fallback to old method
            symbol_map = {
                "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
                "USDC": "usd-coin", "USDT": "tether", "XRP": "ripple",
                "ADA": "cardano", "DOT": "polkadot", "LINK": "chainlink",
                "MATIC": "matic-network", "FET": "fetch-ai", "ONDO": "ondo-finance",
                "ATOM": "cosmos", "ARB": "arbitrum", "OP": "optimism",
                "AVAX": "avalanche-2", "LUNA": "terra-luna", "NEAR": "near",
                "ALGO": "algorand", "FIL": "filecoin", "ICP": "internet-computer",
                "XTZ": "tezos", "EGLD": "elrond-erd-2", "HBAR": "hedera-hashgraph"
            }
            
            ids = [symbol_map.get(s.upper()) for s in symbols if s.upper() in symbol_map]
            ids_str = ",".join(ids)
            
            if not ids_str:
                return {}
            
            url = f"{self.base_url}/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_change=true,7d,30d"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            prices = {}
            for symbol in symbols:
                if symbol.upper() in symbol_map:
                    coin_id = symbol_map[symbol.upper()]
                    if coin_id in data:
                        prices[symbol] = {
                            "price": data[coin_id].get("usd", 0),
                            "change_24h": data[coin_id].get("usd_24h_change", 0),
                            "change_7d": data[coin_id].get("usd_7d_change", 0),
                            "change_30d": data[coin_id].get("usd_30d_change", 0)
                        }
            
            # Special handling for stablecoins
            for symbol in ["USDC", "USDT"]:
                if symbol in symbols:
                    prices[symbol] = {
                        "price": 1.0,
                        "change_24h": 0,
                        "change_7d": 0,
                        "change_30d": 0
                    }
            
            self.price_cache.update(prices)
            return prices
            
        except Exception as e:
            print(f"⚠️ Price fetch error: {e}")
            return {}
    
    def calculate_portfolio_value(self, portfolio: Dict, prices: Dict, gold_price: Optional[Dict] = None) -> Dict:
        """Calculate total portfolio value, P&L, ROI (including gold)"""
        total_value = 0
        asset_values = []
        
        # Process crypto assets
        for asset in portfolio.get("assets", []):
            symbol = asset.get("symbol", "").upper()
            quantity = asset.get("quantity", 0)
            avg_buy = asset.get("avg_buy", 0)
            
            current_price = prices.get(symbol, {}).get("price", 0) if isinstance(prices.get(symbol), dict) else prices.get(symbol, 0)
            current_value = quantity * current_price
            
            asset_info = {
                "symbol": symbol,
                "quantity": quantity,
                "avg_buy_price": avg_buy,
                "current_price": current_price,
                "current_value": current_value,
                "cost_basis": quantity * avg_buy if avg_buy else 0,
                "pnl": current_value - (quantity * avg_buy if avg_buy else 0),
                "roi_pct": ((current_price / avg_buy - 1) * 100) if avg_buy and avg_buy > 0 else 0
            }
            
            asset_values.append(asset_info)
            total_value += current_value
        
        # Add gold if present
        gold_value = 0
        gold_oz = portfolio.get("gold_oz", 0)
        if gold_oz > 0 and gold_price:
            gold_price_per_oz = gold_price.get("price_per_oz", 0)
            gold_value = gold_oz * gold_price_per_oz
            total_value += gold_value
            
            # Get gold avg buy price
            gold_avg_buy = portfolio.get("gold_avg_buy", 0)
            gold_cost_basis = gold_oz * gold_avg_buy if gold_avg_buy else 0
            gold_pnl = gold_value - gold_cost_basis
            gold_roi = ((gold_price_per_oz / gold_avg_buy - 1) * 100) if gold_avg_buy and gold_avg_buy > 0 else 0
            
            asset_values.append({
                "symbol": "XAU",
                "quantity": gold_oz,
                "name": "Gold",
                "current_price": gold_price_per_oz,
                "current_value": gold_value,
                "cost_basis": gold_cost_basis,
                "pnl": gold_pnl,
                "roi_pct": gold_roi
            })
        
        cash = portfolio.get("cash_eur", 0)
        total_value += cash
        
        # Calculate overall metrics
        total_cost_basis = sum(a["cost_basis"] for a in asset_values if a["cost_basis"] > 0)
        total_pnl = sum(a["pnl"] for a in asset_values)
        
        return {
            "total_value_usd": total_value,
            "cash_usd": cash,
            "crypto_value_usd": total_value - cash - gold_value,
            "gold_value_usd": gold_value,
            "total_cost_basis": total_cost_basis,
            "total_pnl": total_pnl,
            "roi_pct": (total_pnl / total_cost_basis * 100) if total_cost_basis > 0 else 0,
            "assets": asset_values,
            "gold_oz": gold_oz,
            "timestamp": datetime.now().isoformat()
        }
    
    def analyze_portfolio(self, portfolio: Dict, prices: Dict, strategy: Dict, gold_price: Optional[Dict] = None) -> Dict:
        """Analyze portfolio against strategy and suggest rebalancing"""
        analysis = self.calculate_portfolio_value(portfolio, prices, gold_price)
        
        # Get target allocations from strategy
        targets = strategy.get("target", {})
        cash_buffer = strategy.get("cash_buffer", 0.05)
        
        # Calculate current allocations
        total = analysis["total_value_usd"]
        current_allocations = {}
        
        for asset in analysis["assets"]:
            symbol = asset["symbol"]
            value = asset["current_value"]
            current_allocations[symbol] = value / total if total > 0 else 0
        
        current_cash_pct = analysis["cash_usd"] / total if total > 0 else 0
        
        # Calculate target vs actual
        rebalance_needed = False
        suggestions = []
        
        for target_symbol, target_pct in targets.items():
            current_pct = current_allocations.get(target_symbol, 0)
            diff_pct = target_pct - current_pct
            
            if abs(diff_pct) > 0.05:  # 5% deviation threshold
                rebalance_needed = True
                target_value = total * target_pct
                current_value = total * current_pct
                diff_value = target_value - current_value
                
                suggestions.append({
                    "symbol": target_symbol,
                    "current_pct": current_pct * 100,
                    "target_pct": target_pct * 100,
                    "diff_pct": diff_pct * 100,
                    "adjustment_usd": diff_value,
                    "action": "buy" if diff_value > 0 else "sell"
                })
        
        # Check cash buffer
        if current_cash_pct < cash_buffer:
            suggestions.append({
                "symbol": "CASH",
                "current_pct": current_cash_pct * 100,
                "target_pct": cash_buffer * 100,
                "adjustment_usd": total * (cash_buffer - current_cash_pct),
                "action": "increase_cash"
            })
            rebalance_needed = True
        
        analysis["current_allocations"] = current_allocations
        analysis["target_allocations"] = targets
        analysis["cash_buffer_pct"] = current_cash_pct * 100
        analysis["rebalance_needed"] = rebalance_needed
        analysis["suggestions"] = suggestions
        
        return analysis
    
    def generate_trading_signals(self, asset_values: List[Dict]) -> List[Dict]:
        """Generate trading signals based on technical analysis"""
        signals = []
        
        for asset in asset_values:
            symbol = asset["symbol"]
            change_24h = asset.get("change_24h", 0)
            roi = asset.get("roi_pct", 0)
            
            # Basic signal logic
            signal_strength = "neutral"
            signal_type = "hold"
            
            if change_24h > 10:
                signal_strength = "strong"
                signal_type = "buy" if roi > 50 else "take_profit"
            elif change_24h < -10:
                signal_strength = "strong"
                signal_type = "sell"
            elif change_24h > 5:
                signal_strength = "moderate"
                signal_type = "buy"
            elif change_24h < -5:
                signal_strength = "moderate"
                signal_type = "sell"
            
            signals.append({
                "symbol": symbol,
                "signal": signal_type,
                "strength": signal_strength,
                "reason": f"24h change: {change_24h:.2f}%, ROI: {roi:.2f}%"
            })
        
        return signals
    
    def check_risk_limits(self, portfolio: Dict, prices: Dict) -> Dict:
        """Check if portfolio is within risk limits"""
        analysis = self.calculate_portfolio_value(portfolio, prices)
        
        risk_checks = {
            "total_exposure_ok": True,
            "single_asset_concentration": {},
            "max_drawdown": 0,
            "liquidity_check": True
        }
        
        total_value = analysis["total_value_usd"]
        
        # Check single asset concentration
        for asset in analysis["assets"]:
            pct = asset["current_value"] / total_value if total_value > 0 else 0
            if pct > 0.4:  # 40% max concentration
                risk_checks["single_asset_concentration"][asset["symbol"]] = pct
                risk_checks["total_exposure_ok"] = False
        
        # Check max drawdown
        total_pnl_pct = analysis["roi_pct"]
        if total_pnl_pct < -20:  # 20% max loss
            risk_checks["max_drawdown"] = total_pnl_pct
            risk_checks["total_exposure_ok"] = False
        
        # Check liquidity (stablecoin ratio)
        stablecoins = ["USDC", "USDT"]
        stable_value = sum(
            a["current_value"] 
            for a in analysis["assets"] 
            if a["symbol"] in stablecoins
        )
        
        if stable_value / total_value < 0.1:  # At least 10% liquid
            risk_checks["liquidity_check"] = False
            risk_checks["total_exposure_ok"] = False
        
        return risk_checks

