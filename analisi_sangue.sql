DROP DATABASE IF EXISTS analisi_sangue;

CREATE DATABASE analisi_sangue;
USE analisi_sangue;


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
