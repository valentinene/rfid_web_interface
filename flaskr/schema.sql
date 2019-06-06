DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS camere;
DROP TABLE IF EXISTS pontaj;

CREATE TABLE camere (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nume TEXT NOT NULL,
  etaj TEXT NOT NULL
);

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL
);

CREATE TABLE pontaj (
  id_user TEXT,
  id_camera TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_user) REFERENCES users(id),
  FOREIGN KEY (id_user) REFERENCES camere(id),
  PRIMARY KEY (id_user, id_camera)
);
