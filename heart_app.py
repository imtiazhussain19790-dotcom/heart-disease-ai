import streamlit as st
import joblib
import numpy as np
from fpdf import FPDF

# 1. Page Config aur Language Selection
st.set_page_config(page_title="Heart AI", page_icon="❤️")
lang = st.sidebar.selectbox("Select Language / زبان منتخب کریں", ["English", "Urdu"])

# Zubaan ke mutabiq labels
if lang == "Urdu":
    title = "دل کی بیماری کی تشخیص کا نظام"
    labels = {
        "age": "عمر (سالوں میں)",
        "sex": "جنس",
        "cp": "سینے میں درد کی قسم (0-3)",
        "bp": "بلڈ پریشر (Resting BP)",
        "chol": "کولیسٹرول (Serum Cholestrol)",
        "btn": "تشخیص کریں",
        "risk": "انتباہ: مریض میں دل کی بیماری کا خطرہ پایا گیا ہے۔",
        "normal": "نتیجہ: مریض میں دل کی بیماری کا کوئی خطرہ نہیں پایا گیا۔",
        "pdf": "رپورٹ ڈاؤن لوڈ کریں (PDF)"
    }
else:
    title = "Heart Disease Prediction System"
    labels = {
        "age": "Age (in years)",
        "sex": "Sex (Male=1, Female=0)",
        "cp": "Chest Pain Type (0-3)",
        "bp": "Resting Blood Pressure (mm Hg)",
        "chol": "Serum Cholestrol (mg/dl)",
        "btn": "Predict",
        "risk": "Warning: The Patient is likely to have heart disease.",
        "normal": "Result: The patient is unlikely to have heart disease.",
        "pdf": "Download Report (PDF)"
    }

# 2. Load Model
model = joblib.load('heart_model.pkl')

# 3. PDF Function
def create_pdf(data, prediction, language):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Heart Disease Diagnostic Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    res = "Risk Detected" if prediction == 1 else "Normal"
    pdf.cell(200, 10, txt=f"Final Prediction: {res}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 4. UI Design
st.title(title)
age = st.number_input(labels["age"], 1, 120, 54)
sex = st.selectbox(labels["sex"], options=[1, 0], format_func=lambda x: 'Male' if x==1 else 'Female')
cp = st.selectbox(labels["cp"], options=[0, 1, 2, 3])
trestbps = st.number_input(labels["bp"], 80, 200, 131)
chol = st.number_input(labels["chol"], 100, 600, 246)

# 5. Prediction Logic
if st.button(labels["btn"]):
    # Model ko saara data bhejna (All 13 features with defaults for rest)
    input_data = np.array([[age, sex, cp, trestbps, chol, 0, 0, 150, 0, 1.0, 1, 0, 2]])
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error(labels["risk"])
    else:
        st.success(labels["normal"])
    
    # PDF Download
    patient_info = {"Age": age, "Sex": sex, "Chest Pain": cp, "Blood Pressure": trestbps, "Cholesterol": chol}
    pdf_bytes = create_pdf(patient_info, prediction[0], lang)
    st.download_button(label=labels["pdf"], data=pdf_bytes, file_name="report.pdf", mime="application/pdf")
