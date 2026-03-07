# Find a Meal

A web application designed to reduce food waste by discovering recipes based on real-time pantry inventory.

## Live Demo
Access the application here: [Find a Meal](http://18.119.17.127/)

## Key Features
* **Pantry-Based Discovery:** Search for recipes using specific ingredients on hand.
* **Intelligent Filtering:** Apply custom dietary restrictions (Vegan, Keto, etc.), cuisine preferences, and caloric limits.
* **Persistent User Profiles:** Save tastes and dislikes to a cloud database to customize future search results.
* **Personal Cookbook:** Create and manage custom recipes.
* **Ingredient Substitutions:** Access a tool to find alternatives for missing ingredients.

## Tech Stack
* **Frontend:** Streamlit
* **Database:** MySQL hosted on AWS RDS
* **Infrastructure:** Deployed on AWS EC2
* **API:** Spoonacular REST API

## How to Use
1.  **Build Your Taste Profile**: Navigate to the **'Preferences'** page from the sidebar. Here, you can select dietary restrictions (e.g., Vegetarian, Keto) and favorite cuisines.
2.  **Inventory Your Pantry**: Go to the **'Find a Recipe'** tab and begin typing ingredients you currently have in your kitchen (e.g., "chicken," "spinach," "eggs").
3.  **Discover Recipes**: Configure your search filters in the sidebar and click **Find Recipes**.
4.  **Manage Your Cookbook**: Click the **'Favorite'** heart on any recipe to save it.
5.  **Handle Missing Ingredient**: If you're missing one item, visit the **'Substitutions'** page. Enter the missing ingredient to get a list of common alternatives to save a trip to the store.
6.  **Enter Your Own Recipes**: Go to **My Cookbook** page to enter recipes of your own.
