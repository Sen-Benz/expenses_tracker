"""Test database module."""

import pytest
import os
import sqlite3
from src.database import Database


@pytest.fixture
def test_db():
    """Create test database."""
    db = Database("test_expenses.db")
    yield db
    # Cleanup
    db.close()
    if os.path.exists("test_expenses.db"):
        os.remove("test_expenses.db")


def test_database_connection(test_db):
    """Test database connection."""
    assert test_db.connection is not None
    assert test_db.cursor is not None


def test_add_transaction(test_db):
    """Test adding a transaction."""
    success = test_db.add_transaction("expense", 50.00, "Food", "Groceries")
    assert success is True

    transactions = test_db.get_all_transactions()
    assert len(transactions) == 1
    assert transactions[0][3] == 50.00  # amount


def test_get_transactions_by_type(test_db):
    """Test filtering transactions by type."""
    test_db.add_transaction("income", 3000.00, "Salary/Income", "Monthly salary")
    test_db.add_transaction("expense", 100.00, "Food", "Groceries")

    income = test_db.get_transactions_by_type("income")
    expenses = test_db.get_transactions_by_type("expense")

    assert len(income) == 1
    assert len(expenses) == 1


def test_delete_transaction(test_db):
    """Test deleting a transaction."""
    test_db.add_transaction("expense", 50.00, "Food", "Test")
    transactions = test_db.get_all_transactions()
    transaction_id = transactions[0][0]

    success = test_db.delete_transaction(transaction_id)
    assert success is True

    transactions = test_db.get_all_transactions()
    assert len(transactions) == 0
