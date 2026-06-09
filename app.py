from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)

# Configuration de la BDD pour Docker
db_config = {
    "host": "db",
    "user": "root",
    "password": "ton_mot_de_passe",
    "database": "magasin_informatique"
}

db_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_db():
    return db_pool.get_connection()

# ACCUEIL
@app.route("/")
def accueil():
    return render_template("accueil.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "admin" and password == "1234":
            return redirect("/admin")

        conn = get_db()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM clients WHERE email=%s AND password=%s", (email, password))
        client = cursor.fetchone()
        cursor.close()
        conn.close()

        if client:
            return redirect(f"/client/{client['id']}")
        return "Erreur login"

    return render_template("login.html")

# PAGE CLIENT
@app.route("/client/<int:id_client>")
def client(id_client):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute("""
        SELECT produits.nom, produits.prix, commandes.quantite
        FROM commandes
        JOIN produits ON produits.id = commandes.id_produit
        WHERE commandes.id_client = %s
    """, (id_client,))
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("client.html", produits=produits)

# PAGE ADMIN
@app.route("/admin")
def admin():
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    cursor.execute("SELECT * FROM commandes")
    commandes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template("admin.html", produits=produits, clients=clients, commandes=commandes)

@app.route("/client/<int:id_client>/commander", methods=["GET", "POST"])
def commander(id_client):
    if request.method == "POST":
        id_produit = request.form["id_produit"]
        quantite = request.form["quantite"]
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO commandes (id_client, id_produit, quantite) VALUES (%s, %s, %s)",
                       (id_client, id_produit, quantite))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(f"/client/{id_client}")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, prix FROM produits")
    produits = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("commander.html", produits=produits, id_client=id_client)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)