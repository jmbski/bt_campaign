DROP TABLE IF EXISTS "missions";

CREATE TABLE "missions" (
    "mission_id"	INTEGER,
    "mission_name"	TEXT NOT NULL UNIQUE,
    "mission_description"	TEXT,
    "mission_data" BLOB,
    PRIMARY KEY("mission_id" AUTOINCREMENT)
)