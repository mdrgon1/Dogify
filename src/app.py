import dogify_cli as c
import audio_player
import local_data
import tkinter.filedialog as f
import re


def sum(a, b):
    print(a + b)


def mul(a, b):
    print(a * b)


c.register_functions(
    "sum", lambda a, b: sum(float(a), float(b)),
    "mul", lambda a, b: mul(float(a), float(b)),
    "db_init", local_data.init,
    "db_close", local_data.close,
    "db_run", local_data.run_statement,
    "db_fetchall", lambda: print(local_data.cursor.fetchall()),
    "db_commit", local_data.commit,
    "db_query", local_data.query,

    "db_insert_song", local_data.insert_song,
    "db_del_songs", lambda ids: local_data.del_songs(local_data.convert_list(ids)),
    "db_get_songs", local_data.get_songs,

    "db_create_col", local_data.create_collection,
    "db_remove_col", lambda ids: local_data.remove_collections(local_data.convert_list(ids)),
    "db_get_col", local_data.get_collections,
    "db_insert_into_col", lambda col_id, ids: local_data.insert_into_collection(col_id, local_data.convert_list(ids)),
    "db_remove_from_col", lambda col_id, ids: local_data.remove_from_collection(col_id, local_data.convert_list(ids)),
    "db_get_songs_in_col", local_data.get_songs_in_collection,

    "audio_play_new", audio_player.play_new,
    "audio_play", audio_player.play,
    "audio_pause", audio_player.pause,
    "audio_stop", audio_player.stop,
    "open_filedialog", lambda: f.askopenfilename(),
    "quit", lambda: local_data.close(),
)


if __name__ == '__main__':
    c.run_cli()
