# Dogify

this repository contains only the source files, anything else like a .idea or an exported build

local_data.db is generated on startup, if the schema changes it should be deleted and regenerated.

## Some Database Functions
note: nested quotes should be double quote inside of single quote, idgaf I'm not writing a real parser

db_run(statement)
- executes sqlite statement

db_commit()
- closes out transaction, commits to the database

db_query(q)
- executes query q and prints result

db_insert_song(name, filepath)
- inserts this data into the database

db_del_songs(ids)
- deletes specified song ids from the database and removes them from any collections

db_get_songs(selection, where)
- fetch data about local song
- example usage: db_get_songs 'filepath, id' where 'name="yuh"'
- use '*' for either argument to match all

db_create_col(name, media)
- creates an empty collection with name and media filepath

db_remove_col(ids)
- removes all collections with the listed ids
- example usage db_remove_col '1, 3, 0'

db_get_col(selection, where)
- fetch data about collection
- example usage: db_get_col 'name, filepath' where 'id IN (0, 1)' 

db_insert_into_col(collection_id, ids)
- inserts songs listed in ids into collection with collection_id

db_remove_from_col(collection_id, ids)
- remove songs with ids from collection with collection_id

db_get_songs_in_col(collection_id, selection, where)
- same as get_songs but only for songs in collection with collection_id

open_filedialog()
- opens file dialog and prints filepath of what you select

audio_play_new(filepath)
- starts playing file at filepath

audio_play audio_stop audio_pause
- all do what you'd expect