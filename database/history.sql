CREATE DATABASE health_checker;

USE health_checker;

CREATE TABLE history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symptoms TEXT NOT NULL,
    predicted_disease VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM history;
