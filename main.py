import numpy as np
import pandas as pd
import pickle
import difflib
import streamlit as st

# Load the model
loaded_model = pickle.load(open('model.sav', 'rb'))

# Function for movie recommendations
def movies_prediction(movie_name):
    movies_data = pd.read_csv('movies.csv')
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    
    if not find_close_match:
        return [], "No matches found for your input movie."
    
    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(loaded_model[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    recommendations = []
    for i, movie in enumerate(sorted_similar_movies[:10], start=1):  # Limit to 10 movies
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        recommendations.append(title_from_index)
    
    return recommendations, f"Showing recommendations for: **{close_match}**"

# Main app
def main():
    # Add custom styles
    st.markdown(
        """
        <style>
        body {
            background: #f4f4f9;
            font-family: 'Helvetica', sans-serif;
        }
        .title {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        .card {
            background: #ffffff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: #333;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # App title
    st.markdown('<h1 class="title">🎬 Movie Recommendations</h1>', unsafe_allow_html=True)

    # Input Section
    st.markdown("### Enter a Movie Name:")
    movie_name = st.text_input('', placeholder="E.g., The Matrix, Interstellar")

    # Recommendations
    if st.button('🔍 Recommend Movies'):
        if movie_name.strip():
            with st.spinner("Fetching recommendations..."):
                recommendations, message = movies_prediction(movie_name)
                st.markdown(message)
                
                if recommendations:
                    for movie in recommendations:
                        # Simple card for each movie name
                        st.markdown(f'<div class="card">{movie}</div>', unsafe_allow_html=True)
                else:
                    st.error("No recommendations found! Please try another movie.")
        else:
            st.error("Please enter a valid movie name!")

    # Footer
    st.markdown('<div class="footer">© 2024 Your Name - All Rights Reserved</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
