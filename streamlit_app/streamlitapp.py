# Import of libraries
import turtle
import streamlit as st
import pandas as pd
from PIL import Image
import sys
import pymongo
import ast
from datetime import datetime

sys.path.append('../')
from config import *

# Page configuration
st.set_page_config(
    page_title = "BookQuest",
    page_icon = '📚',
    layout = 'wide',
    initial_sidebar_state = 'expanded',
)

filters_applied = False

st.title("BookQuest")
st.markdown("### Find your next favorite book 📖")
st.sidebar.title('Filters')

if not filters_applied:
    st.write('''Welcome to BookQuest, your ultimate book recommendation platform. With BookQuest, you can explore a vast collection of books and find your perfect match by customizing filters based on your preferences. Choose your favorite author, select genres that interest you, narrow down by publication year, rating, number of reviews, or even the number of pages.
            
Happy reading with BookQuest! ✨''')

st.markdown("---")

# Data loading
client = pymongo.MongoClient(mongo_db_url)
db = client["books_db"]
collection = db["books"]

data = list(collection.find())
df = pd.DataFrame(data)

base_df = df.copy()

# Sorting the ratings by emoji color-based order
map_rating_to_emoji = lambda rating: (
            f"{rating} 🔴" if 0.00 <= rating <= 2.50 else 
            f"{rating} 🟠" if 2.51 <= rating <= 4.00 else 
            f"{rating} 🟢" if 4.01 <= rating <= 5.00 else ""
        )


# Creating the filter for 'author'
unique_authors = ['Choose an option'] + list(base_df['author'].unique())
selected_author = st.sidebar.selectbox('Author', unique_authors)
if selected_author != 'Choose an option':
    base_df = base_df[base_df['author'] == selected_author]
    filters_applied = True

# Creating the filter for 'genre'
base_df['genre'] = base_df['genre'].apply(lambda x: ast.literal_eval(x))
unique_genres = set()
for value in base_df['genre']:
    unique_genres.update(value.values())
selected_genres = st.sidebar.multiselect('Genre', list(unique_genres))
if selected_genres:
    base_df = base_df[base_df['genre'].apply(lambda x: any(item in selected_genres for item in x.values()))]
    filters_applied = True

# Creating the filter for 'publication_date'
years = [''] + sorted(base_df['publication_date'].dt.year.unique())
selected_year = st.sidebar.select_slider('Publication year', options=years)
if selected_year != '':
    base_df = base_df[base_df['publication_date'].dt.year == selected_year]
    filters_applied = True

# Creating the filter for 'rating'
min_rating, max_rating = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0))
if min_rating != 0.0 or max_rating != 5.0:
    base_df = base_df[(base_df['rating'] >= min_rating) & (base_df['rating'] <= max_rating)]
    filters_applied = True


# Creating the filter for 'rating_count'
min_num_ratings = base_df['rating_count'].min()
max_num_ratings = base_df['rating_count'].max()
if min_num_ratings == max_num_ratings:
    min_num_ratings -= 1  

selected_min, selected_max = st.sidebar.slider('Number of ratings', min_num_ratings, max_num_ratings, (min_num_ratings, max_num_ratings))
if (selected_min, selected_max) != (min_num_ratings, max_num_ratings):
    base_df = base_df[(base_df['rating_count'] >= selected_min) & (base_df['rating_count'] <= selected_max)]
    filters_applied = True

# Creating the filter for 'num_page'
min_num_pages = base_df['num_page'].min()
max_num_pages = base_df['num_page'].max()
if min_num_pages == max_num_pages:
    min_num_pages -= 1  

selected_min, selected_max = st.sidebar.slider('Number of pages', min_num_pages, max_num_pages, (min_num_pages, max_num_pages))
if (selected_min, selected_max) != (min_num_pages, max_num_pages):
    base_df = base_df[(base_df['num_page'] >= selected_min) & (base_df['num_page'] <= selected_max)]
    filters_applied = True


# Displaying the results
if filters_applied and not base_df.empty:

    # Counting the number of results
    st.markdown(f"**Total results:** {len(base_df)}/{len(df)}")

    st.markdown("---")

    # Diviging the results in rows and columns
    num_columns = 3  
    elements_per_row = 3

    total_elements = len(base_df)
    num_full_rows, remainder = divmod(total_elements, elements_per_row)
    rows = num_full_rows + (1 if remainder > 0 else 0)

    for i in range(rows):
        columns = st.columns(num_columns)

        for j in range(elements_per_row):
            index = i * elements_per_row + j

            if index < total_elements:
                row = base_df.iloc[index]

                with columns[j]:
                    st.markdown(f"**Title:** {row['title']}")
                    st.markdown(f"**Author:** {row['author']}")
                    st.markdown(f'**Genre:** {", ".join(row["genre"].values())}')
                    rating_with_emoji = map_rating_to_emoji(row['rating'])
                    st.markdown(f"**Rating:** {rating_with_emoji}")
                    st.markdown(f'**N° of ratings:** {row["rating_count"]}')
                    st.markdown(f'**N° of reviews:** {row["review_count"]}')
                    st.markdown(f'**Publication date:** {row["publication_date"].strftime("%d/%m/%Y")}')
                    st.markdown(f'**N° of pages:** {row["num_page"]}')

                    cover_url = row['cover']
                    if cover_url:
                        st.image(cover_url, caption='Cover', width=100)
                    else:
                        st.write("No cover available")
                    

                    st.markdown("---")


