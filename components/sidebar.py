import streamlit as st


def render_sidebar(df):
    st.sidebar.markdown("## 🎧 Navigation")

    page = st.sidebar.radio(
        "Chọn trang",
        [
            "0. Executive Summary",
            "1. High vs Low Popularity",
            "2. Distribution & Correlation",
            "3. Genre & Artist",
            "4. Time & Trend"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🎛️ Global Filters")

    genres = sorted(df["playlist_genre"].dropna().unique())

    selected_genres = st.sidebar.multiselect(
        "Playlist genre",
        genres,
        default=genres
    )

    min_year = int(df["release_year"].dropna().min())
    max_year = int(df["release_year"].dropna().max())

    selected_years = st.sidebar.slider(
        "Release year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    popularity_range = st.sidebar.slider(
        "Popularity score",
        min_value=0,
        max_value=100,
        value=(0, 100)
    )

    filtered_df = df[
        (df["playlist_genre"].isin(selected_genres)) &
        (df["release_year"].between(selected_years[0], selected_years[1])) &
        (df["track_popularity"].between(popularity_range[0], popularity_range[1]))
    ].copy()

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Filtered tracks: {len(filtered_df):,}")

    return page, filtered_df