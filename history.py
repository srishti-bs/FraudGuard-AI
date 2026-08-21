"""
FraudGuard AI
Transaction History Module
"""

import streamlit as st
import pandas as pd
from data_loader import load_dataset


@st.cache_data
def load_data():
    return load_dataset()

def render_history():

    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;color:white;">📜 Transaction History</h1>
        <p style="color:#dddddd;">
            Search, filter and inspect all recorded transactions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()

    st.markdown("## Filters")

    c1, c2, c3 = st.columns(3)

    with c1:
        status = st.selectbox(
            "Transaction Type",
            ["All", "Safe", "Fraud"]
        )

    with c2:
        min_amount = st.number_input(
            "Minimum Amount",
            value=0.0,
            step=10.0
        )

    with c3:
        search_time = st.text_input(
            "Search by Time"
        )

    filtered = df.copy()

    if status == "Fraud":
        filtered = filtered[filtered["Class"] == 1]

    elif status == "Safe":
        filtered = filtered[filtered["Class"] == 0]

    filtered = filtered[
        filtered["Amount"] >= min_amount
    ]

    if search_time:
        filtered = filtered[
            filtered["Time"]
            .astype(str)
            .str.contains(search_time)
        ]

    st.markdown("---")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Transactions",
            len(filtered)
        )

    with m2:
        st.metric(
            "Fraud Cases",
            filtered["Class"].sum()
        )

    with m3:
        st.metric(
            "Average Amount",
            f"${filtered['Amount'].mean():.2f}"
        )

    st.markdown("---")

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Filtered CSV",
        csv,
        file_name="transaction_history.csv",
        mime="text/csv"
    )

    st.markdown("## Transaction Records")

    st.dataframe(
        filtered.sort_values(
            by="Time",
            ascending=False
        ),
        use_container_width=True,
        height=600
    )


if __name__ == "__main__":
    render_history()