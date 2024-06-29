DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
	"user_id"	INTEGER,
	"user_name"	TEXT NOT NULL UNIQUE,
	"user_email"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("user_id" AUTOINCREMENT)
)