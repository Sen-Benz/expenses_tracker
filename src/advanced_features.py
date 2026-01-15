"""
Advanced features for Expense Tracker GUI
- Recurring transactions
- Search functionality
- Category statistics
- Monthly comparison
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from src.expense_manager import ExpenseManager
import json
from pathlib import Path


class RecurringTransactionManager:
    """Manage recurring transactions."""

    def __init__(self, data_file="data/recurring.json"):
        """Initialize recurring transaction manager."""
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        self.recurring_list = self.load_recurring()

    def load_recurring(self):
        """Load recurring transactions from file."""
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                return json.load(f)
        return []

    def save_recurring(self):
        """Save recurring transactions to file."""
        with open(self.data_file, "w") as f:
            json.dump(self.recurring_list, f, indent=2)

    def add_recurring(self, amount, category, description, frequency):
        """Add a recurring transaction."""
        recurring = {
            "id": len(self.recurring_list) + 1,
            "amount": amount,
            "category": category,
            "description": description,
            "frequency": frequency,  # daily, weekly, monthly, yearly
            "created_at": datetime.now().isoformat(),
        }
        self.recurring_list.append(recurring)
        self.save_recurring()
        return recurring

    def get_recurring(self):
        """Get all recurring transactions."""
        return self.recurring_list

    def delete_recurring(self, recurring_id):
        """Delete a recurring transaction."""
        self.recurring_list = [r for r in self.recurring_list if r["id"] != recurring_id]
        self.save_recurring()

    def apply_recurring(self, expense_manager):
        """Apply due recurring transactions."""
        count = 0
        for recurring in self.recurring_list:
            # Simplified logic - in production, track last applied date
            frequency = recurring["frequency"]
            if frequency == "daily":
                expense_manager.add_expense(
                    recurring["amount"],
                    recurring["category"],
                    f"[Recurring] {recurring['description']}",
                )
                count += 1
        return count


class SpendingAnalytics:
    """Advanced analytics for spending patterns."""

    def __init__(self, expense_manager):
        """Initialize analytics."""
        self.em = expense_manager

    def get_category_trends(self):
        """Get spending trends by category over months."""
        monthly = self.em.get_monthly_summary()
        category_summary = self.em.get_expenses_by_category_summary()
        return {
            "total_categories": len(category_summary),
            "top_category": max(category_summary, key=category_summary.get)
            if category_summary
            else None,
            "top_category_amount": max(category_summary.values())
            if category_summary
            else 0,
            "average_monthly_expense": sum(
                m["expense"] for m in monthly.values()
            ) / len(monthly) if monthly else 0,
        }

    def get_spending_forecast(self, months=3):
        """Forecast spending for next months."""
        monthly = self.em.get_monthly_summary()
        if not monthly:
            return None

        # Calculate average of recent months
        recent_months = list(monthly.values())[-3:] if len(monthly) >= 3 else monthly.values()
        avg_expense = sum(m["expense"] for m in recent_months) / len(recent_months)

        forecast = []
        for i in range(1, months + 1):
            future_month = (datetime.now() + timedelta(days=30 * i)).strftime("%Y-%m")
            forecast.append({"month": future_month, "forecasted_expense": round(avg_expense, 2)})

        return forecast

    def get_savings_rate(self):
        """Calculate savings rate (savings / income)."""
        income = self.em.calculate_total_income()
        expenses = self.em.calculate_total_expenses()
        if income == 0:
            return 0
        return round(((income - expenses) / income) * 100, 2)

    def get_category_percentage(self, category):
        """Get percentage of total spending in a category."""
        expenses = self.em.get_expenses()
        category_total = sum(e.amount for e in expenses if e.category == category)
        total_expenses = self.em.calculate_total_expenses()
        if total_expenses == 0:
            return 0
        return round((category_total / total_expenses) * 100, 2)


class TransactionSearch:
    """Search functionality for transactions."""

    def __init__(self, expense_manager):
        """Initialize search."""
        self.em = expense_manager

    def search_by_description(self, query):
        """Search transactions by description."""
        transactions = self.em.get_all_transactions()
        return [
            t for t in transactions if query.lower() in t.description.lower()
        ]

    def search_by_date_range(self, start_date, end_date):
        """Search by date range."""
        return self.em.get_transactions_by_date(start_date, end_date)

    def search_by_amount_range(self, min_amount, max_amount):
        """Search by amount range."""
        transactions = self.em.get_all_transactions()
        return [
            t for t in transactions
            if min_amount <= t.amount <= max_amount
        ]

    def search_by_category_and_date(self, category, start_date, end_date):
        """Complex search: category and date range."""
        transactions = self.em.get_transactions_by_date(start_date, end_date)
        return [t for t in transactions if t.category == category]


class BudgetAlert:
    """Alert system for budget warnings."""

    def __init__(self, expense_manager):
        """Initialize alert system."""
        self.em = expense_manager
        self.alert_threshold = 0.80  # Alert at 80% of budget

    def check_alerts(self):
        """Check for budget alerts."""
        alerts = []
        budget_status = self.em.check_budget_status()

        for category, status in budget_status.items():
            percentage = status["percentage"] / 100
            if percentage >= self.alert_threshold:
                alerts.append({
                    "category": category,
                    "message": f"{category}: {status['percentage']:.1f}% of budget used",
                    "severity": "warning" if percentage < 1.0 else "critical",
                    "spent": status["spent"],
                    "budget": status["budget"],
                })

        return alerts

    def get_alert_summary(self):
        """Get summary of all alerts."""
        alerts = self.check_alerts()
        return {
            "total_alerts": len(alerts),
            "warnings": sum(1 for a in alerts if a["severity"] == "warning"),
            "critical": sum(1 for a in alerts if a["severity"] == "critical"),
            "alerts": alerts,
        }
