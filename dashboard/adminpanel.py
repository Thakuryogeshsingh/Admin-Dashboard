import streamlit as st
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="Anay@123",
    database="anaysingh"
)
cursor = db.cursor()

# Streamlit UI
st.title("Admin Panel")

# Function to create user
def create_user(username, email, password):
    query = "INSERT INTO users (username, email, password, Active) VALUES (%s, %s, %s, 1)"
    cursor.execute(query, (username, email, password,))
    db.commit()
    st.success("User created successfully!")

# Function to update user details
def update_user(user_id, new_email):
    query = "UPDATE users SET email = %s WHERE id = %s"
    cursor.execute(query, (new_email, user_id))
    db.commit()
    st.success("User details updated successfully!")

# Function to delete user
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    db.commit()
    st.success("User deleted successfully!")

# Function to toggle user status (active/inactive)
def toggle_user_status(user_id, new_status):
    query = "UPDATE users SET active = %s WHERE id = %s"
    cursor.execute(query, (new_status, user_id))
    db.commit()
    st.success("User status updated successfully!")

# Streamlit UI components
option = st.selectbox("Select action", ["Create User", "Update User", "Delete User", "User Status"])

if option == "Create User":
    st.subheader("Create User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create"):
        create_user(username, email, password)

elif option == "Update User":
    st.subheader("Update User Details")
    user_id = st.text_input("User ID")
    new_email = st.text_input("New Email")
    if st.button("Update"):
        update_user(user_id, new_email)

elif option == "Delete User":
    st.subheader("Delete User")
    user_id = st.text_input("User ID")
    if st.button("Delete"):
        delete_user(user_id)

elif option == "User Status":
    st.subheader("User Status")
    user_id = st.text_input("User ID")
    new_status = st.selectbox("Select Status", ["Active", "Inactive"])
    if st.button("Save"):
        status_code = 1 if new_status == "Active" else 0
        toggle_user_status(user_id, status_code)

# Display admin profile
st.sidebar.subheader("Admin Profile")
st.sidebar.write("Username:, username")
st.sidebar.write("Email: admin@example.com")
