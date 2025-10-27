"""
AdAstraGPT Goal Tracker
Track progress towards financial goals (e.g. 1 Million by 2030)
"""

from typing import Dict, Optional, List
from datetime import datetime, timedelta
import math

class GoalTracker:
    """Track financial goals with realistic planning"""
    
    def __init__(self):
        self.goals = {}
        
    def set_million_goal(self, target_year: int = 2030, starting_amount: float = 0) -> Dict:
        """Set 1 Million Euro goal by target year"""
        now = datetime.now()
        target_date = datetime(target_year, 1, 1)
        years_remaining = (target_date - now).days / 365.25
        
        # Calculate required annual return
        if years_remaining <= 0:
            required_return = 0
        else:
            # PV * (1 + r)^n = FV
            # r = (FV/PV)^(1/n) - 1
            if starting_amount > 0:
                required_return = (1_000_000 / starting_amount) ** (1 / years_remaining) - 1
            else:
                required_return = math.inf
        
        self.goals["million_2030"] = {
            "target": 1_000_000,
            "target_year": target_year,
            "current": starting_amount,
            "years_remaining": years_remaining,
            "required_annual_return": required_return,
            "required_monthly_savings": self._calculate_monthly_savings(
                current=starting_amount,
                target=1_000_000,
                years=years_remaining,
                annual_return=0.10  # Assume 10% average return
            ),
            "created_at": now.isoformat(),
            "mantra": "1 Million bis 2030 - Unveränderlich",
            "min_monthly_contribution": 200
        }
        
        return self.goals["million_2030"]
    
    def _calculate_monthly_savings(self, current: float, target: float, years: float, annual_return: float) -> float:
        """Calculate required monthly savings to reach goal"""
        if years <= 0:
            return 0
        
        monthly_return = (1 + annual_return) ** (1/12) - 1
        months = years * 12
        
        # Formula for required monthly contribution:
        # PMT = (FV - PV * (1+r)^n) / (((1+r)^n - 1) / r)
        if monthly_return > 0:
            fv_factor = (1 + monthly_return) ** months
            monthly_payment = (target - current * fv_factor) / (((fv_factor - 1) / monthly_return) if monthly_return > 0 else months)
        else:
            monthly_payment = (target - current) / months
        
        return max(0, monthly_payment)
    
    def update_progress(self, current_value: float, contributions: float = 0, min_monthly: float = 200) -> Dict:
        """Update progress towards goal"""
        if "million_2030" not in self.goals:
            return {"status": "no_goal_set"}
        
        goal = self.goals["million_2030"]
        now = datetime.now()
        target_date = datetime(goal["target_year"], 1, 1)
        
        # Calculate progress
        target = goal["target"]
        years_passed = (now - datetime.fromisoformat(goal["created_at"])).days / 365.25
        years_remaining = goal["years_remaining"]
        total_years = years_passed + years_remaining
        
        # Progress percentage
        progress_pct = (current_value / target) * 100
        
        # Are we on track?
        expected_value = goal["current"] * (1 + goal["required_annual_return"]) ** years_passed
        on_track = current_value >= expected_value
        deviation = current_value - expected_value
        deviation_pct = (deviation / expected_value * 100) if expected_value > 0 else 0
        
        # Required action if off-track
        if not on_track:
            # How much more do we need per month?
            additional_monthly = self._calculate_monthly_savings(
                current=current_value,
                target=target,
                years=years_remaining,
                annual_return=0.10
            )
        else:
            additional_monthly = 0
        
        # Projection
        assumed_return = 0.10  # 10% annual
        projected_end_value = current_value * (1 + assumed_return) ** years_remaining
        
        goal["current"] = current_value
        goal["progress_pct"] = progress_pct
        goal["on_track"] = on_track
        goal["deviation"] = deviation
        goal["deviation_pct"] = deviation_pct
        goal["additional_monthly_needed"] = additional_monthly
        goal["projected_end_value"] = projected_end_value
        goal["updated_at"] = now.isoformat()
        
        # Calculate with minimum €200/month contribution
        total_months = years_remaining * 12
        total_contributions = min_monthly * total_months
        future_value_with_contributions = current_value * (1 + assumed_return) ** years_remaining + total_contributions
        goal["future_with_min_contributions"] = future_value_with_contributions
        
        # Ultra-aggressive scenario (what would be needed)
        missing_amount = 1_000_000 - future_value_with_contributions
        ultra_aggressive_return = (1_000_000 / (current_value + total_contributions)) ** (1/years_remaining) - 1
        goal["ultra_aggressive_return_needed"] = ultra_aggressive_return * 100
        goal["missing_with_current_strategy"] = missing_amount
        
        return goal
    
    def get_status_report(self) -> Dict:
        """Get comprehensive status report"""
        if "million_2030" not in self.goals:
            return {"error": "No goal set"}
        
        goal = self.goals["million_2030"]
        
        now = datetime.now()
        target_date = datetime(goal["target_year"], 1, 1)
        days_remaining = (target_date - now).days
        
        # Health score (0-100)
        progress_score = min(goal.get("progress_pct", 0) / 100, 1) * 50
        on_track_score = 50 if goal.get("on_track", False) else 0
        health_score = progress_score + on_track_score
        
        # Status emoji
        if health_score >= 80:
            status_emoji = "🟢"
            status_text = "Exzellent"
        elif health_score >= 60:
            status_emoji = "🟡"
            status_text = "Auf Kurs"
        elif health_score >= 40:
            status_emoji = "🟠"
            status_text = "Zurückfallen"
        else:
            status_emoji = "🔴"
            status_text = "Kritisch"
        
        return {
            "status_emoji": status_emoji,
            "status_text": status_text,
            "health_score": round(health_score, 1),
            "target": goal["target"],
            "current": goal.get("current", 0),
            "progress_pct": goal.get("progress_pct", 0),
            "on_track": goal.get("on_track", False),
            "deviation_pct": goal.get("deviation_pct", 0),
            "projected_end_value": goal.get("projected_end_value", 0),
            "days_remaining": days_remaining,
            "years_remaining": round(goal["years_remaining"], 1),
            "required_annual_return": goal["required_annual_return"] * 100,
            "additional_monthly_needed": goal.get("additional_monthly_needed", 0),
            "current_strategy_rating": self._rate_strategy(goal),
            "recommendations": self._get_recommendations(goal)
        }
    
    def _rate_strategy(self, goal: Dict) -> str:
        """Rate current strategy (1-5 stars)"""
        health = goal.get("health_score", 0)
        
        if health >= 80:
            return "⭐⭐⭐⭐⭐"
        elif health >= 60:
            return "⭐⭐⭐⭐"
        elif health >= 40:
            return "⭐⭐⭐"
        elif health >= 20:
            return "⭐⭐"
        else:
            return "⭐"
    
    def _get_recommendations(self, goal: Dict) -> List[str]:
        """Get actionable recommendations"""
        recommendations = []
        
        on_track = goal.get("on_track", True)
        deviation_pct = goal.get("deviation_pct", 0)
        current = goal.get("current", 0)
        target = goal.get("target", 1_000_000)
        
        if not on_track:
            if deviation_pct < -20:
                recommendations.append("⚠️ Deutlich hinter Plan! Erhöhe monatliche Sparrate.")
            if deviation_pct < -10:
                recommendations.append("💡 Betrachte aggressivere Asset-Allocation (mehr Risiko für mehr Return).")
            if deviation_pct < 0:
                recommendations.append("📈 Überprüfe Portfolio-Performance. Vielleicht besser diversifizieren?")
        
        if goal.get("additional_monthly_needed", 0) > 0:
            recommendations.append(f"💰 Benötige zusätzlich €{goal['additional_monthly_needed']:.0f}/Monat um Ziel zu erreichen.")
        
        if (target - current) / target > 0.3:  # Still far from goal
            recommendations.append("🎯 Bleib bei der Strategie. Langfristiges Investieren braucht Geduld.")
        
        # Check if projected end value is close to target
        projected = goal.get("projected_end_value", 0)
        if projected < target * 0.9:
            recommendations.append(f"📊 Bei aktueller Rate wirst du €{projected:.0f} erreichen. Strategie anpassen?")
        
        return recommendations if recommendations else ["✅ Alles auf Kurs! Weiter so!"]
    
    def simulate_scenarios(self, current_value: float) -> Dict:
        """Simulate different scenarios to reach goal"""
        goal = self.goals["million_2030"]
        years = goal["years_remaining"]
        target = goal["target"]
        
        scenarios = {
            "conservative": self._calculate_required_rate(current_value, target, years, 0.07),  # 7% return
            "moderate": self._calculate_required_rate(current_value, target, years, 0.10),    # 10% return
            "aggressive": self._calculate_required_rate(current_value, target, years, 0.15),  # 15% return
        }
        
        return scenarios
    
    def _calculate_required_rate(self, current: float, target: float, years: float, assumed_return: float) -> Dict:
        """Calculate required monthly savings for scenario"""
        final_value = current * (1 + assumed_return) ** years
        shortfall = target - final_value
        
        if shortfall > 0:
            monthly_savings = self._calculate_monthly_savings(0, shortfall, years, assumed_return)
        else:
            monthly_savings = 0
        
        success_probability = 1.0 if shortfall <= 0 else max(0, 1 - (shortfall / target))
        
        return {
            "assumed_annual_return": assumed_return * 100,
            "projected_value": final_value,
            "shortfall": shortfall,
            "required_monthly_savings": monthly_savings,
            "success_probability": success_probability
        }
    
    def get_health_score_details(self) -> Dict:
        """Get detailed health score breakdown"""
        if "million_2030" not in self.goals:
            return {}
        
        goal = self.goals["million_2030"]
        current = goal.get("current", 0)
        target = goal["target"]
        progress = goal.get("progress_pct", 0)
        on_track = goal.get("on_track", False)
        
        # Calculate different score components
        progress_score = min(progress / 10, 5)  # Max 5 points
        timing_score = 5 if on_track else max(0, 5 + goal.get("deviation_pct", 0) / 10)
        momentum_score = min(abs(goal.get("deviation_pct", 0)), 5)
        
        total_score = (progress_score + timing_score + momentum_score) / 15 * 100
        
        return {
            "total_score": round(total_score, 1),
            "components": {
                "progress": round(progress_score * 20, 1),
                "timing": round(timing_score * 20, 1),
                "momentum": round(momentum_score * 20, 1)
            },
            "interpretation": self._interpret_health(total_score)
        }
    
    def _interpret_health(self, score: float) -> str:
        """Interpret health score"""
        if score >= 80:
            return "Exzellent - Du bist deutlich über Plan"
        elif score >= 60:
            return "Gut - Auf Kurs zur Million"
        elif score >= 40:
            return "OK - Leicht hinter Plan, aber machbar"
        elif score >= 20:
            return "Schwierig - Braucht mehr Engagement"
        else:
            return "Kritisch - Strategie überarbeiten nötig"

