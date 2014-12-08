__author__ = 'Administrator'

import unittest
from db import SQLServerDriverConnectionPoll


class SQLServerDriverConnectionPollTest(unittest.TestCase):
    db = None
    def setUp(self):
        self.db_poll = SQLServerDriverConnectionPoll.get_instance()
        self.db_poll.re_init()
        self.count = self.db_poll.get_db_idle_count()

    def tearDown(self):
        pass


    def test_get_idle_count(self):
        self.assertEqual(self.count, 10)

    def test_lend_one(self):
        db1 = self.db_poll.lend()
        count = self.db_poll.get_db_idle_count()
        self.assertEqual(db1['busy'], True)
        self.assertEqual(count, self.count -1)

    def test_restore(self):
        db2 = self.db_poll.lend()
        self.assertEqual(db2['busy'], True)
        count = self.db_poll.get_db_idle_count()
        self.assertEqual(count, self.count -1)

        self.db_poll.restore(db2)
        count = self.db_poll.get_db_idle_count()
        self.assertEqual(count, self.count)

    def test_lend_11(self):
        for x in xrange(1,self.count + 1):
            self.db_poll.lend()
        count = self.db_poll.get_db_idle_count()
        self.assertEqual(count, 0)

        db11 = self.db_poll.lend()
        self.assertEqual(db11['idx'], str(self.count+1))



if __name__ == '__main__':
    unittest.main()


