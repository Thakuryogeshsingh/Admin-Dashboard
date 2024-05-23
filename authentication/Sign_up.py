import streamlit as st
import mysql.connector
from mysql.connector import Error
from bcrypt import hashpw, gensalt

# Function to securely hash passwords
def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to verify hashed password
def verify_password(plain_password, hashed_password):
    return hashpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password.encode('utf-8')

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
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
    return connection

# Function to create user table if it doesn't exist
def create_user_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating user table: {e}")

# Function to handle signup
def signup(connection):
    st.title("Sign Up")
    st.write("Create an account to access the application.")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            hashed_password = hash_password(password)
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO users (username, email, password) 
                    VALUES (%s, %s, %s)
                """, (username, email, hashed_password))
                connection.commit()
                st.success("Account created successfully!")
                st.write(f"Username: {username}")
                st.write(f"Email: {email}")
                st.write("Go to login page:", "[Login](../authentication/login.py)")


            except Error as e:
                st.error(f"Error creating user: {e}")
        else:
            st.error("Passwords do not match. Please try again.")

if __name__ == "__main__":
    # Database connection configuration
    host = "localhost"
    user = "root"
    password ="Anay@123"
    database = "anaysingh"
    
    connection = create_connection(host, user, password, database)
    create_user_table(connection)
    signup(connection)
