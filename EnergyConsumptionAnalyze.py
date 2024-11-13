import numpy as np
import streamlit as st
import pandas as pd
import tempfile

st.set_page_config(page_title="Engineering Student Calculator", layout="centered")
st.title("Engineering Student Calculator 📐")

st.markdown("""
<style>
    .main {background-color: #e8eff7;}  
    .stButton > button {color: white; background-color: #007BFF; font-size: 16px;} /* Botão com cor de destaque */
    .stRadio > label, .stNumberInput > label {color: #2C3E50; font-weight: bold; font-size: 20px;} /* Subtítulo em cor mais escura e tamanho maior */
    .css-10trblm p {color: #2C3E50; font-size: 20px; font-weight: bold;} /* Letras menores com cor e tamanho mais visíveis */
</style>
""", unsafe_allow_html=True)

weighted_option = st.radio("Do the grades have weights?", ("Yes", "No"))

num_grades = int(st.number_input("Enter the number of grades", min_value=1, step=1))

grades = []
weights = []

for i in range(num_grades):
    grade = st.number_input(f"Enter grade {i + 1}:", step=0.1)
    grades.append(grade)
    
    if weighted_option == "Yes":
        weight = st.number_input(f"Enter weight for grade {i + 1}:", min_value=0, max_value=10)
        weights.append(weight)

grades = np.array(grades)

average = None

if weighted_option == "Yes":
    weights = np.array(weights)
    total_weight = np.sum(weights)
    if total_weight > 0:
        average = np.sum(grades * weights) / total_weight
        st.write(f"**Weighted average of grades = {average:.2f}**")
    else:
        st.warning("The sum of weights is zero. Please enter valid weights.")
else:
    average = np.mean(grades)
    st.write(f"**Average of grades = {average:.2f}**")

if average is not None:
    if average >= 7:
        st.success("No final exam required, you already pass. Congratulations! 🎉")
    else:
        final_weight = 0.6  
        exam_weight = 0.4   
        required_exam_grade = (5 - average * final_weight) / exam_weight
        if required_exam_grade > 10:
            st.error("You already Fail, Study more next time! 📚")
        else:
            st.warning(f"You can pass if you get **{required_exam_grade:.2f}** or more in the final exam")

data = {
    "Grade": grades,
    "Weight": weights if weighted_option == "Yes" else ["N/A"] * num_grades,
    "Average": [average] * num_grades if average is not None else ["N/A"] * num_grades,
    "Required Exam Grade": [required_exam_grade if average is not None and average < 7 else "N/A"] * num_grades
}
df = pd.DataFrame(data)

with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
    df.to_excel(tmp_file.name, index=False)
    tmp_file_path = tmp_file.name

with open(tmp_file_path, "rb") as file:
    st.download_button(label="Download Excel File", data=file, file_name="Engineering_Student_Calculator_Results.xlsx")