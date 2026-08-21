"""
FraudGuard AI
Reports Module
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from data_loader import load_dataset


@st.cache_data
def load_data():
    return load_dataset()


def render_reports():

    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;color:white;">
            📄 Fraud Detection Reports
        </h1>
        <div style="color:#d6d6d6; margin-top:10px;">
        Executive Summary & Download Center
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Executive Summary & Download Center")

    df = load_data()

    total = len(df)
    fraud = int(df["Class"].sum())
    safe = total - fraud
    fraud_rate = fraud / total * 100

    amount = df["Amount"].sum()
    avg = df["Amount"].mean()
    maximum = df["Amount"].max()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Transactions", f"{total:,}")

    with c2:
        st.metric("Fraud Cases", fraud)

    with c3:
        st.metric("Safe Transactions", safe)

    with c4:
        st.metric("Fraud Rate", f"{fraud_rate:.3f}%")

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.subheader("Financial Statistics")

        st.info(f"""
**Total Transaction Volume**

${amount:,.2f}

---

**Average Transaction**

${avg:.2f}

---

**Highest Transaction**

${maximum:.2f}
""")

    with right:

        st.subheader("Executive Summary")

        st.success(f"""
✔ Dataset contains **{total:,}** transactions.

✔ Fraud detected:

**{fraud}**

✔ Fraud percentage:

**{fraud_rate:.3f}%**

✔ Safe transactions:

**{safe:,}**
""")

    st.markdown("---")

    st.subheader("Download Dataset")

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        "Fraud_Report.csv",
        "text/csv"
    )

    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    st.download_button(
        "⬇ Download Excel Report",
        excel_buffer.getvalue(),
        "Fraud_Report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")

    st.subheader("Report Preview")

    st.dataframe(
        df.head(50),
        use_container_width=True
    )


if __name__ == "__main__":
    render_reports()