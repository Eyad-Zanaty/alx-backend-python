import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields rows from user_data in batches"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes batches and prints users over age 25"""
    for batch in stream_users_in_batches(batch_size):             # loop 1
        filtered = (user for user in batch if user["age"] > 25)   # generator expression (NOT a loop)
        for user in filtered:                                     # loop 2
            print(user)
