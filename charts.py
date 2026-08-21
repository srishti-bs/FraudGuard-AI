"""
FraudGuard AI - Enterprise Credit Card Fraud Detection System
Module: charts.py
Author: Senior Python Developer / Data Scientist / UI Designer
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_dataset

@st.cache_data
def load_analytics_data():
    """Optimized data loading for analytics module."""
    try:
        df = load_dataset()
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()

def render_analytics():
    """Renders the comprehensive Fraud Analytics Dashboard."""
    df = load_analytics_data()

    if df.empty:
        st.warning("No data available for analytics. Please check creditcard.csv.")
        return

    # --- HEADER ---
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; color: white; font-size: 32px;">📊 Fraud Analytics Dashboard</h1>
            <p style="margin:0; color: #e0e0e0; opacity: 0.8;">Visual insights into transaction behaviour and fraud patterns.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TOP METRICS ---
    total_tx = len(df)
    fraud_tx = df[df['Class'] == 1].shape[0]
    safe_tx = total_tx - fraud_tx
    fraud_rate = (fraud_tx / total_tx) * 100

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Transactions", f"{total_tx:,}")
    with m2:
        st.metric("Fraud Transactions", f"{fraud_tx:,}", delta=f"{fraud_rate:.4f}%", delta_color="inverse")
    with m3:
        st.metric("Safe Transactions", f"{safe_tx:,}")
    with m4:
        st.metric("Fraud Rate", f"{fraud_rate:.3f}%")

    st.markdown("---")

    # --- ROW 1: Donut & Bar Chart ---
    row1_col1, row1_col2 = st.columns([1, 1])

    with row1_col1:
        with st.container(border=True):
            st.subheader("Fraud vs Safe Distribution")
            pie_df = df.copy()
            pie_df["Status"] = pie_df["Class"].map({0: "Safe", 1: "Fraud"})

            fig_donut = px.pie(
                    pie_df,
                    names="Status",
                    hole=0.5,
                    color="Status",
                    color_discrete_map={
                        "Safe": "#76B900",
                        "Fraud": "#FF4B4B"
                    }
            )
            fig_donut.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350)
            st.plotly_chart(fig_donut, use_container_width=True)

    with row1_col2:
        with st.container(border=True):
            st.subheader("Top 20 Transaction Amounts")
            top_20_df = df.nlargest(20, 'Amount')
            fig_bar = px.bar(
                top_20_df, x=top_20_df.index.astype(str), y='Amount',
                color='Amount', color_continuous_scale='Viridis'
            )
            fig_bar.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350)
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- ROW 2: Histogram & Scatter ---
    row2_col1, row2_col2 = st.columns([1, 1])

    with row2_col1:
        with st.container(border=True):
            st.subheader("Distribution of Amounts")
            fig_hist = px.histogram(
                df, x="Amount", nbins=50, 
                color_discrete_sequence=['#76B900'], 
                log_y=True
            )
            fig_hist.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350)
            st.plotly_chart(fig_hist, use_container_width=True)

    with row2_col2:
        with st.container(border=True):
            st.subheader("Time vs Amount Analysis")
            fig_scatter = px.scatter(
                df.sample(n=min(5000, len(df))), x="Time", y="Amount", 
                color="Class", color_discrete_map={0: '#76B900', 1: '#FF4B4B'},
                opacity=0.6
            )
            fig_scatter.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350)
            st.plotly_chart(fig_scatter, use_container_width=True)

    # --- ROW 3: Box Plot & Line Chart ---
    row3_col1, row3_col2 = st.columns([1, 1])

    with row3_col1:
        with st.container(border=True):
            st.subheader("Transaction Amount by Class")
            fig_box = px.box(
                df, x="Class", y="Amount", color="Class",
                color_discrete_map={0: '#76B900', 1: '#FF4B4B'},
                points="outliers"
            )
            fig_box.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350, yaxis_type="log")
            st.plotly_chart(fig_box, use_container_width=True)

    with row3_col2:
        with st.container(border=True):
            st.subheader("Transaction Density over Time")
            # Aggregating count over time bins for line chart
            temp_df = df.copy()

            temp_df["Time_Bin"] = pd.cut(
            temp_df["Time"],
            bins=50,
            labels=False
        )

        time_trend = temp_df.groupby("Time_Bin").size().reset_index(name="Counts")
        fig_line = px.line(
                    time_trend, x='Time_Bin', y='Counts',
                    line_shape='spline', render_mode='svg'
                )   
        fig_line.update_traces(line_color='#76B900')
        fig_line.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=350)
        st.plotly_chart(fig_line, use_container_width=True)

    # --- ROW 4: Heatmap ---
    with st.container(border=True):
        st.subheader("Feature Correlation Matrix")
        corr_cols = ['Time', 'Amount', 'V1', 'V2', 'V3', 'V4', 'V5', 'Class']
        corr_matrix = df[corr_cols].corr()
        fig_heatmap = px.imshow(
            corr_matrix, text_auto=True, aspect="auto",
            color_continuous_scale='RdBu_r', origin='lower'
        )
        fig_heatmap.update_layout(template="plotly_dark", margin=dict(t=30, b=30, l=0, r=0), height=450)
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # --- BOTTOM: DATAFRAME ---
    st.markdown("### 📑 Latest 100 Transactions (Audit Log)")
    st.dataframe(
        df.tail(100).sort_index(ascending=False), 
        use_container_width=True,
        hide_index=True
    )

if __name__ == "__main__":
    render_analytics()