CREATE DATABASE banking_app;

USE banking_app;

CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,  
    username VARCHAR(255) UNIQUE, 
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE accounts (
	id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT, FOREIGN KEY (user_id) REFERENCES users(id), 
    account_type VARCHAR(255),
    account_number VARCHAR(255) UNIQUE,
    balance DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
	id INT AUTO_INCREMENT PRIMARY KEY,
    from_account_id INT, FOREIGN KEY(from_account_id) REFERENCES accounts(id),
	to_account_id INT, FOREIGN KEY (to_account_id) REFERENCES accounts(id),
    amount DECIMAL(10,2),
    type VARCHAR(255),
    decription VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM transactions;