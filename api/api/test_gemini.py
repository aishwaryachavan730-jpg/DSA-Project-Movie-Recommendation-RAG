from gemini_api import generate_recommendation


movies = [
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Science Fiction, Adventure, Drama",
        "overview": "A team of explorers travel through a wormhole.",
        "tmdb_rating": 8.417,
        "imdb_rating": 8.7,
        "director": "Christopher Nolan",
        "actors": "Matthew McConaughey, Anne Hathaway",
        "awards": "Won 1 Oscar."
    },
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Action, Science Fiction, Adventure",
        "overview": "A thief enters the dreams of others.",
        "tmdb_rating": 8.364,
        "imdb_rating": 8.8,
        "director": "Christopher Nolan",
        "actors": "Leonardo DiCaprio",
        "awards": "Won 4 Oscars."
    }
]


answer = generate_recommendation(
    "Suggest a science fiction movie",
    movies
)

print("\nGemini Response:")
print(answer)