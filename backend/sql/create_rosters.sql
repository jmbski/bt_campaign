DROP TABLE IF EXISTS "rosters";

CREATE TABLE "rosters" (
    "roster_id"	INTEGER,
    "roster_name"	TEXT NOT NULL UNIQUE,
    "roster_description"	TEXT,
    "roster_owner"	INTEGER NOT NULL,
    "roster_salvage_points" INTEGER,
    "max_battle_value" INTEGER,
    "roster_data" BLOB,
    PRIMARY KEY("roster_id" AUTOINCREMENT),
    FOREIGN KEY("roster_owner") REFERENCES "users"("user_id")
)