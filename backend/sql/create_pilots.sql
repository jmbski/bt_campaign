DROP TABLE IF EXISTS "pilots";

CREATE TABLE "pilots" (
    "pilot_id" INTEGER,
    "pilot_name" TEXT NOT NULL UNIQUE,
    "pilot_callsign" TEXT,
    "gunnery_skill" INTEGER NOT NULL DEFAULT 4,
    "piloting_skill" INTEGER NOT NULL DEFAULT 5,
    "pilot_data" BLOB,
    "portrait_path" TEXT,
    "roster_id" INTEGER NOT NULL,
    'mech_id' INTEGER UNIQUE,
    PRIMARY KEY("pilot_id" AUTOINCREMENT),
    FOREIGN KEY("roster_id") REFERENCES "rosters"("roster_id")
    FOREIGN KEY("mech_id") REFERENCES "mechs"("mech_id")
)