"""Core expense manager for tracking and analysis."""

from datetime import datetime
from src.database import Database
from src.transaction import Transaction


class ExpenseManager:
    """Manage expenses, income, and related operations."""

    EXPENSE_CATEGORIES = [
        "Food",
        "Transport",
        "Entertainment",
        "Utilities",
        "Healthcare",
        "Education",
        "Rent",
        "Shopping",
        "Other",
    ]

    def __init__(self, db_path="data/expenses.db"):
        """Initialize expense manager."""
        self.db = Database(db_path)

    def add_income(self, amount, description):
        """Add income transaction."""
        if amount <= 0:
            print("✗ Amount must be greater than 0")
            return False

        success = self.db.add_transaction("income", amount, "Salary/Income", description)
        if success:
            print(f"✓ Income added: ${amount:.2f} - {description}")
        return success

    def add_expense(self, amount, category, description):
        """Add expense transaction."""
        if amount <= 0:
            print("✗ Amount must be greater than 0")
            return False

        if category not in self.EXPENSE_CATEGORIES:
            print(f"✗ Invalid category. Valid categories: {', '.join(self.EXPENSE_CATEGORIES)}")
            return False

        success = self.db.add_transaction("expense", amount, category, description)
        if success:
            print(f"✓ Expense added: ${amount:.2f} ({category}) - {description}")
        return success

    def get_all_transactions(self):
        """Get all transactions."""
        transactions = self.db.get_all_transactions()
        return [Transaction.from_tuple(t) for t in transactions]

    def get_expenses(self):
        """Get all expenses."""
        transactions = self.db.get_transactions_by_type("expense")
        return [Transaction.from_tuple(t) for t in transactions]

    def get_income(self):
        """Get all income."""
        transactions = self.db.get_transactions_by_type("income")
        return [Transaction.from_tuple(t) for t in transactions]

    def get_transactions_by_date(self, start_date, end_date):
        """Get transactions within date range."""
        transactions = self.db.get_transactions_by_date_range(start_date, end_date)
        return [Transaction.from_tuple(t) for t in transactions]

    def get_expenses_by_category(self, category):
        """Get expenses in a specific category."""
        transactions = self.db.get_transactions_by_category(category)
        return [Transaction.from_tuple(t) for t in transactions]

    def delete_transaction(self, transaction_id):
        """Delete a transaction."""
        success = self.db.delete_transaction(transaction_id)
        if success:
            print(f"✓ Transaction {transaction_id} deleted")
        return success

    def calculate_total_income(self, transactions=None):
        """Calculate total income."""
        if transactions is None:
            transactions = self.get_income()
        return sum(t.amount for t in transactions)

    def calculate_total_expenses(self, transactions=None):
        """Calculate total expenses."""
        if transactions is None:
            transactions = self.get_expenses()
        return sum(t.amount for t in transactions)

    def calculate_balance(self):
        """Calculate current balance (income - expenses)."""
        income = self.calculate_total_income()
        expenses = self.calculate_total_expenses()
        return income - expenses

    def get_expenses_by_category_summary(self):
        """Get summary of expenses by category."""
        expenses = self.get_expenses()
        summary = {}
        for expense in expenses:
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount
        return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))

    def get_monthly_summary(self):
        """Get summary grouped by month."""
        transactions = self.get_all_transactions()
        summary = {}
        for transaction in transactions:
            month = transaction.date[:7]  # YYYY-MM
            if month not in summary:
                summary[month] = {"income": 0, "expense": 0}

            if transaction.transaction_type == "income":
                summary[month]["income"] += transaction.amount
            else:
                summary[month]["expense"] += transaction.amount

        return dict(sorted(summary.items()))

    def set_budget(self, category, amount):
        """Set budget for a category."""
        if amount <= 0:
            print("✗ Budget amount must be greater than 0")
            return False

        success = self.db.set_budget(category, amount)
        if success:
            print(f"✓ Budget set for {category}: ${amount:.2f}")
        return success

    def get_budget(self, category):
        """Get budget for a category."""
        return self.db.get_budget(category)

    def check_budget_status(self):
        """Check spending against budgets."""
        budgets = self.db.get_budgets()
        expenses_by_category = self.get_expenses_by_category_summary()
        status = {}

        for category, budget_amount in budgets:
            spent = expenses_by_category.get(category, 0)
            remaining = budget_amount - spent
            percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0

            status[category] = {
                "budget": budget_amount,
                "spent": spent,
                "remaining": remaining,
                "percentage": percentage,
            }

        return status

    def close(self):
        """Close database connection."""
        self.db.close()
