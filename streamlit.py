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
    page_title = "BookBuddy",
    page_icon = '📚',
    layout = 'wide',
    initial_sidebar_state = 'expanded',
)
st.title("BookBuddy")

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
if selected_author != 'Choose an option':
    filtered_df = df[df['author'] == selected_author]
    st.write(filtered_df)
    st.write(f"Author selected: {selected_author}")
else:
    st.write("No author selected")

# Filter for the genre
df['genre'] = df['genre'].apply(lambda x: ast.literal_eval(x))
unique_genres = set()
for value in df['genre']:
    unique_genres.update(value.values())
selected_genres = st.sidebar.multiselect('Genre', list(unique_genres))
filtered_df = df[df['genre'].apply(lambda x: any(item in selected_genres for item in x.values()))]
if selected_genres:
    st.write(filtered_df)
else:
    st.write("No genres selected")


# Filter for the publication year
years = sorted(df['publication_date'].dt.year.unique())
years.insert(0, '')
selected_year = st.sidebar.select_slider('Publication year', options=years)
if selected_year != '':
    filtered_df = df[df['publication_date'].dt.year == selected_year]
    st.write(filtered_df)
else:
    st.write("No year selected")

# Filtro para la calificación
min_rating, max_rating = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0))
if min_rating != 0.0 or max_rating != 5.0:
    filtered_df = df[(df['rating'] >= min_rating) & (df['rating'] <= max_rating)]
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No matching data")
else:
    st.write("No rating filter applied")

# Filtro para el número de ratings
min_num_ratings = df['rating_count'].min()
max_num_ratings = df['rating_count'].max()

# Filtro para el número de ratings con valores por defecto que abarquen todo el rango
selected_min, selected_max = st.sidebar.slider('Number of ratings', min_num_ratings, max_num_ratings, (min_num_ratings, max_num_ratings))
if (selected_min, selected_max) != (min_num_ratings, max_num_ratings):
    filtered_df = df[(df['rating_count'] >= selected_min) & (df['rating_count'] <= selected_max)]
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No matching data")
else:
    st.write("No number of ratings filter applied")

# Filtro para el número de paginas
min_num_pages = df['num_page'].min()
max_num_pages = df['num_page'].max()
selected_min, selected_max = st.sidebar.slider('Number of pages', min_num_pages, max_num_pages, (min_num_pages, max_num_pages))
if (selected_min, selected_max) != (min_num_pages, max_num_pages):
    filtered_df = df[(df['num_page'] >= selected_min) & (df['num_page'] <= selected_max)]
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No matching data")
else:
    st.write("No number of pages filter applied")
