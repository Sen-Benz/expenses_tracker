# Expense Tracker App

A comprehensive Python-based expense tracking application for managing income, expenses, and generating detailed financial reports.

## Features

✨ **Core Functionality**
- 💰 Track income and expenses with categories
- 📊 Generate summary and detailed reports
- 📈 Visualize spending patterns with charts
- 🏦 Budget tracking and alerts
- 📅 Date-based filtering and sorting
- 💾 Data persistence with SQLite database
- 📄 Export reports to CSV and PDF formats

✨ **GUI Features**
- 📊 **Dashboard**: Real-time financial overview with automatic updates
- ➕ **Add Expense**: Intuitive form with quick-add buttons for common expenses
- 📋 **Transactions**: View, filter, and delete transactions with advanced filtering
- 📈 **Reports**: Generate comprehensive reports and export to CSV/PDF
- 🎯 **Budget**: Set budgets per category with visual status indicators
- 📉 **Analytics**: Spending trends, savings rate, and expense forecasting
- 🔍 **Search**: Powerful search by description, amount range, date range, and category

✨ **Advanced Features**
- 💡 Spending analytics with category trends
- 📊 3-month expense forecasting
- ⚠️ Smart budget alerts and warnings
- 🔍 Advanced transaction search and filtering
- 📱 Responsive GUI design with color-coded data

## Project Structure

```
expense_tracker/
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── database.py             # Database management
│   ├── transaction.py          # Transaction model
│   ├── expense_manager.py      # Core business logic
│   ├── report_generator.py     # Report creation
│   └── visualizer.py           # Charts and graphs
├── data/
│   └── expenses.db             # SQLite database
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_expense_manager.py
│   └── test_reports.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. **Clone or download the project**
   ```bash
   cd expense_tracker
   ```

2. **Create a virtual environment** (optional but recommended)
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

## Usage

### Run the GUI Application (Recommended)

```bash
python launch_gui.py
```

**Features:**
- 📊 **Dashboard**: Visual summary of income, expenses, and balance
- ➕ **Add Expense**: Easy form to add expenses and income with quick-add buttons
- 📋 **Transactions**: View, filter, and delete transactions
- 📈 **Reports**: Generate detailed reports and export to CSV/PDF
- 🎯 **Budget**: Set and track budgets for expense categories

### Run the CLI Application

```bash
python src/main.py
```

### Available Commands

```
Commands:
  add-income <amount> <description>          Add income
  add-expense <amount> <category> <desc>     Add expense
  list-all                                   List all transactions
  list-expenses                              List only expenses
  list-income                                List only income
  filter-date <YYYY-MM-DD> <YYYY-MM-DD>    Filter by date range
  summary                                    Display summary report
  detailed-report                            Generate detailed report
  budget <category> <amount>                 Set category budget
  visualize                                  Generate charts
  export-csv <filename>                      Export to CSV
  export-pdf <filename>                      Export to PDF
  help                                       Show help
  exit                                       Exit application
```

### Example Usage

```bash
# Add an income transaction
add-income 3000 "Monthly Salary"

# Add expense transactions
add-expense 50 Food "Groceries"
add-expense 1200 Rent "Monthly rent"
add-expense 30 Transport "Gas"

# View all transactions
list-all

# Get summary
summary

# Export to CSV
export-csv expenses_report.csv

# Generate visualization
visualize

# Generate PDF report
export-pdf monthly_report.pdf
```

## Features in Detail

### 📊 Transaction Management
- Add, view, and delete transactions
- Categorize expenses (Food, Rent, Transport, Entertainment, etc.)
- Track both income and expenses
- Automatic date/time tracking

### 📈 Reporting
- Summary reports (total income, expenses, balance)
- Detailed transaction history
- Category-wise breakdown
- Date-range filtering
- CSV and PDF export

### 📉 Visualizations
- Pie charts for expense distribution by category
- Bar charts for monthly trends
- Income vs. expense comparison
- Budget vs. actual spending

### 💡 Budget Management
- Set budget limits per category
- Track spending against budget
- Budget alerts and warnings

## Requirements

- Python 3.8+
- pandas
- matplotlib
- seaborn
- reportlab
- tabulate

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 guidelines. For linting:

```bash
pip install pylint
pylint src/
```

## Future Enhancements

- [ ] Web interface using Flask/Django
- [ ] Database backup and sync
- [ ] Recurring transactions
- [ ] Multi-user support
- [ ] Mobile app
- [ ] Cloud synchronization
- [ ] Email report delivery
- [ ] Smart expense categorization

## License

MIT License - feel free to use this project for learning purposes.

## Author

Your Name - Entry Level Portfolio Project

---

## Skills Demonstrated

✅ **Python Programming**
- OOP principles
- File I/O and data persistence
- Error handling

✅ **Data Management**
- Database design with SQLite
- Data manipulation with pandas
- CSV/JSON handling

✅ **Data Analysis & Visualization**
- Matplotlib and Seaborn charts
- Statistical analysis
- Report generation

✅ **Software Engineering**
- Project structure and organization
- Testing and TDD
- Documentation
- Git version control

✅ **CLI Development**
- User input handling
- Command parsing
- Interactive menus
