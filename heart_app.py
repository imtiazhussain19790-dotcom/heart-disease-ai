import streamlit as st
import joblib
import numpy as np
from fpdf import FPDF

# 1. Page Config aur Language Selection
st.set_page_config(page_title="Heart AI", page_icon="❤️")

# Sidebar mein language ka option
lang = st.sidebar.selectbox("Select Language / زبان منتخب کریں", ["English", "Urdu"])

# Zubaan ke mutabiq alfaz ka chunao
if lang == "Urdu":
    # ... پرانا کوڈ یہاں رہے گا ...
    cp_label = "سینے میں درد کی قسم (0-3)"
    bp_label = "بلڈ پریشر (mm Hg)"
    chol_label = "کولیسٹرول (mg/dl)"
else:
    # ... پرانا کوڈ یہاں رہے گا ...
    cp_label = "Chest Pain Type (0-3)"
    bp_label = "Resting Blood Pressure"
    chol_label = "Serum Cholestrol"
# 2. Load Model
model = joblib.load('heart_model.pkl')

# 3. PDF Function
def create_pdf(age, sex, prediction, language):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    t = "Heart Disease Report" if language == "English" else "Dil ki Bimari ki Report"
    pdf.cell(200, 10, txt=t, ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {'Male' if sex==1 else 'Female'}", ln=True)
    res = "Risk Detected" if prediction == 1 else "Normal"
    pdf.cell(200, 10, txt=f"Result: {res}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# 4. UI Elements
st.title(title)
age = st.number_input(age_label, min_value=1, max_value=120, value=54)
sex = st.selectbox(sex_label, options=[1, 0], format_func=lambda x: 'Male' if x==1 else 'Female')
cp = st.selectbox(cp_label, options=[0, 1, 2, 3])
trestbps = st.number_input(bp_label, 80, 200, 131)
chol = st.number_input(chol_label, 100, 600, 246)
# 5. Prediction Logic
if st.button(predict_btn):input_data = np.array([[age, sex, cp, trestbps, chol, 0, 0, 150, 0, 1.0, 1, 0, 2]])
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.error(risk_msg)
    else:
        st.success(normal_msg)
    
    # PDF Button
    try:
        pdf_bytes = create_pdf(age, sex, prediction[0], lang)
        st.download_button(label=pdf_btn_label, 
                            data=pdf_bytes, 
                            file_name="heart_report.pdf", 
                            mime="application/pdf")
    except Exception as e:
        st.warning("Error generating PDF")
