import streamlit as st
from display_recipe import display_all
from database import add_fav_to_db

def personal_recipes_page():
    st.title("My Cookbook")
    st.subheader("Add your own recipes here")
    
    if 'personal_recipes' not in st.session_state:
        st.session_state['personal_recipes'] = []
        
    with st.expander("+ Add a new recipe"):
        with st.form("new_recipe_form", clear_on_submit=True):
            title = st.text_input("Recipe Name")
            cuisine = st.text_input("Cuisine Type")
            prep_time = st.number_input("Ready in (mins)", min_value=1, value=30)
            ingredients = st.text_area("Ingredients")
            instructions = st.text_area("Cooking Steps")
            
            submit = st.form_submit_button("Save Recipe")
            
            if submit:
                if title and ingredients and instructions:
                    new_recipe = {
                        "id": f"personal_recipe_{len(st.session_state['personal_recipes'])}",
                        "title": title,
                        "cuisines": [cuisine] if cuisine else [""],
                        "readyInMinutes": prep_time,
                        "usedIngredients": [{"name": i.strip()} for i in ingredients.split('\n') if i.strip()],
                        "analyzedInstructions": [{"steps": [{"number": idx+1, "step": s.strip()} 
                                                  for idx, s in enumerate(instructions.split('\n')) if s.strip()]}],
                        "sourceUrl": "#",
                        "image": "https://placehold.co/600x400?text=No+Image+Available"
                    }
                    
                    add_fav_to_db(1, new_recipe, is_personal=True)
                    st.session_state['personal_recipes'].append(new_recipe)
                    st.success(f"Added {title} to cookbook")
                    st.rerun()
                else:
                    st.error("Please provide title, ingredients, and instructions")
                    
    if not st.session_state['personal_recipes']:
        st.info("Your cookbook is empty. Add your first recipe")
    else:
        st.divider()
        display_all(st.session_state['personal_recipes'])