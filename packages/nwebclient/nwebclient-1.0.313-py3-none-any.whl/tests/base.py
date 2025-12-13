import unittest

from nwebclient import base as b

class BaseTestCase(unittest.TestCase):
    def test_DictProxy(self):

        t = b.DictProxy({'a': 42})

        self.assertEqual(t['a'], 42)


if __name__ == '__main__':
    unittest.main()
