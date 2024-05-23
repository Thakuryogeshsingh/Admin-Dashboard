import mysql.connector

# Establish connection to your MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Anay@123",
    database="anaysingh"
)

# Create cursor object
mycursor = mydb.cursor()

# Execute the SQL query to select data from the table
mycursor.execute("SELECT * FROM register_users")
# Fetch the results
result = mycursor.fetchall()
for row in result:
    print(row)

# Close cursor and connection
mycursor.close()
mydb.close()


import mysql.connector

# Establish connection to your MySQL server
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Anay@123"
)

# Create a cursor object
mycursor = mydb.cursor()

# Execute SQL query to show databases
mycursor.execute("SHOW DATABASES")

# Fetch the results
databases = mycursor.fetchall()

# Print the list of databases
for db in databases:
    print(db[0])

# Close cursor and connection
mycursor.close()
mydb.close()
