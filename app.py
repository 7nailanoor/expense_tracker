from flask import Flask, render_template, request, redirect,url_for
import pymysql
import json
from datetime import datetime
from collections import defaultdict
import calendar


app = Flask(__name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='iamnaila',  # change if your password is different
        db='expense_tracker',
        cursorclass=pymysql.cursors.DictCursor 
    )

# Home route: View expenses with filters and sorting
@app.route('/')
def view_expenses():
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_by = request.args.get('sort_by', 'date')

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT e.id,e.date, c.name AS category, e.amount, e.description
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE 1=1
    """
    filters = []

    if category and category != 'All':
        query += " AND c.name = %s"
        filters.append(category)

    if start_date:
        query += " AND e.date >= %s"
        filters.append(start_date)

    if end_date:
        query += " AND e.date <= %s"
        filters.append(end_date)

    if sort_by == 'amount':
        query += " ORDER BY e.amount DESC"
    else:
        query += " ORDER BY e.date DESC"

    cursor.execute(query, filters)
    expenses = cursor.fetchall()

    cursor.execute("SELECT name FROM categories")
    categories = [row['name'] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return render_template('expenses.html', expenses=expenses, categories=categories)
@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('view_expenses'))




@app.route("/add", methods=["GET", "POST"])
def add_expense():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        amount = request.form["amount"]
        date = request.form["date"]
        description = request.form["description"]
        category_id = request.form["category"]

        cursor.execute(
            "INSERT INTO expenses (amount, date, description, category_id) VALUES (%s, %s, %s, %s)",
            (amount, date, description, category_id)
        )
        connection.commit()
        return redirect(url_for("dashboard"))

    # GET method: fetch categories
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()  # list of tuples like [(1, 'Food'), (2, 'Travel')]

    cursor.close()
    connection.close()
    return render_template("add.html", categories=categories)





@app.route("/dashboard", methods=["GET"])
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()

    all_months = list(range(1, 13))

    # All years (2000 → current year + 5)
    current_year = datetime.now().year
    all_years = list(range(2000, current_year + 6))

    # Get selected month/year from request or defaults
    selected_month = request.args.get('month', type=int)
    selected_year = request.args.get('year',  type=int)
    # Total spending
    cursor.execute("""
        SELECT SUM(amount) AS total
        FROM expenses
        WHERE MONTH(date)=%s AND YEAR(date)=%s
    """, (selected_month, selected_year))
    total_spending = cursor.fetchone()["total"] or 0

    # Top 3 categories
    cursor.execute("""
        SELECT c.name AS category, SUM(e.amount) AS total
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE MONTH(e.date)=%s AND YEAR(e.date)=%s
        GROUP BY c.name
        ORDER BY total DESC
        LIMIT 3
    """, (selected_month, selected_year))
    top_categories = cursor.fetchall()

    # Pie chart data
    cursor.execute("""
        SELECT c.name AS category, SUM(e.amount) AS total
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE MONTH(e.date)=%s AND YEAR(e.date)=%s
        GROUP BY c.name
    """, (selected_month, selected_year))
    pie_data = cursor.fetchall()

    # Budgets for selected month/year
    month_year_str = f"{selected_year}-{str(selected_month).zfill(2)}"
    cursor.execute("""
        SELECT category, budget_limit
        FROM budgets
        WHERE month_year=%s
    """, (month_year_str,))
    budget_data = cursor.fetchall()
    budgets = {row["category"]: row["budget_limit"] for row in budget_data}

    # All categories
    cursor.execute("SELECT name FROM categories")
    all_categories = [row["name"] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        available_months=all_months,
        available_years=all_years,
        selected_month=selected_month,
        selected_year=selected_year,
        total_spending=total_spending,
        top_categories=top_categories,
        pie_data=pie_data,
        budgets=budgets,
        all_categories=all_categories
    )

@app.route("/set_budget", methods=["POST"])
def set_budget():
    month = int(request.form.get("month"))
    year = int(request.form.get("year"))
    month_year = f"{year}-{str(month).zfill(2)}"

    connection = get_db_connection()
    cursor = connection.cursor()

    for key, value in request.form.items():
        if key.startswith("budget_limit_") and value:
            category = key.replace("budget_limit_", "")
            cursor.execute("""
                INSERT INTO budgets (category, month_year, budget_limit)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE budget_limit=VALUES(budget_limit)
            """, (category, month_year, value))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(f"/dashboard?month={month}&year={year}")
# All your routes here...

@app.template_filter('month_name')
def month_name(month_number):
    import calendar
    return calendar.month_name[month_number]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


