import streamlit as st
import joblib
import numpy as np 
model=joblib.load('heart_model.pkl')
st.title('Heart Disease Prediction System')
st.write("Enter the patient's health metrics below to predict the risk of heart disease")
st.sidebar.header("Patient Data Input")
age = st.number_input("Age (in years)", min_value=1, max_value=120, value=54)
sex = st.selectbox("Sex", options=[1, 0], format_func=lambda x: 'Male' if x==1 else 'Female')
cp = st.selectbox("Chest Pain Type (0-3)", options=[0, 1, 2, 3])
trestbps = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 131)
chol = st.number_input("Serum Cholestrol (mg/dl)", 100, 600, 246)
if st.button("Predict")
input_data=np.array([[age,sex,cp,trestbps,chol,0,0,150,0,1.0,1,0,2]])
prediction=model.predict(input_data)
if prediction [0]==1:
        st.error("Warning:The Patient is likely to have heart disease. please consult the doctor.")
 else:
        st.success("Result: The patient is unlikely to have heart disease.")       
