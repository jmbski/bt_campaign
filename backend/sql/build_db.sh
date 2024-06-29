#!/bin/bash
SQL_DIR="/home/joseph/coding_base/bt_campaign/backend/sql"
TARGET_DB="/home/joseph/coding_base/bt_campaign/backend/bt_campaign.sqlite3"
RUN_PY=$1

# Set PRAGMA foreign_keys to OFF while running the create scripts
sqlite3 $TARGET_DB "PRAGMA foreign_keys = OFF;"

# Iterate through the sql files starting with 'create' in SQL_DIR and run them
# using sqlite3 targeting TARGET_DB

for file in $(ls $SQL_DIR | grep create); do
    echo "Running $file"
    sqlite3 $TARGET_DB < $SQL_DIR/$file
done

# Set PRAGMA foreign_keys to ON after running the create scripts
sqlite3 $TARGET_DB "PRAGMA foreign_keys = ON;"

# Check if the user wants to run the python scripts
if [ "$RUN_PY" == "-r" ]; then
    
    # Run the python scripts to populate the database
    echo "Populating the database"

    echo "Loading MUL Data"
    python3 /home/joseph/coding_base/bt_campaign/backend/main.py -u

    echo "Loading MTF Data"
    python3 /home/joseph/coding_base/bt_campaign/backend/main.py -U

    echo "Combining data"
    python3 /home/joseph/coding_base/bt_campaign/backend/main.py -C
fi