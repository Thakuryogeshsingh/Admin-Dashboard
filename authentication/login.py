import streamlit as st
import mysql.connector
from mysql.connector import Error
from bcrypt import checkpw
import os

# Function to create database connection
def create_connection(host, user, password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        # st.write("Connected to MySQL database")
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
    return connection

# Function to verify user credentials
def authenticate_user(connection, username, password):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT UserID, Password FROM myuser WHERE UserID = %s AND Password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            st.error("Invalid username or password. Please try again.")
            return False
    except Error as e:
        st.error(f"Error authenticating user: {e}")
        return False

def login(connection):
    st.title("Login")
    # st.write("Please enter your credentials to login.")
    username = st.text_input("UserID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(connection, username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    # Database connection configuration
    host = "127.0.0.1"
    user = "root"
    password = "Anay@123"
    database = "anaysingh"
    
    # Create database connection
    connection = create_connection(host, user, password, database)
    
    if connection:
        login(connection)
    else:
        st.error("Failed to connect to the database.")

# Get the current working directory
current_directory = os.getcwd()
print("Current directory:", current_directory)

# List all files and directories in the current directory
files_and_directories = os.listdir(current_directory)
print("Files and directories in the current directory:", files_and_directories)