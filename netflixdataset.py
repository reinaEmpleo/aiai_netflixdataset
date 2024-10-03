# import streamlit as st

# # Title of the app
# st.title("Testing one two three")

# # Header and Subheader
# st.header("Welcome to Streamlit")
# st.subheader("This is a simple web app built with Streamlit!")

# # Text input
# user_input = st.text_input("Enter your name")

# # Display the user's input
# st.write("Hello, ", user_input)

# # Simple button
# if st.button("Click Me"):
#     st.write("You clicked the button!")

# # Checkbox
# if st.checkbox("Show more"):
#     st.write("Here is more information.")

import streamlit as st
import pandas as pd

# Title of the app
st.title("Netflix Data Science Project")

# Load dataset directly from the file (no user upload)
# Assuming the dataset (e.g., 'netflix_titles.csv') is in your project folder
df = pd.read_csv('netflix_titles.csv')

# Create tabs
OverviewTab, DashboadTab, AnalysisTab = st.tabs(["Dataset Overview", "Dashboard", "Analysis"])

# Data Overview tab
with OverviewTab:  
    # Introduction 
    st.write("### Introduction")
    st.write("Text")
    # Display the dataframe
    st.write("### Netflix Dataset Overview")
    st.dataframe(df)

    # Show basic statistics
    st.write("### Basic Statistics")
    st.write(df.describe())

    # Show the number of rows and columns
    st.write(f"**Number of rows:** {df.shape[0]}")
    st.write(f"**Number of columns:** {df.shape[1]}")

    # Show the first 5 rows of the dataset
    st.write("### First 5 Rows of the Dataset")
    st.write(df.head())

    # Visualizations: Example - Count of titles by type
    st.write("### Count of Titles by Type (Movies/TV Shows)")
    title_type_count = df['type'].value_counts()

    # Bar chart of titles by type
    st.bar_chart(title_type_count)

    # Visualization: Example - Distribution of release years
    st.write("### Distribution of Titles by Release Year")
    release_years = df['release_year'].value_counts().sort_index()

    # Line chart of release year distribution
    st.line_chart(release_years)

    # Filtering: Example - Show all movies released after a certain year
    st.write("### Filtered Data: Movies Released After 2015")
    filtered_df = df[df['release_year'] > 2015]
    st.dataframe(filtered_df)
