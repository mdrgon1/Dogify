BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS song(name TEXT NOT NULL, filepath TEXT, id INTEGER PRIMARY KEY );
    CREATE TABLE IF NOT EXISTS collection(name TEXT NOT NULL, media_path TEXT, song_ids id_list, id INTEGER PRIMARY KEY );
COMMIT;