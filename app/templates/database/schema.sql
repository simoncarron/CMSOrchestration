drop table if exists users;

CREATE TABLE users (
    userID INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
);

INSERT INTO users (userID,first_name,last_name,email)VALUES ('simon.carron', 'Simon', 'Carron', 'simon.carron@gmail.com' );
