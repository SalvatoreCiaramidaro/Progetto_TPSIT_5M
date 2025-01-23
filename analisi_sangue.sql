DROP DATABASE IF EXISTS analisi_sangue;

CREATE DATABASE analisi_sangue;
USE analisi_sangue;



DROP TABLE IF EXISTS `users`;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    nome_operatore VARCHAR(50) NOT NULL
);

INSERT INTO users (username, password,nome_operatore) VALUES ('user1', 'password123','Operatore 1');
INSERT INTO users (username, password,nome_operatore) VALUES ('user2', 'password456','Operatore 2');
INSERT INTO users (username, password,nome_operatore) VALUES ('user3', 'password789','Operatore 3');


DROP TABLE IF EXISTS `analisi`;

CREATE TABLE analisi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    cognome VARCHAR(50),
    codice_fiscale VARCHAR(16),
    sesso CHAR(1),
    eta INT,
    data_ora_prelievo DATETIME,
    luogo_prelievo VARCHAR(100),
    denominazione_analisi VARCHAR(100),
    risultato FLOAT,
    unita_misura VARCHAR(20),
    valori_riferimento VARCHAR(50),
    strumenti INT,
    cod_operatore INT
);

SELECT * FROM users;
SELECT * FROM analisi;