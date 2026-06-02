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

        cursor = db.cursor(dictionary=True, buffered=True)

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


# PAGE CLIENT (Modifiée pour envoyer l'id_client au HTML)
@app.route("/client/<int:id_client>")
def client(id_client):
    cursor = db.cursor(dictionary=True, buffered=True)

    # Requête basée sur le point 5 de ta feuille de manipulation
    cursor.execute("""
        SELECT produits.nom, produits.prix, details_commandes.quantite
        FROM details_commandes
        JOIN commandes ON commandes.id = details_commandes.id_commande
        JOIN produits ON produits.id = details_commandes.id_produit
        WHERE commandes.id_client = %s
    """, (id_client,))
    
    produits = cursor.fetchall()

    # C'est le "id_client=id_client" ici qui va faire apparaître ton bouton !
    return render_template("client.html", produits=produits, id_client=id_client)


# PASSER UNE COMMANDE (Respecte les 5 étapes de ton sujet à la lettre)
@app.route('/client/<int:id_client>/commander', methods=['GET', 'POST'])
def commander(id_client):
    cursor = db.cursor(dictionary=True, buffered=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM produits WHERE stock > 0")
        produits = cursor.fetchall()
        return render_template('commander.html', id_client=id_client, produits=produits)

    if request.method == 'POST':
        id_produit = int(request.form['id_produit'])
        quantite_demandee = int(request.form['quantite'])

        # 1- Vérifier le stock du produit
        cursor.execute("SELECT * FROM produits WHERE id = %s", (id_produit,))
        produit = cursor.fetchone()

        if not produit or produit['stock'] < quantite_demandee:
            return "Stock insuffisant ou produit inexistant !", 400

        total_commande = produit['prix'] * quantite_demandee

        # 2- Créer une commande dans la table commandes
        cursor.execute(
            "INSERT INTO commandes (id_client, date_commande, total) VALUES (%s, NOW(), %s)",
            (id_client, total_commande)
        )
        id_commande = cursor.lastrowid

        # 3- Ajouter le détail dans details_commandes
        cursor.execute(
            "INSERT INTO details_commandes (id_commande, id_produit, quantite, prix_unitaire) VALUES (%s, %s, %s, %s)",
            (id_commande, id_produit, quantite_demandee, produit['prix'])
        )

        # 4- Diminuer le stock du produit
        cursor.execute(
            "UPDATE produits SET stock = stock - %s WHERE id = %s",
            (quantite_demandee, id_produit)
        )

        db.commit()
        
        # 5- Rediriger le client vers son espace
        return redirect(f'/client/{id_client}')


# PAGE ADMIN
@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()

    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()

    return render_template("admin.html", produits=produits, clients=clients)


if __name__ == "__main__":
    app.run(debug=True)