
import unittest

from nwebclient import runner as r


class BaseTestCase(unittest.TestCase):

    def test_dispatcher(self):
        d = r.LazyDispatcher()
        job = r.PrintJob()
        d.add_runner(job)
        result = d.execute({'type': job.type})
        self.assertTrue(result['success'])

    def test_dispatcher_loadrunner(self):
        d = r.LazyDispatcher()
        job = r.PrintJob()
        d.loadRunner('print', job)
        result = d.execute({'type': job.type})
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()