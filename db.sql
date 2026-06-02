CREATE DATABASE magasin_informatique;
USE magasin_informatique;
CREATE TABLE clients (
    id INT AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    adresse VARCHAR(150),
    telephone VARCHAR(20),
    PRIMARY KEY (id)
);
CREATE TABLE produits (
    id INT AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    description TEXT,
    prix DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 0,
    image VARCHAR(100),
    PRIMARY KEY (id),
    CHECK (prix >= 0),
    CHECK (stock >= 0)
);
CREATE TABLE commandes (
    id INT AUTO_INCREMENT,
    id_client INT NOT NULL,
    date_commande DATE NOT NULL,
    total DECIMAL(10,2) DEFAULT 0,
    statut VARCHAR(30) DEFAULT 'En attente',
    PRIMARY KEY (id),
    FOREIGN KEY (id_client) REFERENCES clients(id)
);
CREATE TABLE details_commandes (
    id INT AUTO_INCREMENT,
    id_commande INT NOT NULL,
    id_produit INT NOT NULL,
    quantite INT NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_commande) REFERENCES commandes(id),
    FOREIGN KEY (id_produit) REFERENCES produits(id),
    CHECK (quantite > 0)
);
INSERT INTO clients (nom, prenom, email, password, adresse, telephone) VALUES
('Dupont', 'Marie', 'marie@gmail.com', '1234', 'Paris', '0600000001'),
('Martin', 'Paul', 'paul@gmail.com', '1234', 'Evry', '0600000002'),
('Benali', 'Sofia', 'sofia@gmail.com', '1234', 'Corbeil', '0600000003');

INSERT INTO produits (nom, description, prix, stock, image) VALUES
('Ordinateur portable HP', 'PC portable 15 pouces', 699.99, 10, 'hp.jpg'),
('Souris Logitech', 'Souris sans fil', 19.99, 50, 'souris.jpg'),
('Clavier Gamer', 'Clavier RGB mécanique', 49.99, 25, 'clavier.jpg'),
('Écran Samsung', 'Écran 24 pouces Full HD', 129.99, 15, 'ecran.jpg');
INSERT INTO commandes (id_client, date_commande, total, statut) VALUES
(1, '2026-06-01', 719.98, 'En attente'),
(2, '2026-06-01', 49.99, 'Validée');
