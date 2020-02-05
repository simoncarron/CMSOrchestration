drop table if exists adminConfig;

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO user (id,email,username,password)VALUES ('1', 'simon.carron@gmail.com', 'simon.carron', '12345' );