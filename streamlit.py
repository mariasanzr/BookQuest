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

base_df = df.copy()

# Filtro para el autor
unique_authors = ['Choose an option'] + list(base_df['author'].unique())
selected_author = st.sidebar.selectbox('Author', unique_authors)
if selected_author != 'Choose an option':
    base_df = base_df[base_df['author'] == selected_author]

# Filtro para el género
base_df['genre'] = base_df['genre'].apply(lambda x: ast.literal_eval(x))
unique_genres = set()
for value in base_df['genre']:
    unique_genres.update(value.values())
selected_genres = st.sidebar.multiselect('Genre', list(unique_genres))
if selected_genres:
    base_df = base_df[base_df['genre'].apply(lambda x: any(item in selected_genres for item in x.values()))]

# Filtro para el año de publicación
years = [''] + sorted(base_df['publication_date'].dt.year.unique())
selected_year = st.sidebar.select_slider('Publication year', options=years)
if selected_year != '':
    base_df = base_df[base_df['publication_date'].dt.year == selected_year]

# Filtro para la calificación
min_rating, max_rating = st.sidebar.slider('Rating', 0.0, 5.0, (0.0, 5.0))
if min_rating != 0.0 or max_rating != 5.0:
    base_df = base_df[(base_df['rating'] >= min_rating) & (base_df['rating'] <= max_rating)]

# Filtro para el número de ratings
min_num_ratings = base_df['rating_count'].min()
max_num_ratings = base_df['rating_count'].max()

# Verificar si los valores son iguales y ajustar uno de ellos si es necesario
if min_num_ratings == max_num_ratings:
    # Si los valores son iguales, ajusta uno de ellos
    min_num_ratings -= 1  # Restar 1 al valor mínimo, por ejemplo

selected_min, selected_max = st.sidebar.slider('Number of ratings', min_num_ratings, max_num_ratings, (min_num_ratings, max_num_ratings))
if (selected_min, selected_max) != (min_num_ratings, max_num_ratings):
    base_df = base_df[(base_df['rating_count'] >= selected_min) & (base_df['rating_count'] <= selected_max)]

# Filtro para el número de páginas
min_num_pages = base_df['num_page'].min()
max_num_pages = base_df['num_page'].max()

# Verificar si los valores son iguales y ajustar uno de ellos si es necesario
if min_num_pages == max_num_pages:
    # Si los valores son iguales, ajusta uno de ellos
    min_num_pages -= 1  # Restar 1 al valor mínimo, por ejemplo

selected_min, selected_max = st.sidebar.slider('Number of pages', min_num_pages, max_num_pages, (min_num_pages, max_num_pages))
if (selected_min, selected_max) != (min_num_pages, max_num_pages):
    base_df = base_df[(base_df['num_page'] >= selected_min) & (base_df['num_page'] <= selected_max)]

# Mostrar los resultados filtrados
if not base_df.empty:
    st.write(base_df)
else:
    st.write("No matching data")
