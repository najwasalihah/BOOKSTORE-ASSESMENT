#!/usr/bin/env python
# coding: utf-8


import pyodbc

# Replace with your actual connection details
server = 'Najwa\SQLEXPRESS'
database = 'bookstore'
username = 'adam'
password = '1234'

# Establish a connection
connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)



#CREATE TABLE CUSTOMERS // SCHEMA GENERATION QUERY
cursor = connection.cursor()

cursor.execute('''
                CREATE TABLE customers (
                id INT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                tel VARCHAR(20),
                created_at DATE,
                updated_at DATE)
''')

connection.commit()



#CREATE TABLE INVOICES // SCHEMA GENERATION QUERY
cursor = connection.cursor()

cursor.execute('''
                CREATE TABLE invoices (
                id INT PRIMARY KEY,
                number VARCHAR(50),
                sub_total DECIMAL(10, 2),
                tax_total DECIMAL(10, 2),
                total DECIMAL(10, 2),
                customer_id INT,
                created_at DATE,
                updated_at DATE,
                FOREIGN KEY (customer_id) REFERENCES customers(id))
''')

connection.commit()




#CREATE TABLE INVOICE LINE // SCHEMA GENERATION QUERY

cursor = connection.cursor()

cursor.execute('''
                CREATE TABLE invoice_line (
                id INT PRIMARY KEY,
                description VARCHAR(255),
                unit_price DECIMAL(10, 2),
                quantity INT,
                sub_total DECIMAL(10, 2),
                tax_total DECIMAL(10, 2),
                total DECIMAL(10, 2),
                tax_id INT,
                sku_id INT,
                invoice_id INT,
                FOREIGN KEY (invoice_id) REFERENCES invoices(id))
''')

connection.commit()



cursor = connection.cursor()

# Query 1: Number of customers purchasing more than 5 books
sql_query1 = '''
    SELECT
        c.id,
        c.name,
        COUNT(DISTINCT i.id) AS number_of_invoices,
        SUM(il.quantity) AS total_books_purchased
    FROM
        customers AS c
    JOIN
        invoices AS i ON c.id = i.customer_id
    JOIN
        invoice_line AS il ON i.id = il.invoice_id
    GROUP BY
        c.id, c.name
    HAVING
        SUM(il.quantity) > 5;
'''

cursor.execute(sql_query1)
columns1 = [column[0] for column in cursor.description]
print(columns1)
row1 = cursor.fetchall()
for row in row1:
    print(row)


cursor = connection.cursor()

# Query 2: List of customers who never purchased anything
sql_query2 = '''
    SELECT
        c.id,
        c.name
    FROM
        customers c
    WHERE NOT EXISTS (
        SELECT 1
        FROM invoices i
        WHERE i.customer_id = c.id
    );
'''

cursor.execute(sql_query2)
columns2 = [column[0] for column in cursor.description]
print(columns2)
row2 = cursor.fetchall()
for row in row2:
    print(row)


cursor = connection.cursor()

# Query 3: List of books purchased with user information
sql_query3 = '''
    SELECT
        c.id AS customer_id,
        c.name AS customer_name,
        il.description AS book_name,
        il.sku_id,
        il.quantity,
        il.unit_price
    FROM
        customers c
    JOIN
        invoices i ON c.id = i.customer_id
    JOIN
        invoice_line il ON i.id = il.invoice_id;
'''

cursor.execute(sql_query3)
columns3 = [column[0] for column in cursor.description]
print(columns3)
row3 = cursor.fetchall()
for row in row3:
    print(row)



cursor.close()

