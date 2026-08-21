"""
FraudGuard AI - Enterprise Credit Card Fraud Detection System
Module: predict.py
Author: Senior Python Developer / UI Designer
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from io import BytesIO


@st.cache_resource
def load_assets():
    """Load the trained model and scaler artifacts."""
    try:
        model = joblib.load("fraud_model.pkl")
        scaler = joblib.load("scaler.pkl")
        return model, scaler
    except Exception as e:
        st.error(f"Error loading model assets: {e}")
        return None, None

def create_gauge_chart(probability):
    """Create a professional Plotly gauge for fraud probability."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Fraud Probability (%)", 'font': {'size': 18, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#76B900" if probability < 0.5 else "#FF4B4B"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(118, 185, 0, 0.3)'},
                {'range': [30, 70], 'color': 'rgba(255, 165, 0, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(255, 75, 75, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': probability * 100
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig

def render_prediction():
    """Main UI for the Prediction Module."""
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; color: white; font-size: 28px;">AI Prediction Engine</h1>
            <p style="margin:0; color: #e0e0e0; opacity: 0.8;">Run real-time inference on banking transactions</p>
        </div>
    """, unsafe_allow_html=True)

    model, scaler = load_assets()
    if model is None or scaler is None:
        st.warning("Model or Scaler not found. Please ensure 'fraud_model.pkl' and 'scaler.pkl' exist.")
        return

    # 1. File Upload Section
    st.success("🟢 AI Prediction Engine Online")
    with st.container(border=True):
        st.subheader("📁 Upload Transaction Data")
        uploaded_file = st.file_uploader("Choose creditcard.csv", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # 2. Transaction Selection
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🔍 Select Transaction")
            selected_index = st.number_input(
                "Enter Transaction Index",
                min_value=0,
                max_value=len(df)-1,
                value=0,
                step=1
            )
            selected_index = int(selected_index)
            
            actual = "FRAUD" if df.iloc[selected_index]["Class"] == 1 else "SAFE"
            analyze_btn = st.button("🚀 Analyze Transaction", use_container_width=True)

        with col2:
            st.markdown("### 📑 Data Preview")
            st.dataframe(df.iloc[[selected_index]], use_container_width=True)

        # 3. Inference Logic
        if analyze_btn:
            # Prepare data (Drop 'Class' if it exists in the test row)
            features = df.drop(columns=['Class'], errors='ignore')
            row = features.iloc[[selected_index]].copy()
            
            # Scaling and Prediction
            # Scale ONLY the Amount column
            row["Amount"] = scaler.transform(row[["Amount"]])

            # Predict
            prob = model.predict_proba(row)[0][1]
            
            prediction = model.predict(row)[0]

            prediction = "FRAUD" if prediction == 1 else "SAFE"
            # Check whether the model predicted correctly
            prediction_status = "✅ Correct Prediction" if prediction == actual else "❌ Incorrect Prediction"
            confidence = prob if prob > 0.5 else (1 - prob)
            
            # Risk Assessment
            risk_level = "HIGH" if prob > 0.8 else ("MEDIUM" if prob > 0.3 else "LOW")
            risk_color = "#FF4B4B" if risk_level == "HIGH" else ("#FFA500" if risk_level == "MEDIUM" else "#76B900")
            
            recommendation = (
                "🚨 IMMEDIATE ACTION: Freeze account and contact customer." if risk_level == "HIGH" 
                else "⚠️ MONITOR: Flag for manual review." if risk_level == "MEDIUM"
                else "✅ APPROVED: Transaction matches legitimate patterns."
            )

            # 4. Results Display
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                st.plotly_chart(create_gauge_chart(prob), use_container_width=True)

            with res_col2:
                st.markdown(f"""
                <div class="glass-card">

                <h3 style="margin-top:0; color:white;">
                📋 Analysis Report
                </h3>

                <p style="color:white;">
                <b>Actual Transaction:</b>
                <span style="color:#4FC3F7; font-weight:bold;">     
                {actual}
                </span>
                </p>

                <p style="color:white;">
                <b>Model Prediction:</b>
                <span style="color:{risk_color}; font-weight:bold;">
                {prediction}
                </span>
                </p>

                <p style="color:white;">
                <b>Prediction Result:</b>
                {prediction_status}
                </p>

                <hr style="border-color:rgba(255,255,255,.15);">

                <p style="color:white;">
                <b>Confidence Score:</b>
                {confidence:.2%}
                </p>

                <p style="color:white;">
                <b>Fraud Probability:</b>
                {prob:.2%}
                </p>

                <p style="color:white;">
                <b>Risk Level:</b>
                <span style="color:{risk_color}; font-weight:bold;">
                {risk_level}
                </span>
                </p>

                <hr style="border-color:rgba(255,255,255,.15);">

                <p style="color:white;">
                <b>Recommendation</b>
                </p>

                <p style="color:white;">
                {recommendation}
                </p>

                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
                st.subheader("📄 Transaction Features Used for Prediction")
                st.dataframe(row, use_container_width=True)

            # 5. Export Functionality
            report_data = {
                "Transaction_ID": selected_index,
                "Prediction": prediction,
                "Probability": prob,
                "Risk_Level": risk_level,
                "Timestamp": pd.Timestamp.now()
            }
            report_df = pd.DataFrame([report_data])
            
            csv_report = report_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Download Prediction Report",
                data=csv_report,
                file_name=f"fraud_report_{selected_index}.csv",
                mime="text/csv",
                use_container_width=True
            )

    else:
        st.info("Please upload a CSV file to begin analysis.")

if __name__ == "__main__":
    render_prediction()