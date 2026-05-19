import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger
import os

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def fetch_expenses_by_months():
    logger.info("fetch_expenses_by_months")
    with get_db_cursor() as cursor:
        cursor.execute("""
                SELECT MONTH(expense_date) AS month,
                SUM(amount) AS total_expense 
                FROM expenses 
                GROUP BY Month(expense_date)
                ORDER BY Month(expense_date);
                """)
        expenses = cursor.fetchall()
        # expenses = [{"month": expense[0], "total_expense": float(expense[1])} for expense in expenses]
        return expenses


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )
def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start_date: {start_date}, end_date: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
                select category, sum(amount) as total 
                from expenses
                where expense_date 
                between %s and %s
                group by category
                ;
            """,(start_date, end_date)
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    for expense in expenses:
        print(expense)
    # delete_expenses_for_date("2024-03-27")
    summary = fetch_expense_summary("2024-08-01","2024-08-05")
    for record in summary:
        print(record)