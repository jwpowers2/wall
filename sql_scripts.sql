create database wall;

use wall;


create table users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), password VARCHAR(255), created_at DATETIME, updated_at DATETIME);


create table messages (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id INT, FOREIGN KEY (user_id) REFERENCES users (id), message TEXT,created_at DATETIME, updated_at DATETIME);

create table comments (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, message_id INT, FOREIGN KEY (message_id) REFERENCES messages (id), user_id INT, FOREIGN KEY (user_id) REFERENCES users (id), comment TEXT,created_at DATETIME, updated_at DATETIME);


