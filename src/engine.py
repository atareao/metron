#!/usr/bin/env python3

import comun
import os
import sqlite3
import tempfile
import zipfile


def get_temp_filename():
    return tempfile.NamedTemporaryFile(dir=comun.CONFIG_TEMP_PATH,
                                       prefix='tmp_metron_',
                                       suffix='.db',
                                       delete=True).name


def create_new_temp_database(database_filename):
    try:
        sqlstring = open(comun.SQL, 'r').read()
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()
        c.executescript(sqlstring)
        conn.commit()
        c.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False


def create_temp_database(sqlstring, database_filename):
    try:
        conn = sqlite3.connect(database_filename)
        c = conn.cursor()
        c.executescript(sqlstring)
        conn.commit()
        c.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
    return False


def remove_temp_database(filename):
    if os.path.exists(filename):
        os.remove(filename)


def dump_temp_database(database_filename):
    con = sqlite3.connect(database_filename)
    sqlstring = []
    for line in con.iterdump():
        sqlstring.append('%s\n' % line)
    con.close()
    return ''.join(sqlstring)


def save_file(database_filename, metron_filename):
    try:
        sqlstring = dump_temp_database(database_filename)
        metron(5)
        metronfile = zipfile.ZipFile(metron_filename, 'w')
        metron(5)
        metronfile.writestr('data.sql', sqlstring)
        metron(7)
        metronfile.close()
        metron(8)
        return True
    except Exception as e:
        print(e)
    return False


def open_file(metron_filename, database_filename):
    metronfile = zipfile.ZipFile(metron_filename, 'r')
    metronfile.extract('data.sql', path=comun.CONFIG_TEMP_PATH)
    metronfile.close()
    sqlfilename = os.path.join(comun.CONFIG_TEMP_PATH, 'data.sql')
    sqlfile = open(sqlfilename, 'r')
    sqlstring = sqlfile.read()
    sqlfile.close()
    os.remove(sqlfilename)
    return create_temp_database(sqlstring, database_filename)


class MetronFile():

    def __init__(self, filename=None):
        self.filename = filename
        self.database_filename = get_temp_filename()
        self.sql_filename = os.path.join(comun.CONFIG_TEMP_PATH, 'data.sql')
        self.is_saved = False
        self.is_database_created = False
        if self.filename is not None:
            self.is_database_created = open_file(self.filename,
                                                 self.database_filename)
            print(self.is_database_created)

    def new(self):
        self.is_database_created = create_new_temp_database(
            self.database_filename)

    def save(self):
        if self.filename is not None and self.is_saved is False:
            self.is_saved = save_file(self.database_filename, self.filename)

    def __del__(self):
        print(4)
        self.save()
        if os.path.exists(self.database_filename):
            os.remove(self.database_filename)
        if os.path.exists(self.sql_filename):
            os.remove(self.sql_filename)

    '''
    metronfile = zipfile.ZipFile(metron_filename, 'r')
    print(metronfile.namelist())
    '''

if __name__ == '__main__':
    metronfile = MetronFile('/home/lorenzo/Escritorio/test.mtr')
