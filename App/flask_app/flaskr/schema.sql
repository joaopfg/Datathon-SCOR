DROP TABLE IF EXISTS bq;

CREATE TABLE bq (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  weight REAL NOT NULL,
  bmi REAL NOT NULL,
  pulse REAL NOT NULL,
  age REAL NOT NULL,
  sleep REAL NOT NULL,
  smoke TEXT NOT NULL,
  phys_activ TEXT NOT NULL,
  walk_bic TEXT NOT NULL,
  vig_activ TEXT NOT NULL,
  mod_activ TEXT NOT NULL,
  tv_day REAL NOT NULL,
  fat_foods REAL NOT NULL,
  alcohol_day REAL NOT NULL,
  alcohol_year REAL NOT NULL
);