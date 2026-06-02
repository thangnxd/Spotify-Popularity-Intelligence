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


def show_popularity_analysis(filtered_df, full_df):

    df = filtered_df.copy()

    st.markdown(
        """
        <div class="page-header">
            <h2>High vs Low Popularity <span class="tag">Feature Gap Analysis</span></h2>
            <p style="color:#B8BBC7;">
                So sánh sự khác biệt giữa nhóm bài hát có popularity cao và thấp.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.warning("Không có dữ liệu.")
        return

    # ===================================
    # Feature list
    # ===================================

    features = [
        "energy",
        "danceability",
        "valence",
        "acousticness",
        "speechiness",
        "instrumentalness",
        "liveness",
        "tempo"
    ]

    high_df = df[df["popularity_level"] == "High"]
    low_df = df[df["popularity_level"] == "Low"]

    if len(high_df) == 0 or len(low_df) == 0:
        st.warning("Bộ lọc hiện tại không đủ nhóm High và Low.")
        return

    # ===================================
    # Insight cards
    # ===================================

    avg_high = high_df["track_popularity"].mean()
    avg_low = low_df["track_popularity"].mean()

    delta = avg_high - avg_low

    gap_df = pd.DataFrame({
        "feature": features,
        "high": high_df[features].mean().values,
        "low": low_df[features].mean().values
    })

    gap_df["gap"] = gap_df["high"] - gap_df["low"]

    largest_positive = gap_df.sort_values(
        "gap",
        ascending=False
    ).iloc[0]

    largest_negative = gap_df.sort_values(
        "gap",
        ascending=True
    ).iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        insight_box(
            "Popularity Gap",
            f"Nhóm High có popularity trung bình cao hơn khoảng "
            f"<b>{delta:.1f}</b> điểm."
        )

    with c2:
        insight_box(
            "Strongest Positive Feature",
            f"<b>{largest_positive['feature']}</b> cao hơn đáng kể "
            f"ở nhóm High."
        )

    with c3:
        insight_box(
            "Strongest Negative Feature",
            f"<b>{largest_negative['feature']}</b> thấp hơn đáng kể "
            f"ở nhóm High."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===================================
    # Waterfall
    # ===================================

    left, right = st.columns([1,1])

    with left:

        section_title("Feature Contribution Gap")

        waterfall_data = gap_df.sort_values(
            "gap",
            ascending=False
        )

        fig = go.Figure(
            go.Waterfall(
                name="Gap",
                orientation="v",
                measure=["relative"] * len(waterfall_data),
                x=waterfall_data["feature"],
                y=waterfall_data["gap"],
                connector={
                    "line": {"color": "#A0A0A0"}
                }
            )
        )

        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ===================================
    # Radar
    # ===================================

    with right:

        section_title("Audio Profile Comparison")

        radar_features = [
            "energy",
            "danceability",
            "valence",
            "acousticness",
            "speechiness",
            "liveness"
        ]

        high_profile = high_df[radar_features].mean()
        low_profile = low_df[radar_features].mean()

        fig = go.Figure()

        fig.add_trace(
            go.Scatterpolar(
                r=high_profile.values,
                theta=radar_features,
                fill="toself",
                name="High Popularity"
            )
        )

        fig.add_trace(
            go.Scatterpolar(
                r=low_profile.values,
                theta=radar_features,
                fill="toself",
                name="Low Popularity"
            )
        )

        fig.update_layout(
            template=PLOTLY_TEMPLATE,
            height=500,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0,1]
                )
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ===================================
    # Feature Gap Bar Chart
    # ===================================

    section_title("Feature Differences")

    fig = px.bar(
        gap_df.sort_values("gap"),
        x="gap",
        y="feature",
        orientation="h",
        color="gap",
        color_continuous_scale="RdYlGn",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ===================================
    # Distribution comparison
    # ===================================

    section_title("Popularity Distribution")

    fig = px.histogram(
        df,
        x="track_popularity",
        color="popularity_level",
        nbins=40,
        barmode="overlay",
        opacity=0.7,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ===================================
    # Table
    # ===================================

    section_title("Feature Summary")

    summary_df = gap_df.copy()

    summary_df["high"] = summary_df["high"].round(3)
    summary_df["low"] = summary_df["low"].round(3)
    summary_df["gap"] = summary_df["gap"].round(3)

    st.dataframe(
        summary_df.sort_values(
            "gap",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )