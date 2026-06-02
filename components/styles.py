import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 10%, rgba(29,185,84,0.18), transparent 28%),
                radial-gradient(circle at 85% 20%, rgba(139,92,246,0.18), transparent 30%),
                linear-gradient(135deg, #090B10 0%, #0E1117 45%, #111827 100%);
            color: #F5F5F5;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #101318 0%, #0B0D12 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        .main-title {
            font-size: 46px;
            font-weight: 900;
            background: linear-gradient(90deg, #1DB954, #A7F3D0, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 4px;
        }

        .sub-title {
            font-size: 18px;
            color: #B8BBC7;
            margin-bottom: 28px;
        }

        .page-header {
            background: rgba(24, 26, 32, 0.82);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            padding: 26px 30px;
            margin-bottom: 24px;
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        }

        .card {
            background: linear-gradient(180deg, rgba(31,34,43,0.95), rgba(18,20,27,0.95));
            padding: 22px;
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 14px 36px rgba(0,0,0,0.35);
            min-height: 125px;
        }

        .metric-label {
            color: #A0A0A0;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .metric-value {
            color: #FFFFFF;
            font-size: 32px;
            font-weight: 800;
            margin-top: 8px;
        }

        .metric-note {
            color: #A0A0A0;
            font-size: 13px;
            margin-top: 6px;
        }

        .insight-box {
            background: linear-gradient(135deg, rgba(29,185,84,0.15), rgba(139,92,246,0.12));
            border: 1px solid rgba(255,255,255,0.10);
            border-left: 5px solid #1DB954;
            padding: 18px 20px;
            border-radius: 18px;
            margin-bottom: 16px;
            box-shadow: 0 10px 28px rgba(0,0,0,0.25);
        }

        .tag {
            background: linear-gradient(90deg, #1DB954, #A7F3D0);
            color: #07110B;
            padding: 5px 12px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
        }

        .section-title {
            font-size: 24px;
            font-weight: 800;
            color: #FFFFFF;
            margin-top: 16px;
            margin-bottom: 12px;
        }

        [data-testid="stPlotlyChart"] {
            background: rgba(24,26,32,0.75);
            border-radius: 22px;
            padding: 10px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="stDataFrame"] {
            background: rgba(24,26,32,0.75);
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.08);
        }
        </style>
        """,
        unsafe_allow_html=True
    )