import hashlib
import mysql.connector

# 1. Connexion à la base de données
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="magasin_informatique"
)

cursor = db.cursor(dictionary=True)

print("--- DÉBUT DE LA SÉCURISATION ---")

# 2. Récupérer tous les clients actuels
cursor.execute("SELECT id, password FROM clients")
clients = cursor.fetchall()

for client in clients:
    id_client = client['id']
    mdp_clair = client['password']
    
    # Sécurité : Si le mot de passe est déjà haché (64 caractères pour SHA-256), on n'y touche pas
    if len(mdp_clair) == 64 and all(c in '0123456789abcdefABCDEF' for c in mdp_clair):
        print(f"[Info] Le client ID {id_client} a déjà un mot de passe sécurisé.")
        continue

    # 3. Hachage du mot de passe en SHA-256
    mdp_hache = hashlib.sha256(mdp_clair.encode('utf-8')).hexdigest()
    
    # 4. Mise à jour dans la base de données
    cursor.execute(
        "UPDATE clients SET password = %s WHERE id = %s",
        (mdp_hache, id_client)
    )
    print(f"[Succès] Client ID {id_client} : '{mdp_clair}' transformé en -> {mdp_hache[:10]}...")

# 5. Sauvegarder les changements
db.commit()
cursor.close()
db.close()

print("--- TOUS LES MOTS DE PASSE ONT ÉTÉ HACHÉS AVEC SUCCÈS ! ---")