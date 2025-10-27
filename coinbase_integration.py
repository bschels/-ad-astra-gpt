"""
AdAstraGPT Coinbase Integration
Direct API access for automatic transaction import
"""

import requests
import hmac
import hashlib
import base64
import time
from typing import List, Dict, Optional
from datetime import datetime

class CoinbaseAPI:
    """Coinbase API Integration for AdAstraGPT"""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.coinbase.com/api/v3"
        self.brokerage_base = "https://api.coinbase.com/api/v3/brokerage"
        
    def _generate_signature(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """Generate Coinbase API signature"""
        message = f"{timestamp}{method}{path}{body}".encode()
        secret = base64.b64decode(self.api_secret)
        signature = hmac.new(secret, message, hashlib.sha256).digest()
        return base64.b64encode(signature).decode()
    
    def _make_request(self, method: str, path: str, body: Optional[Dict] = None) -> Dict:
        """Make authenticated API request"""
        timestamp = str(int(time.time()))
        
        body_str = ""
        if body:
            import json
            body_str = json.dumps(body, separators=(',', ':'))
        
        signature = self._generate_signature(timestamp, method, path, body_str)
        
        headers = {
            "CB-ACCESS-KEY": self.api_key,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "CB-ACCESS-SIGN": signature,
            "Content-Type": "application/json"
        }
        
        url = f"{self.brokerage_base}{path}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body_str, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    
    def get_accounts(self) -> List[Dict]:
        """Get all trading accounts"""
        try:
            data = self._make_request("GET", "/accounts")
            accounts = []
            
            for acc in data.get("accounts", []):
                # Only trade accounts, not wallets
                if acc.get("type") == "ACCOUNT_TYPE_CRYPTO_CURRENCY":
                    balance = acc.get("available_balance", {})
                    if balance:
                        accounts.append({
                            "account_id": acc.get("uuid"),
                            "currency": acc.get("currency"),
                            "available": float(balance.get("value", 0)),
                            "hold": float(acc.get("hold", {}).get("value", 0)),
                            "type": acc.get("type")
                        })
            
            return accounts
            
        except Exception as e:
            print(f"⚠️ Coinbase accounts error: {e}")
            return []
    
    def get_portfolio_balances(self) -> Dict:
        """Get current portfolio balances"""
        accounts = self.get_accounts()
        
        portfolio = {
            "cash_usd": 0,
            "assets": []
        }
        
        for acc in accounts:
            currency = acc["currency"]
            amount = acc["available"]
            
            if currency == "USD":
                portfolio["cash_usd"] += amount
            else:
                portfolio["assets"].append({
                    "symbol": currency,
                    "quantity": amount,
                    "source": "coinbase"
                })
        
        return portfolio
    
    def get_transaction_history(self, start_date: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get transaction history"""
        try:
            # Note: This is a simplified version
            # Real implementation would need to use proper transaction endpoints
            path = f"/orders?limit={limit}"
            
            data = self._make_request("GET", path)
            
            transactions = []
            
            for order in data.get("orders", []):
                # Parse order data
                t_type = "buy" if order.get("side") == "ORDER_SIDE_BUY" else "sell"
                
                transactions.append({
                    "id": order.get("order_id"),
                    "date": order.get("creation_time", datetime.now().isoformat()),
                    "type": t_type,
                    "asset": order.get("product_id", "").split("-")[0],
                    "quantity": float(order.get("quantity", 0)),
                    "price": float(order.get("average_filled_price", 0)),
                    "total": float(order.get("total_value", 0)),
                    "status": order.get("order_placement_source"),
                    "source": "coinbase"
                })
            
            return transactions
            
        except Exception as e:
            print(f"⚠️ Transaction history error: {e}")
            return []
    
    def get_market_data(self, product_id: str) -> Dict:
        """Get market data for a product"""
        try:
            path = f"/products/{product_id}"
            data = self._make_request("GET", path)
            
            return {
                "symbol": product_id.split("-")[0],
                "price": float(data.get("price", 0)),
                "volume_24h": float(data.get("volume_24h", 0)),
                "best_bid": float(data.get("best_bid", 0)),
                "best_ask": float(data.get("best_ask", 0))
            }
            
        except Exception as e:
            print(f"⚠️ Market data error: {e}")
            return {}
    
    def sync_transactions(self) -> Dict:
        """Sync all transactions from Coinbase"""
        accounts = self.get_accounts()
        history = self.get_transaction_history()
        
        # Get balances
        portfolio = self.get_portfolio_balances()
        
        return {
            "accounts": accounts,
            "transactions": history,
            "portfolio": portfolio,
            "synced_at": datetime.now().isoformat()
        }

