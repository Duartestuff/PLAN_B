CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    logged INTEGER CHECK(logged IN(0, 1))

);

INSERT INTO users (username, password, logged)
VALUES ('Admin', 'Admin123', 0);