import dogify_cli as c
import local_data

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
    "db_insert_song", local_data.insert_song,
    "db_query", local_data.query,
    "db_get_songs", local_data.get_songs,
    "quit", lambda: local_data.close(),
)


if __name__ == '__main__':
    c.run_cli()
