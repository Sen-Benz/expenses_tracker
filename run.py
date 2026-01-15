#!/usr/bin/env python3
"""
Quick start guide to run the Expense Tracker application interactively.
"""

from src.main import ExpenseTrackerCLI


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("Welcome to Expense Tracker!")
    print("=" * 50)
    print("\nStarting interactive CLI...\n")

    cli = ExpenseTrackerCLI()
    cli.run()
