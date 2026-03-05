import streamlit as st

def get_sidebar_filters():
    st.sidebar.header("Search Filters")
    filters = st.sidebar.selectbox(
        "Sort By:",
        ["Maximize Used Ingredients", "Minimize Missing Ingredients"]
    )
    
    # setting this to a max of 20 cuz api limit
    num_recipes = st.sidebar.slider("Number of Recipes", 1, 20, 5)
    num_cals = st.sidebar.slider("Max Calories Per Serving", 100, 2000, 800, step=50)
    
    return filters, num_recipes, num_cals