import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

def get_engine():
    connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
    return create_engine(connection_string)

def init_db():
    engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INT PRIMARY KEY,
                diet_json JSON,
                cuisines_json JSON,
                dislikes_json JSON,
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS favorites (
                fav_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                recipe_id VARCHAR(100) NOT NULL,
                recipe_data JSON NOT NULL,
                is_personal BOOLEAN DEFAULT FALSE
            )
        """))

def save_profile_to_db(user_id, profile):
    engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO user_profiles (user_id, diet_json, cuisines_json, dislikes_json)
            VALUES (:u_id, :diet, :cuis, :dis)
            ON DUPLICATE KEY UPDATE 
            diet_json = :diet, cuisines_json = :cuis, dislikes_json = :dis
        """), {
            "u_id": user_id,
            "diet": json.dumps(profile['diet']),
            "cuis": json.dumps(profile['cuisines']),
            "dis": json.dumps(profile['dislikes'])
        })
        
def add_fav_to_db(user_id, recipe, is_personal=False):
    engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO favorites (user_id, recipe_id, recipe_data, is_personal)
            VALUES (:u_id, :r_id, :data, :personal)
        """), {
            "u_id": user_id,
            "r_id": str(recipe['id']),
            "data": json.dumps(recipe),
            "personal": is_personal
        })

def remove_fav_from_db(user_id, recipe_id):
    engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM favorites WHERE user_id = :u_id AND recipe_id = :r_id"), 
                            {"u_id": user_id, "r_id": str(recipe_id)})
        
def load_user_data(user_id):
    """Fetches everything for a user to populate session_state on startup."""
    engine = get_engine()
    with engine.connect() as conn:
        # Load Profile
        prof_res = conn.execute(text("SELECT * FROM user_profiles WHERE user_id = :u_id"), {"u_id": user_id}).fetchone()
        
        # Load Favorites
        fav_res = conn.execute(text("SELECT recipe_data FROM favorites WHERE user_id = :u_id AND is_personal = FALSE"), {"u_id": user_id}).fetchall()
        
        # Load Personal Recipes
        pers_res = conn.execute(text("SELECT recipe_data FROM favorites WHERE user_id = :u_id AND is_personal = TRUE"), {"u_id": user_id}).fetchall()
        
        return {
            "profile": {
                "diet": json.loads(prof_res[1]) if prof_res else [],
                "cuisines": json.loads(prof_res[2]) if prof_res else [],
                "dislikes": json.loads(prof_res[3]) if prof_res else []
            },
            "favorites": [json.loads(r[0]) for r in fav_res],
            "personal": [json.loads(r[0]) for r in pers_res]
        }