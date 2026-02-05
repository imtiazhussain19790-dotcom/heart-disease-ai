import streamlit as st
import joblib
import numpy as np
from fpdf import FPDF
# ایپ کی ظاہری شکل بہتر بنائیں
st.set_page_config(page_title="Heart AI", page_icon="❤️", layout="centered")

# اسٹائلنگ کے لیے کچھ کسٹم میسجز
# اسٹائلنگ کے لیے کسٹم کوڈ
st.markdown("""<style>
    main {background-color: #f0f2f6;}
    </style>
    """, unsafe_allow_html=True)
    .main) {background-color: #f0f2f6;}
    </style>
    """, unsafe_allow_html=True)
# 1. Load your saved model
model = joblib.load('heart_model.pkl')

# 2. PDF Creation Function
def create_pdf(age, sex, prediction):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Heart Disease Diagnostic Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Patient Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {'Male' if sex==1 else 'Female'}", ln=True)
    result_text = "Positive (Risk Detected)" if prediction == 1 else "Negative (Normal)"
    pdf.cell(200, 10, txt=f"Final Result: {result_text}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 3. App UI Design
st.title("Heart Disease Prediction System")
st.write("Enter the patient's health metrics below to predict the risk of heart disease.")

# Input fields (Only once)
age = st.number_input("Age (in years)", min_value=1, max_value=120, value=54)
sex = st.selectbox("Sex", options=[1, 0], format_func=lambda x: 'Male' if x==1 else 'Female')
cp = st.selectbox("Chest Pain Type (0-3)", options=[0, 1, 2, 3])
trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 131)
chol = st.number_input("Serum Cholestrol (mg/dl)", 100, 600, 246)

# 4. Prediction Logic
if st.button("Predict"):
    input_data = np.array([[age, sex, cp, trestbps, chol, 0, 0, 150, 0, 1.0, 1, 0, 2]])
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error("Warning: The Patient is likely to have heart disease.")
    else:
        st.success("Result: The patient is unlikely to have heart disease.")
    
    # Generate and Download PDF Report
    try:
        pdf_bytes = create_pdf(age, sex, prediction[0])
        st.download_button(label="📥 Download Report (PDF)", 
                            data=pdf_bytes, 
                            file_name="heart_report.pdf", 
                            mime="application/pdf")
    except Exception as e:
        st.warning("PDF could not be generated. Please ensure 'fpdf' is in requirements.txt")
