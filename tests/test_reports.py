"""Test report generator module."""

import pytest
import os
from src.expense_manager import ExpenseManager
from src.report_generator import ReportGenerator


@pytest.fixture
def report_gen():
    """Create test report generator."""
    em = ExpenseManager("test_expenses.db")
    rg = ReportGenerator(em)
    yield rg, em
    em.close()
    if os.path.exists("test_expenses.db"):
        os.remove("test_expenses.db")


def test_summary_report(report_gen):
    """Test summary report generation."""
    rg, em = report_gen
    em.add_income(3000, "Salary")
    em.add_expense(500, "Rent", "Rent")

    report = rg.generate_summary_report()
    assert "3000.00" in report
    assert "500.00" in report


def test_detailed_report(report_gen):
    """Test detailed report generation."""
    rg, em = report_gen
    em.add_income(3000, "Salary")
    em.add_expense(50, "Food", "Groceries")

    report = rg.generate_detailed_report()
    assert "Salary" in report or "3000" in report


def test_export_csv(report_gen):
    """Test CSV export."""
    rg, em = report_gen
    em.add_income(3000, "Salary")
    em.add_expense(50, "Food", "Groceries")

    filename = "test_export.csv"
    success = rg.export_to_csv(filename)
    assert success is True
    assert os.path.exists(filename)

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
