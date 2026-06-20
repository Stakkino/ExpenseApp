CREATE DATABASE IF NOT EXISTS expenseapp
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE expenseapp;

CREATE TABLE IF NOT EXISTS Utilisateur(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(80) NOT NULL,
    prenom VARCHAR(250),
    email VARCHAR(250) NOT NULL UNIQUE,
    datenaissance DATE,
    mdp VARCHAR(255) NOT NULL,
    creat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Categorie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE,
    couleur VARCHAR(7)  DEFAULT '#3498DB'
);

INSERT INTO Categorie (nom, couleur)VALUES 
('Alimentation',                '#E74C3C'),
('Logement',                    '#8E44AD'),
('Transport',                   '#2E86C1'),
('Santé',                       '#1E8449'),
('Education & Scolarité',       '#D35400'),
('Loisirs & Divertissement',    '#F39C12'),
('Habillement & Soins',         '#C0392B'),
('Abonnement & Communication',  '#16A085'),
('Urgences & Imprevus',         '#E74C3C'),
('Autres',                      '#7F8C8D');


CREATE TABLE IF NOT EXISTS Recette (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur int NOT NULL,
    montantr DECIMAL(12,2)NOT NULL,
    descriptions VARCHAR(100),
    dater DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur) REFERENCES Utilisateur(id) ON DELETE CASCADE,
    CHECK (montantr > 0)
);


CREATE TABLE IF NOT EXISTS Depense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categorie INT NOT NULL, 
    utilisateur int NOT NULL,
    descriptions VARCHAR(200),
    montantd DECIMAL(12,2) NOT NULL,
    dated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categorie) REFERENCES Categorie(id),
    FOREIGN KEY (utilisateur) REFERENCES Utilisateur(id) ON DELETE CASCADE,
    CHECK (montantd > 0)
); 


CREATE TABLE IF NOT EXISTS Economie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur int NOT NULL,
    types ENUM('Ajouter', 'Retrait') NOT NULL,
    montante DECIMAL(12,2) NOT NULL,
    descriptions VARCHAR(200),
    datee DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur) REFERENCES Utilisateur(id) ON DELETE CASCADE
);