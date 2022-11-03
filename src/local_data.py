# very small sqlite wrapper that connects to local_data.db
import sqlite3 as s

DATABASE_PATH = "local_data/local_data.db"
connection = None
cursor = None


def init():
    global connection
    global cursor

    # creates database on first execution
    connection = s.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # initialize necessary tables
    with open("local_data/schema.sql", "r") as f:
        for line in f.readlines():
            for statement in line.split(";\t\n"):
                cursor.execute(statement)
    print("initialized database")


def close():
    cursor.close()
    connection.close()


def run_statement(s):
    for statement in s.split(";"):
        print(cursor.execute(s))


def commit():
    cursor.execute("COMMIT")


def insert_song(name, filepath):
    cursor.execute("SELECT * FROM song")
    song_id = None
    if len(cursor.fetchall()) == 0:
        song_id = 0
    cursor.execute("INSERT INTO song VALUES(?, ?, ?)", [name, filepath, song_id])
    cursor.execute("COMMIT")


def get_songs(selection, where):
    cursor.execute("SELECT {} FROM song WHERE {}".format(selection, where))
    print(cursor.fetchall())


def query(q):
    cursor.execute(q)
    print(cursor.fetchall())


def dump_schema():
    with open("local_data/schema.sql", "w") as f:
        f.writelines(connection.iterdump())
