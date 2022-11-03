# Dogify

this repository contains only the source files, anything else like a .idea or an exported build

local_data.db is generated on startup, if the schema changes it should be deleted and regenerated.

## Some Database Functions
note: nested quotes should be double quote inside of single quote, idgaf I'm not writing a real parser

db_run(statement)
- executes sqlite statement

db_commit()
- closes out transaction, commits to the database

db_insert_song(name filepath)
- inserts this data into the database

db_query(q)
- executes query q and prints result

db_get_songs(selection, where)
- fetch data about local song
- example usage: db_get_songs 'filepath, id' where 'name="yuh"'

open_filedialog()
- opens file dialog and prints filepath of what you select

audio_play_new(filepath)
- starts playing file at filepath

audio_play audio_stop audio_pause all do what you'd expect