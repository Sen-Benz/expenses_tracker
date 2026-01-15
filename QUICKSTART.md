# QUICK START GUIDE

## 🚀 Getting Started with Expense Tracker

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
   ```bash
   cd expense_tracker
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎯 How to Use

### Option 1: GUI Application (Recommended for beginners)

```bash
python launch_gui.py
```

**GUI Tabs:**

1. **📊 Dashboard**
   - View your financial summary
   - See income, expenses, and current balance
   - Visual expense breakdown

2. **➕ Add Expense**
   - Add expenses with categories
   - Add income transactions
   - Use quick-add buttons for common expenses
   - Set custom dates

3. **📋 Transactions**
   - View all transactions
   - Filter by type (All/Income/Expenses)
   - Delete transactions
   - Sort by date

4. **📈 Reports**
   - Generate detailed reports
   - Export to CSV
   - Export to PDF
   - View category breakdown

5. **🎯 Budget**
   - Set budgets for categories
   - View budget status
   - Track spending vs budget
   - See remaining budget

6. **📉 Analytics** (NEW!)
   - Spending trends
   - Savings rate calculation
   - 3-month expense forecast
   - Budget alerts and warnings

7. **🔍 Search** (NEW!)
   - Search by description
   - Search by amount range
   - Search by date range
   - Combined searches

---

### Option 2: CLI Application

```bash
python src/main.py
```

**Available Commands:**

```
Transaction Management:
  add-income <amount> <description>
  add-expense <amount> <category> <description>
  list-all
  list-income
  list-expenses
  delete <id>

Reports:
  summary
  detailed-report
  category-report
  monthly-report
  filter-date <start> <end>

Budget:
  set-budget <category> <amount>
  budget-report

Export:
  export-csv <filename>
  export-pdf <filename>
  visualize

Utility:
  help
  categories
  exit
```

---

### Option 3: Run Demo

```bash
python demo.py
```

This will:
- Add sample transactions
- Set sample budgets
- Generate reports
- Create visualizations
- Export data to CSV

---

## 📊 Example Workflow

### GUI Example:
1. Launch: `python launch_gui.py`
2. Go to **Add Expense** tab
3. Click "🍔 Food" to add $15 for food
4. Add more expenses using quick buttons
5. Go to **Dashboard** to see summary
6. Go to **Analytics** to see trends
7. Go to **Search** to find specific transactions
8. Go to **Reports** to export data

### CLI Example:
```bash
python src/main.py

# Add transactions
add-income 5000 "Monthly salary"
add-expense 50 Food "Groceries"
add-expense 1200 Rent "Monthly rent"

# View summary
summary

# Check budget
budget-report

# Export
export-csv my_expenses.csv

# Exit
exit
```

---

## 📁 Project Structure

```
expense_tracker/
├── src/
│   ├── main.py              # CLI application
│   ├── gui.py               # GUI application
│   ├── database.py          # Database management
│   ├── expense_manager.py   # Core business logic
│   ├── report_generator.py  # Reports
│   ├── visualizer.py        # Charts
│   └── advanced_features.py # Analytics & Search
├── data/
│   └── expenses.db          # SQLite database
├── reports/                 # Generated charts
├── launch_gui.py            # GUI launcher
├── demo.py                  # Demo script
└── requirements.txt         # Dependencies
```

---

## 💡 Tips & Tricks

### Quick Add Features
- Use the quick-add buttons on the Add Expense tab
- Set default amounts for common expenses
- Bulk add expenses using CLI with scripts

### Budget Management
- Set realistic budgets for each category
- Check Analytics tab for warnings
- Review budget status regularly

### Data Export
- Export to CSV for spreadsheet analysis
- Generate PDF reports for sharing
- Create charts for presentations

### Search Tips
- Use partial descriptions to find transactions
- Search by amount range to find unusual expenses
- Filter by date to analyze specific periods

---

## 🐛 Troubleshooting

### GUI won't launch
```bash
# Verify tkinter is installed (comes with Python)
python -m tkinter  # Should open a test window

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database errors
```bash
# Delete the database and restart (creates new one)
rm data/expenses.db
python launch_gui.py
```

### Import errors
```bash
# Reinstall all packages
pip install -r requirements.txt
```

---

## 📞 Need Help?

- Check the README.md for detailed documentation
- Run `help` command in CLI application
- Review example transactions using `python demo.py`

---

## 🎓 Learning from This Project

This project demonstrates:
- **Python fundamentals**: Classes, functions, file I/O
- **Database design**: SQLite schema and queries
- **GUI development**: Tkinter widgets and layouts
- **Data analysis**: Pandas operations and statistics
- **Visualization**: Matplotlib charts and graphs
- **Testing**: Pytest unit tests
- **Export formats**: CSV and PDF generation

---

**Happy expense tracking! 💰**
