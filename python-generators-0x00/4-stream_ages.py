import mysql.connector

def stream_user_ages():
    """Generator that yields ages from user_data table one by one"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password_here",
        database="ALX_prodev"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # loop 1
        yield age

    cursor.close()
    connection.close()


def compute_average_age():
    """Compute and print the average age using the generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users in the database.")
