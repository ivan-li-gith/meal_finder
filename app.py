from preferences import get_preferences
import streamlit as st
from pantry import get_current_ig, find_recipes
from substitution import substitution_page
from favorites import favorites_page
from welcome import welcome_page
from personal_recipes import personal_recipes_page
from database import init_db, load_user_data

pages = ["Welcome", "Preferences", "Favorites", "Find a Recipe", "Substitutions", "My Cookbook"]



if 'init_db' not in st.session_state:
    init_db()
    saved_data = load_user_data(1)
    st.session_state['profile'] = saved_data['profile']
    st.session_state['favorites'] = saved_data['favorites']
    st.session_state['personal_recipes'] = saved_data['personal']
    st.session_state['init_db'] = True

if 'page' not in st.session_state:
    st.session_state['page'] = 'Welcome'
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = []
    
st.sidebar.title("Find a Meal")

current_index = pages.index(st.session_state['page'])
selection = st.sidebar.radio(
    "Go to", 
    pages, 
    index=current_index,
    key="nav_selection"
)

if selection != st.session_state['page']:
    st.session_state['page'] = selection
    st.rerun()
        
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