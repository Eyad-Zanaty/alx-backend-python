import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    """Connect to the MySQL server (not to a specific database)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here"  # replace with your actual MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password_here",  # replace with your actual password
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table with specified fields"""
    table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL,
        INDEX (user_id)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(table_query)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, csv_file):
    """Insert data from CSV into user_data table"""
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:

                cursor.execute("SELECT email FROM user_data WHERE email = %s", (row['email'],))
                if cursor.fetchone():
                    continue 

                user_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
