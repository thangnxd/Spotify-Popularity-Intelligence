import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


PLOTLY_TEMPLATE = "plotly_dark"


def kpi_card(label, value, note=""):
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
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


def section_title(title):
    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        """,
        unsafe_allow_html=True
    )


def show_executive_summary(filtered_df, full_df):
    df = filtered_df.copy()

    st.markdown(
        """
        <div class="page-header">
            <h2>Executive Summary <span class="tag">Overview</span></h2>
            <p style="color:#B8BBC7;">
                Bức tranh tổng quan về dữ liệu Spotify: quy mô dữ liệu, mức độ phổ biến,
                phân bố thể loại và xu hướng phát hành theo thời gian.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning("Không có dữ liệu sau khi áp dụng bộ lọc.")
        return

    # =========================
    # KPI values
    # =========================
    total_tracks = len(df)
    total_artists = df["track_artist"].nunique()
    total_genres = df["playlist_genre"].nunique()
    avg_popularity = df["track_popularity"].mean()

    high_avg = df[df["popularity_level"] == "High"]["track_popularity"].mean()
    low_avg = df[df["popularity_level"] == "Low"]["track_popularity"].mean()

    if high_avg == high_avg and low_avg == low_avg:
        delta_text = f"+{high_avg - low_avg:.1f} điểm"
    else:
        delta_text = "N/A"

    # =========================
    # KPI row
    # =========================
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Total Tracks",
            f"{total_tracks:,}",
            "Số bài hát trong phạm vi lọc"
        )

    with c2:
        kpi_card(
            "Artists",
            f"{total_artists:,}",
            "Số nghệ sĩ khác nhau"
        )

    with c3:
        kpi_card(
            "Genres",
            f"{total_genres}",
            "Số playlist genre"
        )

    with c4:
        kpi_card(
            "Avg Popularity",
            f"{avg_popularity:.1f}",
            f"High - Low delta: {delta_text}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Insight callouts
    # =========================
    genre_avg = (
        df.groupby("playlist_genre")["track_popularity"]
        .mean()
        .sort_values(ascending=False)
    )

    top_genre = genre_avg.index[0]
    top_genre_score = genre_avg.iloc[0]

    common_genre = df["playlist_genre"].value_counts().index[0]
    common_genre_count = df["playlist_genre"].value_counts().iloc[0]

    corr_features = [
        "energy",
        "danceability",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness"
    ]

    corr = (
        df[corr_features + ["track_popularity"]]
        .corr(numeric_only=True)["track_popularity"]
        .drop("track_popularity")
        .sort_values(key=lambda x: x.abs(), ascending=False)
    )

    strongest_feature = corr.index[0]
    strongest_corr = corr.iloc[0]

    i1, i2, i3 = st.columns(3)

    with i1:
        insight_box(
            "Genre nổi bật nhất",
            f"<b>{top_genre}</b> đang có điểm popularity trung bình cao nhất "
            f"trong phạm vi lọc, đạt khoảng <b>{top_genre_score:.1f}</b> điểm."
        )

    with i2:
        insight_box(
            "Genre phổ biến nhất trong dữ liệu",
            f"<b>{common_genre}</b> là genre xuất hiện nhiều nhất với "
            f"<b>{common_genre_count:,}</b> bài hát."
        )

    with i3:
        insight_box(
            "Feature liên quan mạnh nhất",
            f"<b>{strongest_feature}</b> có tương quan mạnh nhất với popularity "
            f"trong các audio feature, với hệ số khoảng <b>{strongest_corr:.2f}</b>."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Chart row 1
    # =========================
    left, right = st.columns([1.15, 1])

    with left:
        section_title("Popularity Distribution")

        fig = px.histogram(
            df,
            x="track_popularity",
            nbins=40,
            marginal="box",
            color="popularity_level",
            color_discrete_map={
                "Low": "#8B5CF6",
                "Medium": "#38BDF8",
                "High": "#1DB954"
            },
            title=None,
            template=PLOTLY_TEMPLATE
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            bargap=0.05,
            xaxis_title="Track popularity",
            yaxis_title="Number of tracks",
            legend_title="Popularity level",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        section_title("Genre Distribution")

        genre_count = (
            df["playlist_genre"]
            .value_counts()
            .reset_index()
        )
        genre_count.columns = ["playlist_genre", "count"]

        fig = px.bar(
            genre_count,
            x="count",
            y="playlist_genre",
            orientation="h",
            color="count",
            color_continuous_scale="Greens",
            template=PLOTLY_TEMPLATE
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Number of tracks",
            yaxis_title="Genre",
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        fig.update_yaxes(categoryorder="total ascending")

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Chart row 2
    # =========================
    left2, right2 = st.columns([1, 1])

    with left2:
        section_title("Average Popularity by Genre")

        genre_pop = (
            df.groupby("playlist_genre")["track_popularity"]
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )

        fig = px.bar(
            genre_pop,
            x="track_popularity",
            y="playlist_genre",
            orientation="h",
            color="track_popularity",
            color_continuous_scale="Viridis",
            template=PLOTLY_TEMPLATE
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Average popularity",
            yaxis_title="Genre",
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:
        section_title("Release Trend")

        year_count = (
            df.dropna(subset=["release_year"])
            .groupby("release_year")
            .size()
            .reset_index(name="count")
            .sort_values("release_year")
        )

        fig = px.line(
            year_count,
            x="release_year",
            y="count",
            markers=True,
            template=PLOTLY_TEMPLATE
        )

        fig.update_traces(
            line=dict(width=3, color="#1DB954"),
            marker=dict(size=6)
        )

        fig.update_layout(
            height=430,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Release year",
            yaxis_title="Number of tracks",
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Data preview
    # =========================
    section_title("Sample Tracks")

    preview_cols = [
        "track_name",
        "track_artist",
        "playlist_genre",
        "playlist_subgenre",
        "track_popularity",
        "energy",
        "danceability",
        "valence",
        "release_year"
    ]

    existing_cols = [col for col in preview_cols if col in df.columns]

    st.dataframe(
        df[existing_cols]
        .sort_values("track_popularity", ascending=False)
        .head(15),
        use_container_width=True,
        hide_index=True
    )