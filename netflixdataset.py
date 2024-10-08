import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px  # Import Plotly for interactive graphs

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

    .main-content {{
        font-family: 'Lato', sans-serif;
        color: white;
        position: relative;
        z-index: 1;
    }}

    h1 {{
        font-family: 'Lato', sans-serif;
        font-size: 60px;
        font-weight: 900;  
        letter-spacing: 2px;  
        color: white;
    }}

    h2, h3 {{
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 20px;
    }}

    .intro-text {{
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 400;
        letter-spacing: 1.4px;
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
    st.divider()
    st.write("## Netflix Dataset Overview", ":bar_chart:")
    st.dataframe(df)

    st.write("### Basic Statistics")
    st.write(df.describe())

    st.write(f"**Number of rows:** {df.shape[0]}")
    st.write(f"**Number of columns:** {df.shape[1]}")

    st.write("### First 5 Rows of the Dataset")
    st.write(df.head())

    st.write("### Count of Titles by Type (Movies/TV Shows)")
    title_type_count = df['type'].value_counts()
    st.bar_chart(title_type_count)

    st.write("### Distribution of Titles by Release Year")
    release_years = df['release_year'].value_counts().sort_index()
    st.line_chart(release_years)

    st.write("### Filtered Data: Movies Released After 2015")
    filtered_df = df[df['release_year'] > 2015]
    st.dataframe(filtered_df)

# Dashboard Tab
with DashboadTab:
    st.header("Netflix Dashboard")

    # Distribution of content by country (top 10 countries)
    st.write("### Distribution of Content by Country")
    country_count = df['country'].value_counts().head(10)
    st.bar_chart(country_count)

    # Plotly bar chart for content distribution by country
    st.write("### Top 10 Countries by Content (Interactive)")
    fig_country = px.bar(country_count, x=country_count.index, y=country_count.values, 
                         labels={'x': 'Country', 'y': 'Count'}, title="Top 10 Countries by Content")
    st.plotly_chart(fig_country)

    # Filter titles by country
    st.write("### Filter Titles by Country")
    selected_country = st.selectbox("Select a country", df['country'].dropna().unique())
    filtered_by_country = df[df['country'] == selected_country]
    st.write(filtered_by_country[['title', 'type', 'release_year', 'listed_in']])

    # Content releases over time (area chart)
    st.write("### Content Releases Over Time")
    releases_per_year = df['release_year'].value_counts().sort_index()
    st.area_chart(releases_per_year)

    # Pie chart: Movies vs TV Shows
    st.write("### Proportion of Movies vs TV Shows")
    title_type_count = df['type'].value_counts()
    st.pyplot(title_type_count.plot.pie(autopct='%1.1f%%', figsize=(5, 5)).figure)

