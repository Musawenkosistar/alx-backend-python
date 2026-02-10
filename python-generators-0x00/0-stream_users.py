import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# ---------- 1. Connect to MySQL server ----------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',       # change if your MySQL user is different
            password=''        # change if you have a password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ---------- 2. Create ALX_prodev database ----------
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev ensured.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    finally:
        cursor.close()

# ---------- 3. Connect to ALX_prodev database ----------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ---------- 4. Create user_data table ----------
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        UNIQUE(email)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data ensured.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

# ---------- 5. Generator to read CSV row by row ----------
def csv_row_generator(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row

# ---------- 6. Insert data into table ----------
def insert_data(connection, data):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE name=VALUES(name), age=VALUES(age)
    """
    for row in data:
        cursor.execute(insert_query, (
            str(uuid.uuid4()),  # generate UUID
            row['name'],
            row['email'],
            row['age']
        ))
    connection.commit()
    cursor.close()
    print("Data inserted successfully.")

# ---------- 7. Main execution ----------
if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    conn = connect_db()
    if not conn:
        exit()

    # Step 2: Create database
    create_database(conn)
    conn.close()

    # Step 3: Connect to ALX_prodev
    conn = connect_to_prodev()
    if not conn:
        exit()

    # Step 4: Create table
    create_table(conn)

    # Step 5 & 6: Read CSV and insert data
    csv_file = 'user_data.csv'  # make sure this file exists in the same directory
    generator = csv_row_generator(csv_file)
    insert_data(conn, generator)

    conn.close()

