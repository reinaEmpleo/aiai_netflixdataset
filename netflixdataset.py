import streamlit as st
import pandas as pd
from PIL import Image


# Set the page configuration
st.set_page_config(
    page_title="Netflix Dataset Report",
    page_icon=":tv:",
    layout="centered",
)


# Load the image using PIL (Make sure the image is in your project folder)
image = Image.open("pic.jpg")


# Display the image in the background with custom CSS for blur
st.markdown(
    f"""
    <style>
  @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap');

    /* Background styling */
    .background {{
        position: fixed;
        top: 0;
        left: 0;
        width: 50%;
        height: 50%;
        background-image: url('data:image/jpeg;base64,{st.image(image).image_data}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        z-index: -2;
    }}

    /* Main content */
    .main-content {{
        font-family: 'Lato', sans-serif;
        color: white;
        position: relative;
        z-index: 1;
    }}

    /* h1 styling (for title) */
    h1 {{
        font-family: 'Lato', sans-serif;
        font-size: 60px;
        font-weight: 900;  
        letter-spacing: 2px;  
        color: white;
    }}

    /* h3 styling (for subheaders) */
    h2, h3 {{
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;  /* Letter spacing */
        color: white;
        margin-bottom: 20px;
    }}

    .intro-text {{
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 400;  /* Lighter weight */
        letter-spacing: 1.4px;  /* Letter spacing */
        font-style: italic;
        line-height: 1.5;
        color: white;
        margin-top:5px;
    }}
    </style>

    <div class="background"></div>
    """,
    unsafe_allow_html=True
)

# Title of the app with 'h1' tag style
st.title("Netflix Data Science Project")

# Load dataset directly from the file
df = pd.read_csv('netflix_titles.csv')

# Create tabs
OverviewTab, DashboadTab, AnalysisTab = st.tabs(["Dataset Overview", "Dashboard", "Analysis"])

# Data Overview tab
with OverviewTab:  
    st.markdown(
        '<p class="intro-text">Netflix is one of the most widely used media and video streaming platforms. They have over 8000 movies and television shows available on their platform, and as of mid-2021, they had over 200 million subscribers worldwide. This tabular dataset, found in Kaggle, contains listings of all the movies and TV shows accessible on Netflix, together with information such as cast, directors, ratings, release year, duration, and so on.</p>', 
        unsafe_allow_html=True
    )
    st.markdown(
    '''
    <p class="intro-text">
    The key goals of our data analysis for this Netflix dataset are to obtain more information into the platform's content distribution and patterns. 
    We wanted to know how many Netflix titles are available in different countries, as well as how much content is available in each. 
    In addition, we wanted to know if Netflix had focused more on developing TV episodes or films in recent years. 
    We investigated how the quantity of releases has changed over time by evaluating the data. 
    Finally, we investigated genre trends, determining what genres are prevalent or noticeable in certain countries, 
    as well as which genres are frequently generated in specific regions.
    </p>
    ''', 
    unsafe_allow_html=True
    )

    st.divider()
    # Display the dataframe
    st.write("## Netflix Dataset Overview", ":bar_chart:")
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

