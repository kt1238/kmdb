"""
OMDb API client for fetching movie information
"""
import requests

OMDB_API_KEY = '508e4d85'
OMDB_BASE_URL = 'http://www.omdbapi.com/'


def get_movie_info(title):
    """
    Fetch movie information from OMDb API by title
    Returns dict with movie data or None if not found
    """
    try:
        params = {
            'apikey': OMDB_API_KEY,
            's': title,  # Search by title
            'type': 'movie'
        }
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # If search returned results, return the first movie
        if data.get('Response') == 'True' and data.get('Search'):
            return data['Search'][0]  # First result
        return None
    except (requests.RequestException, ValueError):
        # API error or invalid JSON
        return None


def get_movie_by_imdb_id(imdb_id):
    """
    Fetch detailed movie information by IMDb ID
    Returns dict with detailed movie data or None if not found
    """
    try:
        params = {
            'apikey': OMDB_API_KEY,
            'i': imdb_id,  # IMDb ID
            'type': 'movie'
        }
        response = requests.get(OMDB_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Response') == 'True':
            return data
        return None
    except (requests.RequestException, ValueError):
        return None
