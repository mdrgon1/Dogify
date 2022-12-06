# very small sqlite wrapper that connects to local_data.db
import sqlite3 as s
import re

DATABASE_PATH = "local_data/local_data.db"
connection : s.Connection = None
cursor : s.Cursor = None


def adapt_list(li):
    if not li:
        return ' '
    li = filter(lambda a: a is not None, li)
    li = list(str(a) for a in li)
    return ", ".join(li)
s.register_adapter(list, adapt_list)


def convert_list(str):
    try:
        str = str.decode("utf-8")
    except:
        pass
    if re.match("^\\s*$", str):
        return []
    li = re.split("\\s*,\\s*", str)
    return [int(x) for x in li]
s.register_converter("id_list", convert_list)


# convert list of tuples to a tuple of lists [(1, 'a'), (2, 'b'), (3, 'c')] -> ([1, 2, 3], ['a', 'b', 'c'])
def separate_tuple_list(li):
    if li == []:
        return ()
    return tuple(map(lambda a: list(a), zip(*li)))


def init():
    global connection
    global cursor

    # creates database on first execution
    connection = s.connect(DATABASE_PATH, detect_types=s.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # initialize necessary tables
    with open("local_data/schema.sql", "r") as f:
        for line in f.readlines():
            for statement in line.split(";\t\n"):
                cursor.execute(statement)
    print("initialized database")


def close():
    global cursor
    cursor.close()
    connection.close()


def run_statement(s):
    for statement in s.split(";"):
        return cursor.execute(s)


def commit():
    return cursor.execute("COMMIT")


def insert_song(name, filepath):
    song_id = None
    cursor.execute("SELECT * FROM song")
    if len(cursor.fetchall()) == 0:
        song_id = 0
    cursor.execute("INSERT INTO song VALUES(?, ?, ?)", [name, filepath, song_id])
    return commit()


def del_songs(ids):
    col_ids = get_collections("id", "*")
    for col_id, in col_ids:
        remove_from_collection(col_id, ids)
    cursor.execute("DELETE FROM song WHERE id IN ({})".format(", ".join(['?'] * len(ids))), ids)
    return commit()


def get_songs(selection, where):
    if where != "*":
        cursor.execute("SELECT {} FROM song WHERE {}".format(selection, where))
    else:
        cursor.execute("SELECT {} FROM song".format(selection))
    return cursor.fetchall()


def create_collection(name, media=None):
    collection_id = None
    cursor.execute("SELECT * FROM collection")
    if len(cursor.fetchall()) == 0:
        collection_id = 0
    cursor.execute("INSERT INTO collection VALUES(?, ?, ?, ?)", [name, media, [], collection_id])
    return commit()


def remove_collections(ids):
    cursor.execute("DELETE FROM collection WHERE id IN ({})".format(", ".join(['?'] * len(ids))), ids)
    return commit()


def get_collections(selection, where):
    if where == '*':
        cursor.execute("SELECT {} FROM collection".format(selection))
    else:
        cursor.execute("SELECT {} FROM collection WHERE {}".format(selection, where))
    return cursor.fetchall()


def insert_into_collection(collection_id, ids):
    cursor.execute("SELECT song_ids FROM collection WHERE id=?", [collection_id])
    collection, = cursor.fetchall()[0]
    collection = collection + ids
    cursor.execute("UPDATE collection SET song_ids = ? WHERE id = ?", [collection, collection_id])
    return commit()


def remove_from_collection(collection_id, ids):
    cursor.execute("SELECT song_ids FROM collection WHERE id=?", [collection_id])
    collection, = cursor.fetchall()[0]
    collection = [x for x in collection if x not in ids]
    cursor.execute("UPDATE collection SET song_ids = ? WHERE id = ?", [collection, collection_id])
    return commit()


def get_songs_in_collection(collection_id, selection, where):
    cursor.execute("SELECT song_ids FROM collection WHERE id=?", [int(collection_id)])
    song_ids, = cursor.fetchall()[0]
    if where == '*':
        return get_songs(selection, "id IN {}".format(tuple(song_ids)))
    else:
        return get_songs(selection, "{} AND id IN {}".format(where, tuple(song_ids)))


def query(q):
    cursor.execute(q)
    return cursor.fetchall()


def dump_schema():
    with open("local_data/schema.sql", "w") as f:
        f.writelines(connection.iterdump())
