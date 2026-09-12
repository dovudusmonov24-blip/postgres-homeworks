"""Скрипт для заполнения данными таблиц в БД Postgres."""

 
import csv
import os
 
import psycopg2
 
# Параметры подключения к БД. При необходимости поменяй под свою локальную настройку
# (например, если у Postgres другой пользователь/пароль/порт).
DB_CONFIG = {
    "dbname": "north",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}
 
DATA_DIR = os.path.join(os.path.dirname(__file__), "north_data")
 
 
def read_csv(filename):
    """Читает csv-файл из папки north_data и возвращает список строк (кортежей)."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # пропускаем заголовок
        return [tuple(row) for row in reader]
 
 
def insert_employees(cur, rows):
    query = """
        INSERT INTO employees (employee_id, first_name, last_name, title, birth_date, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (employee_id) DO NOTHING
    """
    cur.executemany(query, rows)
 
 
def insert_customers(cur, rows):
    query = """
        INSERT INTO customers (customer_id, company_name, contact_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING
    """
    cur.executemany(query, rows)
 
 
def insert_orders(cur, rows):
    query = """
        INSERT INTO orders (order_id, customer_id, employee_id, order_date, ship_city)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
    """
    cur.executemany(query, rows)
 
 
def main():
    employees = read_csv("employees_data.csv")
    customers = read_csv("customers_data.csv")
    orders = read_csv("orders_data.csv")
 
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn:
            with conn.cursor() as cur:
                # Сначала employees и customers (на них ссылается orders),
                # потом сами orders.
                insert_employees(cur, employees)
                insert_customers(cur, customers)
                insert_orders(cur, orders)
        print("Данные успешно загружены в таблицы employees, customers, orders.")
    finally:
        conn.close()
 
 
if __name__ == "__main__":
    main()
