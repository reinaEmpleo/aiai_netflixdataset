import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px  # Import Plotly for interactive graphs
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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

# Data Cleaning
# 1. Remove Null Values
df.dropna(subset=['title', 'country', 'release_year', 'rating', 'duration', 'type', 'listed_in'], inplace=True)

# 2. Keep only the first country (if multiple are listed)
df['country'] = df['country'].apply(lambda x: x.split(',')[0].strip() if ',' in x else x)
df = df[df['release_year'] >= 2005]

# Create tabs
OverviewTab, DashboadTab, AnalysisTab = st.tabs(["Dataset Overview", "Data Visualization", "Analysis"])

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
    
    with DashboadTab:
        st.markdown("<h3><span style='color:red'>Netflix</span> Data Visualization of 2015 - 2021</h3>", unsafe_allow_html=True)
        type_count = df.groupby(['release_year', 'type']).size().reset_index(name='count')

        # Separate the data for Movies and TV Shows
        movies_data = type_count[type_count['type'] == 'Movie']
        tv_shows_data = type_count[type_count['type'] == 'TV Show']

        # Create the area chart
        fig = go.Figure()

        # Add Movies data
        fig.add_trace(go.Scatter(
            x=movies_data['release_year'],
            y=movies_data['count'],
            mode='lines',
            name='Movies',
            fill='tozeroy',  # Fill the area beneath the line
            line=dict(color='blue')
        ))

        # Add TV Shows data
        fig.add_trace(go.Scatter(
            x=tv_shows_data['release_year'],
            y=tv_shows_data['count'],
            mode='lines',
            name='TV Shows',
            fill='tozeroy',  # Fill the area beneath the line
            line=dict(color='red')
        ))

        # Update layout for the chart
        fig.update_layout(
            title="Number of Movies and TV Shows by Release Year (2015 and 2021)",
            xaxis_title='Release Year',
            yaxis_title='Number of Titles',
            template='plotly',
            legend_title="Show Type"
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        st.markdown("<i><small>📈 Figure 1: This chart illustrates the trends in Netflix releases for Movies and TV Shows from 2015 to 2021.</small></i>", unsafe_allow_html=True)
        st.markdown("<small><b>Movies:</b> The number of movie releases surged significantly between 2016 and 2017, with the highest count in 2017 at 729 titles. After 2017, the number of movie releases decreased steadily, with a sharp drop after 2019.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>TV Shows</b>: While starting with lower numbers, TV show releases gradually increased, peaking in 2020 with 391 titles. The rise was more consistent compared to movies, but there was a sharp decline post-2020.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>General Trend:</b> Movies dominated in volume throughout the period, but TV Shows saw steady growth, particularly from 2015 onward. The decline in both categories after 2020 may reflect broader industry shifts or impacts, potentially due to the global pandemic.</small>", unsafe_allow_html=True)
        
         # Plot : Movies released by year
        movies = df[df['type'] == 'Movie']
        tv_shows = df[df['type'] == 'TV Show']

        movies_release_year_counts = movies['release_year'].value_counts().sort_index()
        tv_shows_release_year_counts = tv_shows['release_year'].value_counts().sort_index()

        # Create a Plotly figure
        fig4 = go.Figure()

        color_scale = px.colors.sequential.Viridis
         # Treemap for Movies
        top_10_countries = movies['country'].value_counts().nlargest(10).reset_index()
        top_10_countries.columns = ['country', 'count'] 
        fig_treemap = px.treemap(top_10_countries, path=['country'], values='count',
                                title='Top 10 Countries by Number of Movies Produced (2015-2021)',
                                color='count',
                                color_continuous_scale=color_scale)

        st.plotly_chart(fig_treemap)

         # Treemap for TV Shows 
        top_10_countries = tv_shows['country'].value_counts().nlargest(10).reset_index()
        top_10_countries.columns = ['country', 'count'] 
        fig_treemap = px.treemap(top_10_countries, path=['country'], values='count',
                                title='Top 10 Countries by Number of TV Shows Produced (2015-2021)',
                                color='count',
                                color_continuous_scale=px.colors.sequential.Plasma[::-1])

        st.plotly_chart(fig_treemap)

        # Plot : Distribution of ratings
        rating_count = df['rating'].value_counts().reset_index()
        rating_count.columns = ['rating', 'count']
        fig2 = px.pie(rating_count, values='count', names='rating', title="Distribution of Netflix Ratings")
        st.plotly_chart(fig2)

        # Plot: Distribution of Top Genres : Movies
        country_genre_counts = movies.groupby(['country', 'listed_in']).size().unstack(fill_value=0)
        top_countries = country_genre_counts.sum(axis=1).sort_values(ascending=False).head(10).index
        top_country_genre = country_genre_counts.loc[top_countries]
        top_genres = top_country_genre.sum().sort_values(ascending=False).head(10).index

        top_country_genre = top_country_genre[top_genres]
        fig6 = go.Figure()

        # Loop through each genre to add a trace to the figure
        for genre in top_country_genre.columns:
            fig6.add_trace(go.Bar(
                x=top_country_genre.index,
                y=top_country_genre[genre],
                name=genre,
                hoverinfo='y+name',
            ))

        # Update layout for the stacked bar chart
        fig6.update_layout(
            title='Distribution of Top Genres on Movies in Top 10 Countries',
            xaxis_title='Country',
            yaxis_title='Number of Movies',
            barmode='stack',
            legend_title='Genre',
            template='plotly'
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig6)

        # Plot: Distribution of Top Genres : TV Shows 
        country_genre_counts = tv_shows.groupby(['country', 'listed_in']).size().unstack(fill_value=0)
        top_countries = country_genre_counts.sum(axis=1).sort_values(ascending=False).head(10).index
        top_country_genre = country_genre_counts.loc[top_countries]
        top_genres = top_country_genre.sum().sort_values(ascending=False).head(10).index

        top_country_genre = top_country_genre[top_genres]
        fig6 = go.Figure()

        # Loop through each genre to add a trace to the figure
        for genre in top_country_genre.columns:
            fig6.add_trace(go.Bar(
                x=top_country_genre.index,
                y=top_country_genre[genre],
                name=genre,
                hoverinfo='y+name',
            ))

        # Update layout for the stacked bar chart
        fig6.update_layout(
            title='Distribution of Top Genres on TV Shows in Top 10 Countries',
            xaxis_title='Country',
            yaxis_title='Number of Movies',
            barmode='stack',  # Set barmode to stack
            legend_title='Genre',
            template='plotly'
        )

#         # Display the plot in Streamlit
#         st.plotly_chart(fig6)

#     with col2:
#         # Descriptions and Data Analysis
#         st.write("""
#         """)

# Analysis Tab
with AnalysisTab:
    st.write("### Analysis")
    st.write("""
    The analysis of the Netflix dataset reveals significant trends in content production, 
    highlighting a steady increase in movie and TV show releases after 2000, peaking around 2018-2019 
    before a noticeable decline in 2020, likely influenced by external factors such as the pandemic. 

    The data shows that the United States and India are the dominant contributors to Netflix's content library, 
    with a substantial majority of productions originating from these countries, particularly in genres like 
    crime and documentaries. 

    Visualizations such as line plots, bar charts, and heatmaps effectively illustrate this growth and genre diversity, 
    underscoring Netflix's strategic focus on expanding its offerings to engage a global audience. 

    As the platform continues to navigate the competitive streaming landscape, understanding these trends will be 
    crucial for future content development and audience targeting.
    """)



