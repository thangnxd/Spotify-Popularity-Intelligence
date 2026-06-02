import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px


PLOTLY_TEMPLATE = "plotly_dark"


def section_title(title):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        """,
        unsafe_allow_html=True
    )


def insight_box(title, text):
    st.markdown(
        f"""
        <div class="insight-box">
            <div style="font-size:17px;font-weight:800;color:#FFFFFF;margin-bottom:6px;">
                {title}
            </div>
            <div style="font-size:14px;color:#C9CBD3;line-height:1.5;">
                {text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_genre_artist(filtered_df, full_df):
    df = filtered_df.copy()

    st.markdown(
        """
        <div class="page-header">
            <h2>Genre & Artist Profiling <span class="tag">Structure</span></h2>
            <p style="color:#B8BBC7;">
                Khám phá cấu trúc thể loại, thể loại phụ và nghệ sĩ trong dữ liệu Spotify.
                Trang này tập trung vào phân nhóm, cấu trúc phân cấp và đặc trưng âm thanh theo genre.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning("Không có dữ liệu sau khi áp dụng bộ lọc.")
        return

    # =========================
    # Basic summary
    # =========================
    genre_count = df["playlist_genre"].nunique()
    subgenre_count = df["playlist_subgenre"].nunique()
    artist_count = df["track_artist"].nunique()

    genre_pop = (
        df.groupby("playlist_genre")["track_popularity"]
        .mean()
        .sort_values(ascending=False)
    )

    top_genre = genre_pop.index[0]
    top_genre_score = genre_pop.iloc[0]

    largest_genre = df["playlist_genre"].value_counts().index[0]
    largest_genre_count = df["playlist_genre"].value_counts().iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_box(
            "Genre Landscape",
            f"Dữ liệu hiện có <b>{genre_count}</b> genre chính và "
            f"<b>{subgenre_count}</b> subgenre."
        )

    with c2:
        insight_box(
            "Highest Average Popularity",
            f"<b>{top_genre}</b> có popularity trung bình cao nhất, khoảng "
            f"<b>{top_genre_score:.1f}</b> điểm."
        )

    with c3:
        insight_box(
            "Largest Genre",
            f"<b>{largest_genre}</b> là genre có nhiều bài hát nhất, với "
            f"<b>{largest_genre_count:,}</b> bài."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Treemap + Sunburst
    # =========================
    left, right = st.columns(2)

    with left:
        section_title("Treemap: Genre → Subgenre")

        treemap_df = (
            df.groupby(["playlist_genre", "playlist_subgenre"])
            .agg(
                count=("track_name", "count"),
                avg_popularity=("track_popularity", "mean")
            )
            .reset_index()
        )

        fig = px.treemap(
            treemap_df,
            path=["playlist_genre", "playlist_subgenre"],
            values="count",
            color="avg_popularity",
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE,
            hover_data={
                "count": True,
                "avg_popularity": ":.2f"
            }
        )

        fig.update_layout(
            height=620,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        section_title("Sunburst: Genre → Subgenre → Popularity")

        sunburst_df = (
            df.groupby(["playlist_genre", "playlist_subgenre", "popularity_level"])
            .size()
            .reset_index(name="count")
        )

        fig = px.sunburst(
            sunburst_df,
            path=["playlist_genre", "playlist_subgenre", "popularity_level"],
            values="count",
            color="popularity_level",
            color_discrete_map={
                "Low": "#8B5CF6",
                "Medium": "#38BDF8",
                "High": "#1DB954"
            },
            template=PLOTLY_TEMPLATE
        )

        fig.update_layout(
            height=620,
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 100% Stacked Bar
    # =========================
    section_title("Popularity Composition by Genre")

    comp = (
        df.groupby(["playlist_genre", "popularity_level"])
        .size()
        .reset_index(name="count")
    )

    comp["total"] = comp.groupby("playlist_genre")["count"].transform("sum")
    comp["percentage"] = comp["count"] / comp["total"] * 100

    fig = px.bar(
        comp,
        x="playlist_genre",
        y="percentage",
        color="popularity_level",
        template=PLOTLY_TEMPLATE,
        color_discrete_map={
            "Low": "#8B5CF6",
            "Medium": "#38BDF8",
            "High": "#1DB954"
        },
        text=comp["percentage"].round(1)
    )

    fig.update_layout(
        height=520,
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Genre",
        yaxis_title="Percentage (%)",
        legend_title="Popularity level",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.update_xaxes(tickangle=-35)

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Heatmap Genre × Feature
    # =========================
    section_title("Genre Audio Signature Heatmap")

    audio_features = [
        "energy",
        "danceability",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness"
    ]

    feature_matrix = (
        df.groupby("playlist_genre")[audio_features]
        .mean()
        .round(2)
    )

    fig = px.imshow(
        feature_matrix,
        text_auto=True,
        color_continuous_scale="Viridis",
        aspect="auto",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=620,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Audio features",
        yaxis_title="Genre"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Artist Section
    # =========================
    section_title("Top Artists")

    artist_metric = st.selectbox(
        "Chọn cách xếp hạng nghệ sĩ",
        [
            "Số lượng bài hát",
            "Popularity trung bình"
        ]
    )

    if artist_metric == "Số lượng bài hát":
        artist_df = (
            df.groupby("track_artist")
            .agg(
                track_count=("track_name", "count"),
                avg_popularity=("track_popularity", "mean")
            )
            .sort_values("track_count", ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            artist_df.sort_values("track_count"),
            x="track_count",
            y="track_artist",
            orientation="h",
            color="track_count",
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE,
            hover_data={
                "avg_popularity": ":.2f"
            }
        )

        fig.update_layout(
            height=560,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Track count",
            yaxis_title="Artist",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            artist_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        artist_df = (
            df.groupby("track_artist")
            .agg(
                track_count=("track_name", "count"),
                avg_popularity=("track_popularity", "mean")
            )
            .query("track_count >= 2")
            .sort_values("avg_popularity", ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            artist_df.sort_values("avg_popularity"),
            x="avg_popularity",
            y="track_artist",
            orientation="h",
            color="avg_popularity",
            color_continuous_scale="Viridis",
            template=PLOTLY_TEMPLATE,
            hover_data={
                "track_count": True
            }
        )

        fig.update_layout(
            height=560,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Average popularity",
            yaxis_title="Artist",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            artist_df,
            use_container_width=True,
            hide_index=True
        )