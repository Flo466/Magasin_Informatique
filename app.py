import os
from flask import Flask, render_template, request, redirect
from mysql.connector import pooling

app = Flask(__name__)

# Config BDD
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": "root",
    "password": "ton_mot_de_passe",
    "database": "magasin_informatique"
}

db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

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
        email, password = request.form["email"], request.form["password"]
        if email == "admin" and password == "1234":
            return redirect("/admin")

        conn = get_db()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id FROM clients WHERE email=%s AND password=%s", (email, password))
        client = cursor.fetchone()
        cursor.close(); conn.close()

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
        SELECT p.nom, p.prix, dc.quantite
        FROM details_commandes dc
        JOIN commandes c ON dc.id_commande = c.id
        JOIN produits p ON dc.id_produit = p.id
        WHERE c.id_client = %s
    """, (id_client,))
    produits = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("client.html", produits=produits, id_client=id_client)

# PAGE ADMIN
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
    cursor.close(); conn.close()
    return render_template("admin.html", produits=p, clients=c, commandes=cmd)

# PAGE COMMANDER
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
            cursor.close(); conn.close()
            return redirect(f"/client/{id_client}")
        
        cursor.close(); conn.close()
        return render_template("erreur_stock.html", id_client=id_client)

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, prix FROM produits WHERE stock > 0")
    produits = cursor.fetchall()
    cursor.close(); conn.close()
    return render_template("commander.html", produits=produits, id_client=id_client)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)