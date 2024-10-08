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





# Uncomment this kung kinsa mu layout mao ni ang partial graphs hehe thx
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go

# # Title of the app
# st.title("Netflix Data Science Project")

# # Load dataset directly from the file
# df = pd.read_csv('netflix_titles.csv')

# # Data Cleaning
# # 1. Remove Null Values
# df.dropna(subset=['title', 'country', 'release_year', 'rating', 'duration'], inplace=True)

# # 2. Keep only the first country (if multiple are listed)
# df['country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if ',' in x else x)

# # # 3. Remove Outliers (e.g., based on 'duration' for movies and shows)
# # df['duration_num'] = df['duration'].apply(lambda x: int(x.split()[0]) if 'min' in x else None)
# # df = df[df['duration_num'].between(1, 300)]

# # Create tabs
# OverviewTab, DashboardTab, AnalysisTab = st.tabs(["Dataset Overview", "Dashboard", "Analysis"])

# # Data Overview tab
# with OverviewTab:
#     st.write("### Introduction")
#     st.write("This project explores Netflix data, focusing on visualizing patterns in titles, countries, and ratings.")

#     # Display the cleaned dataframe
#     st.write("### Cleaned Netflix Dataset Overview")
#     st.dataframe(df)

#     # Show basic statistics
#     st.write("### Basic Statistics")
#     st.write(df.describe())

#     # Show number of rows and columns
#     st.write(f"**Number of rows:** {df.shape[0]}")
#     st.write(f"**Number of columns:** {df.shape[1]}")

#     # Show first 5 rows of the dataset
#     st.write("### First 5 Rows of the Cleaned Dataset")
#     st.write(df.head())

#     # Filter: Example - Show all movies released after 2015
#     st.write("### Filtered Data: Movies Released After 2015")
#     filtered_df = df[df['release_year'] > 2015]
#     st.dataframe(filtered_df)

# # Dashboard tab
# with DashboardTab:
#     st.write("### Dashboard")

#     # Create two columns for layout
#     col1, col2 = st.columns([1, 2])  # Column 1 (2x width) for graphs, Column 2 (1x width) for description

#     with col1:
#         # Plot : Count of shows/movies by country
#         country_count = df['country'].value_counts().reset_index()
#         country_count.columns = ['country', 'count']
#         fig1 = px.bar(country_count.head(10), x='country', y='count', title="Top 10 Countries by Number of Netflix Titles")
#         st.plotly_chart(fig1)

#         # Plot : Distribution of ratings
#         rating_count = df['rating'].value_counts().reset_index()
#         rating_count.columns = ['rating', 'count']
#         fig2 = px.pie(rating_count, values='count', names='rating', title="Distribution of Netflix Ratings")
#         st.plotly_chart(fig2)

#         # Plot : Movies released by year
#         movies = df[df['type'] == 'Movie']
#         tv_shows = df[df['type'] == 'TV Show']

#         movies_release_year_counts = movies['release_year'].value_counts().sort_index()
#         tv_shows_release_year_counts = tv_shows['release_year'].value_counts().sort_index()

#         # Create a Plotly figure
#         fig4 = go.Figure()

#         # Line chart for Movies
#         fig4.add_trace(go.Scatter(
#             x=movies_release_year_counts.index,
#             y=movies_release_year_counts.values,
#             mode='lines+markers',
#             name='Movies',
#             line=dict(color='blue')
#         ))

#         # Line chart for TV Shows
#         fig4.add_trace(go.Scatter(
#             x=tv_shows_release_year_counts.index,
#             y=tv_shows_release_year_counts.values,
#             mode='lines+markers',
#             name='TV Shows',
#             line=dict(color='red')
#         ))

#         # Update layout
#         fig4.update_layout(
#             title='Line Plot of Release Year: Movies',
#             xaxis_title='Release Year',
#             yaxis_title='Frequency',
#             legend_title='Type',
#             template='plotly'
#         )

#         # Display the plot in Streamlit
#         st.plotly_chart(fig4)  # Use st.plotly_chart to render the Plotly figure
        
#         # PLot Sample
#         top_10_countries = movies['country'].value_counts().nlargest(10).reset_index()
#         top_10_countries.columns = ['country', 'count']  # Rename columns to 'country' and 'count'

#         # Create the treemap
#         fig_treemap = px.treemap(top_10_countries, path=['country'], values='count',
#                                 title='Top 10 Countries by Number of Movies Produced',
#                                 color='count',
#                                 color_continuous_scale=px.colors.sequential.Plasma)

#         st.plotly_chart(fig_treemap)
#         # Plot 6: Distribution of Top Genres in Top Countries
#         country_genre_counts = movies.groupby(['country', 'listed_in']).size().unstack(fill_value=0)

#         # Select the top 10 countries based on total movie counts
#         top_countries = country_genre_counts.sum(axis=1).sort_values(ascending=False).head(10).index

#         # Filter the genre counts to include only the top countries
#         top_country_genre = country_genre_counts.loc[top_countries]

#         # Select the top genres
#         top_genres = top_country_genre.sum().sort_values(ascending=False).head(10).index

#         # Filter the genre counts to include only the top genres
#         top_country_genre = top_country_genre[top_genres]

#         # Create a stacked bar chart using Plotly
#         fig6 = go.Figure()

#         # Loop through each genre to add a trace to the figure
#         for genre in top_country_genre.columns:
#             fig6.add_trace(go.Bar(
#                 x=top_country_genre.index,
#                 y=top_country_genre[genre],
#                 name=genre,
#                 hoverinfo='y+name',
#             ))

#         # Update layout for the stacked bar chart
#         fig6.update_layout(
#             title='Distribution of Top Genres in Top Countries',
#             xaxis_title='Country',
#             yaxis_title='Number of Movies',
#             barmode='stack',  # Set barmode to stack
#             legend_title='Genre',
#             template='plotly'
#         )

#         # Display the plot in Streamlit
#         st.plotly_chart(fig6)

#     with col2:
#         # Descriptions and Data Analysis
#         st.write("""
#         """)

# # Analysis Tab
# with AnalysisTab:
#     st.write("### Analysis")
#     st.write("Further analysis can be added here.")


