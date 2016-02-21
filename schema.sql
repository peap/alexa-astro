CREATE TABLE IF NOT EXISTS alexa_users (
  id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  amazon_id VARCHAR UNIQUE NOT NULL,
  latitude  REAL,
  longitude REAL,
  city      VARCHAR
);
