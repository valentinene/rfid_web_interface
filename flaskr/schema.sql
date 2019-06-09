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
  id_tag INTEGER PRIMARY KEY,
  nume TEXT NOT NULL,
  acces_camera NOT NULL,
  FOREIGN KEY (nume) REFERENCES users(username),
  FOREIGN KEY (acces_camera) REFERENCES camere(id)
);

CREATE TABLE pontaj (
  id_tag TEXT,
  id_camera TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_tag) REFERENCES angajati(id),
  FOREIGN KEY (id_camera) REFERENCES camere(id),
  PRIMARY KEY (id_tag, id_camera)
);
