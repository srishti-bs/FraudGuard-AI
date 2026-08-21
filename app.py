"""
FraudGuard AI - Enterprise Credit Card Fraud Detection System
Main Entry Point: app.py
Author: Senior Python Developer / UI Designer
"""

import streamlit as st

# --- MODULAR IMPORTS ---
# Note: These modules will be implemented in subsequent steps.
from dashboard import render_dashboard
from predict import render_prediction
from charts import render_analytics
from history import render_history
from reports import render_reports
from about import render_about
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FraudGuard AI | Enterprise Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS (NVIDIA-INSPIRED DARK THEME & GLASSMORPHISM) ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Main Theme Colors */
        :root {
            --primary-color: #76B900; /* NVIDIA Green */
            --bg-color: #0E1117;
            --card-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        /* App Background */
        .stApp {
            background-color: var(--bg-color);
            color: #FFFFFF;
        }

        /* Gradient Header */
        .main-header {
            background: linear-gradient(90deg, #1a1a1a 0%, #76B900 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
            border-left: 5px solid #76B900;
        }

        /* Glassmorphism Cards */
        .glass-card{

        background:rgba(255,255,255,.06);

        backdrop-filter:blur(18px);

        border-radius:18px;

        padding:24px;

        border:1px solid rgba(255,255,255,.08);

        box-shadow:
        0 0 20px rgba(0,0,0,.35);

        transition:.35s;

        }
        
        .glass-card:hover{

        transform:translateY(-8px);

        box-shadow:
        0 0 30px rgba(118,185,0,.45);

        border:1px solid #76B900;

        }
        /* Metrics Styling */
        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
            color: var(--primary-color);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid var(--glass-border);
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-header {
                font-size: 18px;
            }
        }
        [data-testid="metric-container"]{

        background:#151A21;

        padding:18px;

        border-radius:15px;

        border:1px solid rgba(255,255,255,.08);

        transition:.3s;

        }

        [data-testid="metric-container"]:hover{

        transform:scale(1.03);

        border-color:#76B900;

        box-shadow:0 0 20px rgba(118,185,0,.25);

        }
        .stButton>button{

        background:#76B900;

        color:white;

        border:none;

        border-radius:12px;

        font-weight:bold;

        transition:.3s;

        }

        .stButton>button:hover{

        background:#8ED000;

        transform:scale(1.05);

        }
        .stDownloadButton>button{

        background:#76B900;

        color:white;

        border:none;

        border-radius:12px;

        font-weight:bold;

        padding:12px;

        }

        .stDownloadButton>button:hover{

        background:#8ED000;

        }
        ::-webkit-scrollbar{

        width:10px;

        }

        ::-webkit-scrollbar-track{

        background:#111;

        }

        ::-webkit-scrollbar-thumb{

        background:#76B900;

        border-radius:10px;

        }
        /* General text */
    body,
    .stApp,
    p,
    span,
    label,
    div {
        color: #F5F5F5 !important;
    }

    /* Headings */
    h1,h2,h3,h4,h5,h6{
        color:white !important;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"]{
        color:#CFCFCF !important;
    }

    /* Tables */
    thead th{
        color:white !important;
    }

    tbody td{
        color:#E6E6E6 !important;
    }

    /* Expander */
    .streamlit-expanderHeader{
        color:white !important;
    }

    /* Selectbox */
    .stSelectbox label{
        color:white !important;
    }

    /* Number Input */
    .stNumberInput label{
        color:white !important;
    }

    /* Text Input */
    .stTextInput label{
        color:white !important;
    }

    /* Radio */
    .stRadio label{
        color:white !important;
    }
                </style>
    """, unsafe_allow_html=True)



# --- MAIN NAVIGATION LOGIC ---
def main():
    inject_custom_css()

    # Sidebar Header
    st.sidebar.markdown("""
    <div style="
    background:linear-gradient(180deg,#76B900,#2E7D32);
    padding:20px;
    border-radius:18px;
    text-align:center;
    margin-bottom:20px;
    box-shadow:0 0 25px rgba(118,185,0,.35);
    ">

    <h1 style="color:white;margin-bottom:5px;">
    🛡️
    </h1>

    <h2 style="color:white;margin-top:0;">
    FraudGuard AI
    </h2>

    <p style="color:white;">
    Enterprise Edition
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.sidebar.success("🟢 AI Protection Active")
    st.sidebar.caption("Machine Learning Engine Online")
    st.sidebar.markdown("---")

    # Define Pages using Streamlit 1.31+ Navigation API
    pages = {
        "Main": [
            st.Page(render_dashboard, title="Dashboard", icon="🏠"),
            st.Page(render_prediction, title="Prediction", icon="🤖"),
            st.Page(render_analytics, title="Analytics", icon="📊"),
        ],
        "Management": [
            st.Page(render_history, title="Transaction History", icon="📜"),
            st.Page(render_reports, title="Reports", icon="📄"),
        ],
        "System": [
            st.Page(render_about, title="About", icon="ℹ️"),
        ]
    }

    # Initialize Navigation
    pg = st.navigation(pages)
    
    # Render sidebar-wide footer
    st.sidebar.markdown("---")

    st.sidebar.markdown("""
    <div style="text-align:center">

    <b>FraudGuard AI</b>

    <br>

    Version 2.0

    <br><br>

    Developed by

    <b>Srishti B.S.</b>

    <br>

    NVIDIA Data Science Internship

    </div>
    """, unsafe_allow_html=True)

    # Execute selected page logic
    pg.run()

if __name__ == "__main__":
    main()