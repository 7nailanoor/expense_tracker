#  Personal Expense Tracker Web App

This is a web-based personal expense tracker built using **Python Flask**, **MySQL**, **HTML/CSS**, **Bootstrap**, and **Chart.js**. The application allows users to manage their expenses by category, set monthly budgets, and visualize spending through dashboards.


##  Features

- Add, view, edit, and delete expenses.
- Filter expenses by date range, category, or amount.
- Dashboard with total expenses and category-wise chart.
- Set monthly budget limits per category.
- Responsive user interface using Bootstrap 5.


##  How to Run the App Locally

### ✅ Requirements

- Python 3.x
- MySQL Server
- pip (Python package manager)

### 📥 Step-by-Step Setup

1. **Clone or Download this Project**
   ```bash
   git clone https://github.com/7nailanoor/expense-tracker.git
   cd expense-tracker
   ```

2. **Install Required Python Packages**
   ```bash
   pip install flask pymysql
   ```

3. **Set Up MySQL Database**
   - Open MySQL Workbench or CLI.
   - Run the SQL script provided in `database.sql` (or the SQL code below):

   ```sql
   CREATE DATABASE expense_tracker;

   USE expense_tracker;

   CREATE TABLE categories (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50) NOT NULL,
       budget_limit DECIMAL(10, 2) DEFAULT 0.00
   );

   INSERT INTO categories (name) VALUES ('Food'), ('Travel'), ('Utilities'), ('Others');

   CREATE TABLE expenses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       amount DECIMAL(10, 2),
       date DATE,
       category VARCHAR(50),
       description VARCHAR(255)
   );
   ```

4. **Run the Flask App**
   ```bash
   python app.py
   ```

5. **Open in Browser**
   Navigate to: `http://127.0.0.1:5000/`


##  Folder Structure

```
expense-tracker/
│
├── app.py
├── templates/
│   ├── base.html
│   ├── add_expense.html
│   ├── expenses.html
│   ├── dashboard.html
├── static/
│   └── style.css
└── README.md
```



