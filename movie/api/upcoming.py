import requests
from django.core.cache import cache
import json

def upcoming_movies():
    cache_key = 'upcoming_movies'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return json.loads(cached_data)

    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"
    headers = {
        "x-rapidapi-key": "0fb3574a43msh1599ef89a74c382p135cbfjsn5c4e0195b16d",
        "x-rapidapi-host": "moviesdatabase.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        result = response.json()
        movies = result.get('results', [])

        # Cache the data for 1 hour (3600 seconds)
        cache.set(cache_key, json.dumps(movies), 3600)

        return movies
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_movie_by_id(movie_id):
    cache_key = f'movie_{movie_id}'
    cached_movie = cache.get(cache_key)

    if cached_movie is not None:
        return json.loads(cached_movie)

    # If not in cache, fetch from the list of upcoming movies
    upcoming = upcoming_movies()
    movie = next((m for m in upcoming if m.get('id') == movie_id), None)

    if movie:
        # Cache the individual movie data
        cache.set(cache_key, json.dumps(movie), 3600)

    return movie