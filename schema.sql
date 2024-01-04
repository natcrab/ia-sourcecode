CREATE TABLE user(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    passw TEXT NOT NULL,
    email TEXT
);

CREATE TABLE votes(
    pollId INTEGER PRIMARY KEY,
    userId INTEGER NOT NULL,
    votes REAL
);