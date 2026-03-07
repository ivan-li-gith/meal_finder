import streamlit as st
import requests
import os

API_KEY = os.environ.get("API_KEY")

def substitution_page():
    st.title("Ingredient Substitution")
    st.subheader("Missing something? Lets see if you have an alternative")
    
    ingredient = st.text_input(
        "Enter the ingredient you're missing:",
        placeholder="e.g. eggs, heavy cream"
    )
    
    if st.button("Find substitute"):
        if not ingredient:
            st.warning("Please enter an ingredient")
        else:
            with st.spinner(f"Finding an alternative for {ingredient}"):
                url = "https://api.spoonacular.com/food/ingredients/substitutes"
                params = {
                    "ingredientName": ingredient.lower(),
                    "apiKey": API_KEY
                }
                
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get('status') == "success":
                        st.success(f"Found {len(data['substitutes'])} substitutes for {ingredient}")
                        for item in data['substitutes']:
                            st.info(f"{item}")      
                    else:
                        st.error(f"Could not find any substitutes for {ingredient}")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    
                        