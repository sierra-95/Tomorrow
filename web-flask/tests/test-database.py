import mysql.connector

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "Tomorrow",
    "password": "P@ssword@!967",
    "database": "Tomorrow"
}

# Attempt to establish a connection
try:
    connection = mysql.connector.connect(**db_config)
    print("Connection to the database successful!")

    # Close the connection
    connection.close()
except mysql.connector.Error as err:
    print(f"Error: {err}")
