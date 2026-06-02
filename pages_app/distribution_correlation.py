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


def show_distribution_correlation(filtered_df, full_df):
    df = filtered_df.copy()

    st.markdown(
        """
        <div class="page-header">
            <h2>Distribution & Correlation <span class="tag">Deep Dive</span></h2>
            <p style="color:#B8BBC7;">
                Phân tích phân phối và mối quan hệ giữa các đặc trưng âm thanh.
                Trang này giúp kiểm chứng xem popularity có liên hệ mạnh với audio features hay không.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning("Không có dữ liệu sau khi áp dụng bộ lọc.")
        return

    audio_features = [
        "energy",
        "danceability",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness",
        "tempo",
        "loudness",
        "duration_min",
        "track_popularity"
    ]

    existing_features = [col for col in audio_features if col in df.columns]

    # =========================
    # Correlation summary
    # =========================
    corr = df[existing_features].corr(numeric_only=True)

    pop_corr = (
        corr["track_popularity"]
        .drop("track_popularity")
        .sort_values(key=lambda x: x.abs(), ascending=False)
    )

    strongest_feature = pop_corr.index[0]
    strongest_corr = pop_corr.iloc[0]

    corr_energy_acoustic = corr.loc["energy", "acousticness"] if "energy" in corr.index and "acousticness" in corr.columns else np.nan
    corr_energy_loudness = corr.loc["energy", "loudness"] if "energy" in corr.index and "loudness" in corr.columns else np.nan

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_box(
            "Popularity correlation is weak",
            f"Feature liên hệ mạnh nhất với popularity là <b>{strongest_feature}</b>, "
            f"nhưng hệ số tương quan chỉ khoảng <b>{strongest_corr:.2f}</b>."
        )

    with c2:
        insight_box(
            "Energy vs Acousticness",
            f"Energy và Acousticness thường đi ngược chiều nhau, "
            f"với correlation khoảng <b>{corr_energy_acoustic:.2f}</b>."
        )

    with c3:
        insight_box(
            "Energy vs Loudness",
            f"Energy và Loudness có xu hướng đồng biến rõ rệt, "
            f"với correlation khoảng <b>{corr_energy_loudness:.2f}</b>."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # Row 1: Correlation Heatmap
    # =========================
    section_title("Correlation Matrix")

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        template=PLOTLY_TEMPLATE,
        aspect="auto"
    )

    fig.update_layout(
        height=650,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Row 2: Scatter plots
    # =========================
    section_title("Feature Relationships")

    left, right = st.columns(2)

    with left:
        fig = px.scatter(
            df,
            x="energy",
            y="acousticness",
            color="playlist_genre",
            hover_data=[
                "track_name",
                "track_artist",
                "track_popularity",
                "playlist_subgenre"
            ],
            opacity=0.7,
            template=PLOTLY_TEMPLATE,
            title="Energy vs Acousticness"
        )

        fig.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title="Genre"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.scatter(
            df,
            x="loudness",
            y="energy",
            color="popularity_level",
            hover_data=[
                "track_name",
                "track_artist",
                "track_popularity",
                "playlist_genre"
            ],
            opacity=0.7,
            template=PLOTLY_TEMPLATE,
            title="Loudness vs Energy"
        )

        fig.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title="Popularity Level"
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Row 3: Distribution comparison
    # =========================
    section_title("Feature Distribution by Popularity Level")

    selected_feature = st.selectbox(
        "Chọn feature để xem phân phối",
        [
            "energy",
            "danceability",
            "valence",
            "acousticness",
            "speechiness",
            "instrumentalness",
            "liveness",
            "tempo",
            "duration_min"
        ]
    )

    left2, right2 = st.columns(2)

    with left2:
        fig = px.violin(
            df,
            x="popularity_level",
            y=selected_feature,
            color="popularity_level",
            box=True,
            points="all",
            template=PLOTLY_TEMPLATE,
            title=f"{selected_feature} distribution by popularity level",
            color_discrete_map={
                "Low": "#8B5CF6",
                "Medium": "#38BDF8",
                "High": "#1DB954"
            }
        )

        fig.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right2:
        fig = px.histogram(
            df,
            x=selected_feature,
            color="popularity_level",
            nbins=40,
            barmode="overlay",
            opacity=0.65,
            template=PLOTLY_TEMPLATE,
            title=f"{selected_feature} histogram",
            color_discrete_map={
                "Low": "#8B5CF6",
                "Medium": "#38BDF8",
                "High": "#1DB954"
            }
        )

        fig.update_layout(
            height=520,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Row 4: Popularity relationship
    # =========================
    section_title("Selected Feature vs Popularity")

    fig = px.scatter(
        df,
        x=selected_feature,
        y="track_popularity",
        color="playlist_genre",
        hover_data=[
            "track_name",
            "track_artist",
            "playlist_subgenre"
        ],
        opacity=0.7,
        trendline="ols",
        template=PLOTLY_TEMPLATE,
        title=f"{selected_feature} vs Track Popularity"
    )

    fig.update_layout(
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title="Genre"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Table
    # =========================
    section_title("Correlation with Popularity")

    corr_table = pop_corr.reset_index()
    corr_table.columns = ["feature", "correlation_with_popularity"]
    corr_table["correlation_with_popularity"] = corr_table["correlation_with_popularity"].round(3)

    st.dataframe(
        corr_table,
        use_container_width=True,
        hide_index=True
    )