import streamlit as st

def get_preferences():
    st.title("Build Your Profile")
    st.subheader("Help me narrow down what your preferences are")
    
    if 'dislikes_list' not in st.session_state:
        st.session_state['dislikes_list'] = []
        
    # diet section
    diet_options = ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Other"]
    user_diet = st.multiselect("Do you have a specific diet?", diet_options)
    final_diet = user_diet.copy()
    
    other_diet = st.text_input("Any other dietary restrictions not listed above?", placeholder="e.g., Dairy-free, Nut-free")
    if other_diet:
        if "Other" in final_diet:
            final_diet.remove("Other")
        final_diet.extend([d.strip() for d in other_diet.split(",") if d.strip()])

    # cuisine section
    cuisines = ["Italian", "Mexican", "Japanese", "Indian", "American", "Thai", "Mediterranean", "Other"]
    fav_cuisine = st.multiselect("Which cuisines do you love?", cuisines)
    final_cuisine = fav_cuisine.copy()
    
    other_cuisine = st.text_input("Any other cuisines you love?")
    if other_cuisine:
        if "Other" in final_cuisine:
            final_cuisine.remove("Other")
        final_cuisine.extend([c.strip() for c in other_cuisine.split(",") if c.strip()])
            
    st.divider()
    
    # dislike section
    
    dislikes = st.text_input("Any ingredient you do not like to eat? (comma seperated)", placeholder="e.g. Cilantro, Mushrooms, Olives")
    
    if st.button("Save my profile"):
        st.session_state['profile'] = {
            "diet": list(set(final_diet)),
            "cuisines": list(set(final_cuisine)),
            "dislikes": [i.strip() for i in dislikes.split(",") if i.strip()]
        }
        st.success("Profile Saved! Ready to check your pantry.")
        st.balloons()


    