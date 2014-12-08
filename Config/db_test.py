__author__ = 'Administrator'

import unittest
from db import SQLServerDriverConnectionPoll


class SQLServerDriverConnectionPollTest(unittest.TestCase):

    def testUp(self):
        print

    # def test_lend_one(self):
    #     db_poll = SQLServerDriverConnectionPoll.get_instance()
    #     db1 = db_poll.lend()
    #     self.assertEqual(db1['idx'], '1')
    #     self.assertEqual(db1['busy'], True)

    def test_lend_more(self):
        db_poll = SQLServerDriverConnectionPoll.get_instance()
        db1 = db_poll.lend()
        db_more = db_poll.lend()
        db_poll.lend()
        db_poll.lend()
        db_poll.lend()

        self.assertEqual(db1['busy'], True)
        self.assertEqual(db_more['idx'], '2')
        self.assertEqual(db_more['busy'], True)


if __name__ == '__main__':
    unittest.main()