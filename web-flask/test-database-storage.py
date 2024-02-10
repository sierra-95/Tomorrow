import mysql.connector

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "Tomorrow",
    "password": "P@ssword@!967",
    "database": "Tomorrow"
}

# Establish a connection
connection = mysql.connector.connect(**db_config)

# Create a cursor
cursor = connection.cursor()

# Execute a query to retrieve data from the users table
cursor.execute("SELECT * FROM users")

# Fetch all rows
result = cursor.fetchall()

# Print the data
for row in result:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
