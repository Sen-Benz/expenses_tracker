"""Report generation module."""

import csv
from datetime import datetime
from tabulate import tabulate


class ReportGenerator:
    """Generate various reports from expense data."""

    def __init__(self, expense_manager):
        """Initialize report generator."""
        self.em = expense_manager

    def generate_summary_report(self):
        """Generate summary report."""
        income = self.em.calculate_total_income()
        expenses = self.em.calculate_total_expenses()
        balance = self.em.calculate_balance()

        report = f"""
╔════════════════════════════════════════╗
║        EXPENSE TRACKER SUMMARY         ║
╚════════════════════════════════════════╝

Total Income:      ${income:>12.2f}
Total Expenses:    ${expenses:>12.2f}
─────────────────────────────────────────
Balance:           ${balance:>12.2f}

"""
        return report

    def generate_detailed_report(self):
        """Generate detailed transaction report."""
        transactions = self.em.get_all_transactions()

        if not transactions:
            return "No transactions found.\n"

        headers = ["Date", "Type", "Category", "Amount", "Description"]
        rows = [
            [
                t.date,
                t.transaction_type.capitalize(),
                t.category,
                f"${t.amount:.2f}",
                t.description,
            ]
            for t in transactions
        ]

        report = "\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n"
        return report

    def generate_category_report(self):
        """Generate expense breakdown by category."""
        summary = self.em.get_expenses_by_category_summary()

        if not summary:
            return "No expenses found.\n"

        headers = ["Category", "Amount", "Percentage"]
        total = sum(summary.values())
        rows = [
            [
                category,
                f"${amount:.2f}",
                f"{(amount / total * 100):.1f}%",
            ]
            for category, amount in summary.items()
        ]

        report = "\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n"
        return report

    def generate_monthly_report(self):
        """Generate monthly summary report."""
        monthly = self.em.get_monthly_summary()

        if not monthly:
            return "No transactions found.\n"

        headers = ["Month", "Income", "Expense", "Balance"]
        rows = [
            [
                month,
                f"${data['income']:.2f}",
                f"${data['expense']:.2f}",
                f"${(data['income'] - data['expense']):.2f}",
            ]
            for month, data in monthly.items()
        ]

        report = "\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n"
        return report

    def generate_budget_report(self):
        """Generate budget status report."""
        budget_status = self.em.check_budget_status()

        if not budget_status:
            return "No budgets set.\n"

        headers = ["Category", "Budget", "Spent", "Remaining", "Usage %"]
        rows = [
            [
                category,
                f"${status['budget']:.2f}",
                f"${status['spent']:.2f}",
                f"${status['remaining']:.2f}",
                f"{status['percentage']:.1f}%",
            ]
            for category, status in budget_status.items()
        ]

        report = "\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n"
        return report

    def export_to_csv(self, filename):
        """Export all transactions to CSV."""
        transactions = self.em.get_all_transactions()

        if not transactions:
            print("✗ No transactions to export")
            return False

        try:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["ID", "Date", "Type", "Category", "Amount", "Description"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for t in transactions:
                    writer.writerow(
                        {
                            "ID": t.transaction_id,
                            "Date": t.date,
                            "Type": t.transaction_type,
                            "Category": t.category,
                            "Amount": f"{t.amount:.2f}",
                            "Description": t.description,
                        }
                    )

            print(f"✓ Exported to {filename}")
            return True
        except IOError as e:
            print(f"✗ Error exporting to CSV: {e}")
            return False

    def export_to_pdf(self, filename):
        """Export report to PDF."""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch

            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = ParagraphStyle(
                "CustomTitle", parent=styles["Heading1"], fontSize=24, textColor=colors.HexColor("#1f77b4")
            )
            story.append(Paragraph("Expense Tracker Report", title_style))
            story.append(Spacer(1, 0.3 * inch))

            # Summary
            income = self.em.calculate_total_income()
            expenses = self.em.calculate_total_expenses()
            balance = self.em.calculate_balance()

            summary_data = [
                ["Metric", "Amount"],
                ["Total Income", f"${income:.2f}"],
                ["Total Expenses", f"${expenses:.2f}"],
                ["Balance", f"${balance:.2f}"],
            ]

            summary_table = Table(summary_data)
            summary_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            story.append(summary_table)
            story.append(Spacer(1, 0.3 * inch))

            # Category breakdown
            story.append(Paragraph("Expense Breakdown by Category", styles["Heading2"]))
            story.append(Spacer(1, 0.1 * inch))

            summary = self.em.get_expenses_by_category_summary()
            if summary:
                cat_data = [["Category", "Amount"]]
                total = sum(summary.values())
                for category, amount in summary.items():
                    cat_data.append([category, f"${amount:.2f}"])

                cat_table = Table(cat_data)
                cat_table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                story.append(cat_table)

            # Build PDF
            doc.build(story)
            print(f"✓ PDF report exported to {filename}")
            return True

        except ImportError:
            print("✗ reportlab not installed. Install with: pip install reportlab")
            return False
        except Exception as e:
            print(f"✗ Error exporting to PDF: {e}")
            return False
