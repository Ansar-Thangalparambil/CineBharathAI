import os
from pathlib import Path
import random
import pandas as pd
import requests
import urllib.parse
from dotenv import load_dotenv

# 1. Setup absolute paths relative to this backend module with dynamic fallback
try:
    CURRENT_DIR = Path(__file__).resolve().parent
except NameError:
    CURRENT_DIR = Path.cwd()
ENV_PATH = CURRENT_DIR / '.env'

# TMDB uses specific ID numbers for genres. We map industry-standard terms to these IDs.
GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Crime & Thriller": 53,
    "Drama": 18,
    "Family": 10751,
    "Feel-good": 35,       # Separated Feel-good (Lighthearted/Comedy ID)
    "Romance": 10749,      # Separated Romance (Romance ID)
    "Horror": 27,
    "Mystery": 9648,
    "Sci-Fi": 878
}

# Dynamic Impression Fatigue Cache
# Format: {(lang, genre_tuple, era): set_of_shown_movie_titles}
RECOMMENDATION_HISTORY = {}

def load_env_credentials():
    """
    Forcibly loads the .env file from the correct physical folder 
    and checks for either v4 Read Access Token or classic v3 Key.
    """
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    v4_token = os.getenv("TMDB_READ_TOKEN")
    v3_key = os.getenv("TMDB_API_KEY")
    
    # Auto-sanitize wrapping quotes or accidental trailing spaces
    def sanitize(val):
        if val:
            cleaned = val.strip().strip("'\"")
            return cleaned if cleaned else None
        return None

    # Return a dictionary of both credentials to let the retriever make smart decisions
    return {
        "v4_token": sanitize(v4_token),
        "v3_key": sanitize(v3_key)
    }

def get_credential_status():
    """
    Performs full credential audits, source tracking, and length calculations.
    Returns a unified state dictionary for any importing frontend (like app.py).
    """
    creds = load_env_credentials()
    v4_token = creds["v4_token"]
    v3_key = creds["v3_key"]
    
    # We prefer the v4 token if present, but hold the v3 key as an active proxy fallback
    credential = v4_token or v3_key
    
    has_valid_credential = True
    diagnostic_reason = None
    is_placeholder = False
    key_source = "None (Empty)"
    
    if credential:
        is_v4 = credential.startswith("eyJ") or len(credential) > 100
        key_source = "TMDB_READ_TOKEN (v4)" if is_v4 else "TMDB_API_KEY (v3)"
        
        # Check if the user is still using our placeholder template strings
        if "xxxx" in credential or "paste entire" in credential or "your_token" in credential:
            has_valid_credential = False
            is_placeholder = True
            diagnostic_reason = "Placeholder template string detected in your configuration."
    else:
        has_valid_credential = False
        diagnostic_reason = "No TMDB_API_KEY or TMDB_READ_TOKEN detected in environment."
        
    return {
        "credential": credential,
        "has_valid_credential": has_valid_credential,
        "is_placeholder": is_placeholder,
        "diagnostic_reason": diagnostic_reason,
        "key_source": key_source,
        "key_length": len(credential) if credential else 0
    }

def get_movies_by_language_and_genres(credential, language_code, genre_names, era="Evergreen"):
    """
    Fetches real-time movies from TMDB with an advanced Multi-Proxy fallback chain,
    User-Agent spoofing, automatic credential detection, and dynamic era/decade filters.
    """
    creds = load_env_credentials()
    v3_key = creds["v3_key"]
    v4_token = creds["v4_token"]

    if not v3_key and not v4_token:
        return pd.DataFrame([{
            'Title': '⚠️ Configuration Error',
            'Rating': 0.0,
            'Release Date': 'N/A',
            'Overview': 'No active API credentials found. Please configure your .env file.'
        }])

    # Format TMDB categories or filters
    genre_ids = [str(GENRE_MAP[g]) for g in genre_names if g in GENRE_MAP]
    genre_query = ",".join(genre_ids)
    
    # Build clean query parameters dynamically
    params = {
        "with_original_language": language_code,
        "with_genres": genre_query,
        "page": 1
    }
    
    era_str = str(era).lower()
    if "80s" in era_str:
        params["primary_release_date.gte"] = "1980-01-01"
        params["primary_release_date.lte"] = "1989-12-31"
        params["sort_by"] = "popularity.desc"
    elif "90s" in era_str:
        params["primary_release_date.gte"] = "1990-01-01"
        params["primary_release_date.lte"] = "1999-12-31"
        params["sort_by"] = "popularity.desc"
    elif "00s" in era_str:
        params["primary_release_date.gte"] = "2000-01-01"
        params["primary_release_date.lte"] = "2009-12-31"
        params["sort_by"] = "popularity.desc"
    elif "10s" in era_str:
        params["primary_release_date.gte"] = "2010-01-01"
        params["primary_release_date.lte"] = "2019-12-31"
        params["sort_by"] = "popularity.desc"
    elif "20s" in era_str:
        params["primary_release_date.gte"] = "2020-01-01"
        params["primary_release_date.lte"] = "2029-12-31"
        params["sort_by"] = "popularity.desc"
    else:
        params["vote_count.gte"] = 50
        params["sort_by"] = "vote_average.desc"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    # Dynamic fallback targets (Alternate base URLs successfully bypass ISP blocks)
    base_urls = [
        "https://api.themoviedb.org/3/discover/movie",
        "https://api.tmdb.org/3/discover/movie"
    ]

    # Populate robust connection routing matrices
    strategies = []
    for url in base_urls:
        strategies.append(("DIRECT", url))
    for url in base_urls:
        strategies.append(("CORSPROXY", url))
        strategies.append(("ALLORIGINS", url))
        strategies.append(("CODETABS", url))
        strategies.append(("THINGPROXY", url))
    
    data = None
    captured_auth_error = None

    # Retrieve the preferred credential
    active_cred = v4_token or v3_key
    is_v4_token = active_cred.startswith("eyJ") or len(active_cred) > 100

    for strategy, base_url in strategies:
        local_params = params.copy()
        local_headers = headers.copy()

        # Safely assign credential queries or custom headers
        if is_v4_token:
            local_headers["Authorization"] = f"Bearer {active_cred}"
        else:
            local_params["api_key"] = active_cred

        # Clean endpoint formulation
        tmdb_url = f"{base_url}?{urllib.parse.urlencode(local_params)}"
        cb_val = random.randint(100000, 999999)

        # Route dynamically through public proxy channels
        if strategy == "DIRECT":
            target_url = tmdb_url
        elif strategy == "CORSPROXY":
            target_url = f"https://corsproxy.io/?url={urllib.parse.quote(tmdb_url)}&_cb={cb_val}"
        elif strategy == "ALLORIGINS":
            target_url = f"https://api.allorigins.win/raw?url={urllib.parse.quote(tmdb_url)}&_cb={cb_val}"
        elif strategy == "CODETABS":
            target_url = f"https://api.codetabs.com/v1/proxy?quest={urllib.parse.quote(tmdb_url)}&_cb={cb_val}"
        elif strategy == "THINGPROXY":
            target_url = f"https://thingproxy.freeboard.io/fetch/{tmdb_url}?_cb={cb_val}"

        try:
            # Python runtime preserves custom headers securely on proxy endpoints
            response = requests.get(target_url, headers=local_headers, timeout=(4, 8))
            
            if response.status_code in [401, 403, 404]:
                try:
                    error_payload = response.json()
                    captured_auth_error = error_payload.get('status_message') or error_payload.get('status_code')
                except Exception:
                    captured_auth_error = f"HTTP {response.status_code} Access Denied"
                continue
                
            if response.status_code == 200:
                try:
                    data = response.json()
                except Exception:
                    continue
                
                if data and isinstance(data, dict):
                    if 'status_message' in data:
                        captured_auth_error = data['status_message']
                        continue
                    elif 'results' in data:
                        break
        except Exception:
            continue

    # Return successful payloads elegantly
    if data and isinstance(data, dict) and 'results' in data:
        movies = data['results']
        
        # If TMDB successfully connected but returned 0 results, return an empty dataframe.
        if not movies:
            return pd.DataFrame()
        
        # Parse standard candidates
        candidate_movies = []
        for m in movies:
            raw_rating = m.get('vote_average')
            try:
                rating = float(raw_rating) if raw_rating is not None else 0.0
            except (ValueError, TypeError):
                rating = 0.0
                
            title = m.get('title') or m.get('original_title') or "Untitled Movie"
            release_date = m.get('release_date') or "N/A"
            overview = m.get('overview') or "No description available."

            candidate_movies.append({
                'Title': str(title),
                'Rating': rating,
                'Release Date': str(release_date),
                'Overview': str(overview)
            })

        # --- THE SMART REPETITION REMOVAL ALGORITHM ---
        query_key = (language_code, tuple(sorted(genre_names)), era)
        if query_key not in RECOMMENDATION_HISTORY:
            RECOMMENDATION_HISTORY[query_key] = set()
            
        seen_titles = RECOMMENDATION_HISTORY[query_key]

        # Isolate unseen options
        unseen_movies = [m for m in candidate_movies if m['Title'] not in seen_titles]
        seen_movies = [m for m in candidate_movies if m['Title'] in seen_titles]

        if len(unseen_movies) >= 10:
            # First query or complete freshness: Pull 10 completely unseen titles!
            selected_movies = random.sample(unseen_movies, 10)
        else:
            # If we've exhausted our unseen list, fill the remainder with previously shown items
            selected_movies = unseen_movies
            needed = 10 - len(selected_movies)
            if needed > 0 and seen_movies:
                selected_movies.extend(random.sample(seen_movies, min(len(seen_movies), needed)))
            
            # Reset history so we can cycle fresh selections on subsequent runs
            seen_titles.clear()

        # Save selected titles in history
        for m in selected_movies:
            seen_titles.add(m['Title'])

        return pd.DataFrame(selected_movies)

    if captured_auth_error:
        return pd.DataFrame([{
            'Title': '🔒 TMDB Authentication Failed',
            'Rating': 0.0,
            'Release Date': 'N/A',
            'Overview': f"The TMDB Server rejected your credentials with the message: '{captured_auth_error}'. Please make sure you copied your full credentials into your configuration file without wrapping quotes."
        }])

    return pd.DataFrame([{
        'Title': '📡 Connection Diagnostic Error',
        'Rating': 0.0,
        'Release Date': 'N/A',
        'Overview': "All secure connection pathways failed to establish a connection. This happens when local network controls block public proxies. Please try switching your mobile hotspot or VPN on/off, or make sure you have supplied a valid TMDB API Key in your `.env` file."
    }])