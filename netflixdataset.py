import streamlit as st

# Title of the app
st.title("Testing one two three")

# Header and Subheader
st.header("Welcome to Streamlit")
st.subheader("This is a simple web app built with Streamlit!")

# Text input
user_input = st.text_input("Enter your name")

# Display the user's input
st.write("Hello, ", user_input)

# Simple button
if st.button("Click Me"):
    st.write("You clicked the button!")

# Checkbox
if st.checkbox("Show more"):
    st.write("Here is more information.")
