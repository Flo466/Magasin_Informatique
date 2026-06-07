<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connexion BDD
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="magasin_informatique"
)

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

        cursor = db.cursor(dictionary=True,buffered=True)

        # ADMIN
        if email == "admin" and password == "1234":
            return redirect("/admin")

        # CLIENT
        cursor.execute(
            "SELECT * FROM clients WHERE email=%s AND password=%s",
            (email, password)
        )
        client = cursor.fetchone()

        if client:
            return redirect(f"/client/{client['id']}")
        else:
            return "Erreur login"

    return render_template("login.html")


# PAGE CLIENT
@app.route("/client/<int:id_client>")
def client(id_client):
    cursor = db.cursor(dictionary=True,buffered=True)

    cursor.execute("""
    SELECT produits.nom, produits.prix, commandes.quantite
    FROM commandes
    JOIN produits ON produits.id = commandes.id_produit
    WHERE commandes.id_client = %s
    """, (id_client,))
    
    produits = cursor.fetchall()

    return render_template("client.html", produits=produits)


# PAGE ADMIN
@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True,buffered=True)

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    cursor.execute("SELECT * FROM commandes")
    commandes = cursor.fetchall()


    return render_template("admin.html", produits=produits, clients=clients, commandes=commandes)
@app.route("/client/<int:id_client>/commander", methods=["GET", "POST"])
def commander(id_client):
    cursor = db.cursor()

    if request.method == "POST":
        id_produit = request.form["id_produit"]
        quantite = request.form["quantite"]

        cursor.execute(
            "INSERT INTO commandes (id_client, id_produit, quantite) VALUES (%s, %s, %s)",
            (id_client, id_produit, quantite)
        )
        db.commit()

        return redirect(f"/client/{id_client}")

    cursor.execute("SELECT id_produit, nom, prix FROM produits")
    produits = cursor.fetchall()

    return render_template("commander.html", produits=produits, id_client=id_client)

=======
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connexion BDD
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="magasin_informatique"
)

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

        cursor = db.cursor(dictionary=True,buffered=True)

        # ADMIN
        if email == "admin" and password == "1234":
            return redirect("/admin")

        # CLIENT
        cursor.execute(
            "SELECT * FROM clients WHERE email=%s AND password=%s",
            (email, password)
        )
        client = cursor.fetchone()

        if client:
            return redirect(f"/client/{client['id']}")
        else:
            return "Erreur login"

    return render_template("login.html")


# PAGE CLIENT
@app.route("/client/<int:id_client>")
def client(id_client):
    cursor = db.cursor(dictionary=True,buffered=True)

    cursor.execute("""
    SELECT produits.nom, produits.prix, commandes.quantite
    FROM commandes
    JOIN produits ON produits.id = commandes.id_produit
    WHERE commandes.id_client = %s
    """, (id_client,))
    
    produits = cursor.fetchall()

    return render_template("client.html", produits=produits)


# PAGE ADMIN
@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True,buffered=True)

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()

    return render_template("admin.html", produits=produits, clients=clients)


>>>>>>> 76ac61fa6ea40e521a8ebf27701d73f5c5a0bfea
app.run(debug=True)