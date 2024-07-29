import requests
from requests.exceptions import RequestException
from django.core.cache import cache
import json

def Anime_movies():
    cache_key = 'anime_movies'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return json.loads(cached_data)

    url = 'https://anime-db.p.rapidapi.com/anime?page=1&size=10&search=Fullmetal&genres=Fantasy%2CDrama&sortBy=ranking&sortOrder=asc'
    headers = {
        'x-rapidapi-key': '0fb3574a43msh1599ef89a74c382p135cbfjsn5c4e0195b16d',
        'x-rapidapi-host': 'anime-db.p.rapidapi.com'
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)  # 5 second timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        anime_data = result.get('data', [])

        # Cache the data for 1 hour (3600 seconds)
        cache.set(cache_key, json.dumps(anime_data), 3600)

        return anime_data
    except RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_anime_by_id(anime_id):
    cache_key = f'anime_{anime_id}'
    cached_anime = cache.get(cache_key)

    if cached_anime is not None:
        return json.loads(cached_anime)

    # If not in cache, fetch from the list of anime movies
    all_anime = Anime_movies()
    anime = next((a for a in all_anime if a.get('_id') == anime_id), None)

    if anime:
        # Cache the individual anime data
        cache.set(cache_key, json.dumps(anime), 3600)

    return anime