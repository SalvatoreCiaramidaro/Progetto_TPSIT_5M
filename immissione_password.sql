CREATE DATABASE your_database;
USE your_database;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, password) VALUES ('user1', 'password123');
INSERT INTO users (username, password) VALUES ('user2', 'password456');
INSERT INTO users (username, password) VALUES ('user3', 'password789');

SELECT * FROM users;