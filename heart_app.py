import streamlit as st
import joblib
import numpy as np
from fpdf import FPDF
model = joblib.load("heart_model.pkl")


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Heart AI",
    page_icon="❤️"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("heart_model.pkl")

# ---------------- PDF FUNCTION ----------------
def create_pdf(age, sex, prediction):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Heart Disease Prediction Report", ln=True, align="C")
    pdf.ln(5)

    pdf.cell(0, 10, f"Age: {age}", ln=True)
    pdf.cell(0, 10, f"Sex: {sex}", ln=True)
    pdf.cell(0, 10, f"Prediction: {prediction}", ln=True)

    return pdf

