import streamlit as st

def welcome_page():
    st.title("Welcome to Find a Meal")
    st.markdown("""
    This application helps you reduce food waste and save money by finding recipes based on what you already have in your pantry.
    
    How to use:
    1. Set Your Profile: Tell us about your diet and favorite cuisines
    2. Check Your Pantry: Enter the ingredients you have on hand
    3. Discover Recipes: Get personalized, cost-effective meal suggestions
    4. Handle Substitutes: Missing an ingredient? Check the 'Substitutions' tool
    """)