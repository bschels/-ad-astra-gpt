"""
AdAstraGPT Tax Optimizer
Steueroptimierung für deutsche Haltefrist-Regelung (1 Jahr steuerfrei)
+ FIFO Trading Logic
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import deque

class Transaction:
    """Individual trade transaction"""
    def __init__(self, date: str, asset: str, t_type: str, amount: float, price: float, total: float):
        self.date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        self.asset = asset.upper()
        self.type = t_type.lower()  # 'buy' or 'sell'
        self.amount = amount
        self.price = price
        self.total = total
    
    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "asset": self.asset,
            "type": self.type,
            "amount": self.amount,
            "price": self.price,
            "total": self.total
        }

class TaxOptimizer:
    """German Tax Optimization (1 Year Holding Period)"""
    
    def __init__(self):
        self.transactions: Dict[str, deque] = {}  # Asset -> queue of transactions
        self.tax_free_threshold = timedelta(days=365)
        
    def add_transaction(self, tx: Transaction):
        """Add a transaction (FIFO)"""
        if tx.asset not in self.transactions:
            self.transactions[tx.asset] = deque()
        
        if tx.type == "buy":
            self.transactions[tx.asset].append(tx)
        elif tx.type == "sell":
            # Process sell using FIFO
            self._process_sell(tx)
    
    def _process_sell(self, sell_tx: Transaction):
        """Process sell transaction using FIFO and tax-free check"""
        if sell_tx.asset not in self.transactions:
            return
        
        sell_amount = sell_tx.amount
        tx_queue = self.transactions[sell_tx.asset]
        
        while sell_amount > 0 and tx_queue:
            buy_tx = tx_queue[0]
            
            if buy_tx.amount <= sell_amount:
                # Sell entire buy_tx amount
                cost_basis = buy_tx.amount * buy_tx.price
                sale_value = buy_tx.amount * sell_tx.price
                
                holding_period = sell_tx.date - buy_tx.date
                is_tax_free = holding_period >= self.tax_free_threshold
                
                # Remove from queue
                tx_queue.popleft()
                sell_amount -= buy_tx.amount
                
            else:
                # Partial sell
                cost_basis = sell_amount * buy_tx.price
                sale_value = sell_amount * sell_tx.price
                
                holding_period = sell_tx.date - buy_tx.date
                is_tax_free = holding_period >= self.tax_free_threshold
                
                # Update remaining
                buy_tx.amount -= sell_amount
                sell_amount = 0
    
    def calculate_taxable_gains(self, asset: str, as_of: datetime) -> Dict:
        """Calculate taxable gains for an asset"""
        if asset not in self.transactions:
            return {"tax_free_amount": 0, "taxable_amount": 0, "holdings": []}
        
        holdings = []
        for tx in self.transactions[asset]:
            holding_period = as_of - tx.date
            days_held = holding_period.days
            is_tax_free = holding_period >= self.tax_free_threshold
            
            holdings.append({
                "date": tx.date.isoformat(),
                "amount": tx.amount,
                "price": tx.price,
                "days_held": days_held,
                "is_tax_free": is_tax_free,
                "tax_free_date": (tx.date + self.tax_free_threshold).isoformat()
            })
        
        return {"holdings": holdings}
    
    def get_tax_free_soon(self, days_ahead: int = 30) -> List[Dict]:
        """Get assets that will become tax-free soon"""
        soon = []
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        for asset, tx_queue in self.transactions.items():
            for tx in tx_queue:
                tax_free_date = tx.date + self.tax_free_threshold
                if tx.date <= cutoff_date and not (tx.date <= datetime.now()):
                    soon.append({
                        "asset": asset,
                        "amount": tx.amount,
                        "buy_date": tx.date.isoformat(),
                        "becomes_tax_free": tax_free_date.isoformat(),
                        "days_remaining": (tax_free_date - datetime.now()).days
                    })
        
        return sorted(soon, key=lambda x: x["becomes_tax_free"])
    
    def get_current_tax_status(self, asset: str) -> Dict:
        """Get current tax status for asset holdings"""
        if asset not in self.transactions:
            return {
                "asset": asset,
                "total_amount": 0,
                "tax_free_amount": 0,
                "taxable_amount": 0,
                "breakdown": []
            }
        
        total_amount = 0
        tax_free_amount = 0
        breakdown = []
        
        now = datetime.now()
        
        for tx in self.transactions[asset]:
            holding_period = now - tx.date
            is_tax_free = holding_period >= self.tax_free_threshold
            days_held = holding_period.days
            
            total_amount += tx.amount
            if is_tax_free:
                tax_free_amount += tx.amount
            
            breakdown.append({
                "date": tx.date.isoformat(),
                "amount": tx.amount,
                "price": tx.price,
                "cost_basis": tx.amount * tx.price,
                "days_held": days_held,
                "is_tax_free": is_tax_free,
                "becomes_tax_free_date": (tx.date + self.tax_free_threshold).isoformat() if not is_tax_free else None
            })
        
        return {
            "asset": asset,
            "total_amount": total_amount,
            "tax_free_amount": tax_free_amount,
            "taxable_amount": total_amount - tax_free_amount,
            "breakdown": breakdown
        }
    
    def recommend_tax_optimized_sell(self, asset: str, target_amount: float) -> Dict:
        """Recommend which coins to sell for tax optimization"""
        if asset not in self.transactions:
            return {"recommendation": "no_holdings"}
        
        tx_queue = self.transactions[asset]
        now = datetime.now()
        
        recommendation = []
        remaining = target_amount
        
        for tx in tx_queue:
            if remaining <= 0:
                break
            
            holding_period = now - tx.date
            is_tax_free = holding_period >= self.tax_free_threshold
            days_to_free = (tx.date + self.tax_free_threshold - now).days if not is_tax_free else 0
            
            sell_amount = min(remaining, tx.amount)
            
            recommendation.append({
                "sell_amount": sell_amount,
                "buy_date": tx.date.isoformat(),
                "buy_price": tx.price,
                "is_tax_free": is_tax_free,
                "tax_free_now": is_tax_free,
                "days_to_tax_free": days_to_free if days_to_free > 0 else 0
            })
            
            remaining -= sell_amount
        
        # Sort: tax-free first, then by time to become tax-free
        recommendation.sort(key=lambda x: (not x["is_tax_free"], x["days_to_tax_free"]))
        
        total_tax_free = sum(r["sell_amount"] for r in recommendation if r["is_tax_free"])
        
        return {
            "asset": asset,
            "target_sell": target_amount,
            "recommendation": recommendation,
            "tax_free_in_sell": total_tax_free,
            "taxable_in_sell": target_amount - total_tax_free,
            "total_potential_tax_liability": (target_amount - total_tax_free) * 0.265 if (target_amount - total_tax_free) > 0 else 0  # ~26.5% in Germany
        }


