import numpy as np
import pandas as pd
import pickle
import difflib
import streamlit as st

# Load the model
try:
    with open('model.sav', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
except FileNotFoundError:
    st.error("Model file 'model.sav' not found. Please ensure it is in the same directory.")
    st.stop()

# Function for movie recommendations
def get_movie_recommendations(movie_name):
    try:
        movies_data = pd.read_csv('movies.csv')
    except FileNotFoundError:
        return [], "Movies data file 'movies.csv' not found. Please ensure it is in the same directory."
    
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if not find_close_match:
        return [], "No matches found for your input movie. Please try another title."

    close_match = find_close_match[0]
    try:
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(loaded_model[index_of_the_movie]))
    except IndexError:
        return [], "An error occurred while processing the movie data. Please try again."

    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    recommendations = []

    for i, movie in enumerate(sorted_similar_movies[:10], start=1):
        index = movie[0]
        try:
            title_from_index = movies_data[movies_data.index == index]['title'].values[0]
            poster_url = movies_data[movies_data.index == index]['poster_url'].values[0] if 'poster_url' in movies_data else None
            recommendations.append((title_from_index, poster_url))
        except IndexError:
            continue

    return recommendations, f"Showing recommendations for: **{close_match}**"

# Main app
def main():
    # Custom styles
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #141414, #0f0f0f);
            font-family: 'Arial', sans-serif;
            color: #ffffff;
        }
        .title {
            text-align: center;
            color: #e50914;
            margin-bottom: 20px;
            font-size: 3em;
            font-weight: bold;
        }
        .input-section {
            text-align: center;
            margin-bottom: 20px;
        }
        .card {
            background: #1f1f1f;
            padding: 20px;
            margin: 15px 0;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        }
        .card img {
            width: 100%;
            border-radius: 10px;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.5);
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            font-size: 14px;
            color: #666;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App title
    st.markdown('<h1 class="title">🎥 Movie Recommendation System</h1>', unsafe_allow_html=True)

    # Input Section
    st.markdown('<div class="input-section">Enter a Movie Name:</div>', unsafe_allow_html=True)
    movie_name = st.text_input('', placeholder="E.g., The Matrix, Interstellar")

    # Recommendations
    if st.button('🔍 Get Recommendations'):
        if movie_name.strip():
            with st.spinner("Fetching recommendations..."):
                recommendations, message = get_movie_recommendations(movie_name)
                st.markdown(message)

                if recommendations:
                    for title, poster_url in recommendations:
                        if poster_url:
                            st.markdown(f'<div class="card"><img src="{poster_url}" alt="{title}"><p>{title}</p></div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="card">{title}</div>', unsafe_allow_html=True)
                else:
                    st.warning("No recommendations found. Try entering another movie title.")
        else:
            st.error("Please enter a valid movie name!")

    # Footer
    st.markdown('<div class="footer">© 2024 MovieLens Recommendation System. All Rights Reserved.</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

