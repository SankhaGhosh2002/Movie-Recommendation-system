
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=829124a81dbd2942c78da02715507c2f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # Find the index of the selected movie
    distances = similarity[movie_index]  # Get similarity scores for this movie
    
    # Get top 5 most similar movies (excluding the first one, which is the selected movie itself)
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = [] 
    for i in movie_list:  # i is a tuple (index, similarity score)
        movie_id = movies.iloc[i[0]].movie_id
       
        recommended_movies.append(movies.iloc[i[0]].title)  # Use `.iloc` for index-based access
         #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

select_movie_name = st.selectbox(
    'What would you like to watch?',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(select_movie_name)
    st.write("Here are the top recommendations for you:")
    import streamlit as st

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
