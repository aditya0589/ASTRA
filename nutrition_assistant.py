import streamlit as st

def show_nutrition_assistant():
    st.title("Nutrition Assistant")
    food_input = st.text_input("Enter a food item or a meal description")
    if st.button("Get Nutrition Info"):
        st.success(f"Fetching nutrition info for: {food_input} (Nutrition logic to be added.)")
