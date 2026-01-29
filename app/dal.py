from typing import List, Dict, Any
from db import get_db_connection


def get_customers_by_credit_limit_range():
    """Return customers with credit limits outside the normal range."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT customerName,creditLimit FROM customers
        WHERE creditLimit > 100000 OR creditLimit < 10000
        """)
        return my_cursor.fetchall()



def get_orders_with_null_comments():
    """Return orders that have null comments."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT orderNumber,comments FROM orders
        WHERE comments IS NULL
        ORDER BY orderDate
        """)
        return my_cursor.fetchall()

def get_first_5_customers():
    """Return the first 5 customers."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT customerName,lastName,firstName FROM customers
        LEFT JOIN employees ON salesRepEmployeeNumber = employeeNumber
        ORDER BY customerName
        LIMIT 5
        """)
        return my_cursor.fetchall()

def get_payments_total_and_average():
    """Return total and average payment amounts."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT SUM(amount),AVG(amount),MIN(amount),MAX(amount) FROM payments
        """)
        return my_cursor.fetchall()

def get_employees_with_office_phone():
    """Return employees with their office phone numbers."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT firstName,lastName,phone FROM employees
        JOIN offices ON employees.officeCode = offices.officeCode
        """)
        return my_cursor.fetchall()

def get_customers_with_shipping_dates():
    """Return customers with their order shipping dates."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT customerName,shippedDate FROM customers 
        LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
        GROUP BY customerName,shippedDate
        """)
        return my_cursor.fetchall()

def get_customer_quantity_per_order():
    """Return customer name and quantity for each order."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT customerName,quantityOrdered FROM orderdetails
        JOIN orders ON orderdetails.orderNumber = orders.orderNumber
        JOIN customers ON orders.customerNumber = customers.customerNumber
        ORDER BY customerName
        """)
        return my_cursor.fetchall()

def get_customers_payments_by_lastname_pattern(pattern: str = "son"):
    """Return customers and payments for last names matching pattern."""
    with get_db_connection().cursor(dictionary=True) as my_cursor:
        my_cursor.execute("""
        SELECT customerName , firstName,lastName,SUM(quantityOrdered*priceEach)  FROM customers
        LEFT JOIN employees ON salesRepEmployeeNumber = employeeNumber
        LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
        JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
        WHERE firstName LIKE '%Mu%' OR firstName LIKE '%Iy%'
        GROUP BY  customerName , firstName, lastName
        ORDER BY SUM(quantityOrdered*priceEach) desc
        """)
        return my_cursor.fetchall()
