import unittest

from nwebclient import visual as subject


class BaseTestCase(unittest.TestCase):

    def test_Layout(self):
        self.assertEqual((1, 1), subject.CubedOrbitalLayout.get_xy(1))
        self.assertEqual((2, 1), subject.CubedOrbitalLayout.get_xy(2))
        self.assertEqual((2, 2), subject.CubedOrbitalLayout.get_xy(3))
        self.assertEqual((1, 2), subject.CubedOrbitalLayout.get_xy(4))
        self.assertEqual((3, 1), subject.CubedOrbitalLayout.get_xy(5))


if __name__ == '__main__':
    unittest.main()
