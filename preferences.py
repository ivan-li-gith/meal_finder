import streamlit as st
from database import save_profile_to_db

def add_custom_pref(category, input_key):
    new_item = st.session_state[input_key].strip().title()
    
    if 'profile' not in st.session_state:
        st.session_state['profile'] = {"diet": [], "cuisines": [], "dislikes":[]}
        
    if new_item and new_item not in st.session_state['profile'][category]:
        st.session_state['profile'][category].append(new_item)
        
    st.session_state[input_key] = ""
    
def add_multi_pref(category, key):
    selected_items = st.session_state[key]
    
    if 'profile' not in st.session_state:
        st.session_state['profile'] = {"diet": [], "cuisines": [], "dislikes":[]}
        
    for item in selected_items:
        if item and item not in st.session_state['profile'][category]:
            st.session_state['profile'][category].append(item)
    
    st.session_state[key] = []
    
def display_preferences(category, column):
    items = st.session_state['profile'].get(category, [])
    
    if items:
        column.write(f"{category.title()}")
        
        for i, item in enumerate(items):
            sub_cols = column.columns([3, 1])
            sub_cols[0].markdown(f"{item}")
            
            if sub_cols[1].button("❌", key=f"del_{category}_{i}"):
                st.session_state['profile'][category].pop(i)
                st.rerun()

def get_preferences():
    st.title("Build Your Profile")
    
    if 'profile' not in st.session_state:
        st.session_state['profile'] = {"diet": [], "cuisines": [], "dislikes":[]}
    
    # display users current profile
    if any(st.session_state['profile'].values()):
        st.write("Your Current Preferences")
        col1, col2, col3 = st.columns(3)
        display_preferences("diet", col1)
        display_preferences("cuisines", col2)
        display_preferences("dislikes", col3)
        st.divider()
    
    st.subheader("Update Your Tastes")
    st.info("Choose from list or enter your own")

    # diet section
    diet_options = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"]
    st.multiselect("Do you have a specific diet?", 
                    diet_options, 
                    key="multi_diet",
                    on_change=add_multi_pref,
                    args=("diet", "multi_diet"))
    
    st.text_input("Enter diet if not listed:",
                  key="diet_input",
                  on_change=add_custom_pref,
                  args=("diet", "diet_input"))
    
    # cuisine section
    cuisine_options = ["Chinese", "Italian", "Mexican", "Japanese", "Indian", "American", "Thai", "Mediterranean", "Other"]
    st.multiselect("Which cuisines do you love?", 
                    cuisine_options, 
                    key="multi_cuisine",
                    on_change=add_multi_pref,
                    args=("cuisines", "multi_cuisine"))
    
    st.text_input("Enter a cuisine if not listed:",
                  key="cuisine_input",
                  on_change=add_custom_pref,
                  args=("cuisines", "cuisine_input"))
    
    # dislike section
    st.text_input("Enter anything you do not like to eat:",
                  key="dislikes_input",
                  on_change=add_custom_pref,
                  args=("dislikes", "dislikes_input"))

    st.divider()
    save()
    

def save():
    if st.button("Save Profile Settings"):
        save_profile_to_db(1, st.session_state['profile']) # Using 1 as a placeholder user_id
        st.success("Profile Saved to Database!")