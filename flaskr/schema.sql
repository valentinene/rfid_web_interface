DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS camere;
DROP TABLE IF EXISTS pontaj;
DROP TABLE IF EXISTS angajati;

CREATE TABLE camere (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nume TEXT NOT NULL,
  etaj TEXT NOT NULL
);

CREATE TABLE users (
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  admin INTEGER DEFAULT 0
);

CREATE TABLE angajati (
    id_angajat INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tag TEXT UNIQUE,
    nume TEXT, acces_camera INTEGER,
    FOREIGN KEY (nume) REFERENCES users(username),
    FOREIGN KEY (acces_camera) REFERENCES camere(id)
);

CREATE TABLE pontaj (
  id_pontaj INTEGER PRIMARY KEY AUTOINCREMENT,
  id_tag TEXT,
  id_camera TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_tag) REFERENCES angajati(id_tag),
  FOREIGN KEY (id_camera) REFERENCES camere(id)
);
