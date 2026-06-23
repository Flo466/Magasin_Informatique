import os
import re
import bcrypt
import secrets
from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import pooling, Error

app = Flask(__name__)

# ====================================================================================================
# 💾 ////////////////////////////////// DATABASE CONFIGURATION ///////////////////////////////////////
# ====================================================================================================
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": "root",
    "password": "ton_mot_de_passe",
    "database": "magasin_informatique"
}

# Connection pool for better performance
db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db_config)

def get_db():
    try:
        return db_pool.get_connection()
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ====================================================================================================
# 🏠 //////////////////////////////////////////// HOME ROUTE //////////////////////////////////////////
# ====================================================================================================
@app.route("/")
def accueil():
    return render_template("accueil.html")

# ====================================================================================================
# 🔑 /////////////////////////////////////////// LOGIN ROUTE //////////////////////////////////////////
# ====================================================================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        if email == "admin" and password == "1234":
            return redirect(url_for("admin"))

        conn = get_db()
        if not conn: return "Database connection error."
        
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id, password, is_verified FROM clients WHERE email=%s", (email,))
        client = cursor.fetchone()
        cursor.close()
        conn.close()

        if client and bcrypt.checkpw(password.encode('utf-8'), client['password'].encode('utf-8')):
            if not client['is_verified']:
                return "Account not verified. Please check your verification code."
            return redirect(url_for("client", id_client=client['id']))
            
        return "Login error: invalid credentials"
        
    return render_template("login.html")

# ====================================================================================================
# 👤 /////////////////////////////////////// CLIENT DASHBOARD ROUTE //////////////////////////////////
# ====================================================================================================
@app.route("/client/<int:id_client>")
def client(id_client):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("""
        SELECT p.nom, p.prix, dc.quantite
        FROM details_commandes dc
        JOIN commandes c ON dc.id_commande = c.id
        JOIN produits p ON dc.id_produit = p.id
        WHERE c.id_client = %s
    """, (id_client,))
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("client.html", produits=produits, id_client=id_client)

# ====================================================================================================
# 🛡️ /////////////////////////////////////// ADMIN DASHBOARD ROUTE //////////////////////////////////
# ====================================================================================================
@app.route("/admin")
def admin():
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM produits")
    p = cursor.fetchall()
    cursor.execute("SELECT * FROM clients")
    c = cursor.fetchall()
    cursor.execute("SELECT * FROM commandes")
    cmd = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin.html", produits=p, clients=c, commandes=cmd)

# ====================================================================================================
# 🛒 /////////////////////////////////////////// ORDERING ROUTE ///////////////////////////////////////
# ====================================================================================================
@app.route("/client/<int:id_client>/commander", methods=["GET", "POST"])
def commander(id_client):
    conn = get_db()
    if request.method == "POST":
        id_prod = request.form["id_produit"]
        qte = int(request.form["quantite"])
        cursor = conn.cursor()
        
        cursor.execute("SELECT stock, prix FROM produits WHERE id=%s", (id_prod,))
        prod = cursor.fetchone()
        
        if prod and prod[0] >= qte:
            cursor.execute("INSERT INTO commandes (id_client, date_commande) VALUES (%s, CURDATE())", (id_client,))
            id_cmd = cursor.lastrowid
            cursor.execute("INSERT INTO details_commandes (id_commande, id_produit, quantite, prix_unitaire) VALUES (%s, %s, %s, %s)",
                           (id_cmd, id_prod, qte, prod[1]))
            cursor.execute("UPDATE produits SET stock = stock - %s WHERE id=%s", (qte, id_prod))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for("client", id_client=id_client))
        
        cursor.close()
        conn.close()
        return render_template("erreur_stock.html", id_client=id_client)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, prix FROM produits WHERE stock > 0")
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("commander.html", produits=produits, id_client=id_client)

# ====================================================================================================
# 🧺 /////////////////////////////////////////// CART ROUTES //////////////////////////////////////////
# ====================================================================================================
@app.route("/panier/<int:id_client>")
def voir_panier(id_client):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("""
        SELECT p.nom, p.prix, pa.quantite, (p.prix * pa.quantite) as total_ligne
        FROM panier pa
        JOIN produits p ON pa.id_produit = p.id
        WHERE pa.id_client = %s
    """, (id_client,))
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("panier.html", articles=articles, id_client=id_client)

@app.route("/ajouter_panier", methods=["POST"])
def ajouter_panier():
    id_client = request.form["id_client"]
    id_produit = request.form["id_produit"]
    quantite = request.form["quantite"]
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO panier (id_client, id_produit, quantite) VALUES (%s, %s, %s)", 
                   (id_client, id_produit, quantite))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("voir_panier", id_client=id_client))

# ====================================================================================================
# 📝 ///////////////////////////////////////////// SIGNUP ROUTE ///////////////////////////////////////
# ====================================================================================================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        nom, prenom, email = request.form["nom"], request.form["prenom"], request.form["email"]
        password = request.form["password"]

        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[0-9]", password):
            return "Password too weak. Must be 8+ chars with uppercase and digit."

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        code = str(secrets.randbelow(900000) + 100000)

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clients (nom, prenom, email, password) VALUES (%s, %s, %s, %s)",
                           (nom, prenom, email, hashed_pw.decode('utf-8')))
            user_id = cursor.lastrowid
            cursor.execute("INSERT INTO email_verification (id_client, token) VALUES (%s, %s)", (user_id, code))
            conn.commit()
            return render_template("signup_success.html", code=code, id=user_id)
        finally:
            cursor.close()
            conn.close()
            
    return render_template("signup.html")

# ====================================================================================================
# ✅ ///////////////////////////////////////// CODE VERIFICATION //////////////////////////////////////
# ====================================================================================================
@app.route("/enter-code", methods=["GET", "POST"])
def enter_code():
    user_id = request.args.get("id")
    if request.method == "POST":
        user_code = request.form["code"]
        conn = get_db()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_client FROM email_verification WHERE id_client=%s AND token=%s", (user_id, user_code))
        if cursor.fetchone():
            cursor.execute("UPDATE clients SET is_verified = 1 WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM email_verification WHERE id_client = %s", (user_id,))
            conn.commit()
            return "Account activated! <a href='/login'>Log in here</a>"
        return "Invalid code."
    return render_template("enter_code.html", id=user_id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)