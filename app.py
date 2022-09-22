import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    api_key = ""
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, api_key)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    movie_iiiddd = movie_info_merge.iloc[index][0]
    movie_release = movie_info_merge.iloc[index][2]
    movie_runtime = movie_info_merge.iloc[index][3]
    movie_vote = movie_info_merge.iloc[index][4]
    movie_genre = movie_info_merge.iloc[index][5]
    movie_cast = movie_info_merge.iloc[index][6]
    movie_director = movie_info_merge.iloc[index][7]

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters,movie_release,movie_runtime,movie_vote,movie_genre,movie_cast,movie_director,movie_iiiddd


st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
movie_info_merge = pickle.load(open('movie_info_merge.pkl','rb'))
movie_info_merge = pd.DataFrame(movie_info_merge)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
enter = st.button("Enter", selected_movie)


if enter:

    recommended_movie_names,recommended_movie_posters,movie_release,movie_runtime,movie_vote,movie_genre,movie_cast,movie_director,movie_iiiddd = recommend(selected_movie)

    st.header('Movie Detail')
    col1, col2 = st.columns([1, 2])
    with col1:
        img = fetch_poster(movie_iiiddd)
        st.image(img, use_column_width=True)
    with col2:
        st.write('Movie Name    : ' + selected_movie)
        st.write('Cast          : ' + str(movie_cast))
        st.write('Director      : ' + str(movie_director))
        st.write('Release Date  : ' + movie_release)
        st.write('Movie Length  : ', movie_runtime, 'minutes')
        st.write('Rating        : ', movie_vote, '/10')
        st.write('Genre         : ' + str(movie_genre))

    st.header('Recommendation')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0])
        st.markdown(recommended_movie_names[0])

    with col2:
        st.image(recommended_movie_posters[1])
        st.markdown(recommended_movie_names[1])

    with col3:
        st.image(recommended_movie_posters[2])
        st.markdown(recommended_movie_names[2])

    with col4:
        st.image(recommended_movie_posters[3])
        st.markdown(recommended_movie_names[3])

    with col5:
        st.image(recommended_movie_posters[4])
        st.markdown(recommended_movie_names[4])





