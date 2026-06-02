import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


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


def show_time_trend(filtered_df, full_df):
    df = filtered_df.copy()

    st.markdown(
        """
        <div class="page-header">
            <h2>Time & Trend Analysis <span class="tag">Temporal View</span></h2>
            <p style="color:#B8BBC7;">
                Phân tích xu hướng phát hành và mức độ phổ biến của bài hát theo thời gian.
                Trang này giúp quan sát dữ liệu theo chiều thời gian và sự thay đổi giữa các genre.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning("Không có dữ liệu sau khi áp dụng bộ lọc.")
        return

    df = df.dropna(subset=["release_year"]).copy()
    df["release_year"] = df["release_year"].astype(int)

    if df.empty:
        st.warning("Không có dữ liệu năm phát hành hợp lệ.")
        return

    # =========================
    # Year summary
    # =========================
    yearly = (
        df.groupby("release_year")
        .agg(
            track_count=("track_name", "count"),
            avg_popularity=("track_popularity", "mean"),
            avg_energy=("energy", "mean"),
            avg_danceability=("danceability", "mean"),
            avg_valence=("valence", "mean"),
            avg_acousticness=("acousticness", "mean")
        )
        .reset_index()
        .sort_values("release_year")
    )

    peak_year_count = yearly.sort_values("track_count", ascending=False).iloc[0]
    peak_year_pop = yearly.sort_values("avg_popularity", ascending=False).iloc[0]

    recent_year = yearly["release_year"].max()
    oldest_year = yearly["release_year"].min()

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_box(
            "Release Coverage",
            f"Dữ liệu đang bao phủ giai đoạn từ <b>{oldest_year}</b> đến "
            f"<b>{recent_year}</b>."
        )

    with c2:
        insight_box(
            "Most Active Release Year",
            f"Năm <b>{int(peak_year_count['release_year'])}</b> có số bài hát nhiều nhất, "
            f"với <b>{int(peak_year_count['track_count'])}</b> bài."
        )

    with c3:
        insight_box(
            "Highest Avg Popularity Year",
            f"Năm <b>{int(peak_year_pop['release_year'])}</b> có popularity trung bình cao nhất, "
            f"đạt khoảng <b>{peak_year_pop['avg_popularity']:.1f}</b> điểm."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Row 1: count + avg popularity
    # =========================
    left, right = st.columns(2)

    with left:
        section_title("Number of Tracks Released by Year")

        fig = px.area(
            yearly,
            x="release_year",
            y="track_count",
            template=PLOTLY_TEMPLATE
        )

        fig.update_traces(
            line=dict(color="#1DB954", width=3),
            fillcolor="rgba(29,185,84,0.25)"
        )

        fig.update_layout(
            height=480,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Release year",
            yaxis_title="Number of tracks",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        section_title("Average Popularity by Year")

        fig = px.line(
            yearly,
            x="release_year",
            y="avg_popularity",
            markers=True,
            template=PLOTLY_TEMPLATE
        )

        fig.update_traces(
            line=dict(color="#8B5CF6", width=3),
            marker=dict(size=7)
        )

        fig.update_layout(
            height=480,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Release year",
            yaxis_title="Average popularity",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Row 2: Genre-Year heatmap
    # =========================
    section_title("Genre Popularity Heatmap by Year")

    min_tracks = st.slider(
        "Chỉ hiển thị genre-year có tối thiểu bao nhiêu bài hát?",
        min_value=1,
        max_value=20,
        value=2
    )

    gy = (
        df.groupby(["playlist_genre", "release_year"])
        .agg(
            avg_popularity=("track_popularity", "mean"),
            track_count=("track_name", "count")
        )
        .reset_index()
    )

    gy = gy[gy["track_count"] >= min_tracks]

    pivot = gy.pivot(
        index="playlist_genre",
        columns="release_year",
        values="avg_popularity"
    )

    if pivot.empty:
        st.warning("Không đủ dữ liệu để vẽ heatmap với ngưỡng hiện tại.")
    else:
        fig = px.imshow(
            pivot,
            color_continuous_scale="Viridis",
            aspect="auto",
            template=PLOTLY_TEMPLATE,
            text_auto=".0f"
        )

        fig.update_layout(
            height=620,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Release year",
            yaxis_title="Genre",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Row 3: Feature trend
    # =========================
    section_title("Audio Feature Trends Over Time")

    selected_features = st.multiselect(
        "Chọn audio features",
        [
            "avg_energy",
            "avg_danceability",
            "avg_valence",
            "avg_acousticness"
        ],
        default=["avg_energy", "avg_danceability", "avg_valence"]
    )

    if selected_features:
        trend_long = yearly.melt(
            id_vars="release_year",
            value_vars=selected_features,
            var_name="feature",
            value_name="value"
        )

        trend_long["feature"] = trend_long["feature"].str.replace("avg_", "")

        fig = px.line(
            trend_long,
            x="release_year",
            y="value",
            color="feature",
            markers=True,
            template=PLOTLY_TEMPLATE
        )

        fig.update_layout(
            height=540,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Release year",
            yaxis_title="Average feature value",
            legend_title="Audio feature",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Hãy chọn ít nhất một audio feature.")

    # =========================
    # Row 4: Top genre by selected year
    # =========================
    section_title("Top Genres in a Selected Year")

    selected_year = st.selectbox(
        "Chọn năm để xem genre nổi bật",
        sorted(df["release_year"].unique(), reverse=True)
    )

    year_genre = (
        df[df["release_year"] == selected_year]
        .groupby("playlist_genre")
        .agg(
            track_count=("track_name", "count"),
            avg_popularity=("track_popularity", "mean")
        )
        .reset_index()
        .sort_values("avg_popularity", ascending=False)
    )

    if year_genre.empty:
        st.warning("Không có dữ liệu cho năm đã chọn.")
    else:
        fig = px.bar(
            year_genre.sort_values("avg_popularity"),
            x="avg_popularity",
            y="playlist_genre",
            orientation="h",
            color="track_count",
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE,
            hover_data={
                "track_count": True,
                "avg_popularity": ":.2f"
            }
        )

        fig.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Average popularity",
            yaxis_title="Genre",
            coloraxis_colorbar_title="Tracks",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            year_genre,
            use_container_width=True,
            hide_index=True
        )