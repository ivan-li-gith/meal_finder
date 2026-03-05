import streamlit as st
import requests
from filters import get_sidebar_filters
from display_recipe import display_all

DEFAULT_API_KEY = '3e40aacc93d64904b28abb657531f31b'

def add_ingredient():
    new_ingredient = st.session_state.new_ingredient_input.strip().lower()
    
    if 'ingredients_list' not in st.session_state:
        st.session_state['ingredients_list'] = []
        
    if new_ingredient and new_ingredient not in st.session_state['ingredients_list']:
        st.session_state['ingredients_list'].append(new_ingredient)
    
    st.session_state.new_ingredient_input = ""
    
def remove_ingredient(index):
    st.session_state['ingredients_list'].pop(index)

def get_current_ig():
    st.title("What's in your pantry?")
    
    if 'profile' in st.session_state:
        st.sidebar.success("Profile Preferences Applied")

    if 'ingredients_list' not in st.session_state:
        st.session_state['ingredients_list'] = []

    st.text_input(
        "Type an ingredient and press Enter:", 
        key="new_ingredient_input",
        placeholder="e.g., spinach, eggs, pasta",
        on_change=add_ingredient
    )
    
    if st.session_state['ingredients_list']:
        st.write("Your Current Ingredients:")
        for i, item in enumerate(st.session_state['ingredients_list']):
            cols = st.columns([4, 1])
            cols[0].markdown(f"- `{item}`")
            
            if cols[1].button("❌", key=f"remove_{i}"):
                remove_ingredient(i)
                st.rerun()
        
        if st.button("Clear All Ingredients"):
            st.session_state['ingredients_list'] = []
            st.rerun()
    
    st.divider()
    
def fetch_from_api(ingredients, api_key, filters, num_recipes, num_cal):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    
    # grab user data if it exists otherwise leave as empty
    user_profile = st.session_state.get('profile', {})
    user_diet = ",".join(user_profile.get('diet', []))
    user_cuisines = ",".join(user_profile.get('cuisines', []))
    user_dislikes = ",".join(user_profile.get('dislikes', []))
    
    sort = {
        "Minimize Missing Ingredients": "min-missing-ingredients",
        "Maximize Used Ingredients": "max-used-ingredients",
    }
    
    params = {
        "apiKey": api_key,
        "includeIngredients": ",".join(ingredients),
        "excludeIngredients": user_dislikes,
        "diet": user_diet,
        "cuisine": user_cuisines,
        "maxCalories": num_cal,
        "number": num_recipes,
        "fillIngredients": True,
        "addRecipeInformation": True,
        "addRecipeInformation": True,
        "instructionsRequired": True,
        "sort": sort.get(filters),
        "ranking": 1,
        "ignorePantry": True
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def find_recipes():
    filters, num_recipes, num_cals = get_sidebar_filters()

    if st.button("Find Recipes"):
        if len(st.session_state['ingredients_list']) < 2:
            st.warning("Add at least 2 ingredients!")
        else:
            with st.spinner("Searching for recipes..."):
                recipes = fetch_from_api(
                    st.session_state['ingredients_list'], 
                    DEFAULT_API_KEY, 
                    filters, 
                    num_recipes,
                    num_cals
                )
                
                if recipes:
                    display_all(recipes)
                else:
                    st.info("No recipes found. Try adding different ingredients.")

