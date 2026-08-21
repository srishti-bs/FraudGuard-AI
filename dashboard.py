"""
FraudGuard AI - Enterprise Credit Card Fraud Detection System
Module: dashboard.py
Author: Senior Python Developer / UI Designer
"""

import streamlit as st
import pandas as pd
from data_loader import load_dataset


@st.cache_data
def load_dashboard_data():
    """Load the dataset for dashboard metrics."""
    try:
        df = load_dataset()
        return df
    except FileNotFoundError:
        st.error("Error: 'creditcard.csv' not found. Please ensure the dataset is in the root directory.")
        return pd.DataFrame()

def render_kpi_cards(df):
    """Render top-level KPI metrics using glassmorphism styling."""
    total_tx = len(df)
    fraud_tx = len(df[df['Class'] == 1])
    safe_tx = len(df[df['Class'] == 0])
    fraud_rate = (fraud_tx / total_tx) * 100
    avg_amount = df['Amount'].mean()

    # Layout: 5 Columns for KPIs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: #888; font-size: 14px; margin-bottom: 5px;">💳 Total Transactions</p>
                <h2 style="margin: 0;">{total_tx:,}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: #76B900; font-size: 14px; margin-bottom: 5px;">✅ Safe Transactions</p>
                <h2 style="margin: 0;">{safe_tx:,}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: #FF4B4B; font-size: 14px; margin-bottom: 5px;">🚨 Fraud Cases</p>
                <h2 style="margin: 0;">{fraud_tx:,}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: #888; font-size: 14px; margin-bottom: 5px;">📉 Fraud Rate</p>
                <h2 style="margin: 0;">{fraud_rate:.3f}%</h2>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
            <div class="glass-card">
                <p style="color: #888; font-size: 14px; margin-bottom: 5px;">💰 Avg. Amount</p>
                <h2 style="margin: 0;">${avg_amount:.2f}</h2>
            </div>
        """, unsafe_allow_html=True)

def render_dashboard():
    """Main function to render the Dashboard UI."""
    df = load_dashboard_data()
    
    if df.empty:
        return

    # Header Section
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; color: white; font-size: 28px;">Financial Overview Dashboard</h1>
            <p style="margin:0; color: #e0e0e0; opacity: 0.8;">Real-time fraud monitoring and transaction analytics</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. KPI Metrics
    st.success("🟢 Fraud Detection System Operational")
    st.markdown("---")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Alerts and Recent Activity Section
    col_left, col_right = st.columns([1, 1])

    with col_left:
        with st.container(border=True):
            st.markdown("### 🚨 Recent Fraud Alerts")
            fraud_df = df[df['Class'] == 1].tail(7)[['Time', 'Amount', 'Class']]
            # Reverse for latest first
            st.dataframe(
                fraud_df.iloc[::-1], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Amount": st.column_config.NumberColumn(format="$%.2f"),
                    "Class": st.column_config.TextColumn(label="Status", default="🚩 FRAUD")
                }
            )

    with col_right:
        with st.container(border=True):
            st.markdown("### ✅ Recent Safe Transactions")
            safe_df = df[df['Class'] == 0].tail(7)[['Time', 'Amount', 'Class']]
            st.dataframe(
                safe_df.iloc[::-1], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Amount": st.column_config.NumberColumn(format="$%.2f"),
                    "Class": st.column_config.TextColumn(label="Status", default="✅ CLEAR")
                }
            )

    # 3. Comprehensive History Table
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 📜 All Recent Transactions")
        # Displaying a mix of latest records
        recent_all = df.tail(15)[['Time', 'V1', 'V2', 'Amount', 'Class']]
        st.dataframe(
            recent_all.iloc[::-1],
            use_container_width=True,
            hide_index=True
        )

    # 4. Footer analytics hint
    st.caption("Data source: creditcard.csv | Last updated: Live Dashboard")

if __name__ == "__main__":
    # For testing isolation
    render_dashboard()