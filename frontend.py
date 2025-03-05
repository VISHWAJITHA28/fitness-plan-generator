import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Personalized Fitness Plan Generator")

# Sidebar - User Input
st.sidebar.header("User Information")
age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
goal = st.sidebar.selectbox("Fitness Goal", ["Lose Weight", "Gain Muscle", "Maintain Fitness"])
condition = st.sidebar.text_input("Health Conditions (if any)")

if st.sidebar.button("Generate Plan"):
    response = requests.get("http://127.0.0.1:5000/recommendations", params={
        "age": age, "gender": gender, "weight": weight, "goal": goal, "condition": condition
    })
    
    if response.status_code == 200:
        plan = response.json()
        st.subheader("Your Personalized Fitness Plan")
        st.write(plan["workout_plan"])
    else:
        st.error("Error fetching recommendations. Try again later.")

# Workout Tracking Placeholder
st.subheader("Workout Tracking")
st.write("Feature coming soon!")

# Meal Tracking Section
st.subheader("Meal Tracking")
food = st.text_input("Enter Food Item")
calories = st.number_input("Calories", min_value=0, max_value=2000, value=0)
protein = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, value=0.0)
carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, value=0.0)
fats = st.number_input("Fats (g)", min_value=0.0, max_value=100.0, value=0.0)

if st.button("Log Meal"):
    meal_response = requests.post("http://127.0.0.1:5000/log_meal", json={
        "user": "John", "food": food, "calories": calories, "protein": protein, "carbs": carbs, "fats": fats
    })
    
    if meal_response.status_code == 200:
        st.success("Meal logged successfully!")
    else:
        st.error("Error logging meal.")

if st.button("View Meal History"):
    meal_history = requests.get("http://127.0.0.1:5000/get_meals", params={"user": "John"})
    
    if meal_history.status_code == 200:
        meals = meal_history.json()["meals"]
        st.subheader("Meal History")
        df = pd.DataFrame(meals, columns=["ID", "User", "Food", "Calories", "Protein", "Carbs", "Fats"])
        st.dataframe(df[["Food", "Calories", "Protein", "Carbs", "Fats"]])
        
        # Visualization
        st.subheader("Nutrient Breakdown")
        fig, ax = plt.subplots()
        df[["Calories", "Protein", "Carbs", "Fats"]].sum().plot(kind="bar", ax=ax)
        st.pyplot(fig)
    else:
        st.error("Error fetching meal history.")

# Weight Logging Form
st.subheader("Log Your Weight")
user_id = st.number_input("User ID", min_value=1, step=1)
user_weight = st.number_input("Enter your weight (kg)", min_value=0.0, step=0.1)

if st.button("Log Weight"):
    response = requests.post("http://127.0.0.1:5000/log_weight", json={"user_id": user_id, "weight": user_weight})
    if response.status_code == 200:
        st.success("Weight logged successfully!")
    else:
        st.error("Failed to log weight.")

# Fetch and Display Weight History
st.subheader("Weight History")
if st.button("Show Weight History"):
    response = requests.get(f"http://127.0.0.1:5000/get_weight?user_id={user_id}")
    if response.status_code == 200:
        weight_data = response.json().get("weight_data", [])
        if weight_data:
            st.write("Your Weight Records:")
            for entry in weight_data:
                st.write(f"📅 {entry[0]} - ⚖️ {entry[1]} kg")
        else:
            st.warning("No weight data found.")
    else:
        st.error("Failed to fetch weight history.")

# Fetch Fitbit Data
if st.sidebar.button("Fetch Fitbit Data"):
    fitbit_response = requests.get("http://127.0.0.1:5000/get_fitbit_data")
    
    if fitbit_response.status_code == 200:
        fitbit_data = fitbit_response.json()
        st.subheader("Your Fitbit Data")
        st.write(f"Steps: {fitbit_data['steps']}")
        st.write(f"Calories Burned: {fitbit_data['calories_burned']}")
    else:
        st.error("Error fetching Fitbit data. Make sure your Fitbit is connected.")
