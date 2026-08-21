import streamlit as st


def render_about():

    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0;color:white;">
        ℹ️ About FraudGuard AI
        </h1>
        <div style="color:#d6d6d6; margin-top:10px;">
        Enterprise Credit Card Fraud Detection System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Project Overview")

    st.write("""
FraudGuard AI is an intelligent fraud detection system developed for
credit card transaction analysis using Machine Learning.

The application predicts fraudulent transactions in real time,
provides advanced analytics dashboards,
maintains transaction history,
and generates professional reports.
""")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Technologies Used")

        st.markdown("""
- Python
- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- Plotly
- Joblib
""")

    with c2:
        st.subheader("Machine Learning")

        st.markdown("""
- Random Forest Classifier
- Feature Scaling
- Fraud Classification
- Real-time Prediction
""")

    st.markdown("---")

    st.subheader("Project Features")

    st.markdown("""
✅ Fraud Prediction

✅ Analytics Dashboard

✅ Transaction History

✅ Professional Reports

✅ Interactive Visualizations

✅ Enterprise UI
""")

    st.markdown("---")

    st.success("""
Developer

Srishti B.S.

B.Tech Computer Science Engineering
(Data Science)

FraudGuard AI
Version 1.0
""")