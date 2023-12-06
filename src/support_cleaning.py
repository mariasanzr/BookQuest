import requests
from bs4 import BeautifulSoup
import re


def get_info(urls):

    # Scrapping books information
        
    for url in urls:

        try:

            # Getting the url and parsing it

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
        
            # Getting all of the books info 

            cover = soup.find_all('img', {'class': 'ResponsiveImage'})
            book_cover = cover[0]['src']
            
            book_title = soup.find_all('h1', {'class':'Text Text__title1'})[0].text
            
            book_author = soup.find_all('span', {'class':'ContributorLink__name'})[0].text
            
            genre = [e.text for e in soup.find_all('ul', {'class':'CollapsableList'})]
            genre = genre[0]
            genres = re.split(r'(?=[A-Z])', genre)
            book_genre = genres[2:7] if len(genres) >= 5 else genres
            book_genre = ', '.join(book_genre)
            
            book_rating = soup.find_all('div', {'class':'RatingStatistics__rating'})[0].text
            
            book_rating_count = soup.find_all('div', {'class':'RatingStatistics__meta'})[0].text
            
            book_year = soup.find_all('p', {'data-testid':'publicationInfo'})[0].text
            
            book_pages = soup.find_all('p', {'data-testid':'pagesFormat'})[0].text
            
            response.close()

            # Creating a dictionary with all of the books info
            
            book_info = { 'Cover': book_cover,
                        'Title': book_title,
                        'Author': book_author,
                        'Genre': book_genre,
                        'Rating': book_rating,
                        'Rating Count': book_rating_count,
                        'Year': book_year,
                        'Pages': book_pages}
            
            yield book_info


        except: 

            pass


def remove_duplicates(text):

    # Removing duplicate values
    
    words = text.split(',')
    unique_words = list(dict.fromkeys(words))
    return ','.join(unique_words)


def common_genres_cleaning(x):

    # Cleaning the 'Genre' column
    
    common_genres = [
    "Adventure", "Autobiography", "Biography", "Children's", "Classics", "Comic", "Contemporary", "Crime", "Detective", "Drama", "Dystopian", "Erotica", "Essay", "Fantasy", "Fiction", "Graphic", "Historical", "Horror", "Humor", "Literary", "Memoir", "Mystery", "Mythology", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Political", "Religion", "Romance", "Satire", "Science", "Self-help", "Short", "Suspense", "Thriller", "Travel", "True Crime", "Western", "Action", "Apocalyptic", "Art", "Bildungsroman", "Chick", "Cinematic", "Cyberpunk", "Experimental", "Fairy", "Family", "Gothic", "Hard", "High", "Romance", "Legal", "Magic", "Medical", "Metafiction", "Military", "Occult", "Picaresque", "Post-Apocalyptic", "Psychological", "Saga", "Science", "Space", "Spy", "Steampunk", "Superhero", "Survival", "Techno-thriller", "Time-travel", "Urban", "Visionary", "War", "Young", "Adult"
    ]
    
    x = x.split(',')
    x = [genre.strip() for genre in x]
    for i in range(len(x)):
        if x[i] == 'L':
            x[i] = 'LGTBIQ+'
        elif x[i] == 'M':
            x[i] = 'BDSM'
        elif x[i] in ['G', 'T', 'I', 'Q', 'D', 'S', 'B']:
            x[i] = ''
    x = [genre for genre in x if genre in common_genres]
    if all(genre not in common_genres for genre in x):
        return ['Unknown']
    else:
        return x

def create_genre_dict(row):

    # Creation of a dictionary with each genre
    
    genre_dict = {}
    for idx, val in enumerate(row):
        genre_dict[f'genre_{idx + 1}'] = val.strip()
    return genre_dict


