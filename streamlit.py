# Import of libraries
from turtle import width
import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io
from config import mongo_db_url
import pymongo
import ast
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title = "Book recommendation system",
    page_icon = '📚',
    layout = 'wide',
    initial_sidebar_state = 'expanded',
)
st.title("Book recommendation system")

# Data loading
client = pymongo.MongoClient(mongo_db_url)
db = client["books_db"]
collection = db["books"]

data = list(collection.find())
df = pd.DataFrame(data)


# Title for the side bar
st.sidebar.header('Filters')

# Filter for the author
unique_authors = df['author'].unique()
unique_authors = ['Choose an option'] + list(unique_authors)
selected_author = st.sidebar.selectbox('Author', unique_authors)
if selected_author != 'Select an author':
    st.write(f"Author selected: {selected_author}")

# Filtro para el género
df['genre'] = df['genre'].apply(lambda x: ast.literal_eval(x))
unique_genres = set()
for value in df['genre']:
    unique_genres.update(value.values())
selected_genres = st.sidebar.multiselect('Genre', list(unique_genres))
filtered_df = df[df['genre'].apply(lambda x: any(item in selected_genres for item in x.values()))]


# Filtro para la fecha de publicación
selected_date = st.sidebar.date_input('Publication date')

# Extraer el año de la fecha seleccionada
if selected_date:
    selected_year = datetime.strptime(str(selected_date), "%Y-%m-%d").year
    st.write(f"Year selected: {selected_year}")
else:
    st.write("No date selected")

# Filtro para la calificación
min_rating, max_rating = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0))

# Filtro para el número de ratings
min_num_ratings = df['rating_count'].min()
max_num_ratings = df['rating_count'].max()

selected_min, selected_max = st.sidebar.slider('Number of ratings', min_num_ratings, max_num_ratings, (min_num_ratings, max_num_ratings))

# Filtro para el número de reviews
min_num_pages = df['num_page'].min()
max_num_pages = df['num_page'].max()

selecting_min, selecting_max = st.sidebar.slider('Number of pages', min_num_pages, max_num_pages, (min_num_pages, max_num_pages))
