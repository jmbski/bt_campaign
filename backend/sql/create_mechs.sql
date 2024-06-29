DROP TABLE IF EXISTS "mechs";

CREATE TABLE "mechs" (
    "mech_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "mech_name" TEXT NOT NULL,
    "mech_variant" TEXT NOT NULL,
    "mech_data_id" INTEGER NOT NULL,
    "mech_data" BLOB,
    "mech_status" TEXT NOT NULL,
    "mech_pilot_id" INTEGER UNIQUE,
    "base_battle_value" INTEGER NOT NULL,
    "adjusted_battle_value" INTEGER,
    "roster_id" INTEGER NOT NULL,
    FOREIGN KEY("mech_pilot_id") REFERENCES "pilots"("pilot_id"),
    FOREIGN KEY("roster_id") REFERENCES "rosters"("roster_id")
    FOREIGN KEY("mech_data_id") REFERENCES "mech_data"("mech_id")
)