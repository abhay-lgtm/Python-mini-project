# Smart Expense Tracker Pro 💰

A comprehensive Python-based expense tracking application with advanced features including financial insights, goal tracking, budget management, and intelligent spending analysis.

## 🌟 Features

### 1. **Financial Insights & Visualization** 📊
- **Weekly & Monthly Reports**: Generate detailed financial reports with key statistics
- **Visual Charts**: Interactive pie and bar charts showing spending distribution by category
- **Key Statistics**: 
  - Total spent in period
  - Daily average spending
  - Top 3 expense categories
  - Remaining balance
- **Export Reports**: Save reports to text files for record keeping

### 2. **Goal-Based Savings** 🎯
- **Set Financial Goals**: Create goals with target amounts and deadlines (e.g., "Save ₹2000 for earphones")
- **Progress Tracking**: Automatically track progress toward each goal
- **Smart Notifications**: Get notified when:
  - You're 80% toward your goal
  - Goal is completed
  - Deadline is approaching (within 7 days)
- **Optional Balance Locking**: Set aside goal money from available balance

### 3. **Smart Budget Reminders** 💵
- **Weekly/Monthly Budgets**: Set spending limits for specific categories or overall
- **Budget Tracking**: Real-time tracking of budget utilization
- **Smart Alerts**: Warnings when spending approaches or exceeds budget limits
- **Customizable Thresholds**: Set custom alert percentages (default 80%)
- **Budget Status Levels**: Safe, Caution, Warning, Exceeded

### 4. **Enhanced Expense Categorization** 🏷️
Predefined categories include:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Personal Care
- Groceries
- Rent
- Savings
- Other

### 5. **Smart Suggestions & Insights** 💡
- **Spending Anomaly Detection**: Alerts when spending is 20% higher than average
- **Cost-Saving Suggestions**: 
  - Identifies high-spending categories
  - Detects frequent small expenses
  - Highlights unusually large transactions
  - Suggests potential savings opportunities
- **Spending Trends**: Analyze whether spending is increasing, decreasing, or stable
- **Month-over-Month Comparison**: Compare current spending with previous months

### 6. **Data Management** 💾
- **Persistent Storage**: All data stored in structured JSON files
- **Export to CSV**: Export expenses for analysis in Excel/Google Sheets
- **View History**: Browse all past transactions
- **Delete Expenses**: Right-click to delete unwanted entries
- **Automatic Backups**: Data persists across sessions

### 7. **User-Friendly GUI** 🖥️
- Clean, intuitive Tkinter interface
- Menu bar for quick access to all features
- Real-time alert notifications
- Quick action buttons
- Context menus for common actions
- Color-coded status indicators

## 📁 Project Structure

```
Python-mini-project/
│
├── balance_manager.py      # Manages account balance
├── tracker.py              # Core expense tracking with enhanced features
├── reports.py              # Financial reports and visualizations
├── goals.py                # Goal-based savings management
├── budgets.py              # Budget tracking and alerts
├── insights.py             # Smart suggestions and spending analysis
├── gui_app.py              # Main GUI application
│
├── balance.json            # Stores current balance
├── expenses.json           # Stores all expense records
├── goals.json              # Stores financial goals
├── budgets.json            # Stores budget configurations
│
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Standard libraries: `tkinter`, `json`, `datetime`, `csv`, `collections`
- **matplotlib** (for charts): `pip install matplotlib`

### Installation

1. **Clone or download the repository**

2. **Install matplotlib** (required for charts):
   ```bash
   pip install matplotlib
   ```

3. **Run the application**:
   ```bash
   python gui_app.py
   ```

### First-Time Setup

1. **Set Initial Balance**:
   - Click "Update Balance" button
   - Enter your starting balance

2. **Start Adding Expenses**:
   - Select a category from dropdown
   - Enter amount
   - Add optional note
   - Choose whether to deduct from balance
   - Click "Add Expense"

## 📖 How to Use

### Adding Expenses
1. Select category from dropdown
2. Enter amount
3. Add optional note for reference
4. Check/uncheck "Deduct from balance" as needed
5. Click "Add Expense"

### Viewing Reports
- **Menu Bar**: View → Weekly Report / Monthly Report
- **Quick Actions**: Click "📊 Reports" button
- Reports show:
  - Key statistics
  - Top 3 categories
  - Visual charts (pie & bar)
  - Detailed breakdown

### Setting Goals
1. Click "🎯 Goals" button
2. Click "Add New Goal"
3. Enter goal details:
   - Goal name (e.g., "Save for laptop")
   - Target amount
   - Optional deadline
   - Optional balance locking
4. Track progress in goals window

### Managing Budgets
1. Click "💵 Budgets" button
2. Click "Add New Budget"
3. Configure budget:
   - Category (or "Overall")
   - Budget amount
   - Period (weekly/monthly)
   - Alert threshold (%)
4. Get automatic warnings when approaching limits

### Viewing Insights
- Click "💡 Insights" button to see:
  - Spending anomalies
  - Cost-saving suggestions
  - Spending trends
  - Month-over-month comparisons

### Exporting Data
- **CSV Export**: File → Export Expenses (CSV)
- **Report Export**: File → Export Report (TXT)
- Files saved in project directory

## 🔧 Technical Details

### Data Persistence
- **JSON Format**: All data stored in human-readable JSON files
- **Automatic Saving**: Changes saved immediately
- **No Database Required**: Lightweight file-based storage

### Alert System
- Automatic alert checking every 30 seconds
- Real-time notifications in top info bar
- Comprehensive alert types:
  - Budget warnings
  - Goal progress updates
  - Spending anomalies

### Modular Architecture
- Clean separation of concerns
- Each module has specific responsibility
- Easy to extend and maintain
- Well-documented with docstrings

## 🎯 Example Workflow

1. **Morning**: Open app, check alerts in top bar
2. **Throughout Day**: Add expenses as they occur
3. **Evening**: Review daily spending in expense list
4. **Weekly**: Check weekly report for insights
5. **Monthly**: 
   - Review monthly report
   - Check goal progress
   - Review budget status
   - Read smart suggestions

## 📊 Sample Use Cases

### Student Budget Management
- Set monthly budget for different categories
- Track expenses for food, transport, books
- Set savings goals for gadgets or trips
- Get alerts when overspending

### Personal Finance Tracking
- Monitor all personal expenses
- Analyze spending patterns
- Identify areas to cut costs
- Track progress toward financial goals

### Project Expense Tracking
- Track project-related expenses
- Categorize by expense type
- Export data for reports
- Maintain balance records

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest features
- Fork and improve
- Share feedback

## 📝 Future Enhancements (Optional)

Potential features for future versions:
- Multi-user support
- Cloud synchronization
- Mobile app companion
- Receipt scanning
- Recurring expenses
- Investment tracking
- Tax calculation helpers

## 👨‍💻 Authors

Student Expense Tracker Project

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Visualization powered by matplotlib
- Inspired by modern expense tracking needs

---

**Note**: This application requires matplotlib for chart visualization. Install it using `pip install matplotlib` before running the application.

**For Support**: Check the code comments and docstrings for detailed explanations of each function.
