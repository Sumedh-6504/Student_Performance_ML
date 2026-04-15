import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Student Math Score Predictor", page_icon="🎓", layout="wide")


# 2. Load the Production Model
@st.cache_resource  # This ensures the model is only loaded once, making the app super fast!
def load_model():
    return joblib.load('models/student_math_model.pkl')


model = load_model()

# 3. App Header
st.title("🎓 Student Math Performance Predictor")
st.markdown("""
This application uses a highly optimized **Gradient Boosting Machine Learning pipeline** 
to predict a student's Math Score based on their demographics and other test scores.
""")
st.divider()

# 4. User Inputs (Creating a beautiful form)
st.sidebar.header("📝 Student Profile")
st.sidebar.markdown("Enter the student's details below:")

# Categorical Inputs
gender = st.sidebar.radio("Gender", ["male", "female"])
race_ethnicity = st.sidebar.selectbox("Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"])
parental_education = st.sidebar.selectbox("Parental Level of Education",
                                          ["some high school", "high school", "some college",
                                           "associate's degree", "bachelor's degree", "master's degree"])
lunch = st.sidebar.radio("Lunch Type", ["standard", "free/reduced"])
test_prep = st.sidebar.radio("Test Preparation Course", ["none", "completed"])

# Numerical Inputs
st.sidebar.divider()
st.sidebar.header("📊 Current Academic Scores")
reading_score = st.sidebar.slider("Reading Score", min_value=0, max_value=100, value=65)
writing_score = st.sidebar.slider("Writing Score", min_value=0, max_value=100, value=65)

# 5. Prediction Logic
if st.button("🚀 Predict Math Score", use_container_width=True):
    # Create a DataFrame from the user inputs
    input_data = pd.DataFrame({
        'gender': [gender],
        'race/ethnicity': [race_ethnicity],
        'parental level of education': [parental_education],
        'lunch': [lunch],
        'test preparation course': [test_prep],
        'reading score': [reading_score],
        'writing score': [writing_score]
    })

    # Predict using the Pipeline
    prediction = model.predict(input_data)[0]

    # 6. Display the Results beautifully
    st.subheader("🎯 Prediction Result")

    # Display columns for layout
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Predicted Math Score", value=f"{prediction:.1f} / 100")

    with col2:
        if prediction >= 60:
            st.success("✅ Prediction: This student is likely to PASS.")
            st.balloons()
        else:
            st.error("⚠️ Prediction: This student is at risk of FAILING (Score < 60).")

    # Business insight dynamically generated
    st.info(
        f"**Insight:** With a Reading score of {reading_score} and a Writing score of {writing_score}, the model evaluates their systemic academic foundation. Try changing the 'Test Preparation Course' to see how much it impacts the predicted grade!")