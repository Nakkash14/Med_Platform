from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector
import logging

# Configuration de FastAPI
app = FastAPI()

# Configuration du middleware CORS pour autoriser les requêtes de Django
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Adresse de votre application Django
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des logs pour détecter les erreurs
logging.basicConfig(level=logging.DEBUG)

# Fonction pour se connecter à Snowflake
def get_snowflake_connection():
    conn = snowflake.connector.connect(
        user="PROJETRCW",
        password="Projet2024",
        account="pphdwnf-ro24832",
        role="SYSADMIN",
        warehouse="COMPUTE_WH",
        database="MED_IT_DB",
        schema="PUBLIC"
    )
    return conn

# Endpoint pour tester la connexion
@app.get("/api/test-connection")
def test_connection():
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP;")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"message": "Connexion réussie", "timestamp": result[0]}
    except Exception as e:
        logging.error(f"Erreur de connexion : {e}")
        raise HTTPException(status_code=500, detail="Erreur de connexion à Snowflake")

# Endpoint pour récupérer tous les utilisateurs
@app.get("/api/users")
def get_users():
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        query = "SELECT id, username, email, date_joined FROM AUTH_USER;"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "date_joined": row[3].strftime("%Y-%m-%d %H:%M:%S")
            }
            for row in results
        ]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des utilisateurs : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne")

# Endpoint pour récupérer le profil d'un utilisateur par son ID
@app.get("/api/user-profile/{user_id}")
def get_user_profile(user_id: int):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()

        # Requête mise à jour avec la bonne correspondance de colonnes
        query = """
        SELECT firstname, lastname, age, dob, gender, email, address, occupation, licence, speciality
        FROM MAIN_USERPROFILE
        WHERE USER_ID = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
            keys = ['firstname', 'lastname', 'age', 'dob', 'gender', 'email', 'address', 'occupation', 'licence', 'speciality']
            profile = dict(zip(keys, result))
            return profile
        else:
            raise HTTPException(status_code=404, detail=f"No profile found for user_id {user_id}")
    except snowflake.connector.errors.ProgrammingError as pe:
        logging.error(f"Erreur SQL : {pe}")
        raise HTTPException(status_code=500, detail=f"Erreur SQL : {str(pe)}")
    except Exception as e:
        logging.error(f"Erreur interne : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        cursor.close()
        conn.close()
