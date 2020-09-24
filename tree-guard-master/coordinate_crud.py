import sqlite_execute


def add(lat, lon):
    query = 'INSERT INTO coordinate (latitude, longitude) VALUES(' + \
        lat+', '+lon+');'
    sqlite_execute.main(query)


def read_all():
    query = 'SELECT * FROM coordinate;'
    sqlite_execute.main(query)
