# Import of libraries

import streamlit as st
import pandas as pd
from PIL import Image
import pylab as plt
import webbrowser
import base64
import io

# Page configuration

st.set_page_config(
    page_title = "Books' recomendation system",
    page_icon = '📚',
    layout = 'wide',
    initial_sidebar_state = 'expanded',
)

st.title("Books' recomendation system")

st.sidebar.write(f'### Filters')

# Setting the background

def set_background():
    page_bg = '''
    <style>
    body {
    background-image: url("https://cdn.pixabay.com/photo/2020/06/19/22/33/wormhole-5319067_960_720.jpg");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg, unsafe_allow_html=True)

# Llamar a la función para establecer el fondo
set_background()

# Data loading

books = pd.read_csv('data/books_cleaned.csv')

st.write('Books dataset')
st.dataframe(books)