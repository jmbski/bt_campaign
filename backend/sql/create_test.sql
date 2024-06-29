DROP TABLE IF EXISTS "test";

CREATE TABLE "test" (
    "test_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "test_name" TEXT NOT NULL,
    "test_data" BLOB
)