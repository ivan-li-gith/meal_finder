from preferences import get_preferences
import streamlit as st
from pantry import get_pantry_recipes
from substitution import substitution_page

if 'page' not in st.session_state:
    st.session_state['page'] = 'Preferences'
    
st.sidebar.title("Meal Optimizer")
selection = st.sidebar.radio("Go to", ["Preferences", "My Pantry", "Substitutions"])

st.session_state['page'] = selection
    
if st.session_state['page'] == 'Preferences':
    get_preferences()
elif st.session_state['page'] == 'My Pantry':
    get_pantry_recipes()
elif st.session_state['page'] == 'Substitutions':
    substitution_page()