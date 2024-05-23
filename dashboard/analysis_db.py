import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Function to load data from CSV or Excel file
def load_data(file):
    try:
        data = pd.read_excel(file)
    except Exception as e:
        st.error(f"Error: Unable to read file. Error message: {str(e)}")
        return None
    return data

# Function to display data overview
def show_overview(data):
    st.subheader("Data Overview")
    st.write(data.head())

# Function to generate line plot
def generate_line_plot(data):
    st.subheader("Line Plot")
    st.write("Under construction...")

# Function to generate bar plot
def generate_bar_plot(data):
    st.subheader("Bar Plot")
    st.write("Under construction...")

# Function to generate scatter plot
def generate_scatter_plot(data):
    st.subheader("Scatter Plot")
    st.write("Under construction...")

# Function to generate heatmap
def generate_heatmap(data):
    st.subheader("Heatmap")
    st.write("Select columns for heatmap:")
    columns = data.columns.tolist()
    heatmap_columns = st.multiselect("Columns", columns)
    
    if st.button("Generate Heatmap"):
        heatmap_data = data[heatmap_columns]
        plt.figure(figsize=(10, 6))
        sns.heatmap(heatmap_data.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
        st.pyplot()

# Function to generate map chart
def generate_map_chart(data):
    st.subheader("Map Chart")
    st.write("Under construction...")

# Main function
def main():
    st.title("Data Analysis Dashboard")

    # File upload section
    st.sidebar.title("Upload File")
    file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

    if file is not None:
        data = load_data(file)
        
        if data is not None:  # Check if data is loaded successfully
            # Display data overview
            show_overview(data)

            # Chart options
            st.sidebar.title("Chart Options")
            chart_option = st.sidebar.selectbox("Select Chart", ("Line Plot", "Bar Plot", "Scatter Plot", "Heatmap", "Map Chart"))

            # Generate selected chart
            if chart_option == "Line Plot":
                generate_line_plot(data)
            elif chart_option == "Bar Plot":
                generate_bar_plot(data)
            elif chart_option == "Scatter Plot":
                generate_scatter_plot(data)
            elif chart_option == "Heatmap":
                generate_heatmap(data)
            elif chart_option == "Map Chart":
                generate_map_chart(data)

if __name__ == "__main__":
    main()
