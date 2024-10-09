import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px  
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

    /* Title styling */
    h1 {{
        font-family: 'Lato', sans-serif;
        font-size: 60px;
        font-weight: 900;  
        letter-spacing: 2px;  
        color: white;
    }}

    /* Subheader styling */
    h2, h3 {{
        font-family: 'Lato', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        color: white;
        margin-bottom: 5px;
    }}

    .special-text{{
        font-family: 'Lato', sans-serif;
        font-weight: 900;
        font-size:20px;
        color: white;
    }}

    /* Text style for introduction and analysis */
    .text-section {{
        font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 400;
        letter-spacing: 1.3px;
        line-height: 1.5;
        color: white;
        margin: 5px 0;
        font-style: italic;
        }}

    .text-another{{
     font-family: 'Lato', sans-serif;
        font-size: 18px;
        font-weight: 400;
        letter-spacing: 1.3px;
        line-height: 1.5;
        color: #E50914;
        margin: 5px 0;
        font-style: italic;
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
    
    st.write("### Introduction")
    st.markdown(
        '<p class="text-section">Netflix is one of the most widely used media and video streaming platforms. They have over 8000 movies and television shows available on their platform, and as of mid-2021, they had over 200 million subscribers worldwide. This tabular dataset, contains listings of all the movies and TV shows accessible on Netflix, together with information such as cast, directors, ratings, release year, duration, and so on.</p>', 
        unsafe_allow_html=True
    )
    st.markdown(
    '''
    <p class="text-section">
    The primary objectives of our analysis of the Netflix dataset are to gain deeper insights into the platform's content distribution and patterns. We aim to identify the number of Netflix titles available across various countries and the extent of content available in each. Additionally, we are interested in determining whether Netflix has focused more on producing TV shows or movies in recent years.
    </p>
    
    <p class="text-section">
    By analyzing the data, we examine how the number of releases has evolved over time. We also explore genre trends, identifying which genres are popular or distinct in specific countries and which genres are commonly produced in different regions. Furthermore, we seek to uncover which countries have the highest number of TV shows and movies, as well as to analyze the number of ratings in the dataset.
    </p>
    ''', 
    unsafe_allow_html=True
)


    st.divider()
#Clean the dataset
    df_cleaned = df.dropna()

    st.markdown('<p class = "special-text">Source:<p>', unsafe_allow_html=True)
    st.markdown('<p class = "text-another"> This dataset is available through Kaggle.<p>', unsafe_allow_html=True)
    st.markdown('<p class = "special-text">Types of Data <p>' , unsafe_allow_html=True)
    st.markdown('<p class = "text-another">Categorical<p>', unsafe_allow_html=True)
    st.divider()


    st.write("## Netflix Dataset Overview", ":bar_chart:")

    # Before Data Cleaning
    st.write('### Before Data Cleaning')
    st.write("#### Dataset")
    st.dataframe(df)

    st.write("### Basic Statistics")
    st.write(df.describe())

    st.write(f"*Number of rows:* {df.shape[0]}")
    st.write(f"*Number of columns:* {df.shape[1]}")
    st.divider()
    # After Data Cleaning
    st.write('### After Data Cleaning')
    
    st.dataframe(df_cleaned)

    st.divider()

    st.write("### Basic Statistics")
    st.write(df_cleaned.describe())

    st.write(f"*Number of rows:* {df_cleaned.shape[0]}")
    st.write(f"*Number of columns:* {df_cleaned.shape[1]}")

    st.divider()

    st.write("### First 5 Rows of the Dataset")
    st.write(df_cleaned.head())
    
    with DashboadTab:
        st.markdown("<h3><span style='color:red'>Netflix</span> Data Visualization of 2005 - 2021</h3>", unsafe_allow_html=True)
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
            title="Number of Movies and TV Shows by Release Year (2005 and 2021)",
            xaxis_title='Release Year',
            yaxis_title='Number of Titles',
            template='plotly',
            legend_title="Show Type"
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

        st.markdown("<i><small>📈 Figure 1: This chart illustrates the trends in Netflix releases for Movies and TV Shows from 2005 to 2021.</small></i>", unsafe_allow_html=True)
        st.markdown("<small><b>Movies:</b> The number of movie releases surged significantly between 2016 and 2017, with the highest count in 2017 at 729 titles. After 2017, the number of movie releases decreased steadily, with a sharp drop after 2019.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>TV Shows</b>: While starting with lower numbers, TV show releases gradually increased, peaking in 2020 with 391 titles. The rise was more consistent compared to movies, but there was a sharp decline post-2020.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>General Trend:</b> Movies dominated in volume throughout the period, but TV Shows saw steady growth, particularly from 2005 onward. The decline in both categories after 2020 may reflect broader industry shifts or impacts, potentially due to the global pandemic.</small>", unsafe_allow_html=True)
        
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
                                title='Top 10 Countries by Number of Movies Produced (2005-2021)',
                                color='count',
                                color_continuous_scale=color_scale)

        st.plotly_chart(fig_treemap)

        st.markdown("<i><small>📈 Figure 2: This treemap visualization highlights the Top 10 Countries by Number of Movies Produced from 2005 to 2021 on Netflix. </small></i>", unsafe_allow_html=True)
        st.markdown("<small><b>United States:</b> Leading the global movie production with 2001 titles, the U.S. dominates the chart, significantly outpacing other countries.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>United Kingdom and Canada:</b> These countries follow, but with much smaller contributions compared to the U.S., showing moderate movie production in the period.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>France, Nigeria, and Egypt:</b> These countries also make notable contributions, with a sizable share of Netflix movie releases.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>Spain, Mexico, and Indonesia:</b> These countries contribute fewer movies, rounding out the list of top 10 movie-producing countries.</small>", unsafe_allow_html=True)

         # Treemap for TV Shows 
        top_10_countries = tv_shows['country'].value_counts().nlargest(10).reset_index()
        top_10_countries.columns = ['country', 'count'] 
        fig_treemap = px.treemap(top_10_countries, path=['country'], values='count',
                                title='Top 10 Countries by Number of TV Shows Produced (2005-2021)',
                                color='count',
                                color_continuous_scale=px.colors.sequential.Plasma[::-1])

        st.plotly_chart(fig_treemap)

        st.markdown("<i><small>📈 Figure 3: This treemap visualization highlights the Top 10 Countries by Number of TV Shows Produced from 2005 to 2021 on Netflix. Key insights include: </small></i>", unsafe_allow_html=True)
        st.markdown("<small><b>United States:</b> The U.S. leads significantly with 806 TV shows, making it the dominant country in Netflix's TV show production.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>United Kingdom:</b> These countries follow, with 238 TV shows, making it second on the list.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>Japan and South Korea:</b> Following the U.K., Japan produced 163 TV shows, while South Korea contributed 164 TV shows, showcasing a strong presence in the Asian entertainment industry.</small>", unsafe_allow_html=True)
        st.markdown("<small><b>Canada, India, France, Australia, Taiwan, and Spain:</b> These countries also made notable contributions, with varying levels of production but still placing within the top 10.</small>", unsafe_allow_html=True)

        # Plot : Distribution of ratings
        rating_count = df['rating'].value_counts().reset_index()
        rating_count.columns = ['rating', 'count']
        fig2 = px.pie(rating_count, values='count', names='rating', title="Distribution of Netflix Ratings")
        st.plotly_chart(fig2)

        st.markdown("<i><small>📊 **Figure 3**: This treemap provides an overview of the **Top 10 Countries** by the number of **TV Shows Produced on Netflix** between **2005 and 2021**. The United States leads significantly, followed by Japan and South Korea, underscoring the dominance of North America and Asia in Netflix's TV show production.</small></i>", unsafe_allow_html=True)
        st.markdown("<small>The pie chart on Netflix ratings distribution reveals that TV-MA (Mature Audiences) dominates with 39.4% of all rated content, indicating that a significant portion of Netflix's content is tailored to adult viewers. TV-14, targeting teenagers, follows with 24.3%, reflecting a large amount of content for younger audiences as well. TV-PG, at 9.7%, and R-rated content, at 8.62%, further contribute to the platform's adult-focused offerings. The presence of TV-Y (3.09%) and TV-Y7 (3.06%) shows Netflix's smaller but notable commitment to children’s programming. The lower percentages for PG (2.9%) and TV-G (2.48%) suggest that family-oriented content forms a smaller portion of the overall library. This data highlights Netflix’s emphasis on mature and teen audiences while maintaining a diverse range of content for different age groups.</small>", unsafe_allow_html=True)

     
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
            title='Distribution of Top Genres on Movies in Top 10 Countries (2005-2021)',
            xaxis_title='Country',
            yaxis_title='Number of Movies',
            barmode='stack',
            legend_title='Genre',
            template='plotly'
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig6)
        st.markdown("<i><small>📊 **Figure**: This stacked bar chart highlights the **Top Genres** in the **Top 10 Countries** for Netflix movies. </small></i>", unsafe_allow_html=True)
        st.markdown("<small>The US dominates with **Documentaries** (265) and **Stand-Up Comedy** (196), showcasing a strong focus on factual and comedic content. **India** leans toward a mix of **Comedies, Dramas, and International Movies**, reflecting its diverse storytelling preferences. The **UK** favors **Documentaries**, while **Canada** balances **family-friendly comedies** and **Documentaries**. **France** highlights a preference for **Dramas** and **International Movies**, indicating a taste for emotionally rich and globally diverse content. Each country's top genres reflect its unique cultural and entertainment priorities.</small>", unsafe_allow_html=True)

        # Plot: Distribution of Top Genres : TV Shows 
        country_genre_counts = tv_shows.groupby(['country', 'listed_in']).size().unstack(fill_value=0)
        top_countries = country_genre_counts.sum(axis=1).sort_values(ascending=False).head(10).index
        top_country_genre = country_genre_counts.loc[top_countries]
        top_genres = top_country_genre.sum().sort_values(ascending=False).head(10).index

        top_country_genre = top_country_genre[top_genres]
        fig7 = go.Figure()

        # Loop through each genre to add a trace to the figure
        for genre in top_country_genre.columns:
            fig7.add_trace(go.Bar(
                x=top_country_genre.index,
                y=top_country_genre[genre],
                name=genre,
                hoverinfo='y+name',
            ))

        # Update layout for the stacked bar chart
        fig7.update_layout(
            title='Distribution of Top Genres on TV Shows in Top 10 Countries (2005-2021)',
            xaxis_title='Country',
            yaxis_title='Number of TV Shows',
            barmode='stack',  # Set barmode to stack
            legend_title='Genre',
            template='plotly'
        )

            # Display the plot in Streamlit
        st.plotly_chart(fig7)
        st.markdown("<i><small>📊 **Figure**: This bar chart presents the **Top Genres** in selected countries for Netflix shows.</small></i>", unsafe_allow_html=True)
        st.markdown("<small>The **US** leads with a significant preference for **Kid's TV** (93), showing a strong demand for child-friendly content, followed by **Reality TV** (72), and both **Docuseries** and **TV Comedies** (60 each). **South Korea** emphasizes a mix of **International, Korean, and Romantic TV Shows** (63), reflecting its global influence and local storytelling. **Japan** stands out with a strong affinity for **Anime** and **International TV Shows** (71), indicating the popularity of animated content and cross-border entertainment.</small>", unsafe_allow_html=True)

    with AnalysisTab:
        st.write("### Analysis")
        st.markdown(
    '''
        <p class="text-section">The analysis of the Netflix dataset reveals significant trends in content production, highlighting a steady increase in movie and TV show releases after 2000, peaking around 2018-2019 before a noticeable decline in 2020, likely influenced by external factors such as the pandemic.</p>
        
        <p class="text-section">The data shows that the United States and India are the dominant contributors to Netflix's content library, with a substantial majority of productions originating from these countries, particularly in genres like crime and documentaries.</p>
        
        <p class="text-section">Visualizations such as line plots, bar charts, and heatmaps effectively illustrate this growth and genre diversity, underscoring Netflix's strategic focus on expanding its offerings to engage a global audience. As the platform continues to navigate the competitive streaming landscape, understanding these trends will be crucial for future content development and audience targeting.</p>
    ''', 
    unsafe_allow_html=True
)
