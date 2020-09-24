import sqlite3


def main(query):
    try:
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()
        print(query)
        c.execute(query)
        db.commit()
        db.close()
    except NameError:
        print(NameError)
        print("An exception occurred")


if __name__ == '__main__':
    query = 'CREATE TABLE coordinate ( coordinate_id INTEGER PRIMARY KEY AUTOINCREMENT, latitude TEXT NOT NULL, longitude TEXT NOT NULL );'
    # query = ''
    main(query)

