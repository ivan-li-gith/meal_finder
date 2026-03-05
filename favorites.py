import streamlit as st
from display_recipe import display_all

def favorites_page():
    st.title("Favorite Recipes")
    
    if 'favorites' not in st.session_state or not st.session_state['favorites']:
        st.info("You have not saved any recipes yet")
    else:
        st.write(f"Favorite Recipes")
        
        st.divider()
        display_all(st.session_state['favorites'])