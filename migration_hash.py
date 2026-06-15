import mysql.connector
import bcrypt
import os

# Configuration identique à app.py
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": "root",
    "password": "ton_mot_de_passe",
    "database": "magasin_informatique"
}

def migrate_passwords():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Récupérer tous les clients
    cursor.execute("SELECT id, email, password FROM clients")
    clients = cursor.fetchall()
    
    for client in clients:
        password_clair = client['password'].encode('utf-8')
        # Générer le hash
        hashed = bcrypt.hashpw(password_clair, bcrypt.gensalt())
        
        # Mettre à jour la base
        cursor.execute(
            "UPDATE clients SET password = %s WHERE id = %s",
            (hashed.decode('utf-8'), client['id'])
        )
        print(f"Client {client['email']} migré.")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    migrate_passwords()