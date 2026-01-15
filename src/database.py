"""Database module for expense tracker."""

import sqlite3
from pathlib import Path
from datetime import datetime


class Database:
    """Handle all database operations for expense tracker."""

    def __init__(self, db_path="data/expenses.db"):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.cursor = self.connection.cursor()
            print(f"✓ Database connected: {self.db_path}")
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
            raise

    def create_tables(self):
        """Create necessary database tables."""
        try:
            # Transactions table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Budgets table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE NOT NULL,
                    amount REAL NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
            raise

    def add_transaction(self, transaction_type, amount, category, description, date=None):
        """Add a new transaction."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        try:
            self.cursor.execute("""
                INSERT INTO transactions (date, type, amount, category, description)
                VALUES (?, ?, ?, ?, ?)
            """, (date, transaction_type, amount, category, description))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error adding transaction: {e}")
            return False

    def get_all_transactions(self):
        """Retrieve all transactions."""
        try:
            self.cursor.execute("""
                SELECT id, date, type, amount, category, description
                FROM transactions
                ORDER BY date DESC
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error retrieving transactions: {e}")
            return []

    def get_transactions_by_type(self, transaction_type):
        """Get transactions by type (expense or income)."""
        try:
            self.cursor.execute("""
                SELECT id, date, type, amount, category, description
                FROM transactions
                WHERE type = ?
                ORDER BY date DESC
            """, (transaction_type,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error retrieving transactions: {e}")
            return []

    def get_transactions_by_date_range(self, start_date, end_date):
        """Get transactions within a date range."""
        try:
            self.cursor.execute("""
                SELECT id, date, type, amount, category, description
                FROM transactions
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (start_date, end_date))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error retrieving transactions: {e}")
            return []

    def get_transactions_by_category(self, category):
        """Get expenses by category."""
        try:
            self.cursor.execute("""
                SELECT id, date, type, amount, category, description
                FROM transactions
                WHERE category = ?
                ORDER BY date DESC
            """, (category,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error retrieving transactions: {e}")
            return []

    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID."""
        try:
            self.cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error deleting transaction: {e}")
            return False

    def set_budget(self, category, amount):
        """Set or update budget for a category."""
        try:
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("""
                INSERT OR REPLACE INTO budgets (category, amount, updated_at)
                VALUES (?, ?, ?)
            """, (category, amount, updated_at))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ Error setting budget: {e}")
            return False

    def get_budgets(self):
        """Get all budgets."""
        try:
            self.cursor.execute("SELECT category, amount FROM budgets")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Error retrieving budgets: {e}")
            return []

    def get_budget(self, category):
        """Get budget for a specific category."""
        try:
            self.cursor.execute("SELECT amount FROM budgets WHERE category = ?", (category,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"✗ Error retrieving budget: {e}")
            return None

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")

    def __del__(self):
        """Destructor to ensure connection is closed."""
        self.close()
