"""Demo script to showcase the expense tracker."""

from src.expense_manager import ExpenseManager
from src.report_generator import ReportGenerator
from src.visualizer import Visualizer


def run_demo():
    """Run a demonstration of the expense tracker."""
    print("=" * 50)
    print("EXPENSE TRACKER - DEMO")
    print("=" * 50)

    # Initialize
    em = ExpenseManager()
    rg = ReportGenerator(em)
    visualizer = Visualizer(em)

    # Add sample data
    print("\n[1/4] Adding sample transactions...")
    em.add_income(5000, "Monthly Salary")
    em.add_expense(1200, "Rent", "Monthly rent payment")
    em.add_expense(300, "Food", "Groceries")
    em.add_expense(50, "Food", "Restaurant lunch")
    em.add_expense(100, "Transport", "Gas")
    em.add_expense(80, "Entertainment", "Movie tickets")
    em.add_expense(200, "Utilities", "Electric bill")

    # Set budgets
    print("\n[2/4] Setting budgets...")
    em.set_budget("Food", 400)
    em.set_budget("Transport", 150)
    em.set_budget("Entertainment", 100)

    # Display summary
    print("\n[3/4] Financial Summary:")
    print(rg.generate_summary_report())

    # Display reports
    print("Category Breakdown:")
    print(rg.generate_category_report())

    print("Budget Status:")
    print(rg.generate_budget_report())

    # Export
    print("\n[4/4] Exporting data...")
    rg.export_to_csv("demo_expenses.csv")
    visualizer.generate_all_charts("reports")

    print("\n" + "=" * 50)
    print("✓ Demo completed successfully!")
    print("=" * 50)

    em.close()


if __name__ == "__main__":
    run_demo()
