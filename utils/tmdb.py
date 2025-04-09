# utils/tmdb.py
import requests
import os

# --- 1. Configuration ---
TMDB_API_KEY = os.environ.get('e15611fc1e262e3309be1e0a15755207')
BASE_URL = 'https://api.themoviedb.org/3'
DEFAULT_LANGUAGE = 'en-US'

# --- 2. Movie Data Fetching ---
def fetch_movies(page=1, endpoint='/trending/movie/week', language=DEFAULT_LANGUAGE):
    """
    Fetches a list of movies from the TMDB API for a specified endpoint.

    Args:
        page (int): The page number of results to retrieve (default: 1).
        endpoint (str): The TMDB API endpoint to use (default: '/trending/movie/week').
                        Examples: '/movie/popular', '/movie/upcoming'.
        language (str): The language of the results (default: 'en-US').

    Returns:
        list: A list of movie dictionaries, or an empty list if an error occurs.
    """
    if not TMDB_API_KEY:
        print("Error: TMDB_API_KEY environment variable not set!")
        return []

    url = f'{BASE_URL}{endpoint}'
    params = {
        'api_key': TMDB_API_KEY,
        'language': language,
        'page': page
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movies from {endpoint}: {e}")
        return []
    except ValueError:
        print(f"Error decoding JSON response from {endpoint}")
        return []
    except KeyError:
        print(f"Error: 'results' key not found in the response from {endpoint}")
        return []

# --- 3. Example Usage (for testing) ---
if __name__ == '__main__':
    print("--- Testing fetch_movies (Trending) ---")
    trending_movies = fetch_movies()
    if trending_movies:
        for movie in trending_movies[:3]:
            print(f"- Title: {movie.get('title')}, ID: {movie.get('id')}")
    else:
        print("Failed to fetch trending movies.")

    print("\n--- Testing fetch_movies (Popular, Page 2) ---")
    popular_movies = fetch_movies(page=2, endpoint='/movie/popular')
    if popular_movies:
        for movie in popular_movies[:3]:
            print(f"- Title: {movie.get('title')}, ID: {movie.get('id')}")
    else:
        print("Failed to fetch popular movies (page 2).")

    print("\n--- Testing Error Handling (No API Key) ---")
    original_api_key = os.environ.get('TMDB_API_KEY')
    os.environ['TMDB_API_KEY'] = ''  # Temporarily unset API key
    error_test_result = fetch_movies()
    if not error_test_result:
        print("Error handling test (no API key): Fetch failed as expected.")
    if original_api_key is not None:
        os.environ['TMDB_API_KEY'] = original_api_key  # Reset API key
    else:
        del os.environ['TMDB_API_KEY']

    print("\n--- Remember to set your TMDB_API_KEY environment variable! ---")