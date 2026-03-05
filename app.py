from preferences import get_preferences
import streamlit as st
from pantry import get_current_ig, find_recipes
from substitution import substitution_page
from favorites import favorites_page

if 'page' not in st.session_state:
    st.session_state['page'] = 'Preferences'
    
st.sidebar.title("Meal Optimizer")
selection = st.sidebar.radio("Go to", ["Preferences", "Find a Recipe", "Substitutions", "Favorites"])

st.session_state['page'] = selection
    
if st.session_state['page'] == 'Preferences':
    get_preferences()
elif st.session_state['page'] == 'Find a Recipe':
    get_current_ig()
    find_recipes()
elif st.session_state['page'] == 'Substitutions':
    substitution_page()
elif st.session_state['page'] == 'Favorites':
    favorites_page()