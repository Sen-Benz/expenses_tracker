"""Data visualization module."""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from collections import defaultdict


class Visualizer:
    """Generate charts and visualizations."""

    def __init__(self, expense_manager):
        """Initialize visualizer."""
        self.em = expense_manager

    def plot_expense_by_category(self, save_path=None):
        """Create pie chart of expenses by category."""
        summary = self.em.get_expenses_by_category_summary()

        if not summary:
            print("✗ No expense data to visualize")
            return

        categories = list(summary.keys())
        amounts = list(summary.values())

        plt.figure(figsize=(10, 7))
        colors = plt.cm.Set3(range(len(categories)))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", colors=colors, startangle=90)
        plt.title("Expense Distribution by Category", fontsize=16, fontweight="bold")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"✓ Chart saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_income_vs_expenses(self, save_path=None):
        """Create bar chart comparing income and expenses."""
        monthly = self.em.get_monthly_summary()

        if not monthly:
            print("✗ No transaction data to visualize")
            return

        months = list(monthly.keys())
        income = [monthly[m]["income"] for m in months]
        expenses = [monthly[m]["expense"] for m in months]

        x = range(len(months))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar([i - width / 2 for i in x], income, width, label="Income", color="#2ecc71")
        plt.bar([i + width / 2 for i in x], expenses, width, label="Expenses", color="#e74c3c")

        plt.xlabel("Month", fontweight="bold")
        plt.ylabel("Amount ($)", fontweight="bold")
        plt.title("Income vs Expenses by Month", fontsize=16, fontweight="bold")
        plt.xticks(x, months, rotation=45)
        plt.legend()
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"✓ Chart saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_spending_trend(self, save_path=None):
        """Create line chart of cumulative spending over time."""
        transactions = sorted(self.em.get_all_transactions(), key=lambda t: t.date)

        if not transactions:
            print("✗ No transaction data to visualize")
            return

        dates = []
        cumulative_balance = []
        current_balance = 0

        for transaction in transactions:
            dates.append(datetime.strptime(transaction.date, "%Y-%m-%d"))
            if transaction.transaction_type == "income":
                current_balance += transaction.amount
            else:
                current_balance -= transaction.amount
            cumulative_balance.append(current_balance)

        plt.figure(figsize=(12, 6))
        plt.plot(dates, cumulative_balance, marker="o", linewidth=2, markersize=6, color="#3498db")
        plt.axhline(y=0, color="r", linestyle="--", alpha=0.5)

        plt.xlabel("Date", fontweight="bold")
        plt.ylabel("Balance ($)", fontweight="bold")
        plt.title("Cumulative Balance Over Time", fontsize=16, fontweight="bold")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"✓ Chart saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def plot_budget_status(self, save_path=None):
        """Create bar chart of budget vs actual spending."""
        budget_status = self.em.check_budget_status()

        if not budget_status:
            print("✗ No budget data to visualize")
            return

        categories = list(budget_status.keys())
        budgets = [budget_status[c]["budget"] for c in categories]
        spent = [budget_status[c]["spent"] for c in categories]

        x = range(len(categories))
        width = 0.35

        plt.figure(figsize=(12, 6))
        plt.bar([i - width / 2 for i in x], budgets, width, label="Budget", color="#3498db")
        plt.bar([i + width / 2 for i in x], spent, width, label="Spent", color="#e74c3c")

        plt.xlabel("Category", fontweight="bold")
        plt.ylabel("Amount ($)", fontweight="bold")
        plt.title("Budget vs Actual Spending", fontsize=16, fontweight="bold")
        plt.xticks(x, categories, rotation=45)
        plt.legend()
        plt.grid(axis="y", alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"✓ Chart saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def generate_all_charts(self, output_dir="reports"):
        """Generate all charts and save to directory."""
        from pathlib import Path

        Path(output_dir).mkdir(exist_ok=True)

        try:
            self.plot_expense_by_category(f"{output_dir}/expenses_by_category.png")
            self.plot_income_vs_expenses(f"{output_dir}/income_vs_expenses.png")
            self.plot_spending_trend(f"{output_dir}/spending_trend.png")
            self.plot_budget_status(f"{output_dir}/budget_status.png")
            print(f"✓ All charts saved to {output_dir}/")
        except Exception as e:
            print(f"✗ Error generating charts: {e}")
