"""Test expense manager module."""

import pytest
import os
from src.expense_manager import ExpenseManager


@pytest.fixture
def manager():
    """Create test expense manager."""
    em = ExpenseManager("test_expenses.db")
    yield em
    em.close()
    if os.path.exists("test_expenses.db"):
        os.remove("test_expenses.db")


def test_add_income(manager):
    """Test adding income."""
    success = manager.add_income(3000, "Monthly salary")
    assert success is True

    income = manager.get_income()
    assert len(income) == 1
    assert income[0].amount == 3000


def test_add_expense(manager):
    """Test adding expense."""
    success = manager.add_expense(50, "Food", "Groceries")
    assert success is True

    expenses = manager.get_expenses()
    assert len(expenses) == 1
    assert expenses[0].amount == 50


def test_calculate_balance(manager):
    """Test balance calculation."""
    manager.add_income(3000, "Salary")
    manager.add_expense(500, "Rent", "Monthly rent")
    manager.add_expense(200, "Food", "Groceries")

    balance = manager.calculate_balance()
    assert balance == 2300


def test_category_summary(manager):
    """Test expense summary by category."""
    manager.add_expense(50, "Food", "Groceries")
    manager.add_expense(30, "Food", "Restaurant")
    manager.add_expense(1200, "Rent", "Monthly rent")

    summary = manager.get_expenses_by_category_summary()
    assert summary["Food"] == 80
    assert summary["Rent"] == 1200


def test_invalid_category(manager, capsys):
    """Test adding expense with invalid category."""
    success = manager.add_expense(50, "InvalidCategory", "Test")
    assert success is False

    captured = capsys.readouterr()
    assert "Invalid category" in captured.out
