# Film Recommendation System

An interactive web app that recommends films to a user based on a title they input. This app provides genre-based movie recommendations from a dataset of movies between 1950-2019 or recommendations of Netflix titles. The system was built using pandas, Streamlit, and Annoy.


  ## Features

  - Input a movie title and get similar recommendations
  - Fuzzy title matching
  - Fast recommendation search using Annoy
  - Clean and interactive UI using Streamlit
  - Displays recommended movies and genres


  ## Demo

  <img width="1406" alt="Screenshot 2025-05-12 at 2 00 49 PM" src="https://github.com/user-attachments/assets/d3ef1572-4436-4c7a-a867-b1415ab9e415" />


  ## How it Works

  - Movies are vectorized using TF-IDF on genres
  - Tree-based index is built by Annoy for fast lookup of similar movies
  - User-provided title is matched with data
  - Similar movies are retrieved based on cosine simlarity
  - Results are rendered in a table using Streamlit


  ## License

  This project is licensed under the MIT License.
