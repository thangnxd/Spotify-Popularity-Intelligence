import streamlit as st

from utils.load_data import load_data
from components.styles import load_css
from components.sidebar import render_sidebar

from pages_app.executive_summary import show_executive_summary
from pages_app.popularity_analysis import show_popularity_analysis
from pages_app.distribution_correlation import show_distribution_correlation
from pages_app.genre_artist import show_genre_artist
from pages_app.time_trend import show_time_trend


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Spotify Popularity Intelligence",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================
# Load style + data
# =========================
load_css()
df = load_data("data/spotify_cleaned.csv")


# =========================
# Header
# =========================
st.markdown(
    """
    <div>
        <div class="main-title">Spotify Popularity Intelligence</div>
        <div class="sub-title">
            Interactive dashboard exploring genre, audio features and popularity patterns in Spotify tracks.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# Sidebar filters
# =========================
page, filtered_df = render_sidebar(df)


# =========================
# Page router
# =========================
if page == "0. Executive Summary":
    show_executive_summary(filtered_df, df)

elif page == "1. High vs Low Popularity":
    show_popularity_analysis(filtered_df, df)

elif page == "2. Distribution & Correlation":
    show_distribution_correlation(filtered_df, df)

elif page == "3. Genre & Artist":
    show_genre_artist(filtered_df, df)

elif page == "4. Time & Trend":
    show_time_trend(filtered_df, df)