import logging
import sys
import unittest
from datetime import datetime, timedelta

import psycopg2
from crawlclima.config import dbconnections
from crawlclima.tasks import fetch_redemet, pega_tweets

logger = logging.getLogger(__name__)  # Verify where this logger comes from

try:
    conn = psycopg2.connect(**dbconnections.PSQL_URI)

except Exception as e:
    logger.error(f"Unable to connect to Postgresql: {e}")
    sys.exit()


@unittest.skip("waiting dbdemo,issue#56")
class TestTasks(unittest.TestCase):
    def setUp(self):
        self.cur = conn.cursor()

    def tearDown(self):
        self.cur.close()

    def test_task_pegatweets(self):
        res = pega_tweets("2021-10-01", "2021-10-05", ["3304557", "3303302"])
        self.cur.execute('SELECT * FROM "Municipio"."Tweet";')
        resp = self.cur.fetchall()
        self.assertEqual(res, 200)
        self.assertGreater(len(resp), 0)

    def test_task_fetch_redemet(self):
        stations = "SBAF"
        today = datetime.today()  # if user_date is None else user_date
        year_start = datetime(datetime.today().year, 1, 1)
        yesterday = today - timedelta(1)
        day = year_start if today.isoweekday() == 5 else yesterday

        res = fetch_redemet(stations, day)
        self.assertEqual(res, None)
        self.cur.execute('SELECT * FROM "Municipio"."Estacao_wu";')
        resp = self.cur.fetchall()
        self.assertGreater(len(resp), 0)


if __name__ == "__main__":
    pass
    # TestTasks().run()
