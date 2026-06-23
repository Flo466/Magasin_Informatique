-- Adminer 5.4.2 MySQL 8.0.46 dump
-- Initialization script for magasin_informatique (TP7 Updated)

SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE IF NOT EXISTS `magasin_informatique` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_0900_ai_ci;

USE `magasin_informatique`;

-- -----------------------------------------------------
-- Table clients
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clients` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(50) NOT NULL,
  `prenom` VARCHAR(50) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `adresse` VARCHAR(150),
  `telephone` VARCHAR(20),
  `is_verified` BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table produits
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `produits` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `prix` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `stock` INT NOT NULL DEFAULT 0,
  `image` VARCHAR(100),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table panier (TP7 Part 1)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `panier` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_client` INT UNSIGNED NOT NULL,
  `id_produit` INT UNSIGNED NOT NULL,
  `quantite` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_panier_client` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_panier_produit` FOREIGN KEY (`id_produit`) REFERENCES `produits` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table commandes
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `commandes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_client` INT UNSIGNED NOT NULL,
  `date_commande` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `statut` VARCHAR(30) DEFAULT 'En attente',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_commandes_client` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table details_commandes
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `details_commandes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_commande` INT UNSIGNED NOT NULL,
  `id_produit` INT UNSIGNED NOT NULL,
  `quantite` INT NOT NULL DEFAULT 1,
  `prix_unitaire` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_details_commande` FOREIGN KEY (`id_commande`) REFERENCES `commandes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_details_produit` FOREIGN KEY (`id_produit`) REFERENCES `produits` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table email_verification
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `email_verification` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_client` INT UNSIGNED NOT NULL,
  `token` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_email_client` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Initial Data
-- -----------------------------------------------------
INSERT INTO `clients` (`nom`, `prenom`, `email`, `password`, `adresse`, `telephone`, `is_verified`) VALUES
('Dupont', 'Marie', 'marie@gmail.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/zBkqquzaQA0T5v99/z1rY715.W', 'Paris', '0600000001', 1),
('Martin', 'Paul', 'paul@gmail.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/zBkqquzaQA0T5v99/z1rY715.W', 'Evry', '0600000002', 1),
('Benali', 'Sofia', 'sofia@gmail.com', '$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/zBkqquzaQA0T5v99/z1rY715.W', 'Corbeil', '0600000003', 1);

INSERT INTO `produits` (`nom`, `description`, `prix`, `stock`, `image`) VALUES
('Ordinateur portable HP', 'PC portable 15 pouces', 699.99, 10, 'hp.jpg'),
('Souris Logitech', 'Souris sans fil', 19.99, 50, 'souris.jpg'),
('Clavier Gamer', 'Clavier RGB mécanique', 49.99, 25, 'clavier.jpg'),
('Écran Samsung', 'Écran 24 pouces Full HD', 129.99, 15, 'ecran.jpg');

INSERT INTO `commandes` (`id_client`, `date_commande`, `total`, `statut`) VALUES
(1, '2026-06-01 10:00:00', 719.98, 'En attente'),
(2, '2026-06-01 14:30:00', 49.99, 'Validée');

SET foreign_key_checks = 1;