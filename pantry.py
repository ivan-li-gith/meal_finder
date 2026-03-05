import streamlit as st
import requests

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

def fetch_recipes(ingredients, api_key, sort_pref, num_recipies, max_calories):
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
        "maxCalories": max_calories,
        "number": num_recipies,
        "fillIngredients": True,
        "addRecipeInformation": True,
        "addRecipeInformation": True,
        "instructionsRequired": True,
        "sort": sort.get(sort_pref),
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

def get_pantry_recipes():
    st.title("What's in your pantry?")
    
    st.sidebar.header("Search Filters")
    sort_option = st.sidebar.selectbox(
        "Sort By:",
        ["Maximize Used Ingredients", "Minimize Missing Ingredients"]
    )
    max_recipes = st.sidebar.slider("Number of Recipes", 1, 20, 5)
    
    max_cals = st.sidebar.slider("Max Calories Per Serving", 100, 2000, 800, step=50)
    
    if 'profile' in st.session_state:
        st.sidebar.success("Profile Preferences Applied")
    else:
        st.sidebar.info("Set Preferences in Profile Tab")
        
    if 'ingredients_list' not in st.session_state:
        st.session_state['ingredients_list'] = []

    st.text_input(
        "Type an ingredient and press Enter:", 
        key="new_ingredient_input",
        placeholder="e.g., spinach, eggs, pasta",
        on_change=add_ingredient
    )
    
    if st.session_state['ingredients_list']:
        st.write("Your Current Pantry:")
        
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
        
    if st.button("Find Recipes"):
        if not DEFAULT_API_KEY:
            st.warning("Please enter your API key.")
        elif len(st.session_state['ingredients_list']) < 2:
            st.warning("Add at least 2 ingredients!")
        else:
            with st.spinner("Searching Spoonacular..."):
                recipes = fetch_recipes(
                    st.session_state['ingredients_list'], 
                    DEFAULT_API_KEY, 
                    sort_option, 
                    max_recipes,
                    max_cals
                )
                
                if recipes:
                    display_recipe_results(recipes)
                else:
                    st.info("No recipes found. Try adding different ingredients.")

def display_recipe_results(recipes):
    for recipe in recipes:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(recipe['image'], width="stretch")
            
            # cuisine type
            cuisine_type = recipe.get('cuisines', [])
            if cuisine_type:
                st.write(f"Cuisine: {', '.join(cuisine_type)}")
                
            # nutritional value
            nutrition = recipe.get('nutrition', {}).get('nutrients', [])
            if nutrition:
                st.markdown("Nutrition per Serving")
                
                for nutrient in nutrition:
                    if nutrient['name'] in ['Calories', 'Fat', 'Carbohydrates', 'Protein']:
                        st.write(f"{nutrient['name']}: {nutrient['amount']}{nutrient['unit']}")
            
        with col2:
            st.write(f"{recipe['title']}")
            
            price_per_serving = recipe.get('pricePerServing', 0) / 100
            servings = recipe.get('servings', 1)
            total_price = price_per_serving * servings
            st.write(f"Estimated Cost per Serving: ${price_per_serving:.2f}")
            st.write(f"Estimated Total Cost: {total_price:.2f}")

            missing_ig_count = len(recipe.get('missedIngredients', []))
            
            st.write(f"Ready in: {recipe.get('readyInMinutes')} mins")
            st.write(f"Missing Ingredient Count: {missing_ig_count}")
            
            used_ig = [ig['name'] for ig in recipe.get('usedIngredients', [])]
            missing_ig = [ig['name'] for ig in recipe.get('missedIngredients', [])]
            
            if used_ig:
                st.success(f"Have: {', '.join(used_ig)}")
                
            if missing_ig:
                st.error(f"Need: {', '.join(missing_ig)}")
                
            instrutions = recipe.get('analyzedInstructions')
            if instrutions:
                with st.expander("View Cooking Steps"):
                    for section in instrutions:
                        for step in section.get('steps', []):
                            st.write(f"Step {step['number']}: {step['step']}")
            else:
                st.write("Unable to load instructions. View the link below.")
                
                
            st.markdown(f"View Full Recipe: {recipe.get('sourceUrl')}")
        st.divider()    