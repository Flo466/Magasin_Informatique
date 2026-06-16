-- Adminer 5.4.2 MySQL 8.0.46 dump
-- Nettoyage et optimisation de la structure

SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE IF NOT EXISTS `magasin_informatique` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_0900_ai_ci;

USE `magasin_informatique`;

-- Table clients
CREATE TABLE `clients` (
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

-- Table produits
CREATE TABLE `produits` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(100) NOT NULL,
  `description` TEXT,
  `prix` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `stock` INT NOT NULL DEFAULT 0,
  `image` VARCHAR(100),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table commandes
CREATE TABLE `commandes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_client` INT UNSIGNED NOT NULL,
  `date_commande` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `statut` VARCHAR(30) DEFAULT 'En attente',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_commandes_client` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table details_commandes
CREATE TABLE `details_commandes` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_commande` INT UNSIGNED NOT NULL,
  `id_produit` INT UNSIGNED NOT NULL,
  `quantite` INT NOT NULL DEFAULT 1,
  `prix_unitaire` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_details_commande` FOREIGN KEY (`id_commande`) REFERENCES `commandes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_details_produit` FOREIGN KEY (`id_produit`) REFERENCES `produits` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table email_verification
CREATE TABLE `email_verification` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_client` INT UNSIGNED NOT NULL,
  `token` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_email_client` FOREIGN KEY (`id_client`) REFERENCES `clients` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET foreign_key_checks = 1;