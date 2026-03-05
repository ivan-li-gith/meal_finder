import streamlit as st

def display_header(recipe):
    st.image(recipe['image'], width='stretch')
    
    # list cuisine types
    cuisines = recipe.get('cuisines', [])
    if cuisines:
        st.write(f"Cuisine: {', '.join(cuisines)}")
    
    # list nutritional values
    nutrition = recipe.get('nutrition', {}).get('nutrients', [])
    if nutrition:
        with st.expander("Nutrition Facts"):
            for nutrient in nutrition:
                if nutrient['name'] in ['Calories', 'Fat', 'Carbohydrates', 'Protein']:
                    st.write(f"{nutrient['name']}: {nutrient['amount']}{nutrient['unit']}")

def display_details(recipe):
    st.write(f"{recipe['title']}")
    
    # cost of recipe
    price_per_serving = recipe.get('pricePerServing', 0) / 100
    servings = recipe.get('servings', 1)
    total_price = price_per_serving * servings
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
        
def display_instructions(recipe):
    instructions = recipe.get('analyzedInstructions')
    
    if instructions:
        with st.expander("View Cooking Steps"):
            for section in instructions:
                for step in section.get('steps', []):
                    st.write(f"Step {step['number']}: {step['step']}")
    else:
        st.write('Instructions unavailable. View link below.')
    
    st.markdown(f"View Full Recipe: {recipe.get('sourceUrl')}")
    
def display_all(recipes):
    for recipe in recipes:
        col1, col2 = st.columns([1,2])
        
        with col1:
            display_header(recipe)
        
        with col2:
            display_details(recipe)
            
            is_favorited = any(fav['id'] == recipe['id'] for fav in st.session_state['favorites'])
            
            if is_favorited:
                if st.button(f"❤️ Unfavorite", key=f"fav_{recipe['id']}"):
                    st.session_state['favorites'] = [fav for fav in st.session_state['favorites'] if fav['id'] != recipe['id']]
                    st.rerun()
            else:
                if st.button(f"🤍 Favorite", key=f"fav_{recipe['id']}"):
                    st.session_state['favorites'].append(recipe)
                    st.toast(f"Added {recipe['title']} to favorites!")

            display_instructions(recipe)
        
        st.divider()