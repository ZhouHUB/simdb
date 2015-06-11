import uuid
from simdb.utils import db_connect, db_disconnect


conn = None
db_name = "simdb_testing_disposable_{}".format(str(uuid.uuid4()))


def simdb_setup():
    "Create a fresh database with unique (random) name."
    global conn
    db_disconnect()
    conn = db_connect(db_name, 'localhost', 27017)

def simdb_teardown():
    "Drop the fresh database and disconnect."
    conn.drop_database(db_name)
    db_disconnect()
