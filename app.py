from preferences import get_preferences
import streamlit as st
from pantry import get_current_ig, find_recipes
from substitution import substitution_page
from favorites import favorites_page
from welcome import welcome_page
from personal_recipes import personal_recipes_page

pages = ["Welcome", "Preferences", "Favorites", "Find a Recipe", "Substitutions", "My Cookbook"]

if 'page' not in st.session_state:
    st.session_state['page'] = 'Welcome'
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []
    
current_index = pages.index(st.session_state['page'])
st.sidebar.title("Find a Meal")
selection = st.sidebar.radio("Go to", pages, index=current_index)
st.session_state['page'] = selection
    
if st.session_state['page'] == 'Welcome':
    welcome_page()
elif st.session_state['page'] == 'Preferences':
    get_preferences()
elif st.session_state['page'] == 'Favorites':
    favorites_page()
elif st.session_state['page'] == 'Find a Recipe':
    get_current_ig()
    find_recipes()
elif st.session_state['page'] == 'Substitutions':
    substitution_page()
elif st.session_state['page'] == 'My Cookbook':
    personal_recipes_page()