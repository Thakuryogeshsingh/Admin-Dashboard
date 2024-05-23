import streamlit as st
import pandas as pd
import mysql.connector
import random
import string
import matplotlib.pyplot as plt
import seaborn as sns

# Function to generate a random 6-digit User ID
def generate_user_id():
    return ''.join(random.choices(string.digits, k=6))

# Function to connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Anay@123",
        database="anaysingh"
    )

# Function to load data from MySQL
def load_data_from_mysql():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("SELECT UserID, Name, Email, PhoneNumber, Password, Status FROM myuser")
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=['UserID', 'Name', 'Email', 'PhoneNumber', 'Password', 'Status'])

# Function to save data to MySQL
def save_data_to_mysql(data):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE myuser")
    for index, row in data.iterrows():
        cursor.execute("INSERT INTO myuser (UserID, Name, Email, PhoneNumber, Password, Status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (row['UserID'], row['Name'], row['Email'], row['PhoneNumber'], row['Password'], row['Status']))
    conn.commit()
    conn.close()

# Main dashboard
st.title("User Management Dashboard")

# Function to display all users
def display_users():
    st.subheader("All Users")
    data = load_data_from_mysql()
    st.dataframe(data)

    # Summary
    st.subheader("Summary")
    total_users = data.shape[0]
    active_users = data[data['Status'] == 'Active'].shape[0]
    inactive_users = data[data['Status'] == 'Inactive'].shape[0]
    st.metric("Total Users", total_users)
    st.metric("Active Users", active_users)
    st.metric("Inactive Users", inactive_users)

    # Line Chart for User Activity Trend
    user_activity_data = data.groupby('Status').size().reset_index(name='Count')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=user_activity_data, x='Status', y='Count', marker='o', color='b')
    plt.title('User Activity Trend')
    plt.xlabel('User Status')
    plt.ylabel('Number of Users')
    st.pyplot(plt)

# Function to add a new user
def add_user():
    st.subheader("Add User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    password = st.text_input("Password", type="password")
    status = st.selectbox("Status", ["Active", "Inactive"])
    if st.button("Add User"):
        data = load_data_from_mysql()
        if email in data['Email'].values:
            st.error("Email already exists. Please use a different email.")
        elif any(str(user_id) == email for user_id in data['UserID'].values):
            st.error("User ID already exists. Please try again.")
        else:
            new_user_id = generate_user_id()
            new_user = pd.DataFrame([[new_user_id, name, email, phone_number, password, status]], columns=data.columns)
            data = pd.concat([data, new_user], ignore_index=True)
            save_data_to_mysql(data)
            st.success(f"User added successfully! User ID: {new_user_id}")

# Function to edit an existing user
def edit_user():
    st.subheader("Edit User")
    data = load_data_from_mysql()
    edit_user_id = st.selectbox("Select User ID to edit", data['UserID'])
    if edit_user_id:
        user_to_edit = data[data['UserID'] == edit_user_id]
        if not user_to_edit.empty:
            name = st.text_input("Name", user_to_edit['Name'].values[0])
            email = st.text_input("Email", user_to_edit['Email'].values[0])
            phone_number = st.text_input("Phone Number", user_to_edit['PhoneNumber'].values[0])
            password = st.text_input("Password", user_to_edit['Password'].values[0], type="password")
            status = st.selectbox("Status", ["Active", "Inactive"], index=0 if user_to_edit['Status'].values[0] == 'Active' else 1)
            if st.button("Update User"):
                data.loc[data['UserID'] == edit_user_id, ['Name', 'Email', 'PhoneNumber', 'Password', 'Status']] = [name, email, phone_number, password, status]
                save_data_to_mysql(data)
                st.success("User updated successfully!")
        else:
            st.error("User ID not found")

# Function to delete a user
def delete_user():
    st.subheader("Delete User")
    data = load_data_from_mysql()
    delete_user_id = st.selectbox("Select User ID to delete", data['UserID'])
    if delete_user_id:
        if st.button("Confirm Delete"):
            data = data[data['UserID'] != delete_user_id]
            save_data_to_mysql(data)
            st.success("User deleted successfully!")

# Function to search for a user
def search_user():
    st.subheader("Search User")
    data = load_data_from_mysql()
    search_query = st.text_input("Enter UserID or Name to search")
    if st.button("Search"):
        if not search_query:
            st.warning("Please enter a search query.")
        else:
            search_result = data[data['UserID'].astype(str).str.contains(search_query) | data['Name'].str.contains(search_query, case=False)]
            if not search_result.empty:
                st.write("Search Results:")
                st.dataframe(search_result)
            else:
                st.warning("No matching users found.")

# Display different options based on user selection
if __name__ == "__main__":
    option = st.sidebar.radio("Select Option", ["Display Users", "Add User", "Edit User", "Delete User", "Search User"])

    if option == "Display Users":
        display_users()
    elif option == "Add User":
        add_user()
    elif option == "Edit User":
        edit_user()
    elif option == "Delete User":
        delete_user()
    elif option == "Search User":
        search_user()
