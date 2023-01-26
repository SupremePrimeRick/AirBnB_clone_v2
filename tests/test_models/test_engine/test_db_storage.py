#!/usr/bin/python3
""" Test class for db_storage """
from os import getenv
from models.state import State
import unittest
import MySQLdb


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage tests not supported in file storage')
class TestDBStorage(unittest.TestCase):
    """ Test class """

    def test_new_and_save(self):
        """ Testing the new and save methods"""
        db = MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                             passwd=getenv('HBNB_MYSQL_PWD'),
                             host=getenv('HBNB_MYSQL_HOST'),
                             db=getenv('HBNB_MYSQL_DB'),
                             port=3306)
        new_state = State(name='Nigeria')
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM states')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        new_state.save()

        db = MySQLdb.connect(user=getenv('HBNB_MYSQL_USER'),
                             passwd=getenv('HBNB_MYSQL_PWD'),
                             host=getenv('HBNB_MYSQL_HOST'),
                             db=getenv('HBNB_MYSQL_DB'),
                             port=3306)
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM states')
        new_count = cur.fetchall()

        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()
