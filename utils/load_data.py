import pandas as pd
import streamlit as st


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    df["track_album_release_date"] = pd.to_datetime(
        df["track_album_release_date"],
        errors="coerce"
    )

    if "release_year" not in df.columns:
        df["release_year"] = df["track_album_release_date"].dt.year

    if "duration_min" not in df.columns:
        df["duration_min"] = df["duration_ms"] / 60000

    df["popularity_level"] = pd.cut(
        df["track_popularity"],
        bins=[0, 40, 70, 100],
        labels=["Low", "Medium", "High"],
        include_lowest=True
    )

    audio_features = [
        "energy",
        "danceability",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness"
    ]

    for col in audio_features:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["track_popularity"] = pd.to_numeric(
        df["track_popularity"],
        errors="coerce"
    )

    df = df.dropna(subset=["track_popularity", "playlist_genre"])

    return df