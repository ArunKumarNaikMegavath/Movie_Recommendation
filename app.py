import streamlit as st
import requests

# Set page config
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #0e1117;
        padding: 20px;
    }
    
    /* Headers */
    h1 {
        color: #FF4B4B;
        text-align: center;
        font-size: 3em !important;
        padding: 20px 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2 {
        color: #FF8C00 ;
        margin-top: 20px !important;
    }
    h3 {
        color: #00FF9F !important;
    }
    
    /* Cards */
    .stCardContainer {
        background-color: #1E2127;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Movie cards */
    .movie-card {
        background-color: #2E3137;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border: 1px solid #3E4147;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
    }
    
    /* Search box */
    .stTextInput input {
        border-radius: 20px;
        border: 2px solid #FF4B4B;
        padding: 10px 20px;
        background-color: #1E2127;
        color: white;
    }
    
    /* Ratings */
    .rating {
        color: #FFD700;
        font-weight: bold;
    }
    
    /* Genre tags */
    .genre-tag {
        background-color: #FF4B4B;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1E2127;
    
    }
    
    /* Custom divider */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #FF4B4B, #FF8C00, #00FF9F);
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# Constants
TMDB_BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Initialize session state for API key
if 'api_key' not in st.session_state:
    st.session_state.api_key = "2807539e279527149de5799dd89b024b"

# Sidebar with gradient background
with st.sidebar:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF4B4B, #FF8C00);
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;'>
            <h2 style='color: white ; margin: 0;'>Arun Kumar Naik</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # api_key_input = st.text_input(
    #     "Enter TMDB API Key:",
    #     value=st.session_state.api_key,
    #     type="password"
    # )
    api_key_input =st.session_state.api_key
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

    st.markdown("""
        <div style='background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin-top: 20px;
                                    >
            <h3 style='color: #00FF9F !important;'>Get Your API Key</h3>
            <ol style='color: white;'>
                <li>Sign up at TMDB</li>
                <li>Go to Settings → API</li>
                <li>Generate API key</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

# Cache API calls
@st.cache_data(ttl=3600)
def fetch_movie_data(query, api_key):
    try:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            "api_key": api_key,
            "query": query,
            "language": "en-US",
            "page": 1
        }
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_movie_details(movie_id, api_key):
    try:
        details_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        credits_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
        params = {"api_key": api_key, "language": "en-US", "append_to_response": "videos,keywords"}
        
        details = requests.get(details_url, params=params, timeout=10).json()
        credits = requests.get(credits_url, params={"api_key": api_key}, timeout=10).json()
        return details, credits
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching details: {str(e)}")
        return None, None

@st.cache_data(ttl=3600)
def get_recommendations(movie_id, api_key):
    try:
        rec_url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
        params = {"api_key": api_key, "language": "en-US", "page": 1}
        return requests.get(rec_url, params=params, timeout=10).json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recommendations: {str(e)}")
        return None

# Main app
st.markdown("<h1>🎬 Movies For You</h1>", unsafe_allow_html=True)
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

if not st.session_state.api_key:
    st.warning("👋 Please enter your TMDB API key in the sidebar to start exploring movies!")
else:
    # Search box with styling
    st.markdown("""
        <div style='background: rgba(255,75,75,0.1); 
                    padding: 0px; 
                    border-radius: 0px; 
                    margin-bottom: 0px;'>
    """, unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search Your Favorite Movie:", 
                                placeholder="Enter a movie title...")
    st.markdown("</div>", unsafe_allow_html=True)

    if search_query:
        with st.spinner("🎬 Searching the movie universe..."):
            search_results = fetch_movie_data(search_query, st.session_state.api_key)
            
            if search_results and 'results' in search_results and search_results['results']:
                movies = {
                    f"{movie['title']} ({movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A'})": movie 
                    for movie in search_results['results']
                }
                
                selected_movie_title = st.selectbox("🎯 Select your movie:", list(movies.keys()))
                
                if selected_movie_title:
                    selected_movie = movies[selected_movie_title]
                    
                    with st.spinner("✨ Fetching movie magic..."):
                        movie_details, credits = get_movie_details(
                            selected_movie['id'],
                            st.session_state.api_key
                        )
                        recommendations = get_recommendations(
                            selected_movie['id'],
                            st.session_state.api_key
                        )
                    
                    if movie_details and recommendations:
                        # Movie details section
                        st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.markdown("""
                                <div style='background: rgba(255,255,255,0.05); 
                                          padding: 10px; 
                                          border-radius: 10px;'>
                            """, unsafe_allow_html=True)
                            if selected_movie.get('poster_path'):
                                st.image(
                                    f"{POSTER_BASE_URL}{selected_movie['poster_path']}",
                                    use_column_width=True
                                )
                            else:
                                st.image("https://via.placeholder.com/500x750?text=No+Poster")
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div style='background: rgba(255,255,255,0.05); 
                                          padding: 20px; 
                                          border-radius: 10px;'>
                                    <h2>{selected_movie_title}</h2>
                                    <p class='rating'>⭐ {selected_movie.get('vote_average', 'N/A')}/10</p>
                                    <p>📅 {selected_movie.get('release_date', 'N/A')}</p>
                                    <h3>Overview</h3>
                                    <p>{selected_movie.get('overview', 'No overview available.')}</p>
                                    <h3>Genres</h3>
                                    {''.join([f"<span class='genre-tag'>{genre['name']}</span> " 
                                            for genre in movie_details.get('genres', [])])}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Recommendations section
                        if recommendations.get('results'):
                            st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
                            st.markdown("<h2>✨ Recommended Movies</h2>", unsafe_allow_html=True)
                            
                            cols = st.columns(3)
                            for idx, movie in enumerate(recommendations['results'][:9]):
                                with cols[idx % 3]:
                                    st.markdown("""
                                        <div class='movie-card'>
                                    """, unsafe_allow_html=True)
                                    
                                    if movie.get('poster_path'):
                                        st.image(
                                            f"{POSTER_BASE_URL}{movie['poster_path']}",
                                            use_column_width=True
                                        )
                                    else:
                                        st.image("https://via.placeholder.com/500x750?text=No+Poster")
                                    
                                    st.markdown(f"""
                                        <h3>{movie['title']}</h3>
                                        <p class='rating'>⭐ {movie.get('vote_average', 'N/A')}/10</p>
                                    """, unsafe_allow_html=True)
                                    
                                    with st.expander("Overview"):
                                        st.write(movie.get('overview', 'No overview available.'))
                                    
                                    st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.info("🎬 No recommendations found for this movie.")
            else:
                st.warning("🔍 No movies found. Try another title!")

# Footer
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        Made with ❤️ for movie lovers
    </div>
""", unsafe_allow_html=True)