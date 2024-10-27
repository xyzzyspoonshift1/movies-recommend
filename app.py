import pandas as pd
import streamlit as st
import pickle
import requests

api_key = pickle.load(open('api_key.pkl', 'rb'))

def fetch_poster_tagline(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return ("https://image.tmdb.org/t/p/w500/" + response.json().get('poster_path'),
                response.json().get('tagline'))
    else:
        #print(f"Error fetching poster: {response.status_code}, {response.text}")
        return None


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_tagline = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_name = movies.iloc[i[0]].title

        recommended_movies.append(movie_name)
        # FETCH POSTER FROM API
        poster, tagline = fetch_poster_tagline(movie_id)
        recommended_movies_poster.append(poster)
        recommended_movies_tagline.append(tagline)

    return recommended_movies,recommended_movies_poster,recommended_movies_tagline

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Pick a movie",
    movies['title'].values,
)

if st.button('Recommend'):
    recommended_movies, recommended_movies_poster, recommended_movies_tagline = recommend(selected_movie)
    cols = st.columns(3)
    for i in range(min(len(recommended_movies), 6)):  # Limit to 6 elements
        with cols[i % 3]:
            st.markdown(f"<h5>{recommended_movies[i]}</h5>", unsafe_allow_html=True)
            st.image(recommended_movies_poster[i])
            st.markdown(f"<h6>{recommended_movies_tagline[i]}</h6>", unsafe_allow_html=True)
            st.markdown("<br>" * 2, unsafe_allow_html=True)

