"""
GUI application for Expense Tracker using tkinter.
Features: Dashboard, Add Expenses, View Transactions, Reports, Visualizations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from src.expense_manager import ExpenseManager
from src.report_generator import ReportGenerator
from src.visualizer import Visualizer
from src.advanced_features import (
    SpendingAnalytics,
    TransactionSearch,
    BudgetAlert,
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class ExpenseTrackerGUI:
    """Main GUI application for Expense Tracker."""

    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Initialize managers
        self.em = ExpenseManager()
        self.rg = ReportGenerator(self.em)
        self.visualizer = Visualizer(self.em)
        self.analytics = SpendingAnalytics(self.em)
        self.search = TransactionSearch(self.em)
        self.budget_alert = BudgetAlert(self.em)

        # Configure styles
        self.setup_styles()

        # Create main layout
        self.create_main_layout()

    def setup_styles(self):
        """Setup custom styles for the application."""
        style = ttk.Style()
        style.theme_use("clam")

        # Configure colors
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), foreground="#1f77b4")
        style.configure("Subtitle.TLabel", font=("Arial", 12, "bold"), foreground="#333")
        style.configure("TButton", font=("Arial", 10))
        style.map(
            "TButton", background=[("active", "#e74c3c"), ("pressed", "#c0392b")]
        )

    def create_main_layout(self):
        """Create the main application layout."""
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=10, pady=10)

        title = ttk.Label(header, text="💰 Expense Tracker Dashboard", style="Title.TLabel")
        title.pack(side=tk.LEFT)

        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.add_expense_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.reports_tab = ttk.Frame(self.notebook)
        self.budget_tab = ttk.Frame(self.notebook)
        self.analytics_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        self.notebook.add(self.add_expense_tab, text="➕ Add Expense")
        self.notebook.add(self.transactions_tab, text="📋 Transactions")
        self.notebook.add(self.reports_tab, text="📈 Reports")
        self.notebook.add(self.budget_tab, text="🎯 Budget")
        self.notebook.add(self.analytics_tab, text="📉 Analytics")
        self.notebook.add(self.search_tab, text="🔍 Search")

        # Create tab content
        self.create_dashboard_tab()
        self.create_add_expense_tab()
        self.create_transactions_tab()
        self.create_reports_tab()
        self.create_budget_tab()
        self.create_analytics_tab()
        self.create_search_tab()

        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(
            footer, text="Built with Python | Powered by Pandas & SQLite", foreground="#666"
        ).pack(side=tk.LEFT)

    def create_dashboard_tab(self):
        """Create dashboard tab with summary and charts."""
        # Summary section
        summary_frame = ttk.LabelFrame(
            self.dashboard_tab, text="Financial Summary", padding=10
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create summary display
        self.update_summary()

        # Chart section
        chart_frame = ttk.LabelFrame(
            self.dashboard_tab, text="Expense Distribution", padding=10
        )
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chart_canvas_frame = ttk.Frame(chart_frame)
        self.chart_canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Refresh button
        refresh_frame = ttk.Frame(self.dashboard_tab)
        refresh_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            refresh_frame, text="🔄 Refresh Dashboard", command=self.refresh_dashboard
        ).pack(side=tk.LEFT)

    def update_summary(self):
        """Update financial summary display."""
        # Clear existing widgets
        for widget in self.dashboard_tab.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and "Summary" in widget.cget("text"):
                for child in widget.winfo_children():
                    child.destroy()
                break

        # Get summary data
        income = self.em.calculate_total_income()
        expenses = self.em.calculate_total_expenses()
        balance = self.em.calculate_balance()

        # Create summary frame
        summary_frame = ttk.LabelFrame(
            self.dashboard_tab, text="Financial Summary", padding=10
        )
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Summary items
        summary_data = [
            ("Total Income", f"${income:,.2f}", "#2ecc71"),
            ("Total Expenses", f"${expenses:,.2f}", "#e74c3c"),
            ("Balance", f"${balance:,.2f}", "#3498db"),
        ]

        for label, value, color in summary_data:
            item_frame = ttk.Frame(summary_frame)
            item_frame.pack(fill=tk.X, pady=5)

            ttk.Label(item_frame, text=label, font=("Arial", 11)).pack(side=tk.LEFT)
            value_label = ttk.Label(
                item_frame, text=value, font=("Arial", 13, "bold"), foreground=color
            )
            value_label.pack(side=tk.RIGHT)

    def create_add_expense_tab(self):
        """Create tab for adding expenses and income."""
        form_frame = ttk.LabelFrame(self.add_expense_tab, text="Add Transaction", padding=15)
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        # Transaction type
        ttk.Label(form_frame, text="Type:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.type_var = tk.StringVar(value="expense")
        type_frame = ttk.Frame(form_frame)
        type_frame.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(
            type_frame, text="Expense", variable=self.type_var, value="expense",
            command=self.update_category_dropdown
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            type_frame, text="Income", variable=self.type_var, value="income",
            command=self.update_category_dropdown
        ).pack(side=tk.LEFT, padx=5)

        # Amount
        ttk.Label(form_frame, text="Amount ($):", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.amount_entry = ttk.Entry(form_frame, width=30)
        self.amount_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        # Category
        ttk.Label(form_frame, text="Category:", font=("Arial", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            form_frame, textvariable=self.category_var, width=27, state="readonly"
        )
        self.category_combo.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self.update_category_dropdown()

        # Date
        ttk.Label(form_frame, text="Date:", font=("Arial", 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=("Arial", 8), foreground="#666").grid(
            row=3, column=2, sticky=tk.W, padx=5
        )

        # Description
        ttk.Label(form_frame, text="Description:", font=("Arial", 10)).grid(
            row=4, column=0, sticky=tk.NW, pady=5
        )
        self.desc_text = tk.Text(form_frame, height=4, width=30)
        self.desc_text.grid(row=4, column=1, sticky=tk.EW, pady=5)

        # Button frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=15)

        ttk.Button(
            button_frame, text="✅ Add Transaction", command=self.add_transaction
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="🔄 Clear Form", command=self.clear_form
        ).pack(side=tk.LEFT, padx=5)

        # Configure grid weight
        form_frame.columnconfigure(1, weight=1)

        # Quick add buttons
        quick_frame = ttk.LabelFrame(
            self.add_expense_tab, text="Quick Add Expense", padding=10
        )
        quick_frame.pack(fill=tk.X, padx=10, pady=10)

        quick_buttons = [
            ("🍔 Food", "Food", 15),
            ("🚗 Transport", "Transport", 20),
            ("🎬 Entertainment", "Entertainment", 15),
            ("💡 Utilities", "Utilities", 50),
        ]

        for label, category, default_amount in quick_buttons:
            ttk.Button(
                quick_frame,
                text=label,
                command=lambda c=category, a=default_amount: self.quick_add_expense(c, a),
            ).pack(side=tk.LEFT, padx=5)

    def update_category_dropdown(self):
        """Update category dropdown based on transaction type."""
        if self.type_var.get() == "expense":
            self.category_combo["values"] = ExpenseManager.EXPENSE_CATEGORIES
            self.category_combo.current(0)
        else:
            self.category_combo["values"] = ["Salary/Income", "Bonus", "Investment"]
            self.category_combo.current(0)

    def add_transaction(self):
        """Add a new transaction."""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.desc_text.get("1.0", tk.END).strip()
            date = self.date_entry.get()
            trans_type = self.type_var.get()

            if not category:
                messagebox.showerror("Error", "Please select a category")
                return

            if not description:
                messagebox.showerror("Error", "Please enter a description")
                return

            if trans_type == "expense":
                self.em.add_expense(amount, category, description)
            else:
                self.em.add_income(amount, description)

            messagebox.showinfo("Success", "✓ Transaction added successfully!")
            self.clear_form()
            self.refresh_dashboard()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def quick_add_expense(self, category, default_amount):
        """Quick add expense with default amount."""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(default_amount))
        self.category_combo.set(category)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert("1.0", f"Quick add: {category}")

    def clear_form(self):
        """Clear the form fields."""
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.desc_text.delete("1.0", tk.END)
        self.category_combo.current(0)

    def create_transactions_tab(self):
        """Create transactions view tab."""
        # Filter frame
        filter_frame = ttk.LabelFrame(self.transactions_tab, text="Filter", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(filter_frame, text="Show:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(
            filter_frame, text="All", variable=self.filter_var, value="all",
            command=self.update_transactions_list
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            filter_frame, text="Income", variable=self.filter_var, value="income",
            command=self.update_transactions_list
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            filter_frame, text="Expenses", variable=self.filter_var, value="expense",
            command=self.update_transactions_list
        ).pack(side=tk.LEFT, padx=5)

        # Transactions list
        list_frame = ttk.LabelFrame(
            self.transactions_tab, text="Transactions", padding=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create treeview
        columns = ("ID", "Date", "Type", "Category", "Amount", "Description")
        self.transactions_tree = ttk.Treeview(
            list_frame, columns=columns, height=15, show="headings"
        )

        # Define column headings
        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            list_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview
        )
        self.transactions_tree.configure(yscroll=scrollbar.set)

        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Delete button
        button_frame = ttk.Frame(self.transactions_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(
            button_frame, text="🗑️ Delete Selected", command=self.delete_transaction
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="🔄 Refresh", command=self.update_transactions_list
        ).pack(side=tk.LEFT, padx=5)

        self.update_transactions_list()

    def update_transactions_list(self):
        """Update the transactions list."""
        # Clear existing items
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        # Get transactions based on filter
        filter_type = self.filter_var.get()
        if filter_type == "all":
            transactions = self.em.get_all_transactions()
        elif filter_type == "income":
            transactions = self.em.get_income()
        else:
            transactions = self.em.get_expenses()

        # Add transactions to tree
        for t in transactions:
            self.transactions_tree.insert(
                "",
                tk.END,
                values=(
                    t.transaction_id,
                    t.date,
                    t.transaction_type.upper(),
                    t.category,
                    f"${t.amount:.2f}",
                    t.description[:30],
                ),
            )

    def delete_transaction(self):
        """Delete selected transaction."""
        selected = self.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return

        item = self.transactions_tree.item(selected[0])
        transaction_id = item["values"][0]

        if messagebox.askyesno("Confirm", "Delete this transaction?"):
            self.em.delete_transaction(transaction_id)
            self.update_transactions_list()
            self.refresh_dashboard()
            messagebox.showinfo("Success", "✓ Transaction deleted")

    def create_reports_tab(self):
        """Create reports tab."""
        button_frame = ttk.Frame(self.reports_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame, text="📊 Generate Charts", command=self.generate_charts
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="💾 Export CSV", command=self.export_csv
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            button_frame, text="📄 Export PDF", command=self.export_pdf
        ).pack(side=tk.LEFT, padx=5)

        # Report display area
        self.report_frame = ttk.Frame(self.reports_tab)
        self.report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load initial reports
        self.show_summary_report()

    def show_summary_report(self):
        """Display summary report."""
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        report_text = self.rg.generate_summary_report()
        report_text += "\n" + self.rg.generate_category_report()
        report_text += "\n" + self.rg.generate_monthly_report()

        text_widget = tk.Text(self.report_frame, height=20, width=80)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, report_text)
        text_widget.config(state=tk.DISABLED)

    def generate_charts(self):
        """Generate and display charts."""
        try:
            self.visualizer.generate_all_charts()
            messagebox.showinfo("Success", "✓ Charts saved to reports/ folder")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating charts: {e}")

    def export_csv(self):
        """Export to CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
        )
        if filename:
            self.rg.export_to_csv(filename)
            messagebox.showinfo("Success", f"✓ Exported to {filename}")

    def export_pdf(self):
        """Export to PDF."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            if self.rg.export_to_pdf(filename):
                messagebox.showinfo("Success", f"✓ Exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export PDF")

    def create_budget_tab(self):
        """Create budget management tab."""
        # Set budget frame
        set_budget_frame = ttk.LabelFrame(
            self.budget_tab, text="Set Budget", padding=10
        )
        set_budget_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(set_budget_frame, text="Category:").pack(side=tk.LEFT, padx=5)
        self.budget_category_var = tk.StringVar()
        budget_combo = ttk.Combobox(
            set_budget_frame,
            textvariable=self.budget_category_var,
            values=ExpenseManager.EXPENSE_CATEGORIES,
            state="readonly",
            width=20,
        )
        budget_combo.pack(side=tk.LEFT, padx=5)
        budget_combo.current(0)

        ttk.Label(set_budget_frame, text="Budget ($):").pack(side=tk.LEFT, padx=5)
        self.budget_amount_entry = ttk.Entry(set_budget_frame, width=15)
        self.budget_amount_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            set_budget_frame, text="💾 Set Budget", command=self.set_budget
        ).pack(side=tk.LEFT, padx=5)

        # Budget status frame
        status_frame = ttk.LabelFrame(
            self.budget_tab, text="Budget Status", padding=10
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.budget_tree = ttk.Treeview(
            status_frame, columns=("Category", "Budget", "Spent", "Remaining", "Usage %"),
            height=10, show="headings"
        )

        for col in ("Category", "Budget", "Spent", "Remaining", "Usage %"):
            self.budget_tree.heading(col, text=col)
            self.budget_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            status_frame, orient=tk.VERTICAL, command=self.budget_tree.yview
        )
        self.budget_tree.configure(yscroll=scrollbar.set)

        self.budget_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(
            self.budget_tab, text="🔄 Refresh", command=self.update_budget_status
        ).pack(pady=10)

        self.update_budget_status()

    def set_budget(self):
        """Set budget for a category."""
        try:
            category = self.budget_category_var.get()
            amount = float(self.budget_amount_entry.get())
            self.em.set_budget(category, amount)
            self.budget_amount_entry.delete(0, tk.END)
            self.update_budget_status()
            messagebox.showinfo("Success", f"✓ Budget set for {category}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def update_budget_status(self):
        """Update budget status display."""
        for item in self.budget_tree.get_children():
            self.budget_tree.delete(item)

        budget_status = self.em.check_budget_status()
        if not budget_status:
            return

        for category, status in budget_status.items():
            self.budget_tree.insert(
                "",
                tk.END,
                values=(
                    category,
                    f"${status['budget']:.2f}",
                    f"${status['spent']:.2f}",
                    f"${status['remaining']:.2f}",
                    f"{status['percentage']:.1f}%",
                ),
            )

    def refresh_dashboard(self):
        """Refresh the dashboard."""
        self.update_summary()
        self.update_transactions_list()
        self.update_budget_status()

    def create_analytics_tab(self):
        """Create analytics and insights tab."""
        # Analytics summary
        summary_frame = ttk.LabelFrame(self.analytics_tab, text="Spending Analytics", padding=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        # Get analytics data
        trends = self.analytics.get_category_trends()
        savings_rate = self.analytics.get_savings_rate()

        analytics_data = [
            ("Savings Rate", f"{savings_rate}%"),
            ("Top Expense Category", f"{trends.get('top_category', 'N/A')}"),
            ("Top Category Amount", f"${trends.get('top_category_amount', 0):.2f}"),
            ("Average Monthly Expense", f"${trends.get('average_monthly_expense', 0):.2f}"),
        ]

        for label, value in analytics_data:
            item_frame = ttk.Frame(summary_frame)
            item_frame.pack(fill=tk.X, pady=5)
            ttk.Label(item_frame, text=label, font=("Arial", 11)).pack(side=tk.LEFT)
            ttk.Label(
                item_frame, text=value, font=("Arial", 12, "bold"), foreground="#3498db"
            ).pack(side=tk.RIGHT)

        # Spending forecast
        forecast_frame = ttk.LabelFrame(self.analytics_tab, text="Spending Forecast (Next 3 Months)", padding=10)
        forecast_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        forecast = self.analytics.get_spending_forecast()
        if forecast:
            forecast_tree = ttk.Treeview(
                forecast_frame, columns=("Month", "Forecasted Expense"), height=8, show="headings"
            )
            forecast_tree.heading("Month", text="Month")
            forecast_tree.heading("Forecasted Expense", text="Forecasted Expense")
            forecast_tree.column("Month", width=150)
            forecast_tree.column("Forecasted Expense", width=200)

            for item in forecast:
                forecast_tree.insert(
                    "",
                    tk.END,
                    values=(item["month"], f"${item['forecasted_expense']:.2f}"),
                )

            forecast_tree.pack(fill=tk.BOTH, expand=True)

        # Budget alerts
        alert_frame = ttk.LabelFrame(self.analytics_tab, text="Budget Alerts", padding=10)
        alert_frame.pack(fill=tk.X, padx=10, pady=10)

        alert_summary = self.budget_alert.get_alert_summary()
        alert_text = f"Total Alerts: {alert_summary['total_alerts']} | "
        alert_text += f"Warnings: {alert_summary['warnings']} | "
        alert_text += f"Critical: {alert_summary['critical']}"
        
        ttk.Label(alert_frame, text=alert_text, font=("Arial", 10)).pack(fill=tk.X)

        if alert_summary["alerts"]:
            alerts_display = ttk.Frame(alert_frame)
            alerts_display.pack(fill=tk.BOTH, expand=True, pady=10)

            for alert in alert_summary["alerts"]:
                alert_label = ttk.Label(
                    alerts_display,
                    text=f"⚠️  {alert['message']}",
                    foreground="#e74c3c" if alert["severity"] == "critical" else "#f39c12",
                )
                alert_label.pack(fill=tk.X, pady=2)

    def create_search_tab(self):
        """Create search and filter tab."""
        # Search options
        search_frame = ttk.LabelFrame(self.search_tab, text="Search Transactions", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        # Search by description
        ttk.Label(search_frame, text="Search by Description:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_desc_entry = ttk.Entry(search_frame, width=40)
        self.search_desc_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Button(
            search_frame, text="🔍 Search", command=self.search_by_description
        ).grid(row=0, column=2, padx=5)

        # Search by amount range
        ttk.Label(search_frame, text="Amount Range ($):").grid(row=1, column=0, sticky=tk.W, pady=5)
        range_frame = ttk.Frame(search_frame)
        range_frame.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(range_frame, text="Min:").pack(side=tk.LEFT, padx=5)
        self.search_min_entry = ttk.Entry(range_frame, width=15)
        self.search_min_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(range_frame, text="Max:").pack(side=tk.LEFT, padx=5)
        self.search_max_entry = ttk.Entry(range_frame, width=15)
        self.search_max_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            search_frame, text="🔍 Search", command=self.search_by_amount
        ).grid(row=1, column=2, padx=5)

        # Search by date range
        ttk.Label(search_frame, text="Date Range (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        date_frame = ttk.Frame(search_frame)
        date_frame.grid(row=2, column=1, sticky=tk.EW, pady=5)

        ttk.Label(date_frame, text="From:").pack(side=tk.LEFT, padx=5)
        self.search_from_entry = ttk.Entry(date_frame, width=15)
        self.search_from_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(date_frame, text="To:").pack(side=tk.LEFT, padx=5)
        self.search_to_entry = ttk.Entry(date_frame, width=15)
        self.search_to_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            search_frame, text="🔍 Search", command=self.search_by_date
        ).grid(row=2, column=2, padx=5)

        search_frame.columnconfigure(1, weight=1)

        # Results
        results_frame = ttk.LabelFrame(self.search_tab, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Date", "Type", "Category", "Amount", "Description")
        self.search_tree = ttk.Treeview(
            results_frame, columns=columns, height=15, show="headings"
        )

        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(
            results_frame, orient=tk.VERTICAL, command=self.search_tree.yview
        )
        self.search_tree.configure(yscroll=scrollbar.set)

        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def search_by_description(self):
        """Search transactions by description."""
        query = self.search_desc_entry.get()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term")
            return

        results = self.search.search_by_description(query)
        self.display_search_results(results)

    def search_by_amount(self):
        """Search transactions by amount range."""
        try:
            min_amt = float(self.search_min_entry.get()) if self.search_min_entry.get() else 0
            max_amt = float(self.search_max_entry.get()) if self.search_max_entry.get() else float('inf')
            results = self.search.search_by_amount_range(min_amt, max_amt)
            self.display_search_results(results)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amounts")

    def search_by_date(self):
        """Search transactions by date range."""
        from_date = self.search_from_entry.get()
        to_date = self.search_to_entry.get()
        
        if not from_date or not to_date:
            messagebox.showwarning("Warning", "Please enter both dates")
            return

        results = self.search.search_by_date_range(from_date, to_date)
        self.display_search_results(results)

    def display_search_results(self, results):
        """Display search results in the tree."""
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        if not results:
            messagebox.showinfo("Results", "No transactions found")
            return

        for t in results:
            self.search_tree.insert(
                "",
                tk.END,
                values=(
                    t.transaction_id,
                    t.date,
                    t.transaction_type.upper(),
                    t.category,
                    f"${t.amount:.2f}",
                    t.description[:30],
                ),
            )

        messagebox.showinfo("Results", f"Found {len(results)} transaction(s)")

    def on_closing(self):
        """Handle window closing."""
        self.em.close()
        self.root.destroy()


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
