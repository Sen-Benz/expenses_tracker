"""Main CLI application for expense tracker."""

import sys
from colorama import Fore, Back, Style, init
from src.expense_manager import ExpenseManager
from src.report_generator import ReportGenerator
from src.visualizer import Visualizer

# Initialize colorama for colored terminal output
init(autoreset=True)


class ExpenseTrackerCLI:
    """Command-line interface for expense tracker."""

    def __init__(self):
        """Initialize CLI."""
        self.em = ExpenseManager()
        self.rg = ReportGenerator(self.em)
        self.visualizer = Visualizer(self.em)
        self.running = True

    def display_banner(self):
        """Display application banner."""
        banner = f"""
{Fore.CYAN}
╔════════════════════════════════════════╗
║     💰 EXPENSE TRACKER APPLICATION 💰  ║
║         Your Personal Finance Tool      ║
╚════════════════════════════════════════╝
{Style.RESET_ALL}
Type 'help' for available commands.
"""
        print(banner)

    def display_help(self):
        """Display help information."""
        help_text = f"""
{Fore.GREEN}Available Commands:{Style.RESET_ALL}

{Fore.YELLOW}Transaction Management:{Style.RESET_ALL}
  add-income <amount> <description>
      Add income (e.g., add-income 3000 "Monthly salary")
  
  add-expense <amount> <category> <description>
      Add expense (e.g., add-expense 50 Food "Groceries")
  
  list-all                     List all transactions
  list-income                  List only income transactions
  list-expenses                List only expenses
  delete <id>                  Delete transaction by ID

{Fore.YELLOW}Reports & Analysis:{Style.RESET_ALL}
  summary                      Show financial summary
  detailed-report              Show all transactions
  category-report              Show expenses by category
  monthly-report               Show monthly summary
  filter-date <start> <end>    Filter by date (YYYY-MM-DD)

{Fore.YELLOW}Budget Management:{Style.RESET_ALL}
  set-budget <category> <amount>   Set budget for category
  budget-report                     Show budget status

{Fore.YELLOW}Visualization & Export:{Style.RESET_ALL}
  visualize                    Generate and show charts
  export-csv <filename>        Export to CSV
  export-pdf <filename>        Export to PDF

{Fore.YELLOW}Utility:{Style.RESET_ALL}
  help                         Show this help message
  categories                   Show available categories
  clear                        Clear screen
  exit                         Exit application

{Fore.GREEN}Categories Available:{Style.RESET_ALL}
  {', '.join(ExpenseManager.EXPENSE_CATEGORIES)}
"""
        print(help_text)

    def display_categories(self):
        """Display available expense categories."""
        print(f"\n{Fore.GREEN}Available Expense Categories:{Style.RESET_ALL}")
        for i, cat in enumerate(ExpenseManager.EXPENSE_CATEGORIES, 1):
            print(f"  {i}. {cat}")

    def process_command(self, command):
        """Process user command."""
        if not command.strip():
            return

        parts = command.strip().split()
        cmd = parts[0].lower()

        try:
            # Transaction Management
            if cmd == "add-income":
                if len(parts) < 3:
                    print(f"{Fore.RED}✗ Usage: add-income <amount> <description>{Style.RESET_ALL}")
                    return
                amount = float(parts[1])
                description = " ".join(parts[2:])
                self.em.add_income(amount, description)

            elif cmd == "add-expense":
                if len(parts) < 4:
                    print(
                        f"{Fore.RED}✗ Usage: add-expense <amount> <category> <description>{Style.RESET_ALL}"
                    )
                    return
                amount = float(parts[1])
                category = parts[2]
                description = " ".join(parts[3:])
                self.em.add_expense(amount, category, description)

            elif cmd == "list-all":
                self.display_transactions(self.em.get_all_transactions())

            elif cmd == "list-income":
                self.display_transactions(self.em.get_income())

            elif cmd == "list-expenses":
                self.display_transactions(self.em.get_expenses())

            elif cmd == "delete":
                if len(parts) < 2:
                    print(f"{Fore.RED}✗ Usage: delete <transaction_id>{Style.RESET_ALL}")
                    return
                transaction_id = int(parts[1])
                self.em.delete_transaction(transaction_id)

            # Reports
            elif cmd == "summary":
                print(self.rg.generate_summary_report())

            elif cmd == "detailed-report":
                print(self.rg.generate_detailed_report())

            elif cmd == "category-report":
                print(self.rg.generate_category_report())

            elif cmd == "monthly-report":
                print(self.rg.generate_monthly_report())

            elif cmd == "filter-date":
                if len(parts) < 3:
                    print(f"{Fore.RED}✗ Usage: filter-date <start_date> <end_date>{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Example: filter-date 2024-01-01 2024-12-31{Style.RESET_ALL}")
                    return
                start_date = parts[1]
                end_date = parts[2]
                transactions = self.em.get_transactions_by_date(start_date, end_date)
                self.display_transactions(transactions)

            # Budget
            elif cmd == "set-budget":
                if len(parts) < 3:
                    print(f"{Fore.RED}✗ Usage: set-budget <category> <amount>{Style.RESET_ALL}")
                    return
                category = parts[1]
                amount = float(parts[2])
                self.em.set_budget(category, amount)

            elif cmd == "budget-report":
                print(self.rg.generate_budget_report())

            # Visualization & Export
            elif cmd == "visualize":
                print(f"{Fore.GREEN}Generating charts...{Style.RESET_ALL}")
                self.visualizer.generate_all_charts()

            elif cmd == "export-csv":
                if len(parts) < 2:
                    print(f"{Fore.RED}✗ Usage: export-csv <filename>{Style.RESET_ALL}")
                    return
                filename = parts[1]
                self.rg.export_to_csv(filename)

            elif cmd == "export-pdf":
                if len(parts) < 2:
                    print(f"{Fore.RED}✗ Usage: export-pdf <filename>{Style.RESET_ALL}")
                    return
                filename = parts[1]
                self.rg.export_to_pdf(filename)

            # Utility
            elif cmd == "help":
                self.display_help()

            elif cmd == "categories":
                self.display_categories()

            elif cmd == "clear":
                import os

                os.system("cls" if os.name == "nt" else "clear")

            elif cmd == "exit":
                self.running = False
                print(f"{Fore.GREEN}✓ Thank you for using Expense Tracker!{Style.RESET_ALL}")

            else:
                print(f"{Fore.RED}✗ Unknown command: {cmd}. Type 'help' for available commands.{Style.RESET_ALL}")

        except ValueError as e:
            print(f"{Fore.RED}✗ Invalid input: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

    def display_transactions(self, transactions):
        """Display transactions in formatted table."""
        if not transactions:
            print(f"{Fore.YELLOW}No transactions found.{Style.RESET_ALL}\n")
            return

        from tabulate import tabulate

        headers = ["ID", "Date", "Type", "Category", "Amount", "Description"]
        rows = [
            [
                t.transaction_id,
                t.date,
                Fore.GREEN + t.transaction_type.upper() + Style.RESET_ALL
                if t.transaction_type == "income"
                else Fore.RED + t.transaction_type.upper() + Style.RESET_ALL,
                t.category,
                f"${t.amount:>8.2f}",
                t.description[:30],
            ]
            for t in transactions
        ]

        print("\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n")

    def run(self):
        """Run the CLI application."""
        self.display_banner()

        while self.running:
            try:
                command = input(f"{Fore.CYAN}expense-tracker$ {Style.RESET_ALL}").strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted by user.{Style.RESET_ALL}")
                self.running = False
            except EOFError:
                self.running = False

        self.em.close()
        print()


def main():
    """Main entry point."""
    app = ExpenseTrackerCLI()
    app.run()


if __name__ == "__main__":
    main()
