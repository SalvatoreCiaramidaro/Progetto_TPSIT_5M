DROP DATABASE IF EXISTS Password;

CREATE DATABASE Password;
USE Password;

DROP TABLE IF EXISTS `users`;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    nome VARCHAR(50) NOT NULL
);

INSERT INTO users (username, password,nome) VALUES ('user1', 'password123','Operatore 1');
INSERT INTO users (username, password,nome) VALUES ('user2', 'password456', 'Operatore 2');
INSERT INTO users (username, password,nome) VALUES ('user3', 'password789','Operatore 3');

SELECT * FROM users;